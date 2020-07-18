from aws_cdk import (
    aws_iam as iam,
    aws_ec2 as ec2,
    aws_s3 as s3,
    aws_sagemaker as sm,
    core
)


class BeularNotebookStack(core.Stack):
    '''
    This will place a SageMaker Notebook instance with the private subnet
    of a VPC. Although the notebook instance is walled off from the internet,
    one can access it via the AWS console and perform outbound requests (and 
    receive responses) thanks to the ACLs and Routing Tables configured with
    the VPC.
    '''
    def __init__(self, scope: core.Construct, id: str, vpc: ec2.Vpc, **kwargs) -> None:  # noqa: E501
        super().__init__(scope, id)

        with open(kwargs.get('on_start_script_path'), 'r') as f:
            on_start_script = f.read()

        with open(kwargs.get('on_create_script_path'), 'r') as f:
            on_create_script = f.read()

        role = iam.Role(
            self, "BeularNotebookRole",
            assumed_by=iam.ServicePrincipal('sagemaker.amazonaws.com'),
            managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name(
                'AmazonSageMakerFullAccess')]
        )

        role.add_to_policy(iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=['SageMaker:ListTags'],  # to set env vars w/ tags
            resources=["*"]  # TODO: specify sagemaker notebook explicitly
        ))

        lifecycle_config = sm.CfnNotebookInstanceLifecycleConfig(
            self, 'BeularNotebookLifecycleConfig',
            notebook_instance_lifecycle_config_name='BeularNotebookLifecycleConfig',  # noqa: E501
            on_create=[dict(content=core.Fn.base64(on_create_script))],
            on_start=[dict(content=core.Fn.base64(on_start_script))]
        )

        bucket = s3.Bucket(
            self, 'beular-sagemaker-api-bucket',
            versioned=False,
            removal_policy=core.RemovalPolicy.DESTROY,
            block_public_access=s3.BlockPublicAccess(
                block_public_acls=True,
                ignore_public_acls=True,
                block_public_policy=True,
                restrict_public_buckets=True
            )
        )
        
        endpoint_name = kwargs.get('endpoint_name')
        lc_name = lifecycle_config.notebook_instance_lifecycle_config_name
        notebook = sm.CfnNotebookInstance(  # noqa: F841
            self, 'BeularNotebook',
            lifecycle_config_name=lc_name,
            role_arn=role.role_arn,
            default_code_repository=kwargs.get('repo'),
            direct_internet_access='Disabled',
            instance_type='ml.t2.medium',  # ml.t2.medium is smallest possible
            notebook_instance_name="BeularSageMakerNotebook",
            subnet_id=vpc.private_subnets[0].subnet_id,
            security_group_ids=[vpc.vpc_default_security_group],
            volume_size_in_gb=5,  # 5 is minimum; max is 16384
            tags=[
                core.CfnTag(key='BUCKET_NAME', value=bucket.bucket_name),
                core.CfnTag(key='ENDPOINT_NAME', value=endpoint_name),
            ],
        )
