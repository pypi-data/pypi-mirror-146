import os
import sys
from typing import List
from google.cloud.dataproc_v1.types.workflow_templates import WorkflowTemplate, TemplateParameter
from google.cloud.dataproc_v1.types import OrderedJob, PySparkJob
from dsframework.base.batch.workflow_base import ZIDS_Workflow


class Workflow(ZIDS_Workflow):

    def __init__(self):
        """! Loads config file and initializes parameters.
        """
        self.default_jars = ['gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar']
        main_project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

        self.pip_packages = ''
        with open(main_project_path + '/requirements_docker.txt') as req_file:
            required_pkg = req_file.read().splitlines()
            required_pkg = [x for x in required_pkg if "#" not in x]
            self.pip_packages = ' '.join(required_pkg)

        super().__init__(self.pip_packages)

    def create_job(self, stage_name, prerequisite_list=None) -> OrderedJob():
        """! Create a job from a given stage

            Args:
                stage_name: Name of the stage to create
                prerequisite_list: list of stage id's that are mandatory to run before current stage

            Returns:
                An Ordered Job, to be inserted into the workflow template
        """
        stage_dir = f'batch_files/stages/{stage_name}'

        stage_job = self.create_ordered_job(stage_dir)

        if prerequisite_list is not None:
            stage_job.prerequisite_step_ids = prerequisite_list

        return stage_job

    def create_stages(self) -> List[OrderedJob]:
        """! Create the stages for the workflow stages
            Returns:
                A List of Ordered Jobs, to be inserted into the workflow template
        """
        # stage get_data
        stage_get_data_job = self.create_job("get_data")

        # stage run_pipeline
        prerequisite_list = [self.project_name + '-stage_get_data']
        stage_run_pipeline_job = self.create_job("run_pipeline", prerequisite_list)

        # stage set_data
        prerequisite_list = [self.project_name + '-stage_run_pipeline']
        stage_set_data_job = self.create_job("set_data", prerequisite_list)

        return [stage_get_data_job, stage_run_pipeline_job, stage_set_data_job]

    def finalize_jobs(self, workflow_template):
        """! Finalize the jobs, introduce additional parameters, etc.
            Args:
                workflow_template: Workflow templates. Includes jobs that we wish to modify
        """

        # Set start and end dates from Airflow composer
        workflow_template.parameters = []

        start_date_param = TemplateParameter()
        start_date_param.description = "start date from airflow composer"
        start_date_param.name = "START_DATE"

        end_date_param = TemplateParameter()
        end_date_param.description = "end date from airflow composer"
        end_date_param.name = "END_DATE"

        for job in workflow_template.jobs:
            start_date_param.fields.append("jobs['" + job.step_id + "'].pysparkJob.args[1]")
            end_date_param.fields.append("jobs['" + job.step_id + "'].pysparkJob.args[2]")

        workflow_template.parameters.append(start_date_param)
        workflow_template.parameters.append(end_date_param)

        # Make sure to change jobs according to specific configuration
        if self.config['specific_jobs_to_run'] and len(self.config['specific_jobs_to_run']):
            specific_jobs_to_run = []
            for job in workflow_template.jobs:
                if job.step_id in self.config['specific_jobs_to_run']:
                    specific_jobs_to_run.append(job)
                    if len(job.prerequisite_step_ids) and not all(
                            elem in specific_jobs_to_run for elem in job.prerequisite_step_ids):
                        raise Exception("job depends on another job not in specific_jobs_to_run list")
            workflow_template.jobs = specific_jobs_to_run

    def create_workflow_template(self):
        """! Create the workflow template, along with all relevant stages
        """

        workflow_template = None

        # Make sure that a cluster exists
        self.check_cluster()

        # Define template structure
        workflow_template = self.create_template_structure()
        workflow_template.jobs = self.create_stages()
        self.finalize_jobs(workflow_template)
        # print(template)
        # print(f"project_path: {self.project_path}")

        # Make sure that the template does not exist
        self.check_template()

        # Create template
        self.create_template(workflow_template)


if __name__ == "__main__":
    """! Triggers the creation of the workflow template, starting from
    basic configuration, defining and creating jobs from the existing stages, 
    and up to creating and instantiating the workflow, if needed.
        Args:
        System argument 1 - Action to be performed on a template (create, delete, instantiate)
    """

    if sys.argv and len(sys.argv) > 1:
        template_action = sys.argv[1]
    workflow = Workflow()

    if template_action == 'create':
        workflow.create_workflow_template()

    # At this point, a template is either previously or recently created
    template = workflow.get_workflow_template()

    if template_action == 'delete' and template:
        workflow.delete_workflow_template(template)

    if template_action == 'instantiate' and template:
        workflow.instantiate_template(template)
