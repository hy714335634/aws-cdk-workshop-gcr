"""
## AWS Batch Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development. They are subject to non-backward compatible changes or removal in any future version. These are not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be announced in the release notes. This means that while you may use them, you may need to update your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

## Launch template support

### Usage

Simply define your Launch Template:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
my_launch_template = ec2.CfnLaunchTemplate(self, "LaunchTemplate",
    launch_template_name="extra-storage-template",
    launch_template_data={
        "block_device_mappings": [{
            "device_name": "/dev/xvdcz",
            "ebs": {
                "encrypted": True,
                "volume_size": 100,
                "volume_type": "gp2"
            }
        }
        ]
    }
)
```

and use it:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
my_compute_env = batch.ComputeEnvironment(self, "ComputeEnv",
    compute_resources={
        "launch_template": {
            "launch_template_name": my_launch_template.launch_template_name
        },
        "vpc": vpc
    },
    compute_environment_name="MyStorageCapableComputeEnvironment"
)
```
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

import aws_cdk.aws_ec2
import aws_cdk.aws_ecr
import aws_cdk.aws_ecs
import aws_cdk.aws_iam
import aws_cdk.core
import constructs

from ._jsii import *


@jsii.enum(jsii_type="@aws-cdk/aws-batch.AllocationStrategy")
class AllocationStrategy(enum.Enum):
    """Properties for how to prepare compute resources that are provisioned for a compute environment.

    stability
    :stability: experimental
    """
    BEST_FIT = "BEST_FIT"
    """Batch will use the best fitting instance type will be used when assigning a batch job in this compute environment.

    stability
    :stability: experimental
    """
    BEST_FIT_PROGRESSIVE = "BEST_FIT_PROGRESSIVE"
    """Batch will select additional instance types that are large enough to meet the requirements of the jobs in the queue, with a preference for instance types with a lower cost per unit vCPU.

    stability
    :stability: experimental
    """
    SPOT_CAPACITY_OPTIMIZED = "SPOT_CAPACITY_OPTIMIZED"
    """This is only available for Spot Instance compute resources and will select additional instance types that are large enough to meet the requirements of the jobs in the queue, with a preference for instance types that are less likely to be interrupted.

    stability
    :stability: experimental
    """

@jsii.implements(aws_cdk.core.IInspectable)
class CfnComputeEnvironment(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-batch.CfnComputeEnvironment"):
    """A CloudFormation ``AWS::Batch::ComputeEnvironment``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-computeenvironment.html
    cloudformationResource:
    :cloudformationResource:: AWS::Batch::ComputeEnvironment
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, service_role: str, type: str, compute_environment_name: typing.Optional[str]=None, compute_resources: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["ComputeResourcesProperty"]]]=None, state: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::Batch::ComputeEnvironment``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param service_role: ``AWS::Batch::ComputeEnvironment.ServiceRole``.
        :param type: ``AWS::Batch::ComputeEnvironment.Type``.
        :param compute_environment_name: ``AWS::Batch::ComputeEnvironment.ComputeEnvironmentName``.
        :param compute_resources: ``AWS::Batch::ComputeEnvironment.ComputeResources``.
        :param state: ``AWS::Batch::ComputeEnvironment.State``.
        """
        props = CfnComputeEnvironmentProps(service_role=service_role, type=type, compute_environment_name=compute_environment_name, compute_resources=compute_resources, state=state)

        jsii.create(CfnComputeEnvironment, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: aws_cdk.core.Construct, id: str, resource_attributes: typing.Any, *, finder: aws_cdk.core.ICfnFinder) -> "CfnComputeEnvironment":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -
        :param finder: The finder interface used to resolve references across the template.

        stability
        :stability: experimental
        """
        options = aws_cdk.core.FromCloudFormationOptions(finder=finder)

        return jsii.sinvoke(cls, "fromCloudFormation", [scope, id, resource_attributes, options])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str, typing.Any]) -> typing.Mapping[str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="serviceRole")
    def service_role(self) -> str:
        """``AWS::Batch::ComputeEnvironment.ServiceRole``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-computeenvironment.html#cfn-batch-computeenvironment-servicerole
        """
        return jsii.get(self, "serviceRole")

    @service_role.setter
    def service_role(self, value: str):
        jsii.set(self, "serviceRole", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> str:
        """``AWS::Batch::ComputeEnvironment.Type``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-computeenvironment.html#cfn-batch-computeenvironment-type
        """
        return jsii.get(self, "type")

    @type.setter
    def type(self, value: str):
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="computeEnvironmentName")
    def compute_environment_name(self) -> typing.Optional[str]:
        """``AWS::Batch::ComputeEnvironment.ComputeEnvironmentName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-computeenvironment.html#cfn-batch-computeenvironment-computeenvironmentname
        """
        return jsii.get(self, "computeEnvironmentName")

    @compute_environment_name.setter
    def compute_environment_name(self, value: typing.Optional[str]):
        jsii.set(self, "computeEnvironmentName", value)

    @builtins.property
    @jsii.member(jsii_name="computeResources")
    def compute_resources(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["ComputeResourcesProperty"]]]:
        """``AWS::Batch::ComputeEnvironment.ComputeResources``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-computeenvironment.html#cfn-batch-computeenvironment-computeresources
        """
        return jsii.get(self, "computeResources")

    @compute_resources.setter
    def compute_resources(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["ComputeResourcesProperty"]]]):
        jsii.set(self, "computeResources", value)

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> typing.Optional[str]:
        """``AWS::Batch::ComputeEnvironment.State``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-computeenvironment.html#cfn-batch-computeenvironment-state
        """
        return jsii.get(self, "state")

    @state.setter
    def state(self, value: typing.Optional[str]):
        jsii.set(self, "state", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-batch.CfnComputeEnvironment.ComputeResourcesProperty", jsii_struct_bases=[], name_mapping={'instance_role': 'instanceRole', 'instance_types': 'instanceTypes', 'maxv_cpus': 'maxvCpus', 'minv_cpus': 'minvCpus', 'subnets': 'subnets', 'type': 'type', 'allocation_strategy': 'allocationStrategy', 'bid_percentage': 'bidPercentage', 'desiredv_cpus': 'desiredvCpus', 'ec2_key_pair': 'ec2KeyPair', 'image_id': 'imageId', 'launch_template': 'launchTemplate', 'placement_group': 'placementGroup', 'security_group_ids': 'securityGroupIds', 'spot_iam_fleet_role': 'spotIamFleetRole', 'tags': 'tags'})
    class ComputeResourcesProperty():
        def __init__(self, *, instance_role: str, instance_types: typing.List[str], maxv_cpus: jsii.Number, minv_cpus: jsii.Number, subnets: typing.List[str], type: str, allocation_strategy: typing.Optional[str]=None, bid_percentage: typing.Optional[jsii.Number]=None, desiredv_cpus: typing.Optional[jsii.Number]=None, ec2_key_pair: typing.Optional[str]=None, image_id: typing.Optional[str]=None, launch_template: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnComputeEnvironment.LaunchTemplateSpecificationProperty"]]]=None, placement_group: typing.Optional[str]=None, security_group_ids: typing.Optional[typing.List[str]]=None, spot_iam_fleet_role: typing.Optional[str]=None, tags: typing.Any=None) -> None:
            """
            :param instance_role: ``CfnComputeEnvironment.ComputeResourcesProperty.InstanceRole``.
            :param instance_types: ``CfnComputeEnvironment.ComputeResourcesProperty.InstanceTypes``.
            :param maxv_cpus: ``CfnComputeEnvironment.ComputeResourcesProperty.MaxvCpus``.
            :param minv_cpus: ``CfnComputeEnvironment.ComputeResourcesProperty.MinvCpus``.
            :param subnets: ``CfnComputeEnvironment.ComputeResourcesProperty.Subnets``.
            :param type: ``CfnComputeEnvironment.ComputeResourcesProperty.Type``.
            :param allocation_strategy: ``CfnComputeEnvironment.ComputeResourcesProperty.AllocationStrategy``.
            :param bid_percentage: ``CfnComputeEnvironment.ComputeResourcesProperty.BidPercentage``.
            :param desiredv_cpus: ``CfnComputeEnvironment.ComputeResourcesProperty.DesiredvCpus``.
            :param ec2_key_pair: ``CfnComputeEnvironment.ComputeResourcesProperty.Ec2KeyPair``.
            :param image_id: ``CfnComputeEnvironment.ComputeResourcesProperty.ImageId``.
            :param launch_template: ``CfnComputeEnvironment.ComputeResourcesProperty.LaunchTemplate``.
            :param placement_group: ``CfnComputeEnvironment.ComputeResourcesProperty.PlacementGroup``.
            :param security_group_ids: ``CfnComputeEnvironment.ComputeResourcesProperty.SecurityGroupIds``.
            :param spot_iam_fleet_role: ``CfnComputeEnvironment.ComputeResourcesProperty.SpotIamFleetRole``.
            :param tags: ``CfnComputeEnvironment.ComputeResourcesProperty.Tags``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html
            """
            self._values = {
                'instance_role': instance_role,
                'instance_types': instance_types,
                'maxv_cpus': maxv_cpus,
                'minv_cpus': minv_cpus,
                'subnets': subnets,
                'type': type,
            }
            if allocation_strategy is not None: self._values["allocation_strategy"] = allocation_strategy
            if bid_percentage is not None: self._values["bid_percentage"] = bid_percentage
            if desiredv_cpus is not None: self._values["desiredv_cpus"] = desiredv_cpus
            if ec2_key_pair is not None: self._values["ec2_key_pair"] = ec2_key_pair
            if image_id is not None: self._values["image_id"] = image_id
            if launch_template is not None: self._values["launch_template"] = launch_template
            if placement_group is not None: self._values["placement_group"] = placement_group
            if security_group_ids is not None: self._values["security_group_ids"] = security_group_ids
            if spot_iam_fleet_role is not None: self._values["spot_iam_fleet_role"] = spot_iam_fleet_role
            if tags is not None: self._values["tags"] = tags

        @builtins.property
        def instance_role(self) -> str:
            """``CfnComputeEnvironment.ComputeResourcesProperty.InstanceRole``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-instancerole
            """
            return self._values.get('instance_role')

        @builtins.property
        def instance_types(self) -> typing.List[str]:
            """``CfnComputeEnvironment.ComputeResourcesProperty.InstanceTypes``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-instancetypes
            """
            return self._values.get('instance_types')

        @builtins.property
        def maxv_cpus(self) -> jsii.Number:
            """``CfnComputeEnvironment.ComputeResourcesProperty.MaxvCpus``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-maxvcpus
            """
            return self._values.get('maxv_cpus')

        @builtins.property
        def minv_cpus(self) -> jsii.Number:
            """``CfnComputeEnvironment.ComputeResourcesProperty.MinvCpus``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-minvcpus
            """
            return self._values.get('minv_cpus')

        @builtins.property
        def subnets(self) -> typing.List[str]:
            """``CfnComputeEnvironment.ComputeResourcesProperty.Subnets``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-subnets
            """
            return self._values.get('subnets')

        @builtins.property
        def type(self) -> str:
            """``CfnComputeEnvironment.ComputeResourcesProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-type
            """
            return self._values.get('type')

        @builtins.property
        def allocation_strategy(self) -> typing.Optional[str]:
            """``CfnComputeEnvironment.ComputeResourcesProperty.AllocationStrategy``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-allocationstrategy
            """
            return self._values.get('allocation_strategy')

        @builtins.property
        def bid_percentage(self) -> typing.Optional[jsii.Number]:
            """``CfnComputeEnvironment.ComputeResourcesProperty.BidPercentage``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-bidpercentage
            """
            return self._values.get('bid_percentage')

        @builtins.property
        def desiredv_cpus(self) -> typing.Optional[jsii.Number]:
            """``CfnComputeEnvironment.ComputeResourcesProperty.DesiredvCpus``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-desiredvcpus
            """
            return self._values.get('desiredv_cpus')

        @builtins.property
        def ec2_key_pair(self) -> typing.Optional[str]:
            """``CfnComputeEnvironment.ComputeResourcesProperty.Ec2KeyPair``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-ec2keypair
            """
            return self._values.get('ec2_key_pair')

        @builtins.property
        def image_id(self) -> typing.Optional[str]:
            """``CfnComputeEnvironment.ComputeResourcesProperty.ImageId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-imageid
            """
            return self._values.get('image_id')

        @builtins.property
        def launch_template(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnComputeEnvironment.LaunchTemplateSpecificationProperty"]]]:
            """``CfnComputeEnvironment.ComputeResourcesProperty.LaunchTemplate``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-launchtemplate
            """
            return self._values.get('launch_template')

        @builtins.property
        def placement_group(self) -> typing.Optional[str]:
            """``CfnComputeEnvironment.ComputeResourcesProperty.PlacementGroup``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-placementgroup
            """
            return self._values.get('placement_group')

        @builtins.property
        def security_group_ids(self) -> typing.Optional[typing.List[str]]:
            """``CfnComputeEnvironment.ComputeResourcesProperty.SecurityGroupIds``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-securitygroupids
            """
            return self._values.get('security_group_ids')

        @builtins.property
        def spot_iam_fleet_role(self) -> typing.Optional[str]:
            """``CfnComputeEnvironment.ComputeResourcesProperty.SpotIamFleetRole``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-spotiamfleetrole
            """
            return self._values.get('spot_iam_fleet_role')

        @builtins.property
        def tags(self) -> typing.Any:
            """``CfnComputeEnvironment.ComputeResourcesProperty.Tags``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-tags
            """
            return self._values.get('tags')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ComputeResourcesProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-batch.CfnComputeEnvironment.LaunchTemplateSpecificationProperty", jsii_struct_bases=[], name_mapping={'launch_template_id': 'launchTemplateId', 'launch_template_name': 'launchTemplateName', 'version': 'version'})
    class LaunchTemplateSpecificationProperty():
        def __init__(self, *, launch_template_id: typing.Optional[str]=None, launch_template_name: typing.Optional[str]=None, version: typing.Optional[str]=None) -> None:
            """
            :param launch_template_id: ``CfnComputeEnvironment.LaunchTemplateSpecificationProperty.LaunchTemplateId``.
            :param launch_template_name: ``CfnComputeEnvironment.LaunchTemplateSpecificationProperty.LaunchTemplateName``.
            :param version: ``CfnComputeEnvironment.LaunchTemplateSpecificationProperty.Version``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-launchtemplatespecification.html
            """
            self._values = {
            }
            if launch_template_id is not None: self._values["launch_template_id"] = launch_template_id
            if launch_template_name is not None: self._values["launch_template_name"] = launch_template_name
            if version is not None: self._values["version"] = version

        @builtins.property
        def launch_template_id(self) -> typing.Optional[str]:
            """``CfnComputeEnvironment.LaunchTemplateSpecificationProperty.LaunchTemplateId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-launchtemplatespecification.html#cfn-batch-computeenvironment-launchtemplatespecification-launchtemplateid
            """
            return self._values.get('launch_template_id')

        @builtins.property
        def launch_template_name(self) -> typing.Optional[str]:
            """``CfnComputeEnvironment.LaunchTemplateSpecificationProperty.LaunchTemplateName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-launchtemplatespecification.html#cfn-batch-computeenvironment-launchtemplatespecification-launchtemplatename
            """
            return self._values.get('launch_template_name')

        @builtins.property
        def version(self) -> typing.Optional[str]:
            """``CfnComputeEnvironment.LaunchTemplateSpecificationProperty.Version``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-launchtemplatespecification.html#cfn-batch-computeenvironment-launchtemplatespecification-version
            """
            return self._values.get('version')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'LaunchTemplateSpecificationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-batch.CfnComputeEnvironmentProps", jsii_struct_bases=[], name_mapping={'service_role': 'serviceRole', 'type': 'type', 'compute_environment_name': 'computeEnvironmentName', 'compute_resources': 'computeResources', 'state': 'state'})
class CfnComputeEnvironmentProps():
    def __init__(self, *, service_role: str, type: str, compute_environment_name: typing.Optional[str]=None, compute_resources: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnComputeEnvironment.ComputeResourcesProperty"]]]=None, state: typing.Optional[str]=None) -> None:
        """Properties for defining a ``AWS::Batch::ComputeEnvironment``.

        :param service_role: ``AWS::Batch::ComputeEnvironment.ServiceRole``.
        :param type: ``AWS::Batch::ComputeEnvironment.Type``.
        :param compute_environment_name: ``AWS::Batch::ComputeEnvironment.ComputeEnvironmentName``.
        :param compute_resources: ``AWS::Batch::ComputeEnvironment.ComputeResources``.
        :param state: ``AWS::Batch::ComputeEnvironment.State``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-computeenvironment.html
        """
        self._values = {
            'service_role': service_role,
            'type': type,
        }
        if compute_environment_name is not None: self._values["compute_environment_name"] = compute_environment_name
        if compute_resources is not None: self._values["compute_resources"] = compute_resources
        if state is not None: self._values["state"] = state

    @builtins.property
    def service_role(self) -> str:
        """``AWS::Batch::ComputeEnvironment.ServiceRole``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-computeenvironment.html#cfn-batch-computeenvironment-servicerole
        """
        return self._values.get('service_role')

    @builtins.property
    def type(self) -> str:
        """``AWS::Batch::ComputeEnvironment.Type``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-computeenvironment.html#cfn-batch-computeenvironment-type
        """
        return self._values.get('type')

    @builtins.property
    def compute_environment_name(self) -> typing.Optional[str]:
        """``AWS::Batch::ComputeEnvironment.ComputeEnvironmentName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-computeenvironment.html#cfn-batch-computeenvironment-computeenvironmentname
        """
        return self._values.get('compute_environment_name')

    @builtins.property
    def compute_resources(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnComputeEnvironment.ComputeResourcesProperty"]]]:
        """``AWS::Batch::ComputeEnvironment.ComputeResources``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-computeenvironment.html#cfn-batch-computeenvironment-computeresources
        """
        return self._values.get('compute_resources')

    @builtins.property
    def state(self) -> typing.Optional[str]:
        """``AWS::Batch::ComputeEnvironment.State``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-computeenvironment.html#cfn-batch-computeenvironment-state
        """
        return self._values.get('state')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnComputeEnvironmentProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnJobDefinition(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-batch.CfnJobDefinition"):
    """A CloudFormation ``AWS::Batch::JobDefinition``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobdefinition.html
    cloudformationResource:
    :cloudformationResource:: AWS::Batch::JobDefinition
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, type: str, container_properties: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["ContainerPropertiesProperty"]]]=None, job_definition_name: typing.Optional[str]=None, node_properties: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["NodePropertiesProperty"]]]=None, parameters: typing.Any=None, retry_strategy: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["RetryStrategyProperty"]]]=None, timeout: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["TimeoutProperty"]]]=None) -> None:
        """Create a new ``AWS::Batch::JobDefinition``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param type: ``AWS::Batch::JobDefinition.Type``.
        :param container_properties: ``AWS::Batch::JobDefinition.ContainerProperties``.
        :param job_definition_name: ``AWS::Batch::JobDefinition.JobDefinitionName``.
        :param node_properties: ``AWS::Batch::JobDefinition.NodeProperties``.
        :param parameters: ``AWS::Batch::JobDefinition.Parameters``.
        :param retry_strategy: ``AWS::Batch::JobDefinition.RetryStrategy``.
        :param timeout: ``AWS::Batch::JobDefinition.Timeout``.
        """
        props = CfnJobDefinitionProps(type=type, container_properties=container_properties, job_definition_name=job_definition_name, node_properties=node_properties, parameters=parameters, retry_strategy=retry_strategy, timeout=timeout)

        jsii.create(CfnJobDefinition, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: aws_cdk.core.Construct, id: str, resource_attributes: typing.Any, *, finder: aws_cdk.core.ICfnFinder) -> "CfnJobDefinition":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -
        :param finder: The finder interface used to resolve references across the template.

        stability
        :stability: experimental
        """
        options = aws_cdk.core.FromCloudFormationOptions(finder=finder)

        return jsii.sinvoke(cls, "fromCloudFormation", [scope, id, resource_attributes, options])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str, typing.Any]) -> typing.Mapping[str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> typing.Any:
        """``AWS::Batch::JobDefinition.Parameters``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobdefinition.html#cfn-batch-jobdefinition-parameters
        """
        return jsii.get(self, "parameters")

    @parameters.setter
    def parameters(self, value: typing.Any):
        jsii.set(self, "parameters", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> str:
        """``AWS::Batch::JobDefinition.Type``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobdefinition.html#cfn-batch-jobdefinition-type
        """
        return jsii.get(self, "type")

    @type.setter
    def type(self, value: str):
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="containerProperties")
    def container_properties(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["ContainerPropertiesProperty"]]]:
        """``AWS::Batch::JobDefinition.ContainerProperties``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobdefinition.html#cfn-batch-jobdefinition-containerproperties
        """
        return jsii.get(self, "containerProperties")

    @container_properties.setter
    def container_properties(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["ContainerPropertiesProperty"]]]):
        jsii.set(self, "containerProperties", value)

    @builtins.property
    @jsii.member(jsii_name="jobDefinitionName")
    def job_definition_name(self) -> typing.Optional[str]:
        """``AWS::Batch::JobDefinition.JobDefinitionName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobdefinition.html#cfn-batch-jobdefinition-jobdefinitionname
        """
        return jsii.get(self, "jobDefinitionName")

    @job_definition_name.setter
    def job_definition_name(self, value: typing.Optional[str]):
        jsii.set(self, "jobDefinitionName", value)

    @builtins.property
    @jsii.member(jsii_name="nodeProperties")
    def node_properties(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["NodePropertiesProperty"]]]:
        """``AWS::Batch::JobDefinition.NodeProperties``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobdefinition.html#cfn-batch-jobdefinition-nodeproperties
        """
        return jsii.get(self, "nodeProperties")

    @node_properties.setter
    def node_properties(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["NodePropertiesProperty"]]]):
        jsii.set(self, "nodeProperties", value)

    @builtins.property
    @jsii.member(jsii_name="retryStrategy")
    def retry_strategy(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["RetryStrategyProperty"]]]:
        """``AWS::Batch::JobDefinition.RetryStrategy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobdefinition.html#cfn-batch-jobdefinition-retrystrategy
        """
        return jsii.get(self, "retryStrategy")

    @retry_strategy.setter
    def retry_strategy(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["RetryStrategyProperty"]]]):
        jsii.set(self, "retryStrategy", value)

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["TimeoutProperty"]]]:
        """``AWS::Batch::JobDefinition.Timeout``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobdefinition.html#cfn-batch-jobdefinition-timeout
        """
        return jsii.get(self, "timeout")

    @timeout.setter
    def timeout(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["TimeoutProperty"]]]):
        jsii.set(self, "timeout", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-batch.CfnJobDefinition.ContainerPropertiesProperty", jsii_struct_bases=[], name_mapping={'image': 'image', 'command': 'command', 'environment': 'environment', 'instance_type': 'instanceType', 'job_role_arn': 'jobRoleArn', 'linux_parameters': 'linuxParameters', 'memory': 'memory', 'mount_points': 'mountPoints', 'privileged': 'privileged', 'readonly_root_filesystem': 'readonlyRootFilesystem', 'resource_requirements': 'resourceRequirements', 'ulimits': 'ulimits', 'user': 'user', 'vcpus': 'vcpus', 'volumes': 'volumes'})
    class ContainerPropertiesProperty():
        def __init__(self, *, image: str, command: typing.Optional[typing.List[str]]=None, environment: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnJobDefinition.EnvironmentProperty"]]]]]=None, instance_type: typing.Optional[str]=None, job_role_arn: typing.Optional[str]=None, linux_parameters: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnJobDefinition.LinuxParametersProperty"]]]=None, memory: typing.Optional[jsii.Number]=None, mount_points: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnJobDefinition.MountPointsProperty"]]]]]=None, privileged: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, readonly_root_filesystem: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, resource_requirements: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnJobDefinition.ResourceRequirementProperty"]]]]]=None, ulimits: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnJobDefinition.UlimitProperty"]]]]]=None, user: typing.Optional[str]=None, vcpus: typing.Optional[jsii.Number]=None, volumes: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnJobDefinition.VolumesProperty"]]]]]=None) -> None:
            """
            :param image: ``CfnJobDefinition.ContainerPropertiesProperty.Image``.
            :param command: ``CfnJobDefinition.ContainerPropertiesProperty.Command``.
            :param environment: ``CfnJobDefinition.ContainerPropertiesProperty.Environment``.
            :param instance_type: ``CfnJobDefinition.ContainerPropertiesProperty.InstanceType``.
            :param job_role_arn: ``CfnJobDefinition.ContainerPropertiesProperty.JobRoleArn``.
            :param linux_parameters: ``CfnJobDefinition.ContainerPropertiesProperty.LinuxParameters``.
            :param memory: ``CfnJobDefinition.ContainerPropertiesProperty.Memory``.
            :param mount_points: ``CfnJobDefinition.ContainerPropertiesProperty.MountPoints``.
            :param privileged: ``CfnJobDefinition.ContainerPropertiesProperty.Privileged``.
            :param readonly_root_filesystem: ``CfnJobDefinition.ContainerPropertiesProperty.ReadonlyRootFilesystem``.
            :param resource_requirements: ``CfnJobDefinition.ContainerPropertiesProperty.ResourceRequirements``.
            :param ulimits: ``CfnJobDefinition.ContainerPropertiesProperty.Ulimits``.
            :param user: ``CfnJobDefinition.ContainerPropertiesProperty.User``.
            :param vcpus: ``CfnJobDefinition.ContainerPropertiesProperty.Vcpus``.
            :param volumes: ``CfnJobDefinition.ContainerPropertiesProperty.Volumes``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html
            """
            self._values = {
                'image': image,
            }
            if command is not None: self._values["command"] = command
            if environment is not None: self._values["environment"] = environment
            if instance_type is not None: self._values["instance_type"] = instance_type
            if job_role_arn is not None: self._values["job_role_arn"] = job_role_arn
            if linux_parameters is not None: self._values["linux_parameters"] = linux_parameters
            if memory is not None: self._values["memory"] = memory
            if mount_points is not None: self._values["mount_points"] = mount_points
            if privileged is not None: self._values["privileged"] = privileged
            if readonly_root_filesystem is not None: self._values["readonly_root_filesystem"] = readonly_root_filesystem
            if resource_requirements is not None: self._values["resource_requirements"] = resource_requirements
            if ulimits is not None: self._values["ulimits"] = ulimits
            if user is not None: self._values["user"] = user
            if vcpus is not None: self._values["vcpus"] = vcpus
            if volumes is not None: self._values["volumes"] = volumes

        @builtins.property
        def image(self) -> str:
            """``CfnJobDefinition.ContainerPropertiesProperty.Image``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html#cfn-batch-jobdefinition-containerproperties-image
            """
            return self._values.get('image')

        @builtins.property
        def command(self) -> typing.Optional[typing.List[str]]:
            """``CfnJobDefinition.ContainerPropertiesProperty.Command``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html#cfn-batch-jobdefinition-containerproperties-command
            """
            return self._values.get('command')

        @builtins.property
        def environment(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnJobDefinition.EnvironmentProperty"]]]]]:
            """``CfnJobDefinition.ContainerPropertiesProperty.Environment``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html#cfn-batch-jobdefinition-containerproperties-environment
            """
            return self._values.get('environment')

        @builtins.property
        def instance_type(self) -> typing.Optional[str]:
            """``CfnJobDefinition.ContainerPropertiesProperty.InstanceType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html#cfn-batch-jobdefinition-containerproperties-instancetype
            """
            return self._values.get('instance_type')

        @builtins.property
        def job_role_arn(self) -> typing.Optional[str]:
            """``CfnJobDefinition.ContainerPropertiesProperty.JobRoleArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html#cfn-batch-jobdefinition-containerproperties-jobrolearn
            """
            return self._values.get('job_role_arn')

        @builtins.property
        def linux_parameters(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnJobDefinition.LinuxParametersProperty"]]]:
            """``CfnJobDefinition.ContainerPropertiesProperty.LinuxParameters``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html#cfn-batch-jobdefinition-containerproperties-linuxparameters
            """
            return self._values.get('linux_parameters')

        @builtins.property
        def memory(self) -> typing.Optional[jsii.Number]:
            """``CfnJobDefinition.ContainerPropertiesProperty.Memory``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html#cfn-batch-jobdefinition-containerproperties-memory
            """
            return self._values.get('memory')

        @builtins.property
        def mount_points(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnJobDefinition.MountPointsProperty"]]]]]:
            """``CfnJobDefinition.ContainerPropertiesProperty.MountPoints``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html#cfn-batch-jobdefinition-containerproperties-mountpoints
            """
            return self._values.get('mount_points')

        @builtins.property
        def privileged(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnJobDefinition.ContainerPropertiesProperty.Privileged``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html#cfn-batch-jobdefinition-containerproperties-privileged
            """
            return self._values.get('privileged')

        @builtins.property
        def readonly_root_filesystem(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnJobDefinition.ContainerPropertiesProperty.ReadonlyRootFilesystem``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html#cfn-batch-jobdefinition-containerproperties-readonlyrootfilesystem
            """
            return self._values.get('readonly_root_filesystem')

        @builtins.property
        def resource_requirements(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnJobDefinition.ResourceRequirementProperty"]]]]]:
            """``CfnJobDefinition.ContainerPropertiesProperty.ResourceRequirements``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html#cfn-batch-jobdefinition-containerproperties-resourcerequirements
            """
            return self._values.get('resource_requirements')

        @builtins.property
        def ulimits(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnJobDefinition.UlimitProperty"]]]]]:
            """``CfnJobDefinition.ContainerPropertiesProperty.Ulimits``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html#cfn-batch-jobdefinition-containerproperties-ulimits
            """
            return self._values.get('ulimits')

        @builtins.property
        def user(self) -> typing.Optional[str]:
            """``CfnJobDefinition.ContainerPropertiesProperty.User``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html#cfn-batch-jobdefinition-containerproperties-user
            """
            return self._values.get('user')

        @builtins.property
        def vcpus(self) -> typing.Optional[jsii.Number]:
            """``CfnJobDefinition.ContainerPropertiesProperty.Vcpus``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html#cfn-batch-jobdefinition-containerproperties-vcpus
            """
            return self._values.get('vcpus')

        @builtins.property
        def volumes(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnJobDefinition.VolumesProperty"]]]]]:
            """``CfnJobDefinition.ContainerPropertiesProperty.Volumes``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html#cfn-batch-jobdefinition-containerproperties-volumes
            """
            return self._values.get('volumes')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ContainerPropertiesProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-batch.CfnJobDefinition.DeviceProperty", jsii_struct_bases=[], name_mapping={'container_path': 'containerPath', 'host_path': 'hostPath', 'permissions': 'permissions'})
    class DeviceProperty():
        def __init__(self, *, container_path: typing.Optional[str]=None, host_path: typing.Optional[str]=None, permissions: typing.Optional[typing.List[str]]=None) -> None:
            """
            :param container_path: ``CfnJobDefinition.DeviceProperty.ContainerPath``.
            :param host_path: ``CfnJobDefinition.DeviceProperty.HostPath``.
            :param permissions: ``CfnJobDefinition.DeviceProperty.Permissions``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-device.html
            """
            self._values = {
            }
            if container_path is not None: self._values["container_path"] = container_path
            if host_path is not None: self._values["host_path"] = host_path
            if permissions is not None: self._values["permissions"] = permissions

        @builtins.property
        def container_path(self) -> typing.Optional[str]:
            """``CfnJobDefinition.DeviceProperty.ContainerPath``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-device.html#cfn-batch-jobdefinition-device-containerpath
            """
            return self._values.get('container_path')

        @builtins.property
        def host_path(self) -> typing.Optional[str]:
            """``CfnJobDefinition.DeviceProperty.HostPath``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-device.html#cfn-batch-jobdefinition-device-hostpath
            """
            return self._values.get('host_path')

        @builtins.property
        def permissions(self) -> typing.Optional[typing.List[str]]:
            """``CfnJobDefinition.DeviceProperty.Permissions``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-device.html#cfn-batch-jobdefinition-device-permissions
            """
            return self._values.get('permissions')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'DeviceProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-batch.CfnJobDefinition.EnvironmentProperty", jsii_struct_bases=[], name_mapping={'name': 'name', 'value': 'value'})
    class EnvironmentProperty():
        def __init__(self, *, name: typing.Optional[str]=None, value: typing.Optional[str]=None) -> None:
            """
            :param name: ``CfnJobDefinition.EnvironmentProperty.Name``.
            :param value: ``CfnJobDefinition.EnvironmentProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-environment.html
            """
            self._values = {
            }
            if name is not None: self._values["name"] = name
            if value is not None: self._values["value"] = value

        @builtins.property
        def name(self) -> typing.Optional[str]:
            """``CfnJobDefinition.EnvironmentProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-environment.html#cfn-batch-jobdefinition-environment-name
            """
            return self._values.get('name')

        @builtins.property
        def value(self) -> typing.Optional[str]:
            """``CfnJobDefinition.EnvironmentProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-environment.html#cfn-batch-jobdefinition-environment-value
            """
            return self._values.get('value')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'EnvironmentProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-batch.CfnJobDefinition.LinuxParametersProperty", jsii_struct_bases=[], name_mapping={'devices': 'devices'})
    class LinuxParametersProperty():
        def __init__(self, *, devices: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnJobDefinition.DeviceProperty"]]]]]=None) -> None:
            """
            :param devices: ``CfnJobDefinition.LinuxParametersProperty.Devices``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties-linuxparameters.html
            """
            self._values = {
            }
            if devices is not None: self._values["devices"] = devices

        @builtins.property
        def devices(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnJobDefinition.DeviceProperty"]]]]]:
            """``CfnJobDefinition.LinuxParametersProperty.Devices``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties-linuxparameters.html#cfn-batch-jobdefinition-containerproperties-linuxparameters-devices
            """
            return self._values.get('devices')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'LinuxParametersProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-batch.CfnJobDefinition.MountPointsProperty", jsii_struct_bases=[], name_mapping={'container_path': 'containerPath', 'read_only': 'readOnly', 'source_volume': 'sourceVolume'})
    class MountPointsProperty():
        def __init__(self, *, container_path: typing.Optional[str]=None, read_only: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, source_volume: typing.Optional[str]=None) -> None:
            """
            :param container_path: ``CfnJobDefinition.MountPointsProperty.ContainerPath``.
            :param read_only: ``CfnJobDefinition.MountPointsProperty.ReadOnly``.
            :param source_volume: ``CfnJobDefinition.MountPointsProperty.SourceVolume``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-mountpoints.html
            """
            self._values = {
            }
            if container_path is not None: self._values["container_path"] = container_path
            if read_only is not None: self._values["read_only"] = read_only
            if source_volume is not None: self._values["source_volume"] = source_volume

        @builtins.property
        def container_path(self) -> typing.Optional[str]:
            """``CfnJobDefinition.MountPointsProperty.ContainerPath``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-mountpoints.html#cfn-batch-jobdefinition-mountpoints-containerpath
            """
            return self._values.get('container_path')

        @builtins.property
        def read_only(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnJobDefinition.MountPointsProperty.ReadOnly``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-mountpoints.html#cfn-batch-jobdefinition-mountpoints-readonly
            """
            return self._values.get('read_only')

        @builtins.property
        def source_volume(self) -> typing.Optional[str]:
            """``CfnJobDefinition.MountPointsProperty.SourceVolume``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-mountpoints.html#cfn-batch-jobdefinition-mountpoints-sourcevolume
            """
            return self._values.get('source_volume')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'MountPointsProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-batch.CfnJobDefinition.NodePropertiesProperty", jsii_struct_bases=[], name_mapping={'main_node': 'mainNode', 'node_range_properties': 'nodeRangeProperties', 'num_nodes': 'numNodes'})
    class NodePropertiesProperty():
        def __init__(self, *, main_node: jsii.Number, node_range_properties: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnJobDefinition.NodeRangePropertyProperty"]]], num_nodes: jsii.Number) -> None:
            """
            :param main_node: ``CfnJobDefinition.NodePropertiesProperty.MainNode``.
            :param node_range_properties: ``CfnJobDefinition.NodePropertiesProperty.NodeRangeProperties``.
            :param num_nodes: ``CfnJobDefinition.NodePropertiesProperty.NumNodes``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-nodeproperties.html
            """
            self._values = {
                'main_node': main_node,
                'node_range_properties': node_range_properties,
                'num_nodes': num_nodes,
            }

        @builtins.property
        def main_node(self) -> jsii.Number:
            """``CfnJobDefinition.NodePropertiesProperty.MainNode``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-nodeproperties.html#cfn-batch-jobdefinition-nodeproperties-mainnode
            """
            return self._values.get('main_node')

        @builtins.property
        def node_range_properties(self) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnJobDefinition.NodeRangePropertyProperty"]]]:
            """``CfnJobDefinition.NodePropertiesProperty.NodeRangeProperties``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-nodeproperties.html#cfn-batch-jobdefinition-nodeproperties-noderangeproperties
            """
            return self._values.get('node_range_properties')

        @builtins.property
        def num_nodes(self) -> jsii.Number:
            """``CfnJobDefinition.NodePropertiesProperty.NumNodes``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-nodeproperties.html#cfn-batch-jobdefinition-nodeproperties-numnodes
            """
            return self._values.get('num_nodes')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'NodePropertiesProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-batch.CfnJobDefinition.NodeRangePropertyProperty", jsii_struct_bases=[], name_mapping={'target_nodes': 'targetNodes', 'container': 'container'})
    class NodeRangePropertyProperty():
        def __init__(self, *, target_nodes: str, container: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnJobDefinition.ContainerPropertiesProperty"]]]=None) -> None:
            """
            :param target_nodes: ``CfnJobDefinition.NodeRangePropertyProperty.TargetNodes``.
            :param container: ``CfnJobDefinition.NodeRangePropertyProperty.Container``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-noderangeproperty.html
            """
            self._values = {
                'target_nodes': target_nodes,
            }
            if container is not None: self._values["container"] = container

        @builtins.property
        def target_nodes(self) -> str:
            """``CfnJobDefinition.NodeRangePropertyProperty.TargetNodes``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-noderangeproperty.html#cfn-batch-jobdefinition-noderangeproperty-targetnodes
            """
            return self._values.get('target_nodes')

        @builtins.property
        def container(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnJobDefinition.ContainerPropertiesProperty"]]]:
            """``CfnJobDefinition.NodeRangePropertyProperty.Container``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-noderangeproperty.html#cfn-batch-jobdefinition-noderangeproperty-container
            """
            return self._values.get('container')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'NodeRangePropertyProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-batch.CfnJobDefinition.ResourceRequirementProperty", jsii_struct_bases=[], name_mapping={'type': 'type', 'value': 'value'})
    class ResourceRequirementProperty():
        def __init__(self, *, type: typing.Optional[str]=None, value: typing.Optional[str]=None) -> None:
            """
            :param type: ``CfnJobDefinition.ResourceRequirementProperty.Type``.
            :param value: ``CfnJobDefinition.ResourceRequirementProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-resourcerequirement.html
            """
            self._values = {
            }
            if type is not None: self._values["type"] = type
            if value is not None: self._values["value"] = value

        @builtins.property
        def type(self) -> typing.Optional[str]:
            """``CfnJobDefinition.ResourceRequirementProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-resourcerequirement.html#cfn-batch-jobdefinition-resourcerequirement-type
            """
            return self._values.get('type')

        @builtins.property
        def value(self) -> typing.Optional[str]:
            """``CfnJobDefinition.ResourceRequirementProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-resourcerequirement.html#cfn-batch-jobdefinition-resourcerequirement-value
            """
            return self._values.get('value')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ResourceRequirementProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-batch.CfnJobDefinition.RetryStrategyProperty", jsii_struct_bases=[], name_mapping={'attempts': 'attempts'})
    class RetryStrategyProperty():
        def __init__(self, *, attempts: typing.Optional[jsii.Number]=None) -> None:
            """
            :param attempts: ``CfnJobDefinition.RetryStrategyProperty.Attempts``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-retrystrategy.html
            """
            self._values = {
            }
            if attempts is not None: self._values["attempts"] = attempts

        @builtins.property
        def attempts(self) -> typing.Optional[jsii.Number]:
            """``CfnJobDefinition.RetryStrategyProperty.Attempts``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-retrystrategy.html#cfn-batch-jobdefinition-retrystrategy-attempts
            """
            return self._values.get('attempts')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'RetryStrategyProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-batch.CfnJobDefinition.TimeoutProperty", jsii_struct_bases=[], name_mapping={'attempt_duration_seconds': 'attemptDurationSeconds'})
    class TimeoutProperty():
        def __init__(self, *, attempt_duration_seconds: typing.Optional[jsii.Number]=None) -> None:
            """
            :param attempt_duration_seconds: ``CfnJobDefinition.TimeoutProperty.AttemptDurationSeconds``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-timeout.html
            """
            self._values = {
            }
            if attempt_duration_seconds is not None: self._values["attempt_duration_seconds"] = attempt_duration_seconds

        @builtins.property
        def attempt_duration_seconds(self) -> typing.Optional[jsii.Number]:
            """``CfnJobDefinition.TimeoutProperty.AttemptDurationSeconds``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-timeout.html#cfn-batch-jobdefinition-timeout-attemptdurationseconds
            """
            return self._values.get('attempt_duration_seconds')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'TimeoutProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-batch.CfnJobDefinition.UlimitProperty", jsii_struct_bases=[], name_mapping={'hard_limit': 'hardLimit', 'name': 'name', 'soft_limit': 'softLimit'})
    class UlimitProperty():
        def __init__(self, *, hard_limit: jsii.Number, name: str, soft_limit: jsii.Number) -> None:
            """
            :param hard_limit: ``CfnJobDefinition.UlimitProperty.HardLimit``.
            :param name: ``CfnJobDefinition.UlimitProperty.Name``.
            :param soft_limit: ``CfnJobDefinition.UlimitProperty.SoftLimit``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ulimit.html
            """
            self._values = {
                'hard_limit': hard_limit,
                'name': name,
                'soft_limit': soft_limit,
            }

        @builtins.property
        def hard_limit(self) -> jsii.Number:
            """``CfnJobDefinition.UlimitProperty.HardLimit``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ulimit.html#cfn-batch-jobdefinition-ulimit-hardlimit
            """
            return self._values.get('hard_limit')

        @builtins.property
        def name(self) -> str:
            """``CfnJobDefinition.UlimitProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ulimit.html#cfn-batch-jobdefinition-ulimit-name
            """
            return self._values.get('name')

        @builtins.property
        def soft_limit(self) -> jsii.Number:
            """``CfnJobDefinition.UlimitProperty.SoftLimit``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ulimit.html#cfn-batch-jobdefinition-ulimit-softlimit
            """
            return self._values.get('soft_limit')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'UlimitProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-batch.CfnJobDefinition.VolumesHostProperty", jsii_struct_bases=[], name_mapping={'source_path': 'sourcePath'})
    class VolumesHostProperty():
        def __init__(self, *, source_path: typing.Optional[str]=None) -> None:
            """
            :param source_path: ``CfnJobDefinition.VolumesHostProperty.SourcePath``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-volumeshost.html
            """
            self._values = {
            }
            if source_path is not None: self._values["source_path"] = source_path

        @builtins.property
        def source_path(self) -> typing.Optional[str]:
            """``CfnJobDefinition.VolumesHostProperty.SourcePath``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-volumeshost.html#cfn-batch-jobdefinition-volumeshost-sourcepath
            """
            return self._values.get('source_path')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'VolumesHostProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-batch.CfnJobDefinition.VolumesProperty", jsii_struct_bases=[], name_mapping={'host': 'host', 'name': 'name'})
    class VolumesProperty():
        def __init__(self, *, host: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnJobDefinition.VolumesHostProperty"]]]=None, name: typing.Optional[str]=None) -> None:
            """
            :param host: ``CfnJobDefinition.VolumesProperty.Host``.
            :param name: ``CfnJobDefinition.VolumesProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-volumes.html
            """
            self._values = {
            }
            if host is not None: self._values["host"] = host
            if name is not None: self._values["name"] = name

        @builtins.property
        def host(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnJobDefinition.VolumesHostProperty"]]]:
            """``CfnJobDefinition.VolumesProperty.Host``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-volumes.html#cfn-batch-jobdefinition-volumes-host
            """
            return self._values.get('host')

        @builtins.property
        def name(self) -> typing.Optional[str]:
            """``CfnJobDefinition.VolumesProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-volumes.html#cfn-batch-jobdefinition-volumes-name
            """
            return self._values.get('name')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'VolumesProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-batch.CfnJobDefinitionProps", jsii_struct_bases=[], name_mapping={'type': 'type', 'container_properties': 'containerProperties', 'job_definition_name': 'jobDefinitionName', 'node_properties': 'nodeProperties', 'parameters': 'parameters', 'retry_strategy': 'retryStrategy', 'timeout': 'timeout'})
class CfnJobDefinitionProps():
    def __init__(self, *, type: str, container_properties: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnJobDefinition.ContainerPropertiesProperty"]]]=None, job_definition_name: typing.Optional[str]=None, node_properties: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnJobDefinition.NodePropertiesProperty"]]]=None, parameters: typing.Any=None, retry_strategy: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnJobDefinition.RetryStrategyProperty"]]]=None, timeout: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnJobDefinition.TimeoutProperty"]]]=None) -> None:
        """Properties for defining a ``AWS::Batch::JobDefinition``.

        :param type: ``AWS::Batch::JobDefinition.Type``.
        :param container_properties: ``AWS::Batch::JobDefinition.ContainerProperties``.
        :param job_definition_name: ``AWS::Batch::JobDefinition.JobDefinitionName``.
        :param node_properties: ``AWS::Batch::JobDefinition.NodeProperties``.
        :param parameters: ``AWS::Batch::JobDefinition.Parameters``.
        :param retry_strategy: ``AWS::Batch::JobDefinition.RetryStrategy``.
        :param timeout: ``AWS::Batch::JobDefinition.Timeout``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobdefinition.html
        """
        self._values = {
            'type': type,
        }
        if container_properties is not None: self._values["container_properties"] = container_properties
        if job_definition_name is not None: self._values["job_definition_name"] = job_definition_name
        if node_properties is not None: self._values["node_properties"] = node_properties
        if parameters is not None: self._values["parameters"] = parameters
        if retry_strategy is not None: self._values["retry_strategy"] = retry_strategy
        if timeout is not None: self._values["timeout"] = timeout

    @builtins.property
    def type(self) -> str:
        """``AWS::Batch::JobDefinition.Type``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobdefinition.html#cfn-batch-jobdefinition-type
        """
        return self._values.get('type')

    @builtins.property
    def container_properties(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnJobDefinition.ContainerPropertiesProperty"]]]:
        """``AWS::Batch::JobDefinition.ContainerProperties``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobdefinition.html#cfn-batch-jobdefinition-containerproperties
        """
        return self._values.get('container_properties')

    @builtins.property
    def job_definition_name(self) -> typing.Optional[str]:
        """``AWS::Batch::JobDefinition.JobDefinitionName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobdefinition.html#cfn-batch-jobdefinition-jobdefinitionname
        """
        return self._values.get('job_definition_name')

    @builtins.property
    def node_properties(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnJobDefinition.NodePropertiesProperty"]]]:
        """``AWS::Batch::JobDefinition.NodeProperties``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobdefinition.html#cfn-batch-jobdefinition-nodeproperties
        """
        return self._values.get('node_properties')

    @builtins.property
    def parameters(self) -> typing.Any:
        """``AWS::Batch::JobDefinition.Parameters``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobdefinition.html#cfn-batch-jobdefinition-parameters
        """
        return self._values.get('parameters')

    @builtins.property
    def retry_strategy(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnJobDefinition.RetryStrategyProperty"]]]:
        """``AWS::Batch::JobDefinition.RetryStrategy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobdefinition.html#cfn-batch-jobdefinition-retrystrategy
        """
        return self._values.get('retry_strategy')

    @builtins.property
    def timeout(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnJobDefinition.TimeoutProperty"]]]:
        """``AWS::Batch::JobDefinition.Timeout``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobdefinition.html#cfn-batch-jobdefinition-timeout
        """
        return self._values.get('timeout')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnJobDefinitionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnJobQueue(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-batch.CfnJobQueue"):
    """A CloudFormation ``AWS::Batch::JobQueue``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobqueue.html
    cloudformationResource:
    :cloudformationResource:: AWS::Batch::JobQueue
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, compute_environment_order: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union["ComputeEnvironmentOrderProperty", aws_cdk.core.IResolvable]]], priority: jsii.Number, job_queue_name: typing.Optional[str]=None, state: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::Batch::JobQueue``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param compute_environment_order: ``AWS::Batch::JobQueue.ComputeEnvironmentOrder``.
        :param priority: ``AWS::Batch::JobQueue.Priority``.
        :param job_queue_name: ``AWS::Batch::JobQueue.JobQueueName``.
        :param state: ``AWS::Batch::JobQueue.State``.
        """
        props = CfnJobQueueProps(compute_environment_order=compute_environment_order, priority=priority, job_queue_name=job_queue_name, state=state)

        jsii.create(CfnJobQueue, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: aws_cdk.core.Construct, id: str, resource_attributes: typing.Any, *, finder: aws_cdk.core.ICfnFinder) -> "CfnJobQueue":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -
        :param finder: The finder interface used to resolve references across the template.

        stability
        :stability: experimental
        """
        options = aws_cdk.core.FromCloudFormationOptions(finder=finder)

        return jsii.sinvoke(cls, "fromCloudFormation", [scope, id, resource_attributes, options])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str, typing.Any]) -> typing.Mapping[str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="computeEnvironmentOrder")
    def compute_environment_order(self) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union["ComputeEnvironmentOrderProperty", aws_cdk.core.IResolvable]]]:
        """``AWS::Batch::JobQueue.ComputeEnvironmentOrder``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobqueue.html#cfn-batch-jobqueue-computeenvironmentorder
        """
        return jsii.get(self, "computeEnvironmentOrder")

    @compute_environment_order.setter
    def compute_environment_order(self, value: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union["ComputeEnvironmentOrderProperty", aws_cdk.core.IResolvable]]]):
        jsii.set(self, "computeEnvironmentOrder", value)

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        """``AWS::Batch::JobQueue.Priority``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobqueue.html#cfn-batch-jobqueue-priority
        """
        return jsii.get(self, "priority")

    @priority.setter
    def priority(self, value: jsii.Number):
        jsii.set(self, "priority", value)

    @builtins.property
    @jsii.member(jsii_name="jobQueueName")
    def job_queue_name(self) -> typing.Optional[str]:
        """``AWS::Batch::JobQueue.JobQueueName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobqueue.html#cfn-batch-jobqueue-jobqueuename
        """
        return jsii.get(self, "jobQueueName")

    @job_queue_name.setter
    def job_queue_name(self, value: typing.Optional[str]):
        jsii.set(self, "jobQueueName", value)

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> typing.Optional[str]:
        """``AWS::Batch::JobQueue.State``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobqueue.html#cfn-batch-jobqueue-state
        """
        return jsii.get(self, "state")

    @state.setter
    def state(self, value: typing.Optional[str]):
        jsii.set(self, "state", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-batch.CfnJobQueue.ComputeEnvironmentOrderProperty", jsii_struct_bases=[], name_mapping={'compute_environment': 'computeEnvironment', 'order': 'order'})
    class ComputeEnvironmentOrderProperty():
        def __init__(self, *, compute_environment: str, order: jsii.Number) -> None:
            """
            :param compute_environment: ``CfnJobQueue.ComputeEnvironmentOrderProperty.ComputeEnvironment``.
            :param order: ``CfnJobQueue.ComputeEnvironmentOrderProperty.Order``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobqueue-computeenvironmentorder.html
            """
            self._values = {
                'compute_environment': compute_environment,
                'order': order,
            }

        @builtins.property
        def compute_environment(self) -> str:
            """``CfnJobQueue.ComputeEnvironmentOrderProperty.ComputeEnvironment``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobqueue-computeenvironmentorder.html#cfn-batch-jobqueue-computeenvironmentorder-computeenvironment
            """
            return self._values.get('compute_environment')

        @builtins.property
        def order(self) -> jsii.Number:
            """``CfnJobQueue.ComputeEnvironmentOrderProperty.Order``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobqueue-computeenvironmentorder.html#cfn-batch-jobqueue-computeenvironmentorder-order
            """
            return self._values.get('order')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ComputeEnvironmentOrderProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-batch.CfnJobQueueProps", jsii_struct_bases=[], name_mapping={'compute_environment_order': 'computeEnvironmentOrder', 'priority': 'priority', 'job_queue_name': 'jobQueueName', 'state': 'state'})
class CfnJobQueueProps():
    def __init__(self, *, compute_environment_order: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union["CfnJobQueue.ComputeEnvironmentOrderProperty", aws_cdk.core.IResolvable]]], priority: jsii.Number, job_queue_name: typing.Optional[str]=None, state: typing.Optional[str]=None) -> None:
        """Properties for defining a ``AWS::Batch::JobQueue``.

        :param compute_environment_order: ``AWS::Batch::JobQueue.ComputeEnvironmentOrder``.
        :param priority: ``AWS::Batch::JobQueue.Priority``.
        :param job_queue_name: ``AWS::Batch::JobQueue.JobQueueName``.
        :param state: ``AWS::Batch::JobQueue.State``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobqueue.html
        """
        self._values = {
            'compute_environment_order': compute_environment_order,
            'priority': priority,
        }
        if job_queue_name is not None: self._values["job_queue_name"] = job_queue_name
        if state is not None: self._values["state"] = state

    @builtins.property
    def compute_environment_order(self) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union["CfnJobQueue.ComputeEnvironmentOrderProperty", aws_cdk.core.IResolvable]]]:
        """``AWS::Batch::JobQueue.ComputeEnvironmentOrder``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobqueue.html#cfn-batch-jobqueue-computeenvironmentorder
        """
        return self._values.get('compute_environment_order')

    @builtins.property
    def priority(self) -> jsii.Number:
        """``AWS::Batch::JobQueue.Priority``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobqueue.html#cfn-batch-jobqueue-priority
        """
        return self._values.get('priority')

    @builtins.property
    def job_queue_name(self) -> typing.Optional[str]:
        """``AWS::Batch::JobQueue.JobQueueName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobqueue.html#cfn-batch-jobqueue-jobqueuename
        """
        return self._values.get('job_queue_name')

    @builtins.property
    def state(self) -> typing.Optional[str]:
        """``AWS::Batch::JobQueue.State``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobqueue.html#cfn-batch-jobqueue-state
        """
        return self._values.get('state')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnJobQueueProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-batch.ComputeEnvironmentProps", jsii_struct_bases=[], name_mapping={'compute_environment_name': 'computeEnvironmentName', 'compute_resources': 'computeResources', 'enabled': 'enabled', 'managed': 'managed', 'service_role': 'serviceRole'})
