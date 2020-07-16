from aws_cdk import (
    aws_apigateway as apig_,
    aws_iam as iam,
    aws_lambda as lambda_,
    core
)


class ModelAPIStack(core.Stack):
    '''
    This stack places a Lambda function and API Gateway instance on top of an 
    already-deployed SageMaker model endpoint.
    '''
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id)

        endpoint_name = kwargs.get('endpoint_name')
        content_type = kwargs.get('content_type')

        lambda_sm = lambda_.Function(
            self, "call-sm-lambda",
            code=lambda_.Code.asset('./lambdas/api'),
            handler="handler.main",
            timeout=core.Duration.seconds(30),
            runtime=lambda_.Runtime.PYTHON_3_7,
            memory_size=150
        )
        
        lambda_sm.add_environment('ENDPOINT_NAME', endpoint_name)
        lambda_sm.add_environment('CONTENT_TYPE', content_type)

        endpoint_arn = (
            f'arn:aws:sagemaker:{self.region}'
            f':{self.account}:endpoint/{endpoint_name}'
        )
        
        lambda_sm.add_to_role_policy(iam.PolicyStatement(
            actions=['sagemaker:InvokeEndpoint', ],
            resources=[endpoint_arn])
        )

        api = apig_.LambdaRestApi(  # noqa: F841
            self, "call-sm-api", 
            proxy=True, 
            handler=lambda_sm
        )

        # TODO: output API's URI        