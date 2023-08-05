# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._inputs import *

__all__ = ['RepositoryArgs', 'Repository']

@pulumi.input_type
class RepositoryArgs:
    def __init__(__self__, *,
                 format: pulumi.Input[str],
                 repository_id: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None,
                 kms_key_name: Optional[pulumi.Input[str]] = None,
                 labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 maven_config: Optional[pulumi.Input['RepositoryMavenConfigArgs']] = None,
                 project: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Repository resource.
        :param pulumi.Input[str] format: The format of packages that are stored in the repository. You can only create
               alpha formats if you are a member of the [alpha user group](https://cloud.google.com/artifact-registry/docs/supported-formats#alpha-access).
               - DOCKER
               - MAVEN ([Preview](https://cloud.google.com/products#product-launch-stages))
               - NPM ([Preview](https://cloud.google.com/products#product-launch-stages))
               - PYTHON ([Preview](https://cloud.google.com/products#product-launch-stages))
               - APT ([alpha](https://cloud.google.com/products#product-launch-stages))
               - YUM ([alpha](https://cloud.google.com/products#product-launch-stages))
               - HELM ([alpha](https://cloud.google.com/products#product-launch-stages))
        :param pulumi.Input[str] repository_id: The last part of the repository name, for example:
               "repo1"
        :param pulumi.Input[str] description: The user-provided description of the repository.
        :param pulumi.Input[str] kms_key_name: The Cloud KMS resource name of the customer managed encryption key that’s
               used to encrypt the contents of the Repository. Has the form:
               `projects/my-project/locations/my-region/keyRings/my-kr/cryptoKeys/my-key`.
               This value may not be changed after the Repository has been created.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: Labels with user-defined metadata.
               This field may contain up to 64 entries. Label keys and values may be no
               longer than 63 characters. Label keys must begin with a lowercase letter
               and may only contain lowercase letters, numeric characters, underscores,
               and dashes.
        :param pulumi.Input[str] location: The name of the location this repository is located in.
        :param pulumi.Input['RepositoryMavenConfigArgs'] maven_config: MavenRepositoryConfig is maven related repository details.
               Provides additional configuration details for repositories of the maven
               format type.
               Structure is documented below.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        """
        pulumi.set(__self__, "format", format)
        pulumi.set(__self__, "repository_id", repository_id)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if kms_key_name is not None:
            pulumi.set(__self__, "kms_key_name", kms_key_name)
        if labels is not None:
            pulumi.set(__self__, "labels", labels)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if maven_config is not None:
            pulumi.set(__self__, "maven_config", maven_config)
        if project is not None:
            pulumi.set(__self__, "project", project)

    @property
    @pulumi.getter
    def format(self) -> pulumi.Input[str]:
        """
        The format of packages that are stored in the repository. You can only create
        alpha formats if you are a member of the [alpha user group](https://cloud.google.com/artifact-registry/docs/supported-formats#alpha-access).
        - DOCKER
        - MAVEN ([Preview](https://cloud.google.com/products#product-launch-stages))
        - NPM ([Preview](https://cloud.google.com/products#product-launch-stages))
        - PYTHON ([Preview](https://cloud.google.com/products#product-launch-stages))
        - APT ([alpha](https://cloud.google.com/products#product-launch-stages))
        - YUM ([alpha](https://cloud.google.com/products#product-launch-stages))
        - HELM ([alpha](https://cloud.google.com/products#product-launch-stages))
        """
        return pulumi.get(self, "format")

    @format.setter
    def format(self, value: pulumi.Input[str]):
        pulumi.set(self, "format", value)

    @property
    @pulumi.getter(name="repositoryId")
    def repository_id(self) -> pulumi.Input[str]:
        """
        The last part of the repository name, for example:
        "repo1"
        """
        return pulumi.get(self, "repository_id")

    @repository_id.setter
    def repository_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "repository_id", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The user-provided description of the repository.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="kmsKeyName")
    def kms_key_name(self) -> Optional[pulumi.Input[str]]:
        """
        The Cloud KMS resource name of the customer managed encryption key that’s
        used to encrypt the contents of the Repository. Has the form:
        `projects/my-project/locations/my-region/keyRings/my-kr/cryptoKeys/my-key`.
        This value may not be changed after the Repository has been created.
        """
        return pulumi.get(self, "kms_key_name")

    @kms_key_name.setter
    def kms_key_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "kms_key_name", value)

    @property
    @pulumi.getter
    def labels(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Labels with user-defined metadata.
        This field may contain up to 64 entries. Label keys and values may be no
        longer than 63 characters. Label keys must begin with a lowercase letter
        and may only contain lowercase letters, numeric characters, underscores,
        and dashes.
        """
        return pulumi.get(self, "labels")

    @labels.setter
    def labels(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "labels", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the location this repository is located in.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter(name="mavenConfig")
    def maven_config(self) -> Optional[pulumi.Input['RepositoryMavenConfigArgs']]:
        """
        MavenRepositoryConfig is maven related repository details.
        Provides additional configuration details for repositories of the maven
        format type.
        Structure is documented below.
        """
        return pulumi.get(self, "maven_config")

    @maven_config.setter
    def maven_config(self, value: Optional[pulumi.Input['RepositoryMavenConfigArgs']]):
        pulumi.set(self, "maven_config", value)

    @property
    @pulumi.getter
    def project(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the project in which the resource belongs.
        If it is not provided, the provider project is used.
        """
        return pulumi.get(self, "project")

    @project.setter
    def project(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "project", value)


@pulumi.input_type
class _RepositoryState:
    def __init__(__self__, *,
                 create_time: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 format: Optional[pulumi.Input[str]] = None,
                 kms_key_name: Optional[pulumi.Input[str]] = None,
                 labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 maven_config: Optional[pulumi.Input['RepositoryMavenConfigArgs']] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 repository_id: Optional[pulumi.Input[str]] = None,
                 update_time: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering Repository resources.
        :param pulumi.Input[str] create_time: The time when the repository was created.
        :param pulumi.Input[str] description: The user-provided description of the repository.
        :param pulumi.Input[str] format: The format of packages that are stored in the repository. You can only create
               alpha formats if you are a member of the [alpha user group](https://cloud.google.com/artifact-registry/docs/supported-formats#alpha-access).
               - DOCKER
               - MAVEN ([Preview](https://cloud.google.com/products#product-launch-stages))
               - NPM ([Preview](https://cloud.google.com/products#product-launch-stages))
               - PYTHON ([Preview](https://cloud.google.com/products#product-launch-stages))
               - APT ([alpha](https://cloud.google.com/products#product-launch-stages))
               - YUM ([alpha](https://cloud.google.com/products#product-launch-stages))
               - HELM ([alpha](https://cloud.google.com/products#product-launch-stages))
        :param pulumi.Input[str] kms_key_name: The Cloud KMS resource name of the customer managed encryption key that’s
               used to encrypt the contents of the Repository. Has the form:
               `projects/my-project/locations/my-region/keyRings/my-kr/cryptoKeys/my-key`.
               This value may not be changed after the Repository has been created.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: Labels with user-defined metadata.
               This field may contain up to 64 entries. Label keys and values may be no
               longer than 63 characters. Label keys must begin with a lowercase letter
               and may only contain lowercase letters, numeric characters, underscores,
               and dashes.
        :param pulumi.Input[str] location: The name of the location this repository is located in.
        :param pulumi.Input['RepositoryMavenConfigArgs'] maven_config: MavenRepositoryConfig is maven related repository details.
               Provides additional configuration details for repositories of the maven
               format type.
               Structure is documented below.
        :param pulumi.Input[str] name: The name of the repository, for example: "projects/p1/locations/us-central1/repositories/repo1"
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] repository_id: The last part of the repository name, for example:
               "repo1"
        :param pulumi.Input[str] update_time: The time when the repository was last updated.
        """
        if create_time is not None:
            pulumi.set(__self__, "create_time", create_time)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if format is not None:
            pulumi.set(__self__, "format", format)
        if kms_key_name is not None:
            pulumi.set(__self__, "kms_key_name", kms_key_name)
        if labels is not None:
            pulumi.set(__self__, "labels", labels)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if maven_config is not None:
            pulumi.set(__self__, "maven_config", maven_config)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if project is not None:
            pulumi.set(__self__, "project", project)
        if repository_id is not None:
            pulumi.set(__self__, "repository_id", repository_id)
        if update_time is not None:
            pulumi.set(__self__, "update_time", update_time)

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> Optional[pulumi.Input[str]]:
        """
        The time when the repository was created.
        """
        return pulumi.get(self, "create_time")

    @create_time.setter
    def create_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "create_time", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The user-provided description of the repository.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def format(self) -> Optional[pulumi.Input[str]]:
        """
        The format of packages that are stored in the repository. You can only create
        alpha formats if you are a member of the [alpha user group](https://cloud.google.com/artifact-registry/docs/supported-formats#alpha-access).
        - DOCKER
        - MAVEN ([Preview](https://cloud.google.com/products#product-launch-stages))
        - NPM ([Preview](https://cloud.google.com/products#product-launch-stages))
        - PYTHON ([Preview](https://cloud.google.com/products#product-launch-stages))
        - APT ([alpha](https://cloud.google.com/products#product-launch-stages))
        - YUM ([alpha](https://cloud.google.com/products#product-launch-stages))
        - HELM ([alpha](https://cloud.google.com/products#product-launch-stages))
        """
        return pulumi.get(self, "format")

    @format.setter
    def format(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "format", value)

    @property
    @pulumi.getter(name="kmsKeyName")
    def kms_key_name(self) -> Optional[pulumi.Input[str]]:
        """
        The Cloud KMS resource name of the customer managed encryption key that’s
        used to encrypt the contents of the Repository. Has the form:
        `projects/my-project/locations/my-region/keyRings/my-kr/cryptoKeys/my-key`.
        This value may not be changed after the Repository has been created.
        """
        return pulumi.get(self, "kms_key_name")

    @kms_key_name.setter
    def kms_key_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "kms_key_name", value)

    @property
    @pulumi.getter
    def labels(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Labels with user-defined metadata.
        This field may contain up to 64 entries. Label keys and values may be no
        longer than 63 characters. Label keys must begin with a lowercase letter
        and may only contain lowercase letters, numeric characters, underscores,
        and dashes.
        """
        return pulumi.get(self, "labels")

    @labels.setter
    def labels(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "labels", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the location this repository is located in.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter(name="mavenConfig")
    def maven_config(self) -> Optional[pulumi.Input['RepositoryMavenConfigArgs']]:
        """
        MavenRepositoryConfig is maven related repository details.
        Provides additional configuration details for repositories of the maven
        format type.
        Structure is documented below.
        """
        return pulumi.get(self, "maven_config")

    @maven_config.setter
    def maven_config(self, value: Optional[pulumi.Input['RepositoryMavenConfigArgs']]):
        pulumi.set(self, "maven_config", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the repository, for example: "projects/p1/locations/us-central1/repositories/repo1"
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def project(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the project in which the resource belongs.
        If it is not provided, the provider project is used.
        """
        return pulumi.get(self, "project")

    @project.setter
    def project(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "project", value)

    @property
    @pulumi.getter(name="repositoryId")
    def repository_id(self) -> Optional[pulumi.Input[str]]:
        """
        The last part of the repository name, for example:
        "repo1"
        """
        return pulumi.get(self, "repository_id")

    @repository_id.setter
    def repository_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "repository_id", value)

    @property
    @pulumi.getter(name="updateTime")
    def update_time(self) -> Optional[pulumi.Input[str]]:
        """
        The time when the repository was last updated.
        """
        return pulumi.get(self, "update_time")

    @update_time.setter
    def update_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "update_time", value)


class Repository(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 format: Optional[pulumi.Input[str]] = None,
                 kms_key_name: Optional[pulumi.Input[str]] = None,
                 labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 maven_config: Optional[pulumi.Input[pulumi.InputType['RepositoryMavenConfigArgs']]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 repository_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        A repository for storing artifacts

        To get more information about Repository, see:

        * [API documentation](https://cloud.google.com/artifact-registry/docs/reference/rest/v1beta2/projects.locations.repositories)
        * How-to Guides
            * [Official Documentation](https://cloud.google.com/artifact-registry/docs/overview)

        ## Example Usage
        ### Artifact Registry Repository Basic

        ```python
        import pulumi
        import pulumi_gcp as gcp

        my_repo = gcp.artifactregistry.Repository("my-repo",
            location="us-central1",
            repository_id="my-repository",
            description="example docker repository",
            format="DOCKER",
            opts=pulumi.ResourceOptions(provider=google_beta))
        ```
        ### Artifact Registry Repository Cmek

        ```python
        import pulumi
        import pulumi_gcp as gcp

        my_repo = gcp.artifactregistry.Repository("my-repo",
            location="us-central1",
            repository_id="my-repository",
            description="example docker repository with cmek",
            format="DOCKER",
            kms_key_name="kms-key",
            opts=pulumi.ResourceOptions(provider=google_beta))
        ```
        ### Artifact Registry Repository Iam

        ```python
        import pulumi
        import pulumi_gcp as gcp

        my_repo = gcp.artifactregistry.Repository("my-repo",
            location="us-central1",
            repository_id="my-repository",
            description="example docker repository with iam",
            format="DOCKER",
            opts=pulumi.ResourceOptions(provider=google_beta))
        test_account = gcp.service_account.Account("test-account",
            account_id="my-account",
            display_name="Test Service Account",
            opts=pulumi.ResourceOptions(provider=google_beta))
        test_iam = gcp.artifactregistry.RepositoryIamMember("test-iam",
            location=my_repo.location,
            repository=my_repo.name,
            role="roles/artifactregistry.reader",
            member=test_account.email.apply(lambda email: f"serviceAccount:{email}"),
            opts=pulumi.ResourceOptions(provider=google_beta))
        ```

        ## Import

        Repository can be imported using any of these accepted formats

        ```sh
         $ pulumi import gcp:artifactregistry/repository:Repository default projects/{{project}}/locations/{{location}}/repositories/{{repository_id}}
        ```

        ```sh
         $ pulumi import gcp:artifactregistry/repository:Repository default {{project}}/{{location}}/{{repository_id}}
        ```

        ```sh
         $ pulumi import gcp:artifactregistry/repository:Repository default {{location}}/{{repository_id}}
        ```

        ```sh
         $ pulumi import gcp:artifactregistry/repository:Repository default {{repository_id}}
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: The user-provided description of the repository.
        :param pulumi.Input[str] format: The format of packages that are stored in the repository. You can only create
               alpha formats if you are a member of the [alpha user group](https://cloud.google.com/artifact-registry/docs/supported-formats#alpha-access).
               - DOCKER
               - MAVEN ([Preview](https://cloud.google.com/products#product-launch-stages))
               - NPM ([Preview](https://cloud.google.com/products#product-launch-stages))
               - PYTHON ([Preview](https://cloud.google.com/products#product-launch-stages))
               - APT ([alpha](https://cloud.google.com/products#product-launch-stages))
               - YUM ([alpha](https://cloud.google.com/products#product-launch-stages))
               - HELM ([alpha](https://cloud.google.com/products#product-launch-stages))
        :param pulumi.Input[str] kms_key_name: The Cloud KMS resource name of the customer managed encryption key that’s
               used to encrypt the contents of the Repository. Has the form:
               `projects/my-project/locations/my-region/keyRings/my-kr/cryptoKeys/my-key`.
               This value may not be changed after the Repository has been created.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: Labels with user-defined metadata.
               This field may contain up to 64 entries. Label keys and values may be no
               longer than 63 characters. Label keys must begin with a lowercase letter
               and may only contain lowercase letters, numeric characters, underscores,
               and dashes.
        :param pulumi.Input[str] location: The name of the location this repository is located in.
        :param pulumi.Input[pulumi.InputType['RepositoryMavenConfigArgs']] maven_config: MavenRepositoryConfig is maven related repository details.
               Provides additional configuration details for repositories of the maven
               format type.
               Structure is documented below.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] repository_id: The last part of the repository name, for example:
               "repo1"
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: RepositoryArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        A repository for storing artifacts

        To get more information about Repository, see:

        * [API documentation](https://cloud.google.com/artifact-registry/docs/reference/rest/v1beta2/projects.locations.repositories)
        * How-to Guides
            * [Official Documentation](https://cloud.google.com/artifact-registry/docs/overview)

        ## Example Usage
        ### Artifact Registry Repository Basic

        ```python
        import pulumi
        import pulumi_gcp as gcp

        my_repo = gcp.artifactregistry.Repository("my-repo",
            location="us-central1",
            repository_id="my-repository",
            description="example docker repository",
            format="DOCKER",
            opts=pulumi.ResourceOptions(provider=google_beta))
        ```
        ### Artifact Registry Repository Cmek

        ```python
        import pulumi
        import pulumi_gcp as gcp

        my_repo = gcp.artifactregistry.Repository("my-repo",
            location="us-central1",
            repository_id="my-repository",
            description="example docker repository with cmek",
            format="DOCKER",
            kms_key_name="kms-key",
            opts=pulumi.ResourceOptions(provider=google_beta))
        ```
        ### Artifact Registry Repository Iam

        ```python
        import pulumi
        import pulumi_gcp as gcp

        my_repo = gcp.artifactregistry.Repository("my-repo",
            location="us-central1",
            repository_id="my-repository",
            description="example docker repository with iam",
            format="DOCKER",
            opts=pulumi.ResourceOptions(provider=google_beta))
        test_account = gcp.service_account.Account("test-account",
            account_id="my-account",
            display_name="Test Service Account",
            opts=pulumi.ResourceOptions(provider=google_beta))
        test_iam = gcp.artifactregistry.RepositoryIamMember("test-iam",
            location=my_repo.location,
            repository=my_repo.name,
            role="roles/artifactregistry.reader",
            member=test_account.email.apply(lambda email: f"serviceAccount:{email}"),
            opts=pulumi.ResourceOptions(provider=google_beta))
        ```

        ## Import

        Repository can be imported using any of these accepted formats

        ```sh
         $ pulumi import gcp:artifactregistry/repository:Repository default projects/{{project}}/locations/{{location}}/repositories/{{repository_id}}
        ```

        ```sh
         $ pulumi import gcp:artifactregistry/repository:Repository default {{project}}/{{location}}/{{repository_id}}
        ```

        ```sh
         $ pulumi import gcp:artifactregistry/repository:Repository default {{location}}/{{repository_id}}
        ```

        ```sh
         $ pulumi import gcp:artifactregistry/repository:Repository default {{repository_id}}
        ```

        :param str resource_name: The name of the resource.
        :param RepositoryArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(RepositoryArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 format: Optional[pulumi.Input[str]] = None,
                 kms_key_name: Optional[pulumi.Input[str]] = None,
                 labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 maven_config: Optional[pulumi.Input[pulumi.InputType['RepositoryMavenConfigArgs']]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 repository_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = RepositoryArgs.__new__(RepositoryArgs)

            __props__.__dict__["description"] = description
            if format is None and not opts.urn:
                raise TypeError("Missing required property 'format'")
            __props__.__dict__["format"] = format
            __props__.__dict__["kms_key_name"] = kms_key_name
            __props__.__dict__["labels"] = labels
            __props__.__dict__["location"] = location
            __props__.__dict__["maven_config"] = maven_config
            __props__.__dict__["project"] = project
            if repository_id is None and not opts.urn:
                raise TypeError("Missing required property 'repository_id'")
            __props__.__dict__["repository_id"] = repository_id
            __props__.__dict__["create_time"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["update_time"] = None
        super(Repository, __self__).__init__(
            'gcp:artifactregistry/repository:Repository',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            create_time: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            format: Optional[pulumi.Input[str]] = None,
            kms_key_name: Optional[pulumi.Input[str]] = None,
            labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            location: Optional[pulumi.Input[str]] = None,
            maven_config: Optional[pulumi.Input[pulumi.InputType['RepositoryMavenConfigArgs']]] = None,
            name: Optional[pulumi.Input[str]] = None,
            project: Optional[pulumi.Input[str]] = None,
            repository_id: Optional[pulumi.Input[str]] = None,
            update_time: Optional[pulumi.Input[str]] = None) -> 'Repository':
        """
        Get an existing Repository resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] create_time: The time when the repository was created.
        :param pulumi.Input[str] description: The user-provided description of the repository.
        :param pulumi.Input[str] format: The format of packages that are stored in the repository. You can only create
               alpha formats if you are a member of the [alpha user group](https://cloud.google.com/artifact-registry/docs/supported-formats#alpha-access).
               - DOCKER
               - MAVEN ([Preview](https://cloud.google.com/products#product-launch-stages))
               - NPM ([Preview](https://cloud.google.com/products#product-launch-stages))
               - PYTHON ([Preview](https://cloud.google.com/products#product-launch-stages))
               - APT ([alpha](https://cloud.google.com/products#product-launch-stages))
               - YUM ([alpha](https://cloud.google.com/products#product-launch-stages))
               - HELM ([alpha](https://cloud.google.com/products#product-launch-stages))
        :param pulumi.Input[str] kms_key_name: The Cloud KMS resource name of the customer managed encryption key that’s
               used to encrypt the contents of the Repository. Has the form:
               `projects/my-project/locations/my-region/keyRings/my-kr/cryptoKeys/my-key`.
               This value may not be changed after the Repository has been created.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: Labels with user-defined metadata.
               This field may contain up to 64 entries. Label keys and values may be no
               longer than 63 characters. Label keys must begin with a lowercase letter
               and may only contain lowercase letters, numeric characters, underscores,
               and dashes.
        :param pulumi.Input[str] location: The name of the location this repository is located in.
        :param pulumi.Input[pulumi.InputType['RepositoryMavenConfigArgs']] maven_config: MavenRepositoryConfig is maven related repository details.
               Provides additional configuration details for repositories of the maven
               format type.
               Structure is documented below.
        :param pulumi.Input[str] name: The name of the repository, for example: "projects/p1/locations/us-central1/repositories/repo1"
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] repository_id: The last part of the repository name, for example:
               "repo1"
        :param pulumi.Input[str] update_time: The time when the repository was last updated.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _RepositoryState.__new__(_RepositoryState)

        __props__.__dict__["create_time"] = create_time
        __props__.__dict__["description"] = description
        __props__.__dict__["format"] = format
        __props__.__dict__["kms_key_name"] = kms_key_name
        __props__.__dict__["labels"] = labels
        __props__.__dict__["location"] = location
        __props__.__dict__["maven_config"] = maven_config
        __props__.__dict__["name"] = name
        __props__.__dict__["project"] = project
        __props__.__dict__["repository_id"] = repository_id
        __props__.__dict__["update_time"] = update_time
        return Repository(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> pulumi.Output[str]:
        """
        The time when the repository was created.
        """
        return pulumi.get(self, "create_time")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        The user-provided description of the repository.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def format(self) -> pulumi.Output[str]:
        """
        The format of packages that are stored in the repository. You can only create
        alpha formats if you are a member of the [alpha user group](https://cloud.google.com/artifact-registry/docs/supported-formats#alpha-access).
        - DOCKER
        - MAVEN ([Preview](https://cloud.google.com/products#product-launch-stages))
        - NPM ([Preview](https://cloud.google.com/products#product-launch-stages))
        - PYTHON ([Preview](https://cloud.google.com/products#product-launch-stages))
        - APT ([alpha](https://cloud.google.com/products#product-launch-stages))
        - YUM ([alpha](https://cloud.google.com/products#product-launch-stages))
        - HELM ([alpha](https://cloud.google.com/products#product-launch-stages))
        """
        return pulumi.get(self, "format")

    @property
    @pulumi.getter(name="kmsKeyName")
    def kms_key_name(self) -> pulumi.Output[Optional[str]]:
        """
        The Cloud KMS resource name of the customer managed encryption key that’s
        used to encrypt the contents of the Repository. Has the form:
        `projects/my-project/locations/my-region/keyRings/my-kr/cryptoKeys/my-key`.
        This value may not be changed after the Repository has been created.
        """
        return pulumi.get(self, "kms_key_name")

    @property
    @pulumi.getter
    def labels(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Labels with user-defined metadata.
        This field may contain up to 64 entries. Label keys and values may be no
        longer than 63 characters. Label keys must begin with a lowercase letter
        and may only contain lowercase letters, numeric characters, underscores,
        and dashes.
        """
        return pulumi.get(self, "labels")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        The name of the location this repository is located in.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="mavenConfig")
    def maven_config(self) -> pulumi.Output[Optional['outputs.RepositoryMavenConfig']]:
        """
        MavenRepositoryConfig is maven related repository details.
        Provides additional configuration details for repositories of the maven
        format type.
        Structure is documented below.
        """
        return pulumi.get(self, "maven_config")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the repository, for example: "projects/p1/locations/us-central1/repositories/repo1"
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def project(self) -> pulumi.Output[str]:
        """
        The ID of the project in which the resource belongs.
        If it is not provided, the provider project is used.
        """
        return pulumi.get(self, "project")

    @property
    @pulumi.getter(name="repositoryId")
    def repository_id(self) -> pulumi.Output[str]:
        """
        The last part of the repository name, for example:
        "repo1"
        """
        return pulumi.get(self, "repository_id")

    @property
    @pulumi.getter(name="updateTime")
    def update_time(self) -> pulumi.Output[str]:
        """
        The time when the repository was last updated.
        """
        return pulumi.get(self, "update_time")

