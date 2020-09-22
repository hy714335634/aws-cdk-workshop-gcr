"""
# cdk-assets-schema

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Stable](https://img.shields.io/badge/cdk--constructs-stable-success.svg?style=for-the-badge)

---
<!--END STABILITY BANNER-->

This module contains the schema definitions for the Asset Manifest.

We expose them via JSII so that they are checked for backwards compatibility
by the `jsii-diff` tool; routines exist in `validate.ts` which will return
them, so that the structs can only be strengthened (i.e., existing fields
may not be removed or made optional).
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from ._jsii import *


class AssetManifestSchema(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/cdk-assets-schema.AssetManifestSchema"):
    """Static class with loader routines.

    This class mostly exists to put the schema structs into input position
    (taken into a function), so that the jsii-diff checker will make sure all
    structs are only allowed to be weakened in future updates. For example,
    it is now allowed to add new required fields, since old CDK frameworks
    would not be emitting those fields yet.

    At the same time, we might as well validate the structure so code doesn't
    barf on invalid disk input.
    """
    def __init__(self) -> None:
        jsii.create(AssetManifestSchema, self, [])

    @jsii.member(jsii_name="currentVersion")
    @builtins.classmethod
    def current_version(cls) -> str:
        """Return the version of the schema module."""
        return jsii.sinvoke(cls, "currentVersion", [])

    @jsii.member(jsii_name="input")
    @builtins.classmethod
    def input(cls, *, version: str, docker_images: typing.Optional[typing.Mapping[str, "DockerImageAsset"]]=None, files: typing.Optional[typing.Mapping[str, "FileAsset"]]=None) -> None:
        """Take a ManifestFile as input.

        The presence of this method makes sure the struct is only ever weakened
        in future releases.

        :param version: Version of the manifest.
        :param docker_images: The Docker image assets in this manifest. Default: - No Docker images
        :param files: The file assets in this manifest. Default: - No files
        """
        file = ManifestFile(version=version, docker_images=docker_images, files=files)

        return jsii.sinvoke(cls, "input", [file])

    @jsii.member(jsii_name="validate")
    @builtins.classmethod
    def validate(cls, file: typing.Any) -> None:
        """Validate the given structured object as a valid ManifestFile schema.

        :param file: -
        """
        return jsii.sinvoke(cls, "validate", [file])


@jsii.data_type(jsii_type="@aws-cdk/cdk-assets-schema.AwsDestination", jsii_struct_bases=[], name_mapping={'assume_role_arn': 'assumeRoleArn', 'assume_role_external_id': 'assumeRoleExternalId', 'region': 'region'})
class AwsDestination():
    def __init__(self, *, assume_role_arn: typing.Optional[str]=None, assume_role_external_id: typing.Optional[str]=None, region: typing.Optional[str]=None) -> None:
        """Destination for assets that need to be uploaded to AWS.

        :param assume_role_arn: The role that needs to be assumed while publishing this asset. Default: - No role will be assumed
        :param assume_role_external_id: The ExternalId that needs to be supplied while assuming this role. Default: - No ExternalId will be supplied
        :param region: The region where this asset will need to be published. Default: - Current region
        """
        self._values = {
        }
        if assume_role_arn is not None: self._values["assume_role_arn"] = assume_role_arn
        if assume_role_external_id is not None: self._values["assume_role_external_id"] = assume_role_external_id
        if region is not None: self._values["region"] = region

    @builtins.property
    def assume_role_arn(self) -> typing.Optional[str]:
        """The role that needs to be assumed while publishing this asset.

        default
        :default: - No role will be assumed
        """
        return self._values.get('assume_role_arn')

    @builtins.property
    def assume_role_external_id(self) -> typing.Optional[str]:
        """The ExternalId that needs to be supplied while assuming this role.

        default
        :default: - No ExternalId will be supplied
        """
        return self._values.get('assume_role_external_id')

    @builtins.property
    def region(self) -> typing.Optional[str]:
        """The region where this asset will need to be published.

        default
        :default: - Current region
        """
        return self._values.get('region')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AwsDestination(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/cdk-assets-schema.DockerImageAsset", jsii_struct_bases=[], name_mapping={'destinations': 'destinations', 'source': 'source'})
class DockerImageAsset():
    def __init__(self, *, destinations: typing.Mapping[str, "DockerImageDestination"], source: "DockerImageSource") -> None:
        """A file asset.

        :param destinations: Destinations for this file asset.
        :param source: Source description for file assets.
        """
        if isinstance(source, dict): source = DockerImageSource(**source)
        self._values = {
            'destinations': destinations,
            'source': source,
        }

    @builtins.property
    def destinations(self) -> typing.Mapping[str, "DockerImageDestination"]:
        """Destinations for this file asset."""
        return self._values.get('destinations')

    @builtins.property
    def source(self) -> "DockerImageSource":
        """Source description for file assets."""
        return self._values.get('source')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'DockerImageAsset(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/cdk-assets-schema.DockerImageDestination", jsii_struct_bases=[AwsDestination], name_mapping={'assume_role_arn': 'assumeRoleArn', 'assume_role_external_id': 'assumeRoleExternalId', 'region': 'region', 'image_tag': 'imageTag', 'repository_name': 'repositoryName'})
class DockerImageDestination(AwsDestination):
    def __init__(self, *, assume_role_arn: typing.Optional[str]=None, assume_role_external_id: typing.Optional[str]=None, region: typing.Optional[str]=None, image_tag: str, repository_name: str) -> None:
        """Where to publish docker images.

        :param assume_role_arn: The role that needs to be assumed while publishing this asset. Default: - No role will be assumed
        :param assume_role_external_id: The ExternalId that needs to be supplied while assuming this role. Default: - No ExternalId will be supplied
        :param region: The region where this asset will need to be published. Default: - Current region
        :param image_tag: Tag of the image to publish.
        :param repository_name: Name of the ECR repository to publish to.
        """
        self._values = {
            'image_tag': image_tag,
            'repository_name': repository_name,
        }
        if assume_role_arn is not None: self._values["assume_role_arn"] = assume_role_arn
        if assume_role_external_id is not None: self._values["assume_role_external_id"] = assume_role_external_id
        if region is not None: self._values["region"] = region

    @builtins.property
    def assume_role_arn(self) -> typing.Optional[str]:
        """The role that needs to be assumed while publishing this asset.

        default
        :default: - No role will be assumed
        """
        return self._values.get('assume_role_arn')

    @builtins.property
    def assume_role_external_id(self) -> typing.Optional[str]:
        """The ExternalId that needs to be supplied while assuming this role.

        default
        :default: - No ExternalId will be supplied
        """
        return self._values.get('assume_role_external_id')

    @builtins.property
    def region(self) -> typing.Optional[str]:
        """The region where this asset will need to be published.

        default
        :default: - Current region
        """
        return self._values.get('region')

    @builtins.property
    def image_tag(self) -> str:
        """Tag of the image to publish."""
        return self._values.get('image_tag')

    @builtins.property
    def repository_name(self) -> str:
        """Name of the ECR repository to publish to."""
        return self._values.get('repository_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'DockerImageDestination(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/cdk-assets-schema.DockerImageSource", jsii_struct_bases=[], name_mapping={'directory': 'directory', 'docker_build_args': 'dockerBuildArgs', 'docker_build_target': 'dockerBuildTarget', 'docker_file': 'dockerFile'})
class DockerImageSource():
    def __init__(self, *, directory: str, docker_build_args: typing.Optional[typing.Mapping[str, str]]=None, docker_build_target: typing.Optional[str]=None, docker_file: typing.Optional[str]=None) -> None:
        """Properties for how to produce a Docker image from a source.

        :param directory: The directory containing the Docker image build instructions. This path is relative to the asset manifest location.
        :param docker_build_args: Additional build arguments. Default: - No additional build arguments
        :param docker_build_target: Target build stage in a Dockerfile with multiple build stages. Default: - The last stage in the Dockerfile
        :param docker_file: The name of the file with build instructions. Default: "Dockerfile"
        """
        self._values = {
            'directory': directory,
        }
        if docker_build_args is not None: self._values["docker_build_args"] = docker_build_args
        if docker_build_target is not None: self._values["docker_build_target"] = docker_build_target
        if docker_file is not None: self._values["docker_file"] = docker_file

    @builtins.property
    def directory(self) -> str:
        """The directory containing the Docker image build instructions.

        This path is relative to the asset manifest location.
        """
        return self._values.get('directory')

    @builtins.property
    def docker_build_args(self) -> typing.Optional[typing.Mapping[str, str]]:
        """Additional build arguments.

        default
        :default: - No additional build arguments
        """
        return self._values.get('docker_build_args')

    @builtins.property
    def docker_build_target(self) -> typing.Optional[str]:
        """Target build stage in a Dockerfile with multiple build stages.

        default
        :default: - The last stage in the Dockerfile
        """
        return self._values.get('docker_build_target')

    @builtins.property
    def docker_file(self) -> typing.Optional[str]:
        """The name of the file with build instructions.

        default
        :default: "Dockerfile"
        """
        return self._values.get('docker_file')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'DockerImageSource(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/cdk-assets-schema.FileAsset", jsii_struct_bases=[], name_mapping={'destinations': 'destinations', 'source': 'source'})
class FileAsset():
    def __init__(self, *, destinations: typing.Mapping[str, "FileDestination"], source: "FileSource") -> None:
        """A file asset.

        :param destinations: Destinations for this file asset.
        :param source: Source description for file assets.
        """
        if isinstance(source, dict): source = FileSource(**source)
        self._values = {
            'destinations': destinations,
            'source': source,
        }

    @builtins.property
    def destinations(self) -> typing.Mapping[str, "FileDestination"]:
        """Destinations for this file asset."""
        return self._values.get('destinations')

    @builtins.property
    def source(self) -> "FileSource":
        """Source description for file assets."""
        return self._values.get('source')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'FileAsset(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/cdk-assets-schema.FileAssetPackaging")
class FileAssetPackaging(enum.Enum):
    """Packaging strategy for file assets."""
    FILE = "FILE"
    """Upload the given path as a file."""
    ZIP_DIRECTORY = "ZIP_DIRECTORY"
    """The given path is a directory, zip it and upload."""

@jsii.data_type(jsii_type="@aws-cdk/cdk-assets-schema.FileDestination", jsii_struct_bases=[AwsDestination], name_mapping={'assume_role_arn': 'assumeRoleArn', 'assume_role_external_id': 'assumeRoleExternalId', 'region': 'region', 'bucket_name': 'bucketName', 'object_key': 'objectKey'})
class FileDestination(AwsDestination):
    def __init__(self, *, assume_role_arn: typing.Optional[str]=None, assume_role_external_id: typing.Optional[str]=None, region: typing.Optional[str]=None, bucket_name: str, object_key: str) -> None:
        """Where in S3 a file asset needs to be published.

        :param assume_role_arn: The role that needs to be assumed while publishing this asset. Default: - No role will be assumed
        :param assume_role_external_id: The ExternalId that needs to be supplied while assuming this role. Default: - No ExternalId will be supplied
        :param region: The region where this asset will need to be published. Default: - Current region
        :param bucket_name: The name of the bucket.
        :param object_key: The destination object key.
        """
        self._values = {
            'bucket_name': bucket_name,
            'object_key': object_key,
        }
        if assume_role_arn is not None: self._values["assume_role_arn"] = assume_role_arn
        if assume_role_external_id is not None: self._values["assume_role_external_id"] = assume_role_external_id
        if region is not None: self._values["region"] = region

    @builtins.property
    def assume_role_arn(self) -> typing.Optional[str]:
        """The role that needs to be assumed while publishing this asset.

        default
        :default: - No role will be assumed
        """
        return self._values.get('assume_role_arn')

    @builtins.property
    def assume_role_external_id(self) -> typing.Optional[str]:
        """The ExternalId that needs to be supplied while assuming this role.

        default
        :default: - No ExternalId will be supplied
        """
        return self._values.get('assume_role_external_id')

    @builtins.property
    def region(self) -> typing.Optional[str]:
        """The region where this asset will need to be published.

        default
        :default: - Current region
        """
        return self._values.get('region')

    @builtins.property
    def bucket_name(self) -> str:
        """The name of the bucket."""
        return self._values.get('bucket_name')

    @builtins.property
    def object_key(self) -> str:
        """The destination object key."""
        return self._values.get('object_key')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'FileDestination(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/cdk-assets-schema.FileSource", jsii_struct_bases=[], name_mapping={'path': 'path', 'packaging': 'packaging'})
class FileSource():
    def __init__(self, *, path: str, packaging: typing.Optional["FileAssetPackaging"]=None) -> None:
        """Describe the source of a file asset.

        :param path: The filesystem object to upload. This path is relative to the asset manifest location.
        :param packaging: Packaging method. Default: FILE
        """
        self._values = {
            'path': path,
        }
        if packaging is not None: self._values["packaging"] = packaging

    @builtins.property
    def path(self) -> str:
        """The filesystem object to upload.

        This path is relative to the asset manifest location.
        """
        return self._values.get('path')

    @builtins.property
    def packaging(self) -> typing.Optional["FileAssetPackaging"]:
        """Packaging method.

        default
        :default: FILE
        """
        return self._values.get('packaging')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'FileSource(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/cdk-assets-schema.ManifestFile", jsii_struct_bases=[], name_mapping={'version': 'version', 'docker_images': 'dockerImages', 'files': 'files'})
class ManifestFile():
    def __init__(self, *, version: str, docker_images: typing.Optional[typing.Mapping[str, "DockerImageAsset"]]=None, files: typing.Optional[typing.Mapping[str, "FileAsset"]]=None) -> None:
        """Definitions for the asset manifest.

        :param version: Version of the manifest.
        :param docker_images: The Docker image assets in this manifest. Default: - No Docker images
        :param files: The file assets in this manifest. Default: - No files
        """
        self._values = {
            'version': version,
        }
        if docker_images is not None: self._values["docker_images"] = docker_images
        if files is not None: self._values["files"] = files

    @builtins.property
    def version(self) -> str:
        """Version of the manifest."""
        return self._values.get('version')

    @builtins.property
    def docker_images(self) -> typing.Optional[typing.Mapping[str, "DockerImageAsset"]]:
        """The Docker image assets in this manifest.

        default
        :default: - No Docker images
        """
        return self._values.get('docker_images')

    @builtins.property
    def files(self) -> typing.Optional[typing.Mapping[str, "FileAsset"]]:
        """The file assets in this manifest.

        default
        :default: - No files
        """
        return self._values.get('files')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ManifestFile(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "AssetManifestSchema",
    "AwsDestination",
    "DockerImageAsset",
    "DockerImageDestination",
    "DockerImageSource",
    "FileAsset",
    "FileAssetPackaging",
    "FileDestination",
    "FileSource",
    "ManifestFile",
]

publication.publish()