class ComputeEnvironmentProps():
    def __init__(self, *, compute_environment_name: typing.Optional[str]=None, compute_resources: typing.Optional["ComputeResources"]=None, enabled: typing.Optional[bool]=None, managed: typing.Optional[bool]=None, service_role: typing.Optional[aws_cdk.aws_iam.IRole]=None) -> None:
        """Properties for creating a new Compute Environment.

        :param compute_environment_name: A name for the compute environment. Up to 128 letters (uppercase and lowercase), numbers, hyphens, and underscores are allowed. Default: - CloudFormation-generated name
        :param compute_resources: The details of the required compute resources for the managed compute environment. If specified, and this is an unmanaged compute environment, will throw an error. By default, AWS Batch managed compute environments use a recent, approved version of the Amazon ECS-optimized AMI for compute resources. Default: - CloudFormation defaults
        :param enabled: The state of the compute environment. If the state is set to true, then the compute environment accepts jobs from a queue and can scale out automatically based on queues. Default: true
        :param managed: Determines if AWS should manage the allocation of compute resources for processing jobs. If set to false, then you are in charge of providing the compute resource details. Default: true
        :param service_role: The IAM role used by Batch to make calls to other AWS services on your behalf for managing the resources that you use with the service. By default, this role is created for you using the AWS managed service policy for Batch. Default: - Role using the 'service-role/AWSBatchServiceRole' policy.

        stability
        :stability: experimental
        """
        if isinstance(compute_resources, dict): compute_resources = ComputeResources(**compute_resources)
        self._values = {
        }
        if compute_environment_name is not None: self._values["compute_environment_name"] = compute_environment_name
        if compute_resources is not None: self._values["compute_resources"] = compute_resources
        if enabled is not None: self._values["enabled"] = enabled
        if managed is not None: self._values["managed"] = managed
        if service_role is not None: self._values["service_role"] = service_role

    @builtins.property
    def compute_environment_name(self) -> typing.Optional[str]:
        """A name for the compute environment.

        Up to 128 letters (uppercase and lowercase), numbers, hyphens, and underscores are allowed.

        default
        :default: - CloudFormation-generated name

        stability
        :stability: experimental
        """
        return self._values.get('compute_environment_name')

    @builtins.property
    def compute_resources(self) -> typing.Optional["ComputeResources"]:
        """The details of the required compute resources for the managed compute environment.

        If specified, and this is an unmanaged compute environment, will throw an error.

        By default, AWS Batch managed compute environments use a recent, approved version of the
        Amazon ECS-optimized AMI for compute resources.

        default
        :default: - CloudFormation defaults

        stability
        :stability: experimental
        link:
        :link:: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html
        """
        return self._values.get('compute_resources')

    @builtins.property
    def enabled(self) -> typing.Optional[bool]:
        """The state of the compute environment.

        If the state is set to true, then the compute
        environment accepts jobs from a queue and can scale out automatically based on queues.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('enabled')

    @builtins.property
    def managed(self) -> typing.Optional[bool]:
        """Determines if AWS should manage the allocation of compute resources for processing jobs.

        If set to false, then you are in charge of providing the compute resource details.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('managed')

    @builtins.property
    def service_role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """The IAM role used by Batch to make calls to other AWS services on your behalf for managing the resources that you use with the service.

        By default, this role is created for you using
        the AWS managed service policy for Batch.

        default
        :default: - Role using the 'service-role/AWSBatchServiceRole' policy.

        stability
        :stability: experimental
        link:
        :link:: https://docs.aws.amazon.com/batch/latest/userguide/service_IAM_role.html
        """
        return self._values.get('service_role')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ComputeEnvironmentProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-batch.ComputeResourceType")
