# beular-api

Using the AWS Cloud Developer Kit to build, train, and deploy a machine-learning model that can classify End-User License Aggreements as compliant or not using Sagemaker, Lambda, and API Gateway.

## Getting Started

### AWS Account Setup

#### AWS CLI and Boto3 Setup

Although there's a [number of ways](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html#configuring-credentials) for Boto3 to find your credentials, we're going to adopy usage of a shared credential file (`~/.aws/credentials`).

The shared credentials file has a default location of `~/.aws/credentials`. You can change the location of the shared credentials file by setting the `AWS_SHARED_CREDENTIALS_FILE` environment variable.

This file is an INI formatted file with section names corresponding to profiles. With each section, three configuration variables be specified: `aws_access_key_id`, `aws_secret_access_key`, `aws_session_token`. These are the only supported values in the shared credential file.

Below is an minimal example of the shared credentials file (note how we've named the profile 'model-as-a-service'):

```ini
[beular-api]
aws_access_key_id=foo
aws_secret_access_key=bar
aws_session_token=baz
```

#### CDK Installation

Follow the instructions [here](https://docs.aws.amazon.com/cdk/latest/guide/getting_started.html) to install and configure the AWS CDK. You'll need to install node.js as a part of this step if you don't already have it.

>Note that we'll pass our AWS credentials to the AWS CDK CLI using the --profile option with `~/.aws/config`.

#### AWS Service Quotas

AWS accounts have default quotas for EC2 instances to prevent runaway bills on their most expensive instances. If you get an error when you start training in the Jupyter Notebook within Sagemaker, you might need to [request a service quota increase](https://docs.aws.amazon.com/general/latest/gr/aws_service_limits.html) for the associated EC2 instance.

### Python Environment

This project uses Python 3.7.3, although other versions >= 3.5 should be fine. You can install Python from [here](https://www.python.org/downloads/), although using a system utility (e.g. homebrew for OSX) is fine as well.

Next, activate your python virtual environment and install the dependencies:

```bash
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

### Application Configuration

See config.py

## Deploy

This application is comprised of three separate stacks:

1. The Virtual Private Cloud
2. The SageMaker Notebook
3. The Deployed Model API

Additionally, the model's source code is sourced in a separate repository so that we can sync it with our Notebook instance.

## Test

ToDo

### Lint

Style tests can be run with:

```bash
flake8
```
