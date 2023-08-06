import os
import subprocess
from textwrap import dedent

from dsframework.base.batch.dag_base import ZIDS_Dag


class Dag(ZIDS_Dag):
    def __init__(self):
        """! Loads config file and initializes parameters.
        """

        # dag params from airflow 1 - https://airflow.apache.org/docs/apache-airflow/1.10.3/macros.html
        # dag params from airflow 2 - https://airflow.apache.org/docs/apache-airflow/stable/templates-ref.html
        super().__init__()

        # Create DAG python code file
        self.file_name = self.project_name + "_dag.py"
        text_file = open(self.file_name, "w")
        n = text_file.write(dedent(self.get_basic_dag_code()))
        text_file.close()

    def create_dag(self):
        """! Dag main function.
        This function is the "entrypoint" for the dag creation.
        """

        source = self.file_name

        command = '''gcloud composer environments storage dags import \
            --environment "''' + self.environment + '''" \
            --location "''' + self.region + '''" \
            --source "''' + source + '''" \
            --destination "''' + self.folder_path + '''"
        '''
        # print(command)
        process = subprocess.call(command, shell=True)

        os.unlink(self.file_name)
        dag_path = self.bucket_name + '/dags/' + self.folder_path + '/' + source
        print(f'finish uploading dag to - {dag_path}')


if __name__ == "__main__":
    """! Triggers the creation of the workflow dag, which will instantiate a
    workflow template into an actual workflow, executing it.
    """

    dag = Dag()
    dag.create_dag()
