#!/bin/bash
# export GOOGLE_APPLICATION_CREDENTIALS=$GOOGLE_APPLICATION_CREDENTIALS
gcloud config set project dozi-data-science-research-1
python ./batch_files/setup.py clean --all
python ./batch_files/setup.py bdist_wheel
# bash ./batch_files/scripts/venv.sh
# python ./batch_files/scripts/zip_requirements.py
# pip install -r ./requirements_docker.txt --target=dist/requirements
dsf-cli upload-batch-files
# python ./batch_files/workflow/upload_files.py jars
# python ./batch_files/workflow/upload_files.py stages
# python ./batch_files/workflow/upload_files.py whl
# python ./batch_files/workflow/auto_scaling_policy.py
dsf-cli workflow-template create
# dsf-cli create-dag
dsf-cli workflow-template instantiate
gcloud config set project dozi-stg-ds-apps-1
