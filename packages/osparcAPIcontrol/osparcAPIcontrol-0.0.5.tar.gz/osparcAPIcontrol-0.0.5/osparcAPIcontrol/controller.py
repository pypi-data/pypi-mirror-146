import os
import numpy as np
import time
import shutil
import zipfile
import pprint

import osparc
from osparc import UsersApi
from osparc.api import FilesApi, SolversApi
from osparc.models import File, Job, JobInputs, JobOutputs, JobStatus, Solver

from pathlib import Path
from IPython.display import clear_output
from tenacity import retry, stop_after_attempt


class OsparcAPIcontroller:
    def __init__(self, host, username, password):
        self.cfg = osparc.Configuration(host=host,
                                        username=username,
                                        password=password)
        self.api_client = osparc.ApiClient(self.cfg)
        self.users_api = UsersApi(self.api_client)
        self.files_api = FilesApi(self.api_client)
        self.solvers_api = SolversApi(self.api_client)
        self.solvers_in_use = {}

        print(self.users_api.get_my_profile())

    def print_solvers(self):
        all_solvers = self.solvers_api.list_solvers()

        for solver in all_solvers:
            pprint.pprint(solver)

    def initialize_solvers(self, solver_list: list):
        r"""

        :param solver_list: a list of strings of solver.title that should be used. eg: ['isolve-mpi']

        fills the solvers_in_use dictionary with the chosen solver and its titles as keys for later use.
        """
        all_solvers = self.solvers_api.list_solvers()

        for solver in all_solvers:
            if solver.title in solver_list:
                temp_solver_id = solver.id
                temp_solver_version = solver.version
                temp_solver: Solver = self.solvers_api.get_solver_release(solver_key=temp_solver_id,
                                                                          version=temp_solver_version)
                self.solvers_in_use[solver.title] = temp_solver

    @retry(stop=stop_after_attempt(5))
    def upload(self,
               payload_name: str,
               payload: Path,
               metadata: dict):
        r"""
        function used to upload files to the API and save the IDs for later use.

        :param payload_name: name of the file to upload. Used as key in metadata dictionary
        :param payload: Path of file that should be uploaded
        :param metadata: dictionary to which the uploaded files ID will be added
        :return: updated metadata dictionary
        """

        try:
            payload_obj = self.files_api.upload_file(file=payload)

            metadata[payload_name] = payload_obj.id
        except osparc.ApiException as e:
            print("Exception when calling FilesApi->upload_file: %s\n" % e)

        return metadata

    @retry(stop=stop_after_attempt(5))
    def create_job_pyrun(self,
                         payload_name: str,
                         payloads: dict,
                         metadata: dict):
        r"""
        creating a job for a python runner service. The Jobs ID is saved in the metadata dictionary.

        :param payload_name: name of the file to upload. Used as key in metadata dictionary
        :param payloads: dictionary containing the four possible inputs and number of CPUs for the python runner. Eg:
        {'input_0':
         'input_1':
         'input_2':
         'input_3':
         'NCPU': 2}
        :param metadata: dictionary to which the uploaded files ID will be added
        :return: updated metadata dictionary
        """
        assert 's4l Python Runner' in self.solvers_in_use.keys(), 'Please initialize a s4l python runner solver'

        try:
            job = self.solvers_api.create_job(self.solvers_in_use['s4l Python Runner'].id,
                                              self.solvers_in_use['s4l Python Runner'].version,
                                              JobInputs(payloads))
            metadata[payload_name] = (job.id, self.solvers_in_use['s4l Python Runner'].id)
        except osparc.ApiException as e:
            print("Exception when calling SolversApi->create_job: %s\n" % e)

        return metadata

    @retry(stop=stop_after_attempt(5))
    def create_job_isolve(self,
                          simname,
                          file_id,
                          metadata_sim_jobs):
        assert 'isolve-mpi' in self.solvers_in_use.keys(), 'Please initialize an isolve-mpi solver'

        print("Staging sim: %s" % simname, end='\r')
        input_file = self.files_api.get_file(file_id)

        job = self.solvers_api.create_job(self.solvers_in_use['isolve-mpi'].id,
                                          self.solvers_in_use['isolve-mpi'].version,
                                          JobInputs({"input_1": input_file, "NCPU": 4}))

        metadata_sim_jobs[simname] = (job.id, self.solvers_in_use['isolve-mpi'].id)

    def all_done(self, statuses):
        stopped = np.array([status.stopped_at for (jid, status) in statuses.items()])
        return np.all(stopped)

    def run_jobs(self,
                 solver_title: str,
                 all_jobs_metadata: dict):

        statuses = {}
        job_statuses = {}
        for simname, (jid, sid) in all_jobs_metadata.items():
            # status = solvers_api.stop_job(sid, runner_solver_version, jid)
            status: JobStatus = self.solvers_api.start_job(sid,
                                                           self.solvers_in_use[solver_title].version,
                                                           jid)
            statuses[jid] = status
            job_statuses[simname] = f'Progress: {status.progress}/100, State: {status.state}'

        while not self.all_done(statuses):
            clear_output(wait=True)
            succeeded = 0
            pending = 0
            failed = 0
            for simname, (jid, sid) in all_jobs_metadata.items():
                time.sleep(0.5)
                status = self.solvers_api.inspect_job(sid,
                                                      self.solvers_in_use[solver_title].version,
                                                      jid)
                statuses[jid] = status
                job_statuses[simname] = f'Progress: {status.progress}/100, State: {status.state}'
                if status.state == 'SUCCESS':
                    succeeded += 1
                elif status.state == 'FAILED':
                    failed += 1
                if status.state == 'PENDING':
                    pending += 1
            print(f'Succeeded: {succeeded}, Pending: {pending}, Failed: {failed}\n')
            pprint.pprint(job_statuses)

    @retry(stop=stop_after_attempt(5))
    def download_job_output(self,
                            solver_title: str,
                            instructor_packet: tuple,
                            results_dir: Path,
                            metadata: dict):

        simname = instructor_packet[0]
        jid = instructor_packet[1][0]
        sid = instructor_packet[1][1]

        outputs: JobOutputs = self.solvers_api.get_job_outputs(sid,
                                                               self.solvers_in_use[solver_title].version,
                                                               jid)

        metadata[simname] = outputs.results["output_1"].id

        # Download and extract the output which contains
        # a metajson file with the ids of all h5 input files for the isolve
        try:
            download_path: str = self.files_api.download_file(file_id=outputs.results["output_1"].id)
        except osparc.ApiException as e:
            print("Exception when calling FilesApi->download_file: %s\n" % e)

        with zipfile.ZipFile(download_path, 'r') as zip_ref:
            zip_ref.extractall(results_dir.joinpath(f'{simname}'))

        os.remove(download_path)

        return metadata

    def reupload_service(self, metadata_sim_results):

        metadata_simres_reupload = {}

        sim_outputs = Path('data/sim_outputs')
        print(sim_outputs)
        sim_outputs.mkdir(exist_ok=True)

        for sim_name, sim_id in metadata_sim_results.items():
            download_path: str = self.files_api.download_file(file_id=sim_id)
            print("Downloaded to", download_path)
            shutil.move(download_path, f'{sim_outputs}/{sim_name}.h5')
            self.upload(Path(f'{sim_outputs}/{sim_name}.h5'))
            os.remove(f'{sim_outputs}/{sim_name}.h5')