class ComputeResourceType(enum.Enum):
    """Property to specify if the compute environment uses On-Demand or SpotFleet compute resources.

    stability
    :stability: experimental
    """
    ON_DEMAND = "ON_DEMAND"
    """Resources will be EC2 On-Demand resources.

    stability
    :stability: experimental
    """
    SPOT = "SPOT"
    """Resources will be EC2 SpotFleet resources.

    stability
    :stability: experimental
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-batch.ComputeResources", jsii_struct_bases=[], name_mapping={'vpc': 'vpc', 'allocation_strategy': 'allocationStrategy', 'bid_percentage': 'bidPercentage', 'compute_resources_tags': 'computeResourcesTags', 'desiredv_cpus': 'desiredvCpus', 'ec2_key_pair': 'ec2KeyPair', 'image': 'image', 'instance_role': 'instanceRole', 'instance_types': 'instanceTypes', 'launch_template': 'launchTemplate', 'maxv_cpus': 'maxvCpus', 'minv_cpus': 'minvCpus', 'security_groups': 'securityGroups', 'spot_fleet_role': 'spotFleetRole', 'type': 'type', 'vpc_subnets': 'vpcSubnets'})
class ComputeResources():
    def __init__(self, *, vpc: aws_cdk.aws_ec2.IVpc, allocation_strategy: typing.Optional["AllocationStrategy"]=None, bid_percentage: typing.Optional[jsii.Number]=None, compute_resources_tags: typing.Optional[aws_cdk.core.Tag]=None, desiredv_cpus: typing.Optional[jsii.Number]=None, ec2_key_pair: typing.Optional[str]=None, image: typing.Optional[aws_cdk.aws_ec2.IMachineImage]=None, instance_role: typing.Optional[str]=None, instance_types: typing.Optional[typing.List[aws_cdk.aws_ec2.InstanceType]]=None, launch_template: typing.Optional["LaunchTemplateSpecification"]=None, maxv_cpus: typing.Optional[jsii.Number]=None, minv_cpus: typing.Optional[jsii.Number]=None, security_groups: typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]]=None, spot_fleet_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, type: typing.Optional["ComputeResourceType"]=None, vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection]=None) -> None:
        """Properties for defining the structure of the batch compute cluster.

        :param vpc: The VPC network that all compute resources will be connected to.
        :param allocation_strategy: The allocation strategy to use for the compute resource in case not enough instances of the best fitting instance type can be allocated. This could be due to availability of the instance type in the region or Amazon EC2 service limits. If this is not specified, the default for the EC2 ComputeResourceType is BEST_FIT, which will use only the best fitting instance type, waiting for additional capacity if it's not available. This allocation strategy keeps costs lower but can limit scaling. If you are using Spot Fleets with BEST_FIT then the Spot Fleet IAM Role must be specified. BEST_FIT_PROGRESSIVE will select an additional instance type that is large enough to meet the requirements of the jobs in the queue, with a preference for an instance type with a lower cost. The default value for the SPOT instance type is SPOT_CAPACITY_OPTIMIZED, which is only available for for this type of compute resources and will select an additional instance type that is large enough to meet the requirements of the jobs in the queue, with a preference for an instance type that is less likely to be interrupted. Default: AllocationStrategy.BEST_FIT
        :param bid_percentage: This property will be ignored if you set the environment type to ON_DEMAND. The maximum percentage that a Spot Instance price can be when compared with the On-Demand price for that instance type before instances are launched. For example, if your maximum percentage is 20%, then the Spot price must be below 20% of the current On-Demand price for that EC2 instance. You always pay the lowest (market) price and never more than your maximum percentage. If you leave this field empty, the default value is 100% of the On-Demand price. Default: 100
        :param compute_resources_tags: Key-value pair tags to be applied to resources that are launched in the compute environment. For AWS Batch, these take the form of "String1": "String2", where String1 is the tag key and String2 is the tag value—for example, { "Name": "AWS Batch Instance - C4OnDemand" }. Default: - no tags will be assigned on compute resources.
        :param desiredv_cpus: The desired number of EC2 vCPUS in the compute environment. Default: - no desired vcpu value will be used.
        :param ec2_key_pair: The EC2 key pair that is used for instances launched in the compute environment. If no key is defined, then SSH access is not allowed to provisioned compute resources. Default: - no SSH access will be possible.
        :param image: The Amazon Machine Image (AMI) ID used for instances launched in the compute environment. Default: - no image will be used.
        :param instance_role: The Amazon ECS instance profile applied to Amazon EC2 instances in a compute environment. You can specify the short name or full Amazon Resource Name (ARN) of an instance profile. For example, ecsInstanceRole or arn:aws:iam::<aws_account_id>:instance-profile/ecsInstanceRole . For more information, see Amazon ECS Instance Role in the AWS Batch User Guide. Default: - a new role will be created.
        :param instance_types: The types of EC2 instances that may be launched in the compute environment. You can specify instance families to launch any instance type within those families (for example, c4 or p3), or you can specify specific sizes within a family (such as c4.8xlarge). You can also choose optimal to pick instance types (from the C, M, and R instance families) on the fly that match the demand of your job queues. Default: optimal
        :param launch_template: An optional launch template to associate with your compute resources. For more information, see README file. Default: - no custom launch template will be used
        :param maxv_cpus: The maximum number of EC2 vCPUs that an environment can reach. Each vCPU is equivalent to 1,024 CPU shares. You must specify at least one vCPU. Default: 256
        :param minv_cpus: The minimum number of EC2 vCPUs that an environment should maintain (even if the compute environment state is DISABLED). Each vCPU is equivalent to 1,024 CPU shares. By keeping this set to 0 you will not have instance time wasted when there is no work to be run. If you set this above zero you will maintain that number of vCPUs at all times. Default: 0
        :param security_groups: The EC2 security group(s) associated with instances launched in the compute environment. Default: - AWS default security group.
        :param spot_fleet_role: This property will be ignored if you set the environment type to ON_DEMAND. The Amazon Resource Name (ARN) of the Amazon EC2 Spot Fleet IAM role applied to a SPOT compute environment. For more information, see Amazon EC2 Spot Fleet Role in the AWS Batch User Guide. Default: - no fleet role will be used.
        :param type: The type of compute environment: ON_DEMAND or SPOT. Default: ON_DEMAND
        :param vpc_subnets: The VPC subnets into which the compute resources are launched. Default: - private subnets of the supplied VPC.

        stability
        :stability: experimental
        """
        if isinstance(launch_template, dict): launch_template = LaunchTemplateSpecification(**launch_template)
        if isinstance(vpc_subnets, dict): vpc_subnets = aws_cdk.aws_ec2.SubnetSelection(**vpc_subnets)
        self._values = {
            'vpc': vpc,
        }
        if allocation_strategy is not None: self._values["allocation_strategy"] = allocation_strategy
        if bid_percentage is not None: self._values["bid_percentage"] = bid_percentage
        if compute_resources_tags is not None: self._values["compute_resources_tags"] = compute_resources_tags
        if desiredv_cpus is not None: self._values["desiredv_cpus"] = desiredv_cpus
        if ec2_key_pair is not None: self._values["ec2_key_pair"] = ec2_key_pair
        if image is not None: self._values["image"] = image
        if instance_role is not None: self._values["instance_role"] = instance_role
        if instance_types is not None: self._values["instance_types"] = instance_types
        if launch_template is not None: self._values["launch_template"] = launch_template
        if maxv_cpus is not None: self._values["maxv_cpus"] = maxv_cpus
        if minv_cpus is not None: self._values["minv_cpus"] = minv_cpus
        if security_groups is not None: self._values["security_groups"] = security_groups
        if spot_fleet_role is not None: self._values["spot_fleet_role"] = spot_fleet_role
        if type is not None: self._values["type"] = type
        if vpc_subnets is not None: self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        """The VPC network that all compute resources will be connected to.

        stability
        :stability: experimental
        """
        return self._values.get('vpc')

    @builtins.property
    def allocation_strategy(self) -> typing.Optional["AllocationStrategy"]:
        """The allocation strategy to use for the compute resource in case not enough instances of the best fitting instance type can be allocated.

        This could be due to availability of the instance type in
        the region or Amazon EC2 service limits. If this is not specified, the default for the EC2
        ComputeResourceType is BEST_FIT, which will use only the best fitting instance type, waiting for
        additional capacity if it's not available. This allocation strategy keeps costs lower but can limit
        scaling. If you are using Spot Fleets with BEST_FIT then the Spot Fleet IAM Role must be specified.
        BEST_FIT_PROGRESSIVE will select an additional instance type that is large enough to meet the
        requirements of the jobs in the queue, with a preference for an instance type with a lower cost.
        The default value for the SPOT instance type is SPOT_CAPACITY_OPTIMIZED, which is only available for
        for this type of compute resources and will select an additional instance type that is large enough
        to meet the requirements of the jobs in the queue, with a preference for an instance type that is
        less likely to be interrupted.

        default
        :default: AllocationStrategy.BEST_FIT

        stability
        :stability: experimental
        """
        return self._values.get('allocation_strategy')

    @builtins.property
    def bid_percentage(self) -> typing.Optional[jsii.Number]:
        """This property will be ignored if you set the environment type to ON_DEMAND.

        The maximum percentage that a Spot Instance price can be when compared with the On-Demand price for
        that instance type before instances are launched. For example, if your maximum percentage is 20%,
        then the Spot price must be below 20% of the current On-Demand price for that EC2 instance. You always
        pay the lowest (market) price and never more than your maximum percentage. If you leave this field empty,
        the default value is 100% of the On-Demand price.

        default
        :default: 100

        stability
        :stability: experimental
        """
        return self._values.get('bid_percentage')

    @builtins.property
    def compute_resources_tags(self) -> typing.Optional[aws_cdk.core.Tag]:
        """Key-value pair tags to be applied to resources that are launched in the compute environment.

        For AWS Batch, these take the form of "String1": "String2", where String1 is the tag key and
        String2 is the tag value—for example, { "Name": "AWS Batch Instance - C4OnDemand" }.

        default
        :default: - no tags will be assigned on compute resources.

        stability
        :stability: experimental
        """
        return self._values.get('compute_resources_tags')

    @builtins.property
    def desiredv_cpus(self) -> typing.Optional[jsii.Number]:
        """The desired number of EC2 vCPUS in the compute environment.

        default
        :default: - no desired vcpu value will be used.

        stability
        :stability: experimental
        """
        return self._values.get('desiredv_cpus')

    @builtins.property
    def ec2_key_pair(self) -> typing.Optional[str]:
        """The EC2 key pair that is used for instances launched in the compute environment.

        If no key is defined, then SSH access is not allowed to provisioned compute resources.

        default
        :default: - no SSH access will be possible.

        stability
        :stability: experimental
        """
        return self._values.get('ec2_key_pair')

    @builtins.property
    def image(self) -> typing.Optional[aws_cdk.aws_ec2.IMachineImage]:
        """The Amazon Machine Image (AMI) ID used for instances launched in the compute environment.

        default
        :default: - no image will be used.

        stability
        :stability: experimental
        """
        return self._values.get('image')

    @builtins.property
    def instance_role(self) -> typing.Optional[str]:
        """The Amazon ECS instance profile applied to Amazon EC2 instances in a compute environment.

        You can specify
        the short name or full Amazon Resource Name (ARN) of an instance profile. For example, ecsInstanceRole or
        arn:aws:iam::<aws_account_id>:instance-profile/ecsInstanceRole . For more information, see Amazon ECS
        Instance Role in the AWS Batch User Guide.

        default
        :default: - a new role will be created.

        stability
        :stability: experimental
        link:
        :link:: https://docs.aws.amazon.com/batch/latest/userguide/instance_IAM_role.html
        """
        return self._values.get('instance_role')

    @builtins.property
    def instance_types(self) -> typing.Optional[typing.List[aws_cdk.aws_ec2.InstanceType]]:
        """The types of EC2 instances that may be launched in the compute environment.

        You can specify instance
        families to launch any instance type within those families (for example, c4 or p3), or you can specify
        specific sizes within a family (such as c4.8xlarge). You can also choose optimal to pick instance types
        (from the C, M, and R instance families) on the fly that match the demand of your job queues.

        default
        :default: optimal

        stability
        :stability: experimental
        """
        return self._values.get('instance_types')

    @builtins.property
    def launch_template(self) -> typing.Optional["LaunchTemplateSpecification"]:
        """An optional launch template to associate with your compute resources.

        For more information, see README file.

        default
        :default: - no custom launch template will be used

        stability
        :stability: experimental
        link:
        :link:: https://docs.aws.amazon.com/batch/latest/userguide/launch-templates.html
        """
        return self._values.get('launch_template')

    @builtins.property
    def maxv_cpus(self) -> typing.Optional[jsii.Number]:
        """The maximum number of EC2 vCPUs that an environment can reach.

        Each vCPU is equivalent to
        1,024 CPU shares. You must specify at least one vCPU.

        default
        :default: 256

        stability
        :stability: experimental
        """
        return self._values.get('maxv_cpus')

    @builtins.property
    def minv_cpus(self) -> typing.Optional[jsii.Number]:
        """The minimum number of EC2 vCPUs that an environment should maintain (even if the compute environment state is DISABLED).

        Each vCPU is equivalent to 1,024 CPU shares. By keeping this set to 0 you will not have instance time wasted when
        there is no work to be run. If you set this above zero you will maintain that number of vCPUs at all times.

        default
        :default: 0

        stability
        :stability: experimental
        """
        return self._values.get('minv_cpus')

    @builtins.property
    def security_groups(self) -> typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]]:
        """The EC2 security group(s) associated with instances launched in the compute environment.

        default
        :default: - AWS default security group.

        stability
        :stability: experimental
        """
        return self._values.get('security_groups')

    @builtins.property
    def spot_fleet_role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """This property will be ignored if you set the environment type to ON_DEMAND.

        The Amazon Resource Name (ARN) of the Amazon EC2 Spot Fleet IAM role applied to a SPOT compute environment.
        For more information, see Amazon EC2 Spot Fleet Role in the AWS Batch User Guide.

        default
        :default: - no fleet role will be used.

        stability
        :stability: experimental
        link:
        :link:: https://docs.aws.amazon.com/batch/latest/userguide/spot_fleet_IAM_role.html
        """
        return self._values.get('spot_fleet_role')

    @builtins.property
    def type(self) -> typing.Optional["ComputeResourceType"]:
        """The type of compute environment: ON_DEMAND or SPOT.

        default
        :default: ON_DEMAND

        stability
        :stability: experimental
        """
        return self._values.get('type')

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        """The VPC subnets into which the compute resources are launched.

        default
        :default: - private subnets of the supplied VPC.

        stability
        :stability: experimental
        """
        return self._values.get('vpc_subnets')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ComputeResources(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.interface(jsii_type="@aws-cdk/aws-batch.IComputeEnvironment")
class IComputeEnvironment(aws_cdk.core.IResource, jsii.compat.Protocol):
    """Properties of a compute environment.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IComputeEnvironmentProxy

    @builtins.property
    @jsii.member(jsii_name="computeEnvironmentArn")
    def compute_environment_arn(self) -> str:
        """The ARN of this compute environment.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="computeEnvironmentName")
    def compute_environment_name(self) -> str:
        """The name of this compute environment.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...


