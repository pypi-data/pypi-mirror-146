import os
from functools import lru_cache
from typing import cast

from aws_cdk.aws_efs import IAccessPoint
from aws_cdk.aws_lambda import Code, Runtime, FileSystem as LambdaFileSystem, Function
from aws_cdk.aws_s3 import Bucket
from aws_cdk.core import Stack, Duration
from aws_cdk.lambda_layer_awscli import AwsCliLayer

from b_cfn_s3_large_deployment.deployment_props import DeploymentProps


class S3LargeDeploymentFunction(Function):
    from . import source
    SOURCE_PATH = os.path.dirname(source.__file__)

    def __init__(
            self,
            scope: Stack,
            name: str,
            destination_bucket: Bucket,
            deployment_props: DeploymentProps,
            mount_path: str = None,
            access_point: IAccessPoint = None
    ) -> None:
        if deployment_props.use_efs and (mount_path is None or access_point is None):
            raise ValueError('While using EFS its access point and mount path must be set.')

        self.__name = name
        super().__init__(
            scope=scope,
            id=name,
            function_name=name,
            code=self.__code(),
            timeout=Duration.minutes(15),
            handler='main.index.handler',
            runtime=cast(Runtime, Runtime.PYTHON_3_7),
            layers=[
                AwsCliLayer(scope, f'{name}AwsCliLayer')
            ],
            environment=None if not deployment_props.use_efs else {
                'MOUNT_PATH': mount_path
            },
            ephemeral_storage_size=deployment_props.ephemeral_storage_size,
            role=deployment_props.role,
            memory_size=deployment_props.memory_limit,
            vpc=deployment_props.vpc,
            vpc_subnets=deployment_props.vpc_subnets,
            filesystem=(
                LambdaFileSystem.from_efs_access_point(access_point, mount_path)
                if deployment_props.use_efs
                else None
            )
        )

        if deployment_props.vpc:
            self.node.add_dependency(deployment_props.vpc)

        if access_point:
            self.node.add_dependency(access_point)

        destination_bucket.grant_read_write(self)

    @lru_cache
    def __code(self) -> Code:
        return Code.from_asset(self.SOURCE_PATH)

    @property
    def function_name(self):
        return self.__name
