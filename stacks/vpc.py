from aws_cdk import core
import aws_cdk.aws_ec2 as ec2


class VpcStack(core.Stack):
    '''
    This will automatically divide the provided VPC CIDR range, and create 
    public and private subnets within a single Availability Zone. Network 
    routing for the public subnets will be configured to allow outbound 
    access directly via an Internet Gateway. Network routing for the private 
    subnets will be configured to allow outbound access via a set of 
    resilient NAT Gateways (one per AZ).
    '''

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.vpc = ec2.Vpc(
            self, "ModelAsAServiceVPC",
            max_azs=1,
            cidr="10.10.0.0/16",
            subnet_configuration=[ec2.SubnetConfiguration(
                subnet_type=ec2.SubnetType.PUBLIC,
                name="Public",
                cidr_mask=24
            ), ec2.SubnetConfiguration(
                subnet_type=ec2.SubnetType.PRIVATE,
                name="Private",
                cidr_mask=24
            )],
            nat_gateways=1
        )
        
        core.CfnOutput(
            self, "Output",
            value=self.vpc.vpc_id
        )