class _IComputeEnvironmentProxy(jsii.proxy_for(aws_cdk.core.IResource)):
    """Properties of a compute environment.

    stability
    :stability: experimental
    """
    __jsii_type__ = "@aws-cdk/aws-batch.IComputeEnvironment"
    @builtins.property
    @jsii.member(jsii_name="computeEnvironmentArn")
    def compute_environment_arn(self) -> str:
        """The ARN of this compute environment.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "computeEnvironmentArn")

    @builtins.property
    @jsii.member(jsii_name="computeEnvironmentName")
    def compute_environment_name(self) -> str:
        """The name of this compute environment.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "computeEnvironmentName")


@jsii.interface(jsii_type="@aws-cdk/aws-batch.IJobDefinition")
class IJobDefinition(aws_cdk.core.IResource, jsii.compat.Protocol):
    """An interface representing a job definition - either a new one, created with the CDK, *using the {@link JobDefinition} class, or existing ones, referenced using the {@link JobDefinition.fromJobDefinitionArn} method.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IJobDefinitionProxy

    @builtins.property
    @jsii.member(jsii_name="jobDefinitionArn")
    def job_definition_arn(self) -> str:
        """The ARN of this batch job definition.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="jobDefinitionName")
    def job_definition_name(self) -> str:
        """The name of the batch job definition.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...


class _IJobDefinitionProxy(jsii.proxy_for(aws_cdk.core.IResource)):
    """An interface representing a job definition - either a new one, created with the CDK, *using the {@link JobDefinition} class, or existing ones, referenced using the {@link JobDefinition.fromJobDefinitionArn} method.

    stability
    :stability: experimental
    """
    __jsii_type__ = "@aws-cdk/aws-batch.IJobDefinition"
    @builtins.property
    @jsii.member(jsii_name="jobDefinitionArn")
    def job_definition_arn(self) -> str:
        """The ARN of this batch job definition.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "jobDefinitionArn")

    @builtins.property
    @jsii.member(jsii_name="jobDefinitionName")
    def job_definition_name(self) -> str:
        """The name of the batch job definition.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "jobDefinitionName")


@jsii.interface(jsii_type="@aws-cdk/aws-batch.IJobQueue")
class IJobQueue(aws_cdk.core.IResource, jsii.compat.Protocol):
    """Properties of a Job Queue.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IJobQueueProxy

    @builtins.property
    @jsii.member(jsii_name="jobQueueArn")
    def job_queue_arn(self) -> str:
        """The ARN of this batch job queue.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="jobQueueName")
    def job_queue_name(self) -> str:
        """A name for the job queue.

        Up to 128 letters (uppercase and lowercase), numbers, hyphens, and underscores are allowed.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...


