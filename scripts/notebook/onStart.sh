#!/bin/bash

set -e

# OVERVIEW
# This part gets value from Notebook Instance's tag and sets it as environment
# variable for all process including Jupyter in SageMaker Notebook Instance
# Note that this script will fail this condition is not met
#   1. Ensure the Notebook Instance execution role has permission of SageMaker:ListTags

# PARAMETERS
BUCKET_NAME=BUCKET_NAME
ENDPOINT_NAME=ENDPOINT_NAME

NOTEBOOK_ARN=$(jq '.ResourceArn' /opt/ml/metadata/resource-metadata.json --raw-output)
BUCKET_NAME_TAG=$(aws sagemaker list-tags --resource-arn $NOTEBOOK_ARN  | jq -r --arg BUCKET_NAME "$BUCKET_NAME" .'Tags[] | select(.Key == $BUCKET_NAME).Value' --raw-output)
ENDPOINT_NAME_TAG=$(aws sagemaker list-tags --resource-arn $NOTEBOOK_ARN  | jq -r --arg ENDPOINT_NAME "$ENDPOINT_NAME" .'Tags[] | select(.Key == $ENDPOINT_NAME).Value' --raw-output)
touch /etc/profile.d/jupyter-env.sh
echo "export $BUCKET_NAME=$BUCKET_NAME_TAG" >> /etc/profile.d/jupyter-env.sh
echo "export $ENDPOINT_NAME=$ENDPOINT_NAME_TAG" >> /etc/profile.d/jupyter-env.sh
initctl restart jupyter-server --no-wait

# OVERVIEW
# This script installs pip and conda packages in a single SageMaker conda environment

sudo -u ec2-user -i <<'EOF'
# PARAMETERS
ENVIRONMENT=conda_python3
source /home/ec2-user/anaconda3/bin/activate "$ENVIRONMENT"
pip install --upgrade pip
pip install contractions nltk eli5
pip install scikit-learn==0.21.3
python -W ignore -m nltk.downloader punkt
python -W ignore -m nltk.downloader averaged_perceptron_tagger
python -W ignore -m nltk.downloader wordnet
source /home/ec2-user/anaconda3/bin/deactivate
EOF
