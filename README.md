# beular-api

Using the AWS Cloud Developer Kit to build, train, and deploy a machine-learning model that can classify End-User License Aggreements as compliant or not using Sagemaker, Lambda, and API Gateway.

## Getting Started

### AWS Account Setup

You'll need an AWS IAM user with the following AWS-managed policies attached to it:

- AWSLambdaFullAccess
- AmazonS3FullAccess
- AmazonAPIGatewayInvokeFullAccess
- CloudWatchFullAccess
- AmazonAPIGatewayAdministrator
- AmazonVPCFullAccess
- AmazonSageMakerFullAccess
- AWSCloudFormationFullAccess

You'll also need the in-line policies in the `policies/` dir of this repo. Take note of where you'll need to insert your AWS account's id.

Moving forward, we use the name `beular-api` when referencing the AWS account.

#### AWS CLI and Boto3 Setup

Although there's a [number of ways](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html#configuring-credentials) for Boto3 to find your credentials, we're going to adopt usage of a shared credential file (e.g. `~/.aws/credentials`).

The shared credentials file has a default location of `~/.aws/credentials`. You can change the location of the shared credentials file by setting the `AWS_SHARED_CREDENTIALS_FILE` environment variable.

This file is an INI-formatted file with section names corresponding to *profiles*.

Below is a minimal example of the shared credentials file (note how we've named the profile 'beular-api`):

```ini
[beular-api]
aws_access_key_id=foo
aws_secret_access_key=bar
region=us-east-1
output=json
```

#### CDK Installation

Follow the instructions [here](https://docs.aws.amazon.com/cdk/latest/guide/getting_started.html) to install and configure the AWS CDK. You'll need to install node.js as a part of this step if you don't already have it.

To authenticate ourselves, we'll use the `--profile` option to specify our `beular-api` profile.

#### AWS Service Quotas

AWS accounts have default quotas for EC2 instances to prevent runaway bills on their most expensive instances. If you get an error when you start training in the Jupyter Notebook within Sagemaker, you might need to [request a service quota increase](https://docs.aws.amazon.com/general/latest/gr/aws_service_limits.html) for the associated EC2 instance. Or just use an instance for which you already have a quota >= 1.

### Python Environment

This project uses Python 3.7.3, although other versions >= 3.5 should be fine. You can install Python from [here](https://www.python.org/downloads/), although using a system utility (e.g. homebrew for OSX) is fine as well.

Next, activate your python virtual environment and install the dependencies:

```bash
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

### Application Configuration

For simplicity, all configuration details are kept in `config.py`.

## Deploy

This application is comprised of three separate stacks:

1. The Virtual Private Cloud (`stacks/vpc.py`)
2. The SageMaker Notebook (`stacks/notebook.py`)
3. The Deployed Model API (`stacks/api.py`)

Additionally, the models' source code is sourced in a [separate repository](https://github.com/csmcallister/beular-nb) so that we can sync it with our Notebook instance. If you're wanting to use your own repo, make sure it's public and use its git url in the config.

You must deploy the stacks sequentially, as you can't have a SageMaker instance without a VPC to host it. Moreover, you must first train and deploy a model within SageMaker before you can create the model's API.

To deploy the VPC stack:

```bash
cdk deploy VpcStack --profile beular-api
```

Then, to deploy the SageMaker stack:

```bash
cdk deploy BeularNotebookStack --profile beular-api
```

Then, to deploy the API stack (after you've trained a model and deployed it to a SageMaker endpoint!):

```bash
cdk deploy ModelAPIStack --profile beular-api
```

After deploying the API, you can get the API url from the CDK output (or you can check online in the API Gateway console):

```bash
...
 ✅  ModelAPIStack

Outputs:
ModelAPIStack.callsmapiEndpoint123ABC456 = https://abc123execute-api.us-east-1.amazonaws.com/prod/
```

With that in hand, you can now send a request to the API.

If you deployed one of the sklearn models, use:

```bash
curl -X POST -H "Content-Type: text/plain" --data "this is a test" https://fntzl3eq2h.execute-api.us-east-1.amazonaws.com/prod/
[{"pred_prob": "95.0%", "prediction": "0", "expl": "PHN...DwvcD4="}]
```

>Note that the prediction explanation ("expl") is base64-encoded.

If you deployed the BlazingText model:

```python
import requests
uri = 'https://abc123.execute-api.us-east-1.amazonaws.com/prod/'
data = {'instances': ['This is a test of the system']}
r = requests.post(uri, json=data)
r.json()
#[{'prob': [1.0000100135803223], 'label': ['__label__0']}]
```

## Destroy

You can also use the CDK to destroy stacks with, for example:

```bash
cdk destroy ModelAPIStack --profile beular-api
```

which should eventually output:

```bash
✅  ModelAPIStack: destroyed
```

>If you get an error destroying, it's likely due to resource state changes from performing actions in the AWS console. You can always manually delete things in your stack from the console.

## Generate a Cloudformation Template

Althouh you could log into the AWS console and take a look at the Cloudformation stacks there, you can also run the following command to write them as JSON documents to `.cdk.out/`:

```bash
cdk synth --profile beular-api
```

More cdk commands are documented [here](https://docs.aws.amazon.com/fr_fr/cdk/latest/guide/cli.html#cli-commands).

### Lint

Style tests can be run with:

```bash
flake8
```
