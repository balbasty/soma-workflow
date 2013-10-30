from __future__ import with_statement
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 13:51:00 2013

@author: laure.hugo@cea.fr

Workflow test of multiple jobs with dependencies:
* Workflow constitued of (3*n+2) jobs : 3 groups of n jobs, and 2 other jobs
                                        You can change the value n with nb
* Each job is a sleep command : you can change the time with time_sleep
* Dependencies : job1 depends on Group1
                 Group2 depends on job1
                 job2 depends on Group2
                 Group3 depends on job3
* Allowed configurations : Light mode - Local path
                           Local mode - Local path
                           Remote mode - File Transfer
                           Remote mode - Shared Resource Path (SRP)
                           Remote mode - File Transfer and SRP
* Expected comportment : All jobs succeed
* Outcome independant of the configuration
"""

from soma_workflow.client import Helper
from soma_workflow.configuration import LIGHT_MODE
from soma_workflow.configuration import REMOTE_MODE
from soma_workflow.configuration import LOCAL_MODE
import soma_workflow.constants as constants
from soma_workflow.test.examples.workflow_test import WorkflowTest


class NJobsWithDependencies(WorkflowTest):
    allowed_config = [(LIGHT_MODE, WorkflowTest.LOCAL_PATH),
                      (LOCAL_MODE, WorkflowTest.LOCAL_PATH),
                      (REMOTE_MODE, WorkflowTest.FILE_TRANSFER),
                      (REMOTE_MODE, WorkflowTest.SHARED_RESOURCE_PATH),
                      (REMOTE_MODE, WorkflowTest.SHARED_TRANSFER)]

    def test_result(self):
        nb = 10
        time_sleep = 1

        workflow = NJobsWithDependencies.wf_examples.example_n_jobs_with_dependencies(nb=nb, time=time_sleep)
        self.wf_id = NJobsWithDependencies.wf_ctrl.submit_workflow(
            workflow=workflow,
            name=self.__class__.__name__)
        # Transfer input files if file transfer
        if self.path_management == NJobsWithDependencies.FILE_TRANSFER or \
                self.path_management == NJobsWithDependencies.SHARED_TRANSFER:
            Helper.transfer_input_files(self.wf_id,
                                        NJobsWithDependencies.wf_ctrl)
        # Wait for the workflow to finish
        Helper.wait_workflow(self.wf_id, NJobsWithDependencies.wf_ctrl)
        # Transfer output files if file transfer
        if self.path_management == NJobsWithDependencies.FILE_TRANSFER or \
                self.path_management == NJobsWithDependencies.SHARED_TRANSFER:
            Helper.transfer_output_files(self.wf_id,
                                         NJobsWithDependencies.wf_ctrl)

        status = self.wf_ctrl.workflow_status(self.wf_id)
        self.assertTrue(status == constants.WORKFLOW_DONE)
        self.assertTrue(len(Helper.list_failed_jobs(
                        self.wf_id,
                        NJobsWithDependencies.wf_ctrl)) == 0)
        self.assertTrue(len(Helper.list_failed_jobs(
                        self.wf_id,
                        NJobsWithDependencies.wf_ctrl,
                        include_aborted_jobs=True)) == 0)


if __name__ == '__main__':
    NJobsWithDependencies.run_test(debug=False)
