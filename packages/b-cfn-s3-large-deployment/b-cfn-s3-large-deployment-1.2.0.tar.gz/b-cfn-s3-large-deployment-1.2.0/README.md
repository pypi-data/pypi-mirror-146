![Pipeline](https://github.com/Biomapas/B.CfnS3LargeDeployment/workflows/Pipeline/badge.svg?branch=main)

# B.CfnS3LargeDeployment

**b-cfn-s3-large-deployment** - AWS CDK custom resource that handles large files deployment to S3 bucket.

### Description

This custom resource deploys local files or S3 bucket objects to a destination bucket retaining their file-system 
hierarchy.

Two types of deployment sources are available:

- `BucketDeploymentSource` - uses another S3 bucket object(-s) as source for the deployment to a destination bucket. 
  Only files up to 5TB are supported due to S3 bucket limitations;
- `AssetDeploymentSource` - uses `aws-cdk.aws-s3-assets` lib to deploy local files as .zip files to assets bucket from 
  which extracted contents are moved to the destination bucket. Asset files more than 2GB in size are not supported.

See "Known limits" sections below for more information on this resource limitations.

This resource implementation is based on GitHub pull-request https://github.com/aws/aws-cdk/pull/15220.

### Remarks

[Biomapas](https://biomapas.com) aims to modernise life-science
industry by sharing its IT knowledge with other companies and
the community.

### Related technology

- Python >= 3.8
- Amazon Web Services (AWS)

### Assumptions

The project assumes that the person working with it have basic knowledge in python
programming.

### Useful sources

See code documentation for any additional sources and references. Also see `aws-cdk.s3-deployment` library for more 
information as this implementation is based on work done there.

### Install

Use the package manager pip to install this package. This project is not in the PyPi
repository yet. Install directly from source or PyPI.

```bash
pip install .
```

Or

```bash
pip install b-cfn-s3-large-deployment
```

### Usage & Examples

This AWS CloudFormation custom resource is used pretty much the same way as any other resource. Simply initialize it 
within any valid CDK scope giving it unique name/id, providing source(-s) and the destination for the deployment. 

The deployment of files depends on AWS Lambda's `/tmp` directory and its size limits. For large files `/tmp` directory 
size can be configured using Ephemeral storage (`DeploymentProps.ephemeral_storage_size`) supported by AWS Lambda 
functions. 

Optionally, if there's a need for even larger files deployment than what AWS Lambda's `/tmp` directory supports, 
setting the `DeploymentPops.use_efs` and `DeploymentPops.efs_props` fields, AWS Elastic File Storage (EFS) can be 
enabled to allow such files handling.

A simple example of `S3LargeDeploymentResource` usage is shown below:

```python
from aws_cdk.core import App, Stack, Construct
from aws_cdk.aws_s3 import Bucket

from b_cfn_s3_large_deployment.resource import S3LargeDeploymentResource
from b_cfn_s3_large_deployment.deployment_props import DeploymentProps
from b_cfn_s3_large_deployment.deployment_source import AssetDeploymentSource, BucketDeploymentSource


class ExampleStack(Stack):
    def __init__(self, scope: Construct):
        super().__init__(...)

        S3LargeDeploymentResource(
            scope=self,
            name='ExampleLargeDeployment',
            sources=[
                AssetDeploymentSource(path='/path/to/your/local/directory'),
                AssetDeploymentSource(path='/path/to/your/local/zip/file.zip'),
                BucketDeploymentSource(
                  bucket=..., 
                  zip_object_key='your-source-bucket-object-key'
                ),
                ...
            ],
            destination_bucket=Bucket(...),
            props=DeploymentProps(...)
        )
        ...

        
app = App()
ExampleStack(app, 'ExampleStack')

app.synth()
```

Here, three types of supported sources were used:

1. whole, local directory given as a path, which is then deployed to the assets bucket as a .zip object: 

    ```python 
    AssetDeploymentSource(path='/path/to/your/local/directory')
    ```
   
2. single .zip file given as a path, which is then deployed to the assets bucket:
    
    ```python 
    AssetDeploymentSource(path='/path/to/your/local/zip/file.zip')
    ```

3. Single .zip S3 object found in the source bucket, given as an object key. No further pre-processing is 
  applied in this case:
    
    ```python
    BucketDeploymentSource(
       bucket=...,
       zip_object_key='your-source-bucket-object-key'
    )
    ```

In all of these cases, final, source .zip objects are extracted inside `S3LargeDeploymentResource`'s handler 
function storage and the available contents are then deployed to the configured destination. This is all done, while 
maintaining original file structure of source contents.

### Known limits

- `aws_cdk.aws_s3_assets.Asset` supports up to 2GB/asset (limited by NodeJS implementation).
- S3 bucket supports up to 5TB objects.

### Contribution

Found a bug? Want to add or suggest a new feature? Contributions of any kind are gladly
welcome. Contact us, create a pull-request or an issue ticket.