class _IJobQueueProxy(jsii.proxy_for(aws_cdk.core.IResource)):
    """Properties of a Job Queue.

    stability
    :stability: experimental
    """
    __jsii_type__ = "@aws-cdk/aws-batch.IJobQueue"
    @builtins.property
    @jsii.member(jsii_name="jobQueueArn")
    def job_queue_arn(self) -> str:
        """The ARN of this batch job queue.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "jobQueueArn")

    @builtins.property
    @jsii.member(jsii_name="jobQueueName")
    def job_queue_name(self) -> str:
        """A name for the job queue.

        Up to 128 letters (uppercase and lowercase), numbers, hyphens, and underscores are allowed.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "jobQueueName")


@jsii.interface(jsii_type="@aws-cdk/aws-batch.IMultiNodeProps")
class IMultiNodeProps(jsii.compat.Protocol):
    """Properties for specifying multi-node properties for compute resources.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IMultiNodePropsProxy

    @builtins.property
    @jsii.member(jsii_name="count")
    def count(self) -> jsii.Number:
        """The number of nodes associated with a multi-node parallel job.

        stability
        :stability: experimental
        """
        ...

    @count.setter
    def count(self, value: jsii.Number):
        ...

    @builtins.property
    @jsii.member(jsii_name="mainNode")
    def main_node(self) -> jsii.Number:
        """Specifies the node index for the main node of a multi-node parallel job.

        This node index value must be fewer than the number of nodes.

        stability
        :stability: experimental
        """
        ...

    @main_node.setter
    def main_node(self, value: jsii.Number):
        ...

    @builtins.property
    @jsii.member(jsii_name="rangeProps")
    def range_props(self) -> typing.List["INodeRangeProps"]:
        """A list of node ranges and their properties associated with a multi-node parallel job.

        stability
        :stability: experimental
        """
        ...

    @range_props.setter
    def range_props(self, value: typing.List["INodeRangeProps"]):
        ...


class _IMultiNodePropsProxy():
    """Properties for specifying multi-node properties for compute resources.

    stability
    :stability: experimental
    """
    __jsii_type__ = "@aws-cdk/aws-batch.IMultiNodeProps"
    @builtins.property
    @jsii.member(jsii_name="count")
    def count(self) -> jsii.Number:
        """The number of nodes associated with a multi-node parallel job.

        stability
        :stability: experimental
        """
        return jsii.get(self, "count")

    @count.setter
    def count(self, value: jsii.Number):
        jsii.set(self, "count", value)

    @builtins.property
    @jsii.member(jsii_name="mainNode")
    def main_node(self) -> jsii.Number:
        """Specifies the node index for the main node of a multi-node parallel job.

        This node index value must be fewer than the number of nodes.

        stability
        :stability: experimental
        """
        return jsii.get(self, "mainNode")

    @main_node.setter
    def main_node(self, value: jsii.Number):
        jsii.set(self, "mainNode", value)

    @builtins.property
    @jsii.member(jsii_name="rangeProps")
    def range_props(self) -> typing.List["INodeRangeProps"]:
        """A list of node ranges and their properties associated with a multi-node parallel job.

        stability
        :stability: experimental
        """
        return jsii.get(self, "rangeProps")

    @range_props.setter
    def range_props(self, value: typing.List["INodeRangeProps"]):
        jsii.set(self, "rangeProps", value)


@jsii.interface(jsii_type="@aws-cdk/aws-batch.INodeRangeProps")
class INodeRangeProps(jsii.compat.Protocol):
    """Properties for a multi-node batch job.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _INodeRangePropsProxy

    @builtins.property
    @jsii.member(jsii_name="container")
    def container(self) -> "JobDefinitionContainer":
        """The container details for the node range.

        stability
        :stability: experimental
        """
        ...

    @container.setter
    def container(self, value: "JobDefinitionContainer"):
        ...

    @builtins.property
    @jsii.member(jsii_name="fromNodeIndex")
    def from_node_index(self) -> typing.Optional[jsii.Number]:
        """The minimum node index value to apply this container definition against.

        You may nest node ranges, for example 0:10 and 4:5, in which case the 4:5 range properties override the 0:10 properties.

        default
        :default: 0

        stability
        :stability: experimental
        """
        ...

    @from_node_index.setter
    def from_node_index(self, value: typing.Optional[jsii.Number]):
        ...

    @builtins.property
    @jsii.member(jsii_name="toNodeIndex")
    def to_node_index(self) -> typing.Optional[jsii.Number]:
        """The maximum node index value to apply this container definition against. If omitted, the highest value is used relative.

        to the number of nodes associated with the job. You may nest node ranges, for example 0:10 and 4:5,
        in which case the 4:5 range properties override the 0:10 properties.

        default
        :default: {@link IMultiNodeprops.count}

        stability
        :stability: experimental
        """
        ...

    @to_node_index.setter
    def to_node_index(self, value: typing.Optional[jsii.Number]):
        ...


