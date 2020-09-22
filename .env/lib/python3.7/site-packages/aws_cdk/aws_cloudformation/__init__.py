"""
## AWS CloudFormation Construct Library

<!--BEGIN STABILITY BANNER-->---


![Deprecated](https://img.shields.io/badge/deprecated-critical.svg?style=for-the-badge)

> This API may emit warnings. Backward compatibility is not guaranteed.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

import aws_cdk.aws_iam
import aws_cdk.aws_lambda
import aws_cdk.aws_s3
import aws_cdk.aws_sns
import aws_cdk.core
import aws_cdk.cx_api
import constructs

from ._jsii import *


@jsii.implements(aws_cdk.core.IInspectable)
class CfnCustomResource(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cloudformation.CfnCustomResource"):
    """A CloudFormation ``AWS::CloudFormation::CustomResource``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cfn-customresource.html
    cloudformationResource:
    :cloudformationResource:: AWS::CloudFormation::CustomResource
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, service_token: str) -> None:
        """Create a new ``AWS::CloudFormation::CustomResource``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param service_token: ``AWS::CloudFormation::CustomResource.ServiceToken``.
        """
        props = CfnCustomResourceProps(service_token=service_token)

        jsii.create(CfnCustomResource, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: aws_cdk.core.Construct, id: str, resource_attributes: typing.Any, *, finder: aws_cdk.core.ICfnFinder) -> "CfnCustomResource":
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
    @jsii.member(jsii_name="serviceToken")
    def service_token(self) -> str:
        """``AWS::CloudFormation::CustomResource.ServiceToken``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cfn-customresource.html#cfn-customresource-servicetoken
        """
        return jsii.get(self, "serviceToken")

    @service_token.setter
    def service_token(self, value: str):
        jsii.set(self, "serviceToken", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-cloudformation.CfnCustomResourceProps", jsii_struct_bases=[], name_mapping={'service_token': 'serviceToken'})
class CfnCustomResourceProps():
    def __init__(self, *, service_token: str) -> None:
        """Properties for defining a ``AWS::CloudFormation::CustomResource``.

        :param service_token: ``AWS::CloudFormation::CustomResource.ServiceToken``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cfn-customresource.html
        """
        self._values = {
            'service_token': service_token,
        }

    @builtins.property
    def service_token(self) -> str:
        """``AWS::CloudFormation::CustomResource.ServiceToken``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cfn-customresource.html#cfn-customresource-servicetoken
        """
        return self._values.get('service_token')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnCustomResourceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnMacro(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cloudformation.CfnMacro"):
    """A CloudFormation ``AWS::CloudFormation::Macro``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-macro.html
    cloudformationResource:
    :cloudformationResource:: AWS::CloudFormation::Macro
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, function_name: str, name: str, description: typing.Optional[str]=None, log_group_name: typing.Optional[str]=None, log_role_arn: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::CloudFormation::Macro``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param function_name: ``AWS::CloudFormation::Macro.FunctionName``.
        :param name: ``AWS::CloudFormation::Macro.Name``.
        :param description: ``AWS::CloudFormation::Macro.Description``.
        :param log_group_name: ``AWS::CloudFormation::Macro.LogGroupName``.
        :param log_role_arn: ``AWS::CloudFormation::Macro.LogRoleARN``.
        """
        props = CfnMacroProps(function_name=function_name, name=name, description=description, log_group_name=log_group_name, log_role_arn=log_role_arn)

        jsii.create(CfnMacro, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: aws_cdk.core.Construct, id: str, resource_attributes: typing.Any, *, finder: aws_cdk.core.ICfnFinder) -> "CfnMacro":
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
    @jsii.member(jsii_name="functionName")
    def function_name(self) -> str:
        """``AWS::CloudFormation::Macro.FunctionName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-macro.html#cfn-cloudformation-macro-functionname
        """
        return jsii.get(self, "functionName")

    @function_name.setter
    def function_name(self, value: str):
        jsii.set(self, "functionName", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        """``AWS::CloudFormation::Macro.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-macro.html#cfn-cloudformation-macro-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: str):
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::CloudFormation::Macro.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-macro.html#cfn-cloudformation-macro-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]):
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="logGroupName")
    def log_group_name(self) -> typing.Optional[str]:
        """``AWS::CloudFormation::Macro.LogGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-macro.html#cfn-cloudformation-macro-loggroupname
        """
        return jsii.get(self, "logGroupName")

    @log_group_name.setter
    def log_group_name(self, value: typing.Optional[str]):
        jsii.set(self, "logGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="logRoleArn")
    def log_role_arn(self) -> typing.Optional[str]:
        """``AWS::CloudFormation::Macro.LogRoleARN``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-macro.html#cfn-cloudformation-macro-logrolearn
        """
        return jsii.get(self, "logRoleArn")

    @log_role_arn.setter
    def log_role_arn(self, value: typing.Optional[str]):
        jsii.set(self, "logRoleArn", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-cloudformation.CfnMacroProps", jsii_struct_bases=[], name_mapping={'function_name': 'functionName', 'name': 'name', 'description': 'description', 'log_group_name': 'logGroupName', 'log_role_arn': 'logRoleArn'})
class CfnMacroProps():
    def __init__(self, *, function_name: str, name: str, description: typing.Optional[str]=None, log_group_name: typing.Optional[str]=None, log_role_arn: typing.Optional[str]=None) -> None:
        """Properties for defining a ``AWS::CloudFormation::Macro``.

        :param function_name: ``AWS::CloudFormation::Macro.FunctionName``.
        :param name: ``AWS::CloudFormation::Macro.Name``.
        :param description: ``AWS::CloudFormation::Macro.Description``.
        :param log_group_name: ``AWS::CloudFormation::Macro.LogGroupName``.
        :param log_role_arn: ``AWS::CloudFormation::Macro.LogRoleARN``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-macro.html
        """
        self._values = {
            'function_name': function_name,
            'name': name,
        }
        if description is not None: self._values["description"] = description
        if log_group_name is not None: self._values["log_group_name"] = log_group_name
        if log_role_arn is not None: self._values["log_role_arn"] = log_role_arn

    @builtins.property
    def function_name(self) -> str:
        """``AWS::CloudFormation::Macro.FunctionName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-macro.html#cfn-cloudformation-macro-functionname
        """
        return self._values.get('function_name')

    @builtins.property
    def name(self) -> str:
        """``AWS::CloudFormation::Macro.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-macro.html#cfn-cloudformation-macro-name
        """
        return self._values.get('name')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """``AWS::CloudFormation::Macro.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-macro.html#cfn-cloudformation-macro-description
        """
        return self._values.get('description')

    @builtins.property
    def log_group_name(self) -> typing.Optional[str]:
        """``AWS::CloudFormation::Macro.LogGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-macro.html#cfn-cloudformation-macro-loggroupname
        """
        return self._values.get('log_group_name')

    @builtins.property
    def log_role_arn(self) -> typing.Optional[str]:
        """``AWS::CloudFormation::Macro.LogRoleARN``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-macro.html#cfn-cloudformation-macro-logrolearn
        """
        return self._values.get('log_role_arn')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnMacroProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnStack(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cloudformation.CfnStack"):
    """A CloudFormation ``AWS::CloudFormation::Stack``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stack.html
    cloudformationResource:
    :cloudformationResource:: AWS::CloudFormation::Stack
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, template_url: str, notification_arns: typing.Optional[typing.List[str]]=None, parameters: typing.Optional[typing.Union[typing.Optional[typing.Mapping[str, str]], typing.Optional[aws_cdk.core.IResolvable]]]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None, timeout_in_minutes: typing.Optional[jsii.Number]=None) -> None:
        """Create a new ``AWS::CloudFormation::Stack``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param template_url: ``AWS::CloudFormation::Stack.TemplateURL``.
        :param notification_arns: ``AWS::CloudFormation::Stack.NotificationARNs``.
        :param parameters: ``AWS::CloudFormation::Stack.Parameters``.
        :param tags: ``AWS::CloudFormation::Stack.Tags``.
        :param timeout_in_minutes: ``AWS::CloudFormation::Stack.TimeoutInMinutes``.
        """
        props = CfnStackProps(template_url=template_url, notification_arns=notification_arns, parameters=parameters, tags=tags, timeout_in_minutes=timeout_in_minutes)

        jsii.create(CfnStack, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: aws_cdk.core.Construct, id: str, resource_attributes: typing.Any, *, finder: aws_cdk.core.ICfnFinder) -> "CfnStack":
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
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::CloudFormation::Stack.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stack.html#cfn-cloudformation-stack-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="templateUrl")
    def template_url(self) -> str:
        """``AWS::CloudFormation::Stack.TemplateURL``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stack.html#cfn-cloudformation-stack-templateurl
        """
        return jsii.get(self, "templateUrl")

    @template_url.setter
    def template_url(self, value: str):
        jsii.set(self, "templateUrl", value)

    @builtins.property
    @jsii.member(jsii_name="notificationArns")
    def notification_arns(self) -> typing.Optional[typing.List[str]]:
        """``AWS::CloudFormation::Stack.NotificationARNs``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stack.html#cfn-cloudformation-stack-notificationarns
        """
        return jsii.get(self, "notificationArns")

    @notification_arns.setter
    def notification_arns(self, value: typing.Optional[typing.List[str]]):
        jsii.set(self, "notificationArns", value)

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str, str]]]]:
        """``AWS::CloudFormation::Stack.Parameters``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stack.html#cfn-cloudformation-stack-parameters
        """
        return jsii.get(self, "parameters")

    @parameters.setter
    def parameters(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str, str]]]]):
        jsii.set(self, "parameters", value)

    @builtins.property
    @jsii.member(jsii_name="timeoutInMinutes")
    def timeout_in_minutes(self) -> typing.Optional[jsii.Number]:
        """``AWS::CloudFormation::Stack.TimeoutInMinutes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stack.html#cfn-cloudformation-stack-timeoutinminutes
        """
        return jsii.get(self, "timeoutInMinutes")

    @timeout_in_minutes.setter
    def timeout_in_minutes(self, value: typing.Optional[jsii.Number]):
        jsii.set(self, "timeoutInMinutes", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-cloudformation.CfnStackProps", jsii_struct_bases=[], name_mapping={'template_url': 'templateUrl', 'notification_arns': 'notificationArns', 'parameters': 'parameters', 'tags': 'tags', 'timeout_in_minutes': 'timeoutInMinutes'})
class CfnStackProps():
    def __init__(self, *, template_url: str, notification_arns: typing.Optional[typing.List[str]]=None, parameters: typing.Optional[typing.Union[typing.Optional[typing.Mapping[str, str]], typing.Optional[aws_cdk.core.IResolvable]]]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None, timeout_in_minutes: typing.Optional[jsii.Number]=None) -> None:
        """Properties for defining a ``AWS::CloudFormation::Stack``.

        :param template_url: ``AWS::CloudFormation::Stack.TemplateURL``.
        :param notification_arns: ``AWS::CloudFormation::Stack.NotificationARNs``.
        :param parameters: ``AWS::CloudFormation::Stack.Parameters``.
        :param tags: ``AWS::CloudFormation::Stack.Tags``.
        :param timeout_in_minutes: ``AWS::CloudFormation::Stack.TimeoutInMinutes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stack.html
        """
        self._values = {
            'template_url': template_url,
        }
        if notification_arns is not None: self._values["notification_arns"] = notification_arns
        if parameters is not None: self._values["parameters"] = parameters
        if tags is not None: self._values["tags"] = tags
        if timeout_in_minutes is not None: self._values["timeout_in_minutes"] = timeout_in_minutes

    @builtins.property
    def template_url(self) -> str:
        """``AWS::CloudFormation::Stack.TemplateURL``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stack.html#cfn-cloudformation-stack-templateurl
        """
        return self._values.get('template_url')

    @builtins.property
    def notification_arns(self) -> typing.Optional[typing.List[str]]:
        """``AWS::CloudFormation::Stack.NotificationARNs``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stack.html#cfn-cloudformation-stack-notificationarns
        """
        return self._values.get('notification_arns')

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Union[typing.Optional[typing.Mapping[str, str]], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::CloudFormation::Stack.Parameters``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stack.html#cfn-cloudformation-stack-parameters
        """
        return self._values.get('parameters')

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::CloudFormation::Stack.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stack.html#cfn-cloudformation-stack-tags
        """
        return self._values.get('tags')

    @builtins.property
    def timeout_in_minutes(self) -> typing.Optional[jsii.Number]:
        """``AWS::CloudFormation::Stack.TimeoutInMinutes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stack.html#cfn-cloudformation-stack-timeoutinminutes
        """
        return self._values.get('timeout_in_minutes')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnStackProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnWaitCondition(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cloudformation.CfnWaitCondition"):
    """A CloudFormation ``AWS::CloudFormation::WaitCondition``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waitcondition.html
    cloudformationResource:
    :cloudformationResource:: AWS::CloudFormation::WaitCondition
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, count: typing.Optional[jsii.Number]=None, handle: typing.Optional[str]=None, timeout: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::CloudFormation::WaitCondition``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param count: ``AWS::CloudFormation::WaitCondition.Count``.
        :param handle: ``AWS::CloudFormation::WaitCondition.Handle``.
        :param timeout: ``AWS::CloudFormation::WaitCondition.Timeout``.
        """
        props = CfnWaitConditionProps(count=count, handle=handle, timeout=timeout)

        jsii.create(CfnWaitCondition, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: aws_cdk.core.Construct, id: str, resource_attributes: typing.Any, *, finder: aws_cdk.core.ICfnFinder) -> "CfnWaitCondition":
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
    @jsii.member(jsii_name="attrData")
    def attr_data(self) -> aws_cdk.core.IResolvable:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: Data
        """
        return jsii.get(self, "attrData")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="count")
    def count(self) -> typing.Optional[jsii.Number]:
        """``AWS::CloudFormation::WaitCondition.Count``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waitcondition.html#cfn-waitcondition-count
        """
        return jsii.get(self, "count")

    @count.setter
    def count(self, value: typing.Optional[jsii.Number]):
        jsii.set(self, "count", value)

    @builtins.property
    @jsii.member(jsii_name="handle")
    def handle(self) -> typing.Optional[str]:
        """``AWS::CloudFormation::WaitCondition.Handle``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waitcondition.html#cfn-waitcondition-handle
        """
        return jsii.get(self, "handle")

    @handle.setter
    def handle(self, value: typing.Optional[str]):
        jsii.set(self, "handle", value)

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> typing.Optional[str]:
        """``AWS::CloudFormation::WaitCondition.Timeout``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waitcondition.html#cfn-waitcondition-timeout
        """
        return jsii.get(self, "timeout")

    @timeout.setter
    def timeout(self, value: typing.Optional[str]):
        jsii.set(self, "timeout", value)


@jsii.implements(aws_cdk.core.IInspectable)
class CfnWaitConditionHandle(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cloudformation.CfnWaitConditionHandle"):
    """A CloudFormation ``AWS::CloudFormation::WaitConditionHandle``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waitconditionhandle.html
    cloudformationResource:
    :cloudformationResource:: AWS::CloudFormation::WaitConditionHandle
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str) -> None:
        """Create a new ``AWS::CloudFormation::WaitConditionHandle``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        """
        jsii.create(CfnWaitConditionHandle, self, [scope, id])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: aws_cdk.core.Construct, id: str, resource_attributes: typing.Any, *, finder: aws_cdk.core.ICfnFinder) -> "CfnWaitConditionHandle":
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

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")


@jsii.data_type(jsii_type="@aws-cdk/aws-cloudformation.CfnWaitConditionProps", jsii_struct_bases=[], name_mapping={'count': 'count', 'handle': 'handle', 'timeout': 'timeout'})
class CfnWaitConditionProps():
    def __init__(self, *, count: typing.Optional[jsii.Number]=None, handle: typing.Optional[str]=None, timeout: typing.Optional[str]=None) -> None:
        """Properties for defining a ``AWS::CloudFormation::WaitCondition``.

        :param count: ``AWS::CloudFormation::WaitCondition.Count``.
        :param handle: ``AWS::CloudFormation::WaitCondition.Handle``.
        :param timeout: ``AWS::CloudFormation::WaitCondition.Timeout``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waitcondition.html
        """
        self._values = {
        }
        if count is not None: self._values["count"] = count
        if handle is not None: self._values["handle"] = handle
        if timeout is not None: self._values["timeout"] = timeout

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        """``AWS::CloudFormation::WaitCondition.Count``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waitcondition.html#cfn-waitcondition-count
        """
        return self._values.get('count')

    @builtins.property
    def handle(self) -> typing.Optional[str]:
        """``AWS::CloudFormation::WaitCondition.Handle``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waitcondition.html#cfn-waitcondition-handle
        """
        return self._values.get('handle')

    @builtins.property
    def timeout(self) -> typing.Optional[str]:
        """``AWS::CloudFormation::WaitCondition.Timeout``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waitcondition.html#cfn-waitcondition-timeout
        """
        return self._values.get('timeout')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnWaitConditionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-cloudformation.CloudFormationCapabilities")
class CloudFormationCapabilities(enum.Enum):
    """Capabilities that affect whether CloudFormation is allowed to change IAM resources.

    deprecated
    :deprecated: use ``core.CfnCapabilities``

    stability
    :stability: deprecated
    """
    NONE = "NONE"
    """No IAM Capabilities.

    Pass this capability if you wish to block the creation IAM resources.

    stability
    :stability: deprecated
    link:
    :link:: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-iam-template.html#using-iam-capabilities
    """
    ANONYMOUS_IAM = "ANONYMOUS_IAM"
    """Capability to create anonymous IAM resources.

    Pass this capability if you're only creating anonymous resources.

    stability
    :stability: deprecated
    link:
    :link:: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-iam-template.html#using-iam-capabilities
    """
    NAMED_IAM = "NAMED_IAM"
    """Capability to create named IAM resources.

    Pass this capability if you're creating IAM resources that have physical
    names.

    ``CloudFormationCapabilities.NamedIAM`` implies ``CloudFormationCapabilities.IAM``; you don't have to pass both.

    stability
    :stability: deprecated
    link:
    :link:: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-iam-template.html#using-iam-capabilities
    """
    AUTO_EXPAND = "AUTO_EXPAND"
    """Capability to run CloudFormation macros.

    Pass this capability if your template includes macros, for example AWS::Include or AWS::Serverless.

    stability
    :stability: deprecated
    link:
    :link:: https://docs.aws.amazon.com/AWSCloudFormation/latest/APIReference/API_CreateStack.html
    """

class CustomResource(aws_cdk.core.CustomResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cloudformation.CustomResource"):
    """Deprecated.

    deprecated
    :deprecated: use ``core.CustomResource``

    stability
    :stability: deprecated
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, provider: "ICustomResourceProvider", properties: typing.Optional[typing.Mapping[str, typing.Any]]=None, removal_policy: typing.Optional[aws_cdk.core.RemovalPolicy]=None, resource_type: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param provider: The provider which implements the custom resource. You can implement a provider by listening to raw AWS CloudFormation events through an SNS topic or an AWS Lambda function or use the CDK's custom `resource provider framework <https://docs.aws.amazon.com/cdk/api/latest/docs/custom-resources-readme.html>`_ which makes it easier to implement robust providers:: // use the provider framework from aws-cdk/custom-resources: provider: new custom_resources.Provider({ onEventHandler: myOnEventLambda, isCompleteHandler: myIsCompleteLambda, // optional }); Example:: // invoke an AWS Lambda function when a lifecycle event occurs: provider: CustomResourceProvider.fromLambda(myFunction) Example:: // publish lifecycle events to an SNS topic: provider: CustomResourceProvider.fromTopic(myTopic)
        :param properties: Properties to pass to the Lambda. Default: - No properties.
        :param removal_policy: The policy to apply when this resource is removed from the application. Default: cdk.RemovalPolicy.Destroy
        :param resource_type: For custom resources, you can specify AWS::CloudFormation::CustomResource (the default) as the resource type, or you can specify your own resource type name. For example, you can use "Custom::MyCustomResourceTypeName". Custom resource type names must begin with "Custom::" and can include alphanumeric characters and the following characters: _@-. You can specify a custom resource type name up to a maximum length of 60 characters. You cannot change the type during an update. Using your own resource type names helps you quickly differentiate the types of custom resources in your stack. For example, if you had two custom resources that conduct two different ping tests, you could name their type as Custom::PingTester to make them easily identifiable as ping testers (instead of using AWS::CloudFormation::CustomResource). Default: - AWS::CloudFormation::CustomResource

        stability
        :stability: deprecated
        """
        props = CustomResourceProps(provider=provider, properties=properties, removal_policy=removal_policy, resource_type=resource_type)

        jsii.create(CustomResource, self, [scope, id, props])


@jsii.data_type(jsii_type="@aws-cdk/aws-cloudformation.CustomResourceProps", jsii_struct_bases=[], name_mapping={'provider': 'provider', 'properties': 'properties', 'removal_policy': 'removalPolicy', 'resource_type': 'resourceType'})
class CustomResourceProps():
    def __init__(self, *, provider: "ICustomResourceProvider", properties: typing.Optional[typing.Mapping[str, typing.Any]]=None, removal_policy: typing.Optional[aws_cdk.core.RemovalPolicy]=None, resource_type: typing.Optional[str]=None) -> None:
        """Properties to provide a Lambda-backed custom resource.

        :param provider: The provider which implements the custom resource. You can implement a provider by listening to raw AWS CloudFormation events through an SNS topic or an AWS Lambda function or use the CDK's custom `resource provider framework <https://docs.aws.amazon.com/cdk/api/latest/docs/custom-resources-readme.html>`_ which makes it easier to implement robust providers:: // use the provider framework from aws-cdk/custom-resources: provider: new custom_resources.Provider({ onEventHandler: myOnEventLambda, isCompleteHandler: myIsCompleteLambda, // optional }); Example:: // invoke an AWS Lambda function when a lifecycle event occurs: provider: CustomResourceProvider.fromLambda(myFunction) Example:: // publish lifecycle events to an SNS topic: provider: CustomResourceProvider.fromTopic(myTopic)
        :param properties: Properties to pass to the Lambda. Default: - No properties.
        :param removal_policy: The policy to apply when this resource is removed from the application. Default: cdk.RemovalPolicy.Destroy
        :param resource_type: For custom resources, you can specify AWS::CloudFormation::CustomResource (the default) as the resource type, or you can specify your own resource type name. For example, you can use "Custom::MyCustomResourceTypeName". Custom resource type names must begin with "Custom::" and can include alphanumeric characters and the following characters: _@-. You can specify a custom resource type name up to a maximum length of 60 characters. You cannot change the type during an update. Using your own resource type names helps you quickly differentiate the types of custom resources in your stack. For example, if you had two custom resources that conduct two different ping tests, you could name their type as Custom::PingTester to make them easily identifiable as ping testers (instead of using AWS::CloudFormation::CustomResource). Default: - AWS::CloudFormation::CustomResource

        deprecated
        :deprecated: use ``core.CustomResourceProps``

        stability
        :stability: deprecated
        """
        self._values = {
            'provider': provider,
        }
        if properties is not None: self._values["properties"] = properties
        if removal_policy is not None: self._values["removal_policy"] = removal_policy
        if resource_type is not None: self._values["resource_type"] = resource_type

    @builtins.property
    def provider(self) -> "ICustomResourceProvider":
        """The provider which implements the custom resource.

        You can implement a provider by listening to raw AWS CloudFormation events
        through an SNS topic or an AWS Lambda function or use the CDK's custom
        `resource provider framework <https://docs.aws.amazon.com/cdk/api/latest/docs/custom-resources-readme.html>`_ which makes it easier to implement robust
        providers::

           # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
           provider: new custom_resources.Provider({
              onEventHandler: myOnEventLambda,
              isCompleteHandler: myIsCompleteLambda, // optional
           });

        Example::

           # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
           provider: CustomResourceProvider.fromLambda(myFunction)

        Example::

           # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
           provider: CustomResourceProvider.fromTopic(myTopic)

        stability
        :stability: deprecated
        """
        return self._values.get('provider')

    @builtins.property
    def properties(self) -> typing.Optional[typing.Mapping[str, typing.Any]]:
        """Properties to pass to the Lambda.

        default
        :default: - No properties.

        stability
        :stability: deprecated
        """
        return self._values.get('properties')

    @builtins.property
    def removal_policy(self) -> typing.Optional[aws_cdk.core.RemovalPolicy]:
        """The policy to apply when this resource is removed from the application.

        default
        :default: cdk.RemovalPolicy.Destroy

        stability
        :stability: deprecated
        """
        return self._values.get('removal_policy')

    @builtins.property
    def resource_type(self) -> typing.Optional[str]:
        """For custom resources, you can specify AWS::CloudFormation::CustomResource (the default) as the resource type, or you can specify your own resource type name.

        For example, you can use "Custom::MyCustomResourceTypeName".

        Custom resource type names must begin with "Custom::" and can include
        alphanumeric characters and the following characters: _@-. You can specify
        a custom resource type name up to a maximum length of 60 characters. You
        cannot change the type during an update.

        Using your own resource type names helps you quickly differentiate the
        types of custom resources in your stack. For example, if you had two custom
        resources that conduct two different ping tests, you could name their type
        as Custom::PingTester to make them easily identifiable as ping testers
        (instead of using AWS::CloudFormation::CustomResource).

        default
        :default: - AWS::CloudFormation::CustomResource

        see
        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cfn-customresource.html#aws-cfn-resource-type-name
        stability
        :stability: deprecated
        """
        return self._values.get('resource_type')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CustomResourceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-cloudformation.CustomResourceProviderConfig", jsii_struct_bases=[], name_mapping={'service_token': 'serviceToken'})
class CustomResourceProviderConfig():
    def __init__(self, *, service_token: str) -> None:
        """Configuration options for custom resource providers.

        :param service_token: The ARN of the SNS topic or the AWS Lambda function which implements this provider.

        stability
        :stability: deprecated
        """
        self._values = {
            'service_token': service_token,
        }

    @builtins.property
    def service_token(self) -> str:
        """The ARN of the SNS topic or the AWS Lambda function which implements this provider.

        stability
        :stability: deprecated
        """
        return self._values.get('service_token')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CustomResourceProviderConfig(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.interface(jsii_type="@aws-cdk/aws-cloudformation.ICustomResourceProvider")
class ICustomResourceProvider(jsii.compat.Protocol):
    """Represents a provider for an AWS CloudFormation custom resources.

    deprecated
    :deprecated: use ``core.ICustomResourceProvider``

    stability
    :stability: deprecated
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ICustomResourceProviderProxy

    @jsii.member(jsii_name="bind")
    def bind(self, scope: aws_cdk.core.Construct) -> "CustomResourceProviderConfig":
        """Called when this provider is used by a ``CustomResource``.

        :param scope: The resource that uses this provider.

        return
        :return: provider configuration

        stability
        :stability: deprecated
        """
        ...


class _ICustomResourceProviderProxy():
    """Represents a provider for an AWS CloudFormation custom resources.

    deprecated
    :deprecated: use ``core.ICustomResourceProvider``

    stability
    :stability: deprecated
    """
    __jsii_type__ = "@aws-cdk/aws-cloudformation.ICustomResourceProvider"
    @jsii.member(jsii_name="bind")
    def bind(self, scope: aws_cdk.core.Construct) -> "CustomResourceProviderConfig":
        """Called when this provider is used by a ``CustomResource``.

        :param scope: The resource that uses this provider.

        return
        :return: provider configuration

        stability
        :stability: deprecated
        """
        return jsii.invoke(self, "bind", [scope])


class NestedStack(aws_cdk.core.NestedStack, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cloudformation.NestedStack"):
    """A CloudFormation nested stack.

    When you apply template changes to update a top-level stack, CloudFormation
    updates the top-level stack and initiates an update to its nested stacks.
    CloudFormation updates the resources of modified nested stacks, but does not
    update the resources of unmodified nested stacks.

    Furthermore, this stack will not be treated as an independent deployment
    artifact (won't be listed in "cdk list" or deployable through "cdk deploy"),
    but rather only synthesized as a template and uploaded as an asset to S3.

    Cross references of resource attributes between the parent stack and the
    nested stack will automatically be translated to stack parameters and
    outputs.

    stability
    :stability: experimental
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, notifications: typing.Optional[typing.List[aws_cdk.aws_sns.ITopic]]=None, parameters: typing.Optional[typing.Mapping[str, str]]=None, timeout: typing.Optional[aws_cdk.core.Duration]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param notifications: The Simple Notification Service (SNS) topics to publish stack related events. Default: - notifications are not sent for this stack.
        :param parameters: The set value pairs that represent the parameters passed to CloudFormation when this nested stack is created. Each parameter has a name corresponding to a parameter defined in the embedded template and a value representing the value that you want to set for the parameter. The nested stack construct will automatically synthesize parameters in order to bind references from the parent stack(s) into the nested stack. Default: - no user-defined parameters are passed to the nested stack
        :param timeout: The length of time that CloudFormation waits for the nested stack to reach the CREATE_COMPLETE state. When CloudFormation detects that the nested stack has reached the CREATE_COMPLETE state, it marks the nested stack resource as CREATE_COMPLETE in the parent stack and resumes creating the parent stack. If the timeout period expires before the nested stack reaches CREATE_COMPLETE, CloudFormation marks the nested stack as failed and rolls back both the nested stack and parent stack. Default: - no timeout

        stability
        :stability: experimental
        """
        props = NestedStackProps(notifications=notifications, parameters=parameters, timeout=timeout)

        jsii.create(NestedStack, self, [scope, id, props])


@jsii.data_type(jsii_type="@aws-cdk/aws-cloudformation.NestedStackProps", jsii_struct_bases=[], name_mapping={'notifications': 'notifications', 'parameters': 'parameters', 'timeout': 'timeout'})
class NestedStackProps():
    def __init__(self, *, notifications: typing.Optional[typing.List[aws_cdk.aws_sns.ITopic]]=None, parameters: typing.Optional[typing.Mapping[str, str]]=None, timeout: typing.Optional[aws_cdk.core.Duration]=None) -> None:
        """Initialization props for the ``NestedStack`` construct.

        :param notifications: The Simple Notification Service (SNS) topics to publish stack related events. Default: - notifications are not sent for this stack.
        :param parameters: The set value pairs that represent the parameters passed to CloudFormation when this nested stack is created. Each parameter has a name corresponding to a parameter defined in the embedded template and a value representing the value that you want to set for the parameter. The nested stack construct will automatically synthesize parameters in order to bind references from the parent stack(s) into the nested stack. Default: - no user-defined parameters are passed to the nested stack
        :param timeout: The length of time that CloudFormation waits for the nested stack to reach the CREATE_COMPLETE state. When CloudFormation detects that the nested stack has reached the CREATE_COMPLETE state, it marks the nested stack resource as CREATE_COMPLETE in the parent stack and resumes creating the parent stack. If the timeout period expires before the nested stack reaches CREATE_COMPLETE, CloudFormation marks the nested stack as failed and rolls back both the nested stack and parent stack. Default: - no timeout

        stability
        :stability: experimental
        """
        self._values = {
        }
        if notifications is not None: self._values["notifications"] = notifications
        if parameters is not None: self._values["parameters"] = parameters
        if timeout is not None: self._values["timeout"] = timeout

    @builtins.property
    def notifications(self) -> typing.Optional[typing.List[aws_cdk.aws_sns.ITopic]]:
        """The Simple Notification Service (SNS) topics to publish stack related events.

        default
        :default: - notifications are not sent for this stack.

        stability
        :stability: experimental
        """
        return self._values.get('notifications')

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[str, str]]:
        """The set value pairs that represent the parameters passed to CloudFormation when this nested stack is created.

        Each parameter has a name corresponding
        to a parameter defined in the embedded template and a value representing
        the value that you want to set for the parameter.

        The nested stack construct will automatically synthesize parameters in order
        to bind references from the parent stack(s) into the nested stack.

        default
        :default: - no user-defined parameters are passed to the nested stack

        stability
        :stability: experimental
        """
        return self._values.get('parameters')

    @builtins.property
    def timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The length of time that CloudFormation waits for the nested stack to reach the CREATE_COMPLETE state.

        When CloudFormation detects that the nested stack has reached the
        CREATE_COMPLETE state, it marks the nested stack resource as
        CREATE_COMPLETE in the parent stack and resumes creating the parent stack.
        If the timeout period expires before the nested stack reaches
        CREATE_COMPLETE, CloudFormation marks the nested stack as failed and rolls
        back both the nested stack and parent stack.

        default
        :default: - no timeout

        stability
        :stability: experimental
        """
        return self._values.get('timeout')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'NestedStackProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(ICustomResourceProvider)
class CustomResourceProvider(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cloudformation.CustomResourceProvider"):
    """Represents a provider for an AWS CloudFormation custom resources.

    stability
    :stability: deprecated
    """
    @jsii.member(jsii_name="fromLambda")
    @builtins.classmethod
    def from_lambda(cls, handler: aws_cdk.aws_lambda.IFunction) -> "CustomResourceProvider":
        """The Lambda provider that implements this custom resource.

        We recommend using a lambda.SingletonFunction for this.

        :param handler: -

        stability
        :stability: deprecated
        """
        return jsii.sinvoke(cls, "fromLambda", [handler])

    @jsii.member(jsii_name="fromTopic")
    @builtins.classmethod
    def from_topic(cls, topic: aws_cdk.aws_sns.ITopic) -> "CustomResourceProvider":
        """The SNS Topic for the provider that implements this custom resource.

        :param topic: -

        stability
        :stability: deprecated
        """
        return jsii.sinvoke(cls, "fromTopic", [topic])

    @jsii.member(jsii_name="lambda")
    @builtins.classmethod
    def lambda_(cls, handler: aws_cdk.aws_lambda.IFunction) -> "CustomResourceProvider":
        """Use AWS Lambda as a provider.

        :param handler: -

        deprecated
        :deprecated: use ``fromLambda``

        stability
        :stability: deprecated
        """
        return jsii.sinvoke(cls, "lambda", [handler])

    @jsii.member(jsii_name="topic")
    @builtins.classmethod
    def topic(cls, topic: aws_cdk.aws_sns.ITopic) -> "CustomResourceProvider":
        """Use an SNS topic as the provider.

        :param topic: -

        deprecated
        :deprecated: use ``fromTopic``

        stability
        :stability: deprecated
        """
        return jsii.sinvoke(cls, "topic", [topic])

    @jsii.member(jsii_name="bind")
    def bind(self, _: aws_cdk.core.Construct) -> "CustomResourceProviderConfig":
        """Called when this provider is used by a ``CustomResource``.

        :param _: -

        stability
        :stability: deprecated
        """
        return jsii.invoke(self, "bind", [_])

    @builtins.property
    @jsii.member(jsii_name="serviceToken")
    def service_token(self) -> str:
        """the ServiceToken which contains the ARN for this provider.

        stability
        :stability: deprecated
        """
        return jsii.get(self, "serviceToken")


__all__ = [
    "CfnCustomResource",
    "CfnCustomResourceProps",
    "CfnMacro",
    "CfnMacroProps",
    "CfnStack",
    "CfnStackProps",
    "CfnWaitCondition",
    "CfnWaitConditionHandle",
    "CfnWaitConditionProps",
    "CloudFormationCapabilities",
    "CustomResource",
    "CustomResourceProps",
    "CustomResourceProvider",
    "CustomResourceProviderConfig",
    "ICustomResourceProvider",
    "NestedStack",
    "NestedStackProps",
]

publication.publish()
