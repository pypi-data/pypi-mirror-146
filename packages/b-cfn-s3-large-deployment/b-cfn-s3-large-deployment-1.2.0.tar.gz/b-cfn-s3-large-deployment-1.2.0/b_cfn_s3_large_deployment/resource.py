from typing import Dict, List

from aws_cdk.aws_ec2 import IVpc
from aws_cdk.aws_efs import FileSystemProps, FileSystem, Acl, PosixUser
from aws_cdk.aws_s3 import Bucket
from aws_cdk.core import Stack, CustomResource, RemovalPolicy, Construct

from b_cfn_s3_large_deployment.deployment_props import DeploymentProps
from b_cfn_s3_large_deployment.deployment_source import (
    DeploymentSourceContext,
    DeploymentSourceConfig,
    BaseDeploymentSource
)
from b_cfn_s3_large_deployment.efs_props import EfsProps
from b_cfn_s3_large_deployment.function import S3LargeDeploymentFunction

__all__ = [
    'S3LargeDeployment',
    'S3LargeDeploymentResource',
]


class S3LargeDeployment(CustomResource):
    """
    Resource that handles S3 assets deployment with large-files support.

    See README file for possible limitations.

    :param sources: The sources from which to deploy the contents of this bucket.
    :param destination_bucket: The S3 bucket to sync the contents of the zip file to.
    """

    def __init__(
            self,
            scope: Stack,
            name: str,
            sources: List[BaseDeploymentSource],
            destination_bucket: Bucket,
            props: DeploymentProps = None
    ):
        props = props or DeploymentProps()

        if props.use_efs and not props.vpc:
            raise ValueError('Vpc must be specified if ``use_efs`` is set.')

        access_point = None
        access_point_path = '/lambda'
        mount_path = f'/mnt{access_point_path}'
        if props.use_efs and props.vpc:
            file_system = self.__get_efs_filesystem(scope, props.vpc, props.efs_props or EfsProps())
            access_point = file_system.add_access_point(
                f'{name}FunctionAccessPoint',
                path=access_point_path,
                create_acl=Acl(
                    owner_gid='1001',
                    owner_uid='1001',
                    permissions='0777'
                ),
                posix_user=PosixUser(
                    gid='1001',
                    uid='1001'
                )
            )

            access_point.node.add_dependency(file_system.mount_targets_available)

        function = S3LargeDeploymentFunction(
            scope,
            name=f'{name}Function',
            destination_bucket=destination_bucket,
            deployment_props=props,
            mount_path=mount_path,
            access_point=access_point
        )

        self.__sources_configs = {
            source: source.bind(scope, DeploymentSourceContext(handler_role=function.role))
            for source in sources
        }

        super().__init__(
            scope,
            f'CustomResource{name}',
            service_token=function.function_arn,
            removal_policy=RemovalPolicy.DESTROY,
            properties={
                'SourceBucketNames': [src.bucket.bucket_name for src in self.__sources_configs.values()],
                'SourceObjectKeys': [src.zip_object_key for src in self.__sources_configs.values()],
                'DestinationBucketName': destination_bucket.bucket_name,
                'DestinationBucketKeyPrefix': props.destination_key_prefix,
                'RetainOnDelete': props.retain_on_delete,
                'Prune': props.prune,
                'Exclude': props.exclude,
                'Include': props.include,
            }
        )

        self.node.add_dependency(function)
        if access_point:
            self.node.add_dependency(access_point.file_system)

        self.__destination_bucket = destination_bucket
        self.__props = props

    @property
    def source_configs(self) -> Dict[BaseDeploymentSource, DeploymentSourceConfig]:
        return self.__sources_configs.copy()

    @property
    def destination_bucket_name(self) -> str:
        return self.__destination_bucket.bucket_name

    @property
    def destination_bucket_key_prefix(self) -> str:
        return self.__props.destination_key_prefix

    @staticmethod
    def __get_efs_filesystem(scope: Construct, vpc: IVpc, efs_props: EfsProps) -> FileSystem:
        stack = Stack.of(scope)
        efs_uuid = f'Efs{vpc.node.addr.upper()}'
        file_system_props = FileSystemProps(
            vpc=vpc,
            performance_mode=efs_props.performance_mode,
            provisioned_throughput_per_second=efs_props.provisioned_throughput_per_second,
            removal_policy=efs_props.removal_policy,
            throughput_mode=efs_props.throughput_mode
        )

        return stack.node.try_find_child(efs_uuid) or FileSystem(
            scope,
            id=efs_uuid,
            vpc=file_system_props.vpc,
            enable_automatic_backups=file_system_props.enable_automatic_backups,
            encrypted=file_system_props.encrypted,
            file_system_name=file_system_props.file_system_name,
            kms_key=file_system_props.kms_key,
            lifecycle_policy=file_system_props.lifecycle_policy,
            performance_mode=file_system_props.performance_mode,
            provisioned_throughput_per_second=file_system_props.provisioned_throughput_per_second,
            removal_policy=file_system_props.removal_policy,
            security_group=file_system_props.security_group,
            throughput_mode=file_system_props.throughput_mode,
            vpc_subnets=file_system_props.vpc_subnets
        )


# Alias for backward compatibility.
S3LargeDeploymentResource = S3LargeDeployment