class _INodeRangePropsProxy():
    """Properties for a multi-node batch job.

    stability
    :stability: experimental
    """
    __jsii_type__ = "@aws-cdk/aws-batch.INodeRangeProps"
    @builtins.property
    @jsii.member(jsii_name="container")
    def container(self) -> "JobDefinitionContainer":
        """The container details for the node range.

        stability
        :stability: experimental
        """
        return jsii.get(self, "container")

    @container.setter
    def container(self, value: "JobDefinitionContainer"):
        jsii.set(self, "container", value)

    @builtins.property
    @jsii.member(jsii_name="fromNodeIndex")
    def from_node_index(self) -> typing.Optional[jsii.Number]:
        """The minimum node index value to apply this container definition against.

        You may nest node ranges, for example 0:10 and 4:5, in which case the 4:5 range properties override the 0:10 properties.

        default
        :default: 0

        stability
        :stability: experimental
        """
        return jsii.get(self, "fromNodeIndex")

    @from_node_index.setter
    def from_node_index(self, value: typing.Optional[jsii.Number]):
        jsii.set(self, "fromNodeIndex", value)

    @builtins.property
    @jsii.member(jsii_name="toNodeIndex")
    def to_node_index(self) -> typing.Optional[jsii.Number]:
        """The maximum node index value to apply this container definition against. If omitted, the highest value is used relative.

        to the number of nodes associated with the job. You may nest node ranges, for example 0:10 and 4:5,
        in which case the 4:5 range properties override the 0:10 properties.

        default
        :default: {@link IMultiNodeprops.count}

        stability
        :stability: experimental
        """
        return jsii.get(self, "toNodeIndex")

    @to_node_index.setter
    def to_node_index(self, value: typing.Optional[jsii.Number]):
        jsii.set(self, "toNodeIndex", value)


@jsii.implements(IJobDefinition)
class JobDefinition(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-batch.JobDefinition"):
    """Batch Job Definition.

    Defines a batch job definition to execute a specific batch job.

    stability
    :stability: experimental
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, container: "JobDefinitionContainer", job_definition_name: typing.Optional[str]=None, node_props: typing.Optional["IMultiNodeProps"]=None, parameters: typing.Optional[typing.Mapping[str, str]]=None, retry_attempts: typing.Optional[jsii.Number]=None, timeout: typing.Optional[aws_cdk.core.Duration]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param container: An object with various properties specific to container-based jobs.
        :param job_definition_name: The name of the job definition. Up to 128 letters (uppercase and lowercase), numbers, hyphens, and underscores are allowed. Default: Cloudformation-generated name
        :param node_props: An object with various properties specific to multi-node parallel jobs. Default: - undefined
        :param parameters: When you submit a job, you can specify parameters that should replace the placeholders or override the default job definition parameters. Parameters in job submission requests take precedence over the defaults in a job definition. This allows you to use the same job definition for multiple jobs that use the same format, and programmatically change values in the command at submission time. Default: - undefined
        :param retry_attempts: The number of times to move a job to the RUNNABLE status. You may specify between 1 and 10 attempts. If the value of attempts is greater than one, the job is retried on failure the same number of attempts as the value. Default: 1
        :param timeout: The timeout configuration for jobs that are submitted with this job definition. You can specify a timeout duration after which AWS Batch terminates your jobs if they have not finished. Default: - undefined

        stability
        :stability: experimental
        """
        props = JobDefinitionProps(container=container, job_definition_name=job_definition_name, node_props=node_props, parameters=parameters, retry_attempts=retry_attempts, timeout=timeout)

        jsii.create(JobDefinition, self, [scope, id, props])

    @jsii.member(jsii_name="fromJobDefinitionArn")
    @builtins.classmethod
    def from_job_definition_arn(cls, scope: aws_cdk.core.Construct, id: str, job_definition_arn: str) -> "IJobDefinition":
        """Imports an existing batch job definition by its amazon resource name.

        :param scope: -
        :param id: -
        :param job_definition_arn: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromJobDefinitionArn", [scope, id, job_definition_arn])

    @builtins.property
    @jsii.member(jsii_name="jobDefinitionArn")
    def job_definition_arn(self) -> str:
        """The ARN of this batch job definition.

        stability
        :stability: experimental
        """
        return jsii.get(self, "jobDefinitionArn")

    @builtins.property
    @jsii.member(jsii_name="jobDefinitionName")
    def job_definition_name(self) -> str:
        """The name of the batch job definition.

        stability
        :stability: experimental
        """
        return jsii.get(self, "jobDefinitionName")


@jsii.data_type(jsii_type="@aws-cdk/aws-batch.JobDefinitionContainer", jsii_struct_bases=[], name_mapping={'image': 'image', 'command': 'command', 'environment': 'environment', 'gpu_count': 'gpuCount', 'instance_type': 'instanceType', 'job_role': 'jobRole', 'linux_params': 'linuxParams', 'memory_limit_mib': 'memoryLimitMiB', 'mount_points': 'mountPoints', 'privileged': 'privileged', 'read_only': 'readOnly', 'ulimits': 'ulimits', 'user': 'user', 'vcpus': 'vcpus', 'volumes': 'volumes'})
class JobDefinitionContainer():
    def __init__(self, *, image: aws_cdk.aws_ecs.ContainerImage, command: typing.Optional[typing.List[str]]=None, environment: typing.Optional[typing.Mapping[str, str]]=None, gpu_count: typing.Optional[jsii.Number]=None, instance_type: typing.Optional[aws_cdk.aws_ec2.InstanceType]=None, job_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, linux_params: typing.Optional[aws_cdk.aws_ecs.LinuxParameters]=None, memory_limit_mib: typing.Optional[jsii.Number]=None, mount_points: typing.Optional[typing.List[aws_cdk.aws_ecs.MountPoint]]=None, privileged: typing.Optional[bool]=None, read_only: typing.Optional[bool]=None, ulimits: typing.Optional[typing.List[aws_cdk.aws_ecs.Ulimit]]=None, user: typing.Optional[str]=None, vcpus: typing.Optional[jsii.Number]=None, volumes: typing.Optional[typing.List[aws_cdk.aws_ecs.Volume]]=None) -> None:
        """Properties of a job definition container.

        :param image: The image used to start a container.
        :param command: The command that is passed to the container. If you provide a shell command as a single string, you have to quote command-line arguments. Default: - CMD value built into container image.
        :param environment: The environment variables to pass to the container. Default: none
        :param gpu_count: The number of physical GPUs to reserve for the container. The number of GPUs reserved for all containers in a job should not exceed the number of available GPUs on the compute resource that the job is launched on. Default: - No GPU reservation.
        :param instance_type: The instance type to use for a multi-node parallel job. Currently all node groups in a multi-node parallel job must use the same instance type. This parameter is not valid for single-node container jobs. Default: - None
        :param job_role: The IAM role that the container can assume for AWS permissions. Default: - An IAM role will created.
        :param linux_params: Linux-specific modifications that are applied to the container, such as details for device mappings. For now, only the ``devices`` property is supported. Default: - None will be used.
        :param memory_limit_mib: The hard limit (in MiB) of memory to present to the container. If your container attempts to exceed the memory specified here, the container is killed. You must specify at least 4 MiB of memory for a job. Default: 4
        :param mount_points: The mount points for data volumes in your container. Default: - No mount points will be used.
        :param privileged: When this parameter is true, the container is given elevated privileges on the host container instance (similar to the root user). Default: false
        :param read_only: When this parameter is true, the container is given read-only access to its root file system. Default: false
        :param ulimits: A list of ulimits to set in the container. Default: - No limits.
        :param user: The user name to use inside the container. Default: - None will be used.
        :param vcpus: The number of vCPUs reserved for the container. Each vCPU is equivalent to 1,024 CPU shares. You must specify at least one vCPU. Default: 1
        :param volumes: A list of data volumes used in a job. Default: - No data volumes will be used.

        stability
        :stability: experimental
        """
        self._values = {
            'image': image,
        }
        if command is not None: self._values["command"] = command
        if environment is not None: self._values["environment"] = environment
        if gpu_count is not None: self._values["gpu_count"] = gpu_count
        if instance_type is not None: self._values["instance_type"] = instance_type
        if job_role is not None: self._values["job_role"] = job_role
        if linux_params is not None: self._values["linux_params"] = linux_params
        if memory_limit_mib is not None: self._values["memory_limit_mib"] = memory_limit_mib
        if mount_points is not None: self._values["mount_points"] = mount_points
        if privileged is not None: self._values["privileged"] = privileged
        if read_only is not None: self._values["read_only"] = read_only
        if ulimits is not None: self._values["ulimits"] = ulimits
        if user is not None: self._values["user"] = user
        if vcpus is not None: self._values["vcpus"] = vcpus
        if volumes is not None: self._values["volumes"] = volumes

    @builtins.property
    def image(self) -> aws_cdk.aws_ecs.ContainerImage:
        """The image used to start a container.

        stability
        :stability: experimental
        """
        return self._values.get('image')

    @builtins.property
    def command(self) -> typing.Optional[typing.List[str]]:
        """The command that is passed to the container.

        If you provide a shell command as a single string, you have to quote command-line arguments.

        default
        :default: - CMD value built into container image.

        stability
        :stability: experimental
        """
        return self._values.get('command')

    @builtins.property
    def environment(self) -> typing.Optional[typing.Mapping[str, str]]:
        """The environment variables to pass to the container.

        default
        :default: none

        stability
        :stability: experimental
        """
        return self._values.get('environment')

    @builtins.property
    def gpu_count(self) -> typing.Optional[jsii.Number]:
        """The number of physical GPUs to reserve for the container.

        The number of GPUs reserved for all
        containers in a job should not exceed the number of available GPUs on the compute resource that the job is launched on.

        default
        :default: - No GPU reservation.

        stability
        :stability: experimental
        """
        return self._values.get('gpu_count')

    @builtins.property
    def instance_type(self) -> typing.Optional[aws_cdk.aws_ec2.InstanceType]:
        """The instance type to use for a multi-node parallel job.

        Currently all node groups in a
        multi-node parallel job must use the same instance type. This parameter is not valid
        for single-node container jobs.

        default
        :default: - None

        stability
        :stability: experimental
        """
        return self._values.get('instance_type')

    @builtins.property
    def job_role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """The IAM role that the container can assume for AWS permissions.

        default
        :default: - An IAM role will created.

        stability
        :stability: experimental
        """
        return self._values.get('job_role')

    @builtins.property
    def linux_params(self) -> typing.Optional[aws_cdk.aws_ecs.LinuxParameters]:
        """Linux-specific modifications that are applied to the container, such as details for device mappings.

        For now, only the ``devices`` property is supported.

        default
        :default: - None will be used.

        stability
        :stability: experimental
        """
        return self._values.get('linux_params')

    @builtins.property
    def memory_limit_mib(self) -> typing.Optional[jsii.Number]:
        """The hard limit (in MiB) of memory to present to the container.

        If your container attempts to exceed
        the memory specified here, the container is killed. You must specify at least 4 MiB of memory for a job.

        default
        :default: 4

        stability
        :stability: experimental
        """
        return self._values.get('memory_limit_mib')

    @builtins.property
    def mount_points(self) -> typing.Optional[typing.List[aws_cdk.aws_ecs.MountPoint]]:
        """The mount points for data volumes in your container.

        default
        :default: - No mount points will be used.

        stability
        :stability: experimental
        """
        return self._values.get('mount_points')

    @builtins.property
    def privileged(self) -> typing.Optional[bool]:
        """When this parameter is true, the container is given elevated privileges on the host container instance (similar to the root user).

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('privileged')

    @builtins.property
    def read_only(self) -> typing.Optional[bool]:
        """When this parameter is true, the container is given read-only access to its root file system.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('read_only')

    @builtins.property
    def ulimits(self) -> typing.Optional[typing.List[aws_cdk.aws_ecs.Ulimit]]:
        """A list of ulimits to set in the container.

        default
        :default: - No limits.

        stability
        :stability: experimental
        """
        return self._values.get('ulimits')

    @builtins.property
    def user(self) -> typing.Optional[str]:
        """The user name to use inside the container.

        default
        :default: - None will be used.

        stability
        :stability: experimental
        """
        return self._values.get('user')

    @builtins.property
    def vcpus(self) -> typing.Optional[jsii.Number]:
        """The number of vCPUs reserved for the container.

        Each vCPU is equivalent to
        1,024 CPU shares. You must specify at least one vCPU.

        default
        :default: 1

        stability
        :stability: experimental
        """
        return self._values.get('vcpus')

    @builtins.property
    def volumes(self) -> typing.Optional[typing.List[aws_cdk.aws_ecs.Volume]]:
        """A list of data volumes used in a job.

        default
        :default: - No data volumes will be used.

        stability
        :stability: experimental
        """
        return self._values.get('volumes')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'JobDefinitionContainer(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-batch.JobDefinitionProps", jsii_struct_bases=[], name_mapping={'container': 'container', 'job_definition_name': 'jobDefinitionName', 'node_props': 'nodeProps', 'parameters': 'parameters', 'retry_attempts': 'retryAttempts', 'timeout': 'timeout'})
class JobDefinitionProps():
    def __init__(self, *, container: "JobDefinitionContainer", job_definition_name: typing.Optional[str]=None, node_props: typing.Optional["IMultiNodeProps"]=None, parameters: typing.Optional[typing.Mapping[str, str]]=None, retry_attempts: typing.Optional[jsii.Number]=None, timeout: typing.Optional[aws_cdk.core.Duration]=None) -> None:
        """Construction properties of the {@link JobDefinition} construct.

        :param container: An object with various properties specific to container-based jobs.
        :param job_definition_name: The name of the job definition. Up to 128 letters (uppercase and lowercase), numbers, hyphens, and underscores are allowed. Default: Cloudformation-generated name
        :param node_props: An object with various properties specific to multi-node parallel jobs. Default: - undefined
        :param parameters: When you submit a job, you can specify parameters that should replace the placeholders or override the default job definition parameters. Parameters in job submission requests take precedence over the defaults in a job definition. This allows you to use the same job definition for multiple jobs that use the same format, and programmatically change values in the command at submission time. Default: - undefined
        :param retry_attempts: The number of times to move a job to the RUNNABLE status. You may specify between 1 and 10 attempts. If the value of attempts is greater than one, the job is retried on failure the same number of attempts as the value. Default: 1
        :param timeout: The timeout configuration for jobs that are submitted with this job definition. You can specify a timeout duration after which AWS Batch terminates your jobs if they have not finished. Default: - undefined

        stability
        :stability: experimental
        """
        if isinstance(container, dict): container = JobDefinitionContainer(**container)
        self._values = {
            'container': container,
        }
        if job_definition_name is not None: self._values["job_definition_name"] = job_definition_name
        if node_props is not None: self._values["node_props"] = node_props
        if parameters is not None: self._values["parameters"] = parameters
        if retry_attempts is not None: self._values["retry_attempts"] = retry_attempts
        if timeout is not None: self._values["timeout"] = timeout

    @builtins.property
    def container(self) -> "JobDefinitionContainer":
        """An object with various properties specific to container-based jobs.

        stability
        :stability: experimental
        """
        return self._values.get('container')

    @builtins.property
    def job_definition_name(self) -> typing.Optional[str]:
        """The name of the job definition.

        Up to 128 letters (uppercase and lowercase), numbers, hyphens, and underscores are allowed.

        default
        :default: Cloudformation-generated name

        stability
        :stability: experimental
        """
        return self._values.get('job_definition_name')

    @builtins.property
    def node_props(self) -> typing.Optional["IMultiNodeProps"]:
        """An object with various properties specific to multi-node parallel jobs.

        default
        :default: - undefined

        stability
        :stability: experimental
        """
        return self._values.get('node_props')

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[str, str]]:
        """When you submit a job, you can specify parameters that should replace the placeholders or override the default job definition parameters.

        Parameters
        in job submission requests take precedence over the defaults in a job definition.
        This allows you to use the same job definition for multiple jobs that use the same
        format, and programmatically change values in the command at submission time.

        default
        :default: - undefined

        stability
        :stability: experimental
        link:
        :link:: https://docs.aws.amazon.com/batch/latest/userguide/job_definition_parameters.html
        """
        return self._values.get('parameters')

    @builtins.property
    def retry_attempts(self) -> typing.Optional[jsii.Number]:
        """The number of times to move a job to the RUNNABLE status.

        You may specify between 1 and
        10 attempts. If the value of attempts is greater than one, the job is retried on failure
        the same number of attempts as the value.

        default
        :default: 1

        stability
        :stability: experimental
        """
        return self._values.get('retry_attempts')

    @builtins.property
    def timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The timeout configuration for jobs that are submitted with this job definition.

        You can specify
        a timeout duration after which AWS Batch terminates your jobs if they have not finished.

        default
        :default: - undefined

        stability
        :stability: experimental
        """
        return self._values.get('timeout')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'JobDefinitionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(IJobQueue)
class JobQueue(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-batch.JobQueue"):
    """Batch Job Queue.

    Defines a batch job queue to define how submitted batch jobs
    should be ran based on specified batch compute environments.

    stability
    :stability: experimental
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, compute_environments: typing.List["JobQueueComputeEnvironment"], enabled: typing.Optional[bool]=None, job_queue_name: typing.Optional[str]=None, priority: typing.Optional[jsii.Number]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param compute_environments: The set of compute environments mapped to a job queue and their order relative to each other. The job scheduler uses this parameter to determine which compute environment should execute a given job. Compute environments must be in the VALID state before you can associate them with a job queue. You can associate up to three compute environments with a job queue.
        :param enabled: The state of the job queue. If set to true, it is able to accept jobs. Default: true
        :param job_queue_name: A name for the job queue. Up to 128 letters (uppercase and lowercase), numbers, hyphens, and underscores are allowed. Default: - Cloudformation-generated name
        :param priority: The priority of the job queue. Job queues with a higher priority (or a higher integer value for the priority parameter) are evaluated first when associated with the same compute environment. Priority is determined in descending order, for example, a job queue with a priority value of 10 is given scheduling preference over a job queue with a priority value of 1. Default: 1

        stability
        :stability: experimental
        """
        props = JobQueueProps(compute_environments=compute_environments, enabled=enabled, job_queue_name=job_queue_name, priority=priority)

        jsii.create(JobQueue, self, [scope, id, props])

    @jsii.member(jsii_name="fromJobQueueArn")
    @builtins.classmethod
    def from_job_queue_arn(cls, scope: aws_cdk.core.Construct, id: str, job_queue_arn: str) -> "IJobQueue":
        """Fetches an existing batch job queue by its amazon resource name.

        :param scope: -
        :param id: -
        :param job_queue_arn: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromJobQueueArn", [scope, id, job_queue_arn])

    @builtins.property
    @jsii.member(jsii_name="jobQueueArn")
    def job_queue_arn(self) -> str:
        """The ARN of this batch job queue.

        stability
        :stability: experimental
        """
        return jsii.get(self, "jobQueueArn")

    @builtins.property
    @jsii.member(jsii_name="jobQueueName")
    def job_queue_name(self) -> str:
        """A name for the job queue.

        Up to 128 letters (uppercase and lowercase), numbers, hyphens, and underscores are allowed.

        stability
        :stability: experimental
        """
        return jsii.get(self, "jobQueueName")


@jsii.data_type(jsii_type="@aws-cdk/aws-batch.JobQueueComputeEnvironment", jsii_struct_bases=[], name_mapping={'compute_environment': 'computeEnvironment', 'order': 'order'})
class JobQueueComputeEnvironment():
    def __init__(self, *, compute_environment: "IComputeEnvironment", order: jsii.Number) -> None:
        """Properties for mapping a compute environment to a job queue.

        :param compute_environment: The batch compute environment to use for processing submitted jobs to this queue.
        :param order: The order in which this compute environment will be selected for dynamic allocation of resources to process submitted jobs.

        stability
        :stability: experimental
        """
        self._values = {
            'compute_environment': compute_environment,
            'order': order,
        }

    @builtins.property
    def compute_environment(self) -> "IComputeEnvironment":
        """The batch compute environment to use for processing submitted jobs to this queue.

        stability
        :stability: experimental
        """
        return self._values.get('compute_environment')

    @builtins.property
    def order(self) -> jsii.Number:
        """The order in which this compute environment will be selected for dynamic allocation of resources to process submitted jobs.

        stability
        :stability: experimental
        """
        return self._values.get('order')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'JobQueueComputeEnvironment(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-batch.JobQueueProps", jsii_struct_bases=[], name_mapping={'compute_environments': 'computeEnvironments', 'enabled': 'enabled', 'job_queue_name': 'jobQueueName', 'priority': 'priority'})
class JobQueueProps():
    def __init__(self, *, compute_environments: typing.List["JobQueueComputeEnvironment"], enabled: typing.Optional[bool]=None, job_queue_name: typing.Optional[str]=None, priority: typing.Optional[jsii.Number]=None) -> None:
        """Properties of a batch job queue.

        :param compute_environments: The set of compute environments mapped to a job queue and their order relative to each other. The job scheduler uses this parameter to determine which compute environment should execute a given job. Compute environments must be in the VALID state before you can associate them with a job queue. You can associate up to three compute environments with a job queue.
        :param enabled: The state of the job queue. If set to true, it is able to accept jobs. Default: true
        :param job_queue_name: A name for the job queue. Up to 128 letters (uppercase and lowercase), numbers, hyphens, and underscores are allowed. Default: - Cloudformation-generated name
        :param priority: The priority of the job queue. Job queues with a higher priority (or a higher integer value for the priority parameter) are evaluated first when associated with the same compute environment. Priority is determined in descending order, for example, a job queue with a priority value of 10 is given scheduling preference over a job queue with a priority value of 1. Default: 1

        stability
        :stability: experimental
        """
        self._values = {
            'compute_environments': compute_environments,
        }
        if enabled is not None: self._values["enabled"] = enabled
        if job_queue_name is not None: self._values["job_queue_name"] = job_queue_name
        if priority is not None: self._values["priority"] = priority

    @builtins.property
    def compute_environments(self) -> typing.List["JobQueueComputeEnvironment"]:
        """The set of compute environments mapped to a job queue and their order relative to each other.

        The job scheduler uses this parameter to
        determine which compute environment should execute a given job. Compute environments must be in the VALID state before you can associate them
        with a job queue. You can associate up to three compute environments with a job queue.

        stability
        :stability: experimental
        """
        return self._values.get('compute_environments')

    @builtins.property
    def enabled(self) -> typing.Optional[bool]:
        """The state of the job queue.

        If set to true, it is able to accept jobs.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('enabled')

    @builtins.property
    def job_queue_name(self) -> typing.Optional[str]:
        """A name for the job queue.

        Up to 128 letters (uppercase and lowercase), numbers, hyphens, and underscores are allowed.

        default
        :default: - Cloudformation-generated name

        stability
        :stability: experimental
        """
        return self._values.get('job_queue_name')

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        """The priority of the job queue.

        Job queues with a higher priority (or a higher integer value for the priority parameter) are evaluated first
        when associated with the same compute environment. Priority is determined in descending order, for example, a job queue with a priority value
        of 10 is given scheduling preference over a job queue with a priority value of 1.

        default
        :default: 1

        stability
        :stability: experimental
        """
        return self._values.get('priority')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'JobQueueProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-batch.LaunchTemplateSpecification", jsii_struct_bases=[], name_mapping={'launch_template_name': 'launchTemplateName', 'version': 'version'})
class LaunchTemplateSpecification():
    def __init__(self, *, launch_template_name: str, version: typing.Optional[str]=None) -> None:
        """Launch template property specification.

        :param launch_template_name: The Launch template name.
        :param version: The launch template version to be used (optional). Default: - the default version of the launch template

        stability
        :stability: experimental
        """
        self._values = {
            'launch_template_name': launch_template_name,
        }
        if version is not None: self._values["version"] = version

    @builtins.property
    def launch_template_name(self) -> str:
        """The Launch template name.

        stability
        :stability: experimental
        """
        return self._values.get('launch_template_name')

    @builtins.property
    def version(self) -> typing.Optional[str]:
        """The launch template version to be used (optional).

        default
        :default: - the default version of the launch template

        stability
        :stability: experimental
        """
        return self._values.get('version')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'LaunchTemplateSpecification(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(IComputeEnvironment)
class ComputeEnvironment(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-batch.ComputeEnvironment"):
    """Batch Compute Environment.

    Defines a batch compute environment to run batch jobs on.

    stability
    :stability: experimental
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, compute_environment_name: typing.Optional[str]=None, compute_resources: typing.Optional["ComputeResources"]=None, enabled: typing.Optional[bool]=None, managed: typing.Optional[bool]=None, service_role: typing.Optional[aws_cdk.aws_iam.IRole]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param compute_environment_name: A name for the compute environment. Up to 128 letters (uppercase and lowercase), numbers, hyphens, and underscores are allowed. Default: - CloudFormation-generated name
        :param compute_resources: The details of the required compute resources for the managed compute environment. If specified, and this is an unmanaged compute environment, will throw an error. By default, AWS Batch managed compute environments use a recent, approved version of the Amazon ECS-optimized AMI for compute resources. Default: - CloudFormation defaults
        :param enabled: The state of the compute environment. If the state is set to true, then the compute environment accepts jobs from a queue and can scale out automatically based on queues. Default: true
        :param managed: Determines if AWS should manage the allocation of compute resources for processing jobs. If set to false, then you are in charge of providing the compute resource details. Default: true
        :param service_role: The IAM role used by Batch to make calls to other AWS services on your behalf for managing the resources that you use with the service. By default, this role is created for you using the AWS managed service policy for Batch. Default: - Role using the 'service-role/AWSBatchServiceRole' policy.

        stability
        :stability: experimental
        """
        props = ComputeEnvironmentProps(compute_environment_name=compute_environment_name, compute_resources=compute_resources, enabled=enabled, managed=managed, service_role=service_role)

        jsii.create(ComputeEnvironment, self, [scope, id, props])

    @jsii.member(jsii_name="fromComputeEnvironmentArn")
    @builtins.classmethod
    def from_compute_environment_arn(cls, scope: aws_cdk.core.Construct, id: str, compute_environment_arn: str) -> "IComputeEnvironment":
        """Fetches an existing batch compute environment by its amazon resource name.

        :param scope: -
        :param id: -
        :param compute_environment_arn: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromComputeEnvironmentArn", [scope, id, compute_environment_arn])

    @builtins.property
    @jsii.member(jsii_name="computeEnvironmentArn")
    def compute_environment_arn(self) -> str:
        """The ARN of this compute environment.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "computeEnvironmentArn")

    @builtins.property
    @jsii.member(jsii_name="computeEnvironmentName")
    def compute_environment_name(self) -> str:
        """The name of this compute environment.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "computeEnvironmentName")


__all__ = [
    "AllocationStrategy",
    "CfnComputeEnvironment",
    "CfnComputeEnvironmentProps",
    "CfnJobDefinition",
    "CfnJobDefinitionProps",
    "CfnJobQueue",
    "CfnJobQueueProps",
    "ComputeEnvironment",
    "ComputeEnvironmentProps",
    "ComputeResourceType",
    "ComputeResources",
    "IComputeEnvironment",
    "IJobDefinition",
    "IJobQueue",
    "IMultiNodeProps",
    "INodeRangeProps",
    "JobDefinition",
    "JobDefinitionContainer",
    "JobDefinitionProps",
    "JobQueue",
    "JobQueueComputeEnvironment",
    "JobQueueProps",
    "LaunchTemplateSpecification",
]

publication.publish()
