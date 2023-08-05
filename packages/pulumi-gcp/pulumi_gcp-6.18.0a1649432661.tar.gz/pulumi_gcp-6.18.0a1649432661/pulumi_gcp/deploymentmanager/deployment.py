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

__all__ = ['DeploymentArgs', 'Deployment']

@pulumi.input_type
class DeploymentArgs:
    def __init__(__self__, *,
                 target: pulumi.Input['DeploymentTargetArgs'],
                 create_policy: Optional[pulumi.Input[str]] = None,
                 delete_policy: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 labels: Optional[pulumi.Input[Sequence[pulumi.Input['DeploymentLabelArgs']]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 preview: Optional[pulumi.Input[bool]] = None,
                 project: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Deployment resource.
        :param pulumi.Input['DeploymentTargetArgs'] target: Parameters that define your deployment, including the deployment
               configuration and relevant templates.
               Structure is documented below.
        :param pulumi.Input[str] create_policy: Set the policy to use for creating new resources. Only used on
               create and update. Valid values are `CREATE_OR_ACQUIRE` (default) or
               `ACQUIRE`. If set to `ACQUIRE` and resources do not already exist,
               the deployment will fail. Note that updating this field does not
               actually affect the deployment, just how it is updated.
               Default value is `CREATE_OR_ACQUIRE`.
               Possible values are `ACQUIRE` and `CREATE_OR_ACQUIRE`.
        :param pulumi.Input[str] delete_policy: Set the policy to use for deleting new resources on update/delete.
               Valid values are `DELETE` (default) or `ABANDON`. If `DELETE`,
               resource is deleted after removal from Deployment Manager. If
               `ABANDON`, the resource is only removed from Deployment Manager
               and is not actually deleted. Note that updating this field does not
               actually change the deployment, just how it is updated.
               Default value is `DELETE`.
               Possible values are `ABANDON` and `DELETE`.
        :param pulumi.Input[str] description: Optional user-provided description of deployment.
        :param pulumi.Input[Sequence[pulumi.Input['DeploymentLabelArgs']]] labels: Key-value pairs to apply to this labels.
               Structure is documented below.
        :param pulumi.Input[str] name: The name of the template to import, as declared in the YAML
               configuration.
        :param pulumi.Input[bool] preview: If set to true, a deployment is created with "shell" resources
               that are not actually instantiated. This allows you to preview a
               deployment. It can be updated to false to actually deploy
               with real resources.
               ~>**NOTE:** Deployment Manager does not allow update
               of a deployment in preview (unless updating to preview=false). Thus,
               the provider will force-recreate deployments if either preview is updated
               to true or if other fields are updated while preview is true.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        """
        pulumi.set(__self__, "target", target)
        if create_policy is not None:
            pulumi.set(__self__, "create_policy", create_policy)
        if delete_policy is not None:
            pulumi.set(__self__, "delete_policy", delete_policy)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if labels is not None:
            pulumi.set(__self__, "labels", labels)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if preview is not None:
            pulumi.set(__self__, "preview", preview)
        if project is not None:
            pulumi.set(__self__, "project", project)

    @property
    @pulumi.getter
    def target(self) -> pulumi.Input['DeploymentTargetArgs']:
        """
        Parameters that define your deployment, including the deployment
        configuration and relevant templates.
        Structure is documented below.
        """
        return pulumi.get(self, "target")

    @target.setter
    def target(self, value: pulumi.Input['DeploymentTargetArgs']):
        pulumi.set(self, "target", value)

    @property
    @pulumi.getter(name="createPolicy")
    def create_policy(self) -> Optional[pulumi.Input[str]]:
        """
        Set the policy to use for creating new resources. Only used on
        create and update. Valid values are `CREATE_OR_ACQUIRE` (default) or
        `ACQUIRE`. If set to `ACQUIRE` and resources do not already exist,
        the deployment will fail. Note that updating this field does not
        actually affect the deployment, just how it is updated.
        Default value is `CREATE_OR_ACQUIRE`.
        Possible values are `ACQUIRE` and `CREATE_OR_ACQUIRE`.
        """
        return pulumi.get(self, "create_policy")

    @create_policy.setter
    def create_policy(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "create_policy", value)

    @property
    @pulumi.getter(name="deletePolicy")
    def delete_policy(self) -> Optional[pulumi.Input[str]]:
        """
        Set the policy to use for deleting new resources on update/delete.
        Valid values are `DELETE` (default) or `ABANDON`. If `DELETE`,
        resource is deleted after removal from Deployment Manager. If
        `ABANDON`, the resource is only removed from Deployment Manager
        and is not actually deleted. Note that updating this field does not
        actually change the deployment, just how it is updated.
        Default value is `DELETE`.
        Possible values are `ABANDON` and `DELETE`.
        """
        return pulumi.get(self, "delete_policy")

    @delete_policy.setter
    def delete_policy(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "delete_policy", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Optional user-provided description of deployment.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def labels(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['DeploymentLabelArgs']]]]:
        """
        Key-value pairs to apply to this labels.
        Structure is documented below.
        """
        return pulumi.get(self, "labels")

    @labels.setter
    def labels(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['DeploymentLabelArgs']]]]):
        pulumi.set(self, "labels", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the template to import, as declared in the YAML
        configuration.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def preview(self) -> Optional[pulumi.Input[bool]]:
        """
        If set to true, a deployment is created with "shell" resources
        that are not actually instantiated. This allows you to preview a
        deployment. It can be updated to false to actually deploy
        with real resources.
        ~>**NOTE:** Deployment Manager does not allow update
        of a deployment in preview (unless updating to preview=false). Thus,
        the provider will force-recreate deployments if either preview is updated
        to true or if other fields are updated while preview is true.
        """
        return pulumi.get(self, "preview")

    @preview.setter
    def preview(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "preview", value)

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
class _DeploymentState:
    def __init__(__self__, *,
                 create_policy: Optional[pulumi.Input[str]] = None,
                 delete_policy: Optional[pulumi.Input[str]] = None,
                 deployment_id: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 labels: Optional[pulumi.Input[Sequence[pulumi.Input['DeploymentLabelArgs']]]] = None,
                 manifest: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 preview: Optional[pulumi.Input[bool]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 self_link: Optional[pulumi.Input[str]] = None,
                 target: Optional[pulumi.Input['DeploymentTargetArgs']] = None):
        """
        Input properties used for looking up and filtering Deployment resources.
        :param pulumi.Input[str] create_policy: Set the policy to use for creating new resources. Only used on
               create and update. Valid values are `CREATE_OR_ACQUIRE` (default) or
               `ACQUIRE`. If set to `ACQUIRE` and resources do not already exist,
               the deployment will fail. Note that updating this field does not
               actually affect the deployment, just how it is updated.
               Default value is `CREATE_OR_ACQUIRE`.
               Possible values are `ACQUIRE` and `CREATE_OR_ACQUIRE`.
        :param pulumi.Input[str] delete_policy: Set the policy to use for deleting new resources on update/delete.
               Valid values are `DELETE` (default) or `ABANDON`. If `DELETE`,
               resource is deleted after removal from Deployment Manager. If
               `ABANDON`, the resource is only removed from Deployment Manager
               and is not actually deleted. Note that updating this field does not
               actually change the deployment, just how it is updated.
               Default value is `DELETE`.
               Possible values are `ABANDON` and `DELETE`.
        :param pulumi.Input[str] deployment_id: Unique identifier for deployment. Output only.
        :param pulumi.Input[str] description: Optional user-provided description of deployment.
        :param pulumi.Input[Sequence[pulumi.Input['DeploymentLabelArgs']]] labels: Key-value pairs to apply to this labels.
               Structure is documented below.
        :param pulumi.Input[str] manifest: Output only. URL of the manifest representing the last manifest that was successfully deployed.
        :param pulumi.Input[str] name: The name of the template to import, as declared in the YAML
               configuration.
        :param pulumi.Input[bool] preview: If set to true, a deployment is created with "shell" resources
               that are not actually instantiated. This allows you to preview a
               deployment. It can be updated to false to actually deploy
               with real resources.
               ~>**NOTE:** Deployment Manager does not allow update
               of a deployment in preview (unless updating to preview=false). Thus,
               the provider will force-recreate deployments if either preview is updated
               to true or if other fields are updated while preview is true.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] self_link: Output only. Server defined URL for the resource.
        :param pulumi.Input['DeploymentTargetArgs'] target: Parameters that define your deployment, including the deployment
               configuration and relevant templates.
               Structure is documented below.
        """
        if create_policy is not None:
            pulumi.set(__self__, "create_policy", create_policy)
        if delete_policy is not None:
            pulumi.set(__self__, "delete_policy", delete_policy)
        if deployment_id is not None:
            pulumi.set(__self__, "deployment_id", deployment_id)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if labels is not None:
            pulumi.set(__self__, "labels", labels)
        if manifest is not None:
            pulumi.set(__self__, "manifest", manifest)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if preview is not None:
            pulumi.set(__self__, "preview", preview)
        if project is not None:
            pulumi.set(__self__, "project", project)
        if self_link is not None:
            pulumi.set(__self__, "self_link", self_link)
        if target is not None:
            pulumi.set(__self__, "target", target)

    @property
    @pulumi.getter(name="createPolicy")
    def create_policy(self) -> Optional[pulumi.Input[str]]:
        """
        Set the policy to use for creating new resources. Only used on
        create and update. Valid values are `CREATE_OR_ACQUIRE` (default) or
        `ACQUIRE`. If set to `ACQUIRE` and resources do not already exist,
        the deployment will fail. Note that updating this field does not
        actually affect the deployment, just how it is updated.
        Default value is `CREATE_OR_ACQUIRE`.
        Possible values are `ACQUIRE` and `CREATE_OR_ACQUIRE`.
        """
        return pulumi.get(self, "create_policy")

    @create_policy.setter
    def create_policy(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "create_policy", value)

    @property
    @pulumi.getter(name="deletePolicy")
    def delete_policy(self) -> Optional[pulumi.Input[str]]:
        """
        Set the policy to use for deleting new resources on update/delete.
        Valid values are `DELETE` (default) or `ABANDON`. If `DELETE`,
        resource is deleted after removal from Deployment Manager. If
        `ABANDON`, the resource is only removed from Deployment Manager
        and is not actually deleted. Note that updating this field does not
        actually change the deployment, just how it is updated.
        Default value is `DELETE`.
        Possible values are `ABANDON` and `DELETE`.
        """
        return pulumi.get(self, "delete_policy")

    @delete_policy.setter
    def delete_policy(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "delete_policy", value)

    @property
    @pulumi.getter(name="deploymentId")
    def deployment_id(self) -> Optional[pulumi.Input[str]]:
        """
        Unique identifier for deployment. Output only.
        """
        return pulumi.get(self, "deployment_id")

    @deployment_id.setter
    def deployment_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "deployment_id", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Optional user-provided description of deployment.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def labels(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['DeploymentLabelArgs']]]]:
        """
        Key-value pairs to apply to this labels.
        Structure is documented below.
        """
        return pulumi.get(self, "labels")

    @labels.setter
    def labels(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['DeploymentLabelArgs']]]]):
        pulumi.set(self, "labels", value)

    @property
    @pulumi.getter
    def manifest(self) -> Optional[pulumi.Input[str]]:
        """
        Output only. URL of the manifest representing the last manifest that was successfully deployed.
        """
        return pulumi.get(self, "manifest")

    @manifest.setter
    def manifest(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "manifest", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the template to import, as declared in the YAML
        configuration.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def preview(self) -> Optional[pulumi.Input[bool]]:
        """
        If set to true, a deployment is created with "shell" resources
        that are not actually instantiated. This allows you to preview a
        deployment. It can be updated to false to actually deploy
        with real resources.
        ~>**NOTE:** Deployment Manager does not allow update
        of a deployment in preview (unless updating to preview=false). Thus,
        the provider will force-recreate deployments if either preview is updated
        to true or if other fields are updated while preview is true.
        """
        return pulumi.get(self, "preview")

    @preview.setter
    def preview(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "preview", value)

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
    @pulumi.getter(name="selfLink")
    def self_link(self) -> Optional[pulumi.Input[str]]:
        """
        Output only. Server defined URL for the resource.
        """
        return pulumi.get(self, "self_link")

    @self_link.setter
    def self_link(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "self_link", value)

    @property
    @pulumi.getter
    def target(self) -> Optional[pulumi.Input['DeploymentTargetArgs']]:
        """
        Parameters that define your deployment, including the deployment
        configuration and relevant templates.
        Structure is documented below.
        """
        return pulumi.get(self, "target")

    @target.setter
    def target(self, value: Optional[pulumi.Input['DeploymentTargetArgs']]):
        pulumi.set(self, "target", value)


class Deployment(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 create_policy: Optional[pulumi.Input[str]] = None,
                 delete_policy: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 labels: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DeploymentLabelArgs']]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 preview: Optional[pulumi.Input[bool]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 target: Optional[pulumi.Input[pulumi.InputType['DeploymentTargetArgs']]] = None,
                 __props__=None):
        """
        A collection of resources that are deployed and managed together using
        a configuration file

        > **Warning:** This resource is intended only to manage a Deployment resource,
        and attempts to manage the Deployment's resources in the provider as well
        will likely result in errors or unexpected behavior as the two tools
        fight over ownership. We strongly discourage doing so unless you are an
        experienced user of both tools.

        In addition, due to limitations of the API, the provider will treat
        deployments in preview as recreate-only for any update operation other
        than actually deploying an in-preview deployment (i.e. `preview=true` to
        `preview=false`).

        ## Example Usage
        ### Deployment Manager Deployment Basic

        ```python
        import pulumi
        import pulumi_gcp as gcp

        deployment = gcp.deploymentmanager.Deployment("deployment",
            target=gcp.deploymentmanager.DeploymentTargetArgs(
                config=gcp.deploymentmanager.DeploymentTargetConfigArgs(
                    content=(lambda path: open(path).read())("path/to/config.yml"),
                ),
            ),
            labels=[gcp.deploymentmanager.DeploymentLabelArgs(
                key="foo",
                value="bar",
            )])
        ```

        ## Import

        Deployment can be imported using any of these accepted formats

        ```sh
         $ pulumi import gcp:deploymentmanager/deployment:Deployment default projects/{{project}}/deployments/{{name}}
        ```

        ```sh
         $ pulumi import gcp:deploymentmanager/deployment:Deployment default {{project}}/{{name}}
        ```

        ```sh
         $ pulumi import gcp:deploymentmanager/deployment:Deployment default {{name}}
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] create_policy: Set the policy to use for creating new resources. Only used on
               create and update. Valid values are `CREATE_OR_ACQUIRE` (default) or
               `ACQUIRE`. If set to `ACQUIRE` and resources do not already exist,
               the deployment will fail. Note that updating this field does not
               actually affect the deployment, just how it is updated.
               Default value is `CREATE_OR_ACQUIRE`.
               Possible values are `ACQUIRE` and `CREATE_OR_ACQUIRE`.
        :param pulumi.Input[str] delete_policy: Set the policy to use for deleting new resources on update/delete.
               Valid values are `DELETE` (default) or `ABANDON`. If `DELETE`,
               resource is deleted after removal from Deployment Manager. If
               `ABANDON`, the resource is only removed from Deployment Manager
               and is not actually deleted. Note that updating this field does not
               actually change the deployment, just how it is updated.
               Default value is `DELETE`.
               Possible values are `ABANDON` and `DELETE`.
        :param pulumi.Input[str] description: Optional user-provided description of deployment.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DeploymentLabelArgs']]]] labels: Key-value pairs to apply to this labels.
               Structure is documented below.
        :param pulumi.Input[str] name: The name of the template to import, as declared in the YAML
               configuration.
        :param pulumi.Input[bool] preview: If set to true, a deployment is created with "shell" resources
               that are not actually instantiated. This allows you to preview a
               deployment. It can be updated to false to actually deploy
               with real resources.
               ~>**NOTE:** Deployment Manager does not allow update
               of a deployment in preview (unless updating to preview=false). Thus,
               the provider will force-recreate deployments if either preview is updated
               to true or if other fields are updated while preview is true.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[pulumi.InputType['DeploymentTargetArgs']] target: Parameters that define your deployment, including the deployment
               configuration and relevant templates.
               Structure is documented below.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: DeploymentArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        A collection of resources that are deployed and managed together using
        a configuration file

        > **Warning:** This resource is intended only to manage a Deployment resource,
        and attempts to manage the Deployment's resources in the provider as well
        will likely result in errors or unexpected behavior as the two tools
        fight over ownership. We strongly discourage doing so unless you are an
        experienced user of both tools.

        In addition, due to limitations of the API, the provider will treat
        deployments in preview as recreate-only for any update operation other
        than actually deploying an in-preview deployment (i.e. `preview=true` to
        `preview=false`).

        ## Example Usage
        ### Deployment Manager Deployment Basic

        ```python
        import pulumi
        import pulumi_gcp as gcp

        deployment = gcp.deploymentmanager.Deployment("deployment",
            target=gcp.deploymentmanager.DeploymentTargetArgs(
                config=gcp.deploymentmanager.DeploymentTargetConfigArgs(
                    content=(lambda path: open(path).read())("path/to/config.yml"),
                ),
            ),
            labels=[gcp.deploymentmanager.DeploymentLabelArgs(
                key="foo",
                value="bar",
            )])
        ```

        ## Import

        Deployment can be imported using any of these accepted formats

        ```sh
         $ pulumi import gcp:deploymentmanager/deployment:Deployment default projects/{{project}}/deployments/{{name}}
        ```

        ```sh
         $ pulumi import gcp:deploymentmanager/deployment:Deployment default {{project}}/{{name}}
        ```

        ```sh
         $ pulumi import gcp:deploymentmanager/deployment:Deployment default {{name}}
        ```

        :param str resource_name: The name of the resource.
        :param DeploymentArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(DeploymentArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 create_policy: Optional[pulumi.Input[str]] = None,
                 delete_policy: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 labels: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DeploymentLabelArgs']]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 preview: Optional[pulumi.Input[bool]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 target: Optional[pulumi.Input[pulumi.InputType['DeploymentTargetArgs']]] = None,
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
            __props__ = DeploymentArgs.__new__(DeploymentArgs)

            __props__.__dict__["create_policy"] = create_policy
            __props__.__dict__["delete_policy"] = delete_policy
            __props__.__dict__["description"] = description
            __props__.__dict__["labels"] = labels
            __props__.__dict__["name"] = name
            __props__.__dict__["preview"] = preview
            __props__.__dict__["project"] = project
            if target is None and not opts.urn:
                raise TypeError("Missing required property 'target'")
            __props__.__dict__["target"] = target
            __props__.__dict__["deployment_id"] = None
            __props__.__dict__["manifest"] = None
            __props__.__dict__["self_link"] = None
        super(Deployment, __self__).__init__(
            'gcp:deploymentmanager/deployment:Deployment',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            create_policy: Optional[pulumi.Input[str]] = None,
            delete_policy: Optional[pulumi.Input[str]] = None,
            deployment_id: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            labels: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DeploymentLabelArgs']]]]] = None,
            manifest: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            preview: Optional[pulumi.Input[bool]] = None,
            project: Optional[pulumi.Input[str]] = None,
            self_link: Optional[pulumi.Input[str]] = None,
            target: Optional[pulumi.Input[pulumi.InputType['DeploymentTargetArgs']]] = None) -> 'Deployment':
        """
        Get an existing Deployment resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] create_policy: Set the policy to use for creating new resources. Only used on
               create and update. Valid values are `CREATE_OR_ACQUIRE` (default) or
               `ACQUIRE`. If set to `ACQUIRE` and resources do not already exist,
               the deployment will fail. Note that updating this field does not
               actually affect the deployment, just how it is updated.
               Default value is `CREATE_OR_ACQUIRE`.
               Possible values are `ACQUIRE` and `CREATE_OR_ACQUIRE`.
        :param pulumi.Input[str] delete_policy: Set the policy to use for deleting new resources on update/delete.
               Valid values are `DELETE` (default) or `ABANDON`. If `DELETE`,
               resource is deleted after removal from Deployment Manager. If
               `ABANDON`, the resource is only removed from Deployment Manager
               and is not actually deleted. Note that updating this field does not
               actually change the deployment, just how it is updated.
               Default value is `DELETE`.
               Possible values are `ABANDON` and `DELETE`.
        :param pulumi.Input[str] deployment_id: Unique identifier for deployment. Output only.
        :param pulumi.Input[str] description: Optional user-provided description of deployment.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DeploymentLabelArgs']]]] labels: Key-value pairs to apply to this labels.
               Structure is documented below.
        :param pulumi.Input[str] manifest: Output only. URL of the manifest representing the last manifest that was successfully deployed.
        :param pulumi.Input[str] name: The name of the template to import, as declared in the YAML
               configuration.
        :param pulumi.Input[bool] preview: If set to true, a deployment is created with "shell" resources
               that are not actually instantiated. This allows you to preview a
               deployment. It can be updated to false to actually deploy
               with real resources.
               ~>**NOTE:** Deployment Manager does not allow update
               of a deployment in preview (unless updating to preview=false). Thus,
               the provider will force-recreate deployments if either preview is updated
               to true or if other fields are updated while preview is true.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] self_link: Output only. Server defined URL for the resource.
        :param pulumi.Input[pulumi.InputType['DeploymentTargetArgs']] target: Parameters that define your deployment, including the deployment
               configuration and relevant templates.
               Structure is documented below.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _DeploymentState.__new__(_DeploymentState)

        __props__.__dict__["create_policy"] = create_policy
        __props__.__dict__["delete_policy"] = delete_policy
        __props__.__dict__["deployment_id"] = deployment_id
        __props__.__dict__["description"] = description
        __props__.__dict__["labels"] = labels
        __props__.__dict__["manifest"] = manifest
        __props__.__dict__["name"] = name
        __props__.__dict__["preview"] = preview
        __props__.__dict__["project"] = project
        __props__.__dict__["self_link"] = self_link
        __props__.__dict__["target"] = target
        return Deployment(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="createPolicy")
    def create_policy(self) -> pulumi.Output[Optional[str]]:
        """
        Set the policy to use for creating new resources. Only used on
        create and update. Valid values are `CREATE_OR_ACQUIRE` (default) or
        `ACQUIRE`. If set to `ACQUIRE` and resources do not already exist,
        the deployment will fail. Note that updating this field does not
        actually affect the deployment, just how it is updated.
        Default value is `CREATE_OR_ACQUIRE`.
        Possible values are `ACQUIRE` and `CREATE_OR_ACQUIRE`.
        """
        return pulumi.get(self, "create_policy")

    @property
    @pulumi.getter(name="deletePolicy")
    def delete_policy(self) -> pulumi.Output[Optional[str]]:
        """
        Set the policy to use for deleting new resources on update/delete.
        Valid values are `DELETE` (default) or `ABANDON`. If `DELETE`,
        resource is deleted after removal from Deployment Manager. If
        `ABANDON`, the resource is only removed from Deployment Manager
        and is not actually deleted. Note that updating this field does not
        actually change the deployment, just how it is updated.
        Default value is `DELETE`.
        Possible values are `ABANDON` and `DELETE`.
        """
        return pulumi.get(self, "delete_policy")

    @property
    @pulumi.getter(name="deploymentId")
    def deployment_id(self) -> pulumi.Output[str]:
        """
        Unique identifier for deployment. Output only.
        """
        return pulumi.get(self, "deployment_id")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        Optional user-provided description of deployment.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def labels(self) -> pulumi.Output[Optional[Sequence['outputs.DeploymentLabel']]]:
        """
        Key-value pairs to apply to this labels.
        Structure is documented below.
        """
        return pulumi.get(self, "labels")

    @property
    @pulumi.getter
    def manifest(self) -> pulumi.Output[str]:
        """
        Output only. URL of the manifest representing the last manifest that was successfully deployed.
        """
        return pulumi.get(self, "manifest")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the template to import, as declared in the YAML
        configuration.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def preview(self) -> pulumi.Output[Optional[bool]]:
        """
        If set to true, a deployment is created with "shell" resources
        that are not actually instantiated. This allows you to preview a
        deployment. It can be updated to false to actually deploy
        with real resources.
        ~>**NOTE:** Deployment Manager does not allow update
        of a deployment in preview (unless updating to preview=false). Thus,
        the provider will force-recreate deployments if either preview is updated
        to true or if other fields are updated while preview is true.
        """
        return pulumi.get(self, "preview")

    @property
    @pulumi.getter
    def project(self) -> pulumi.Output[str]:
        """
        The ID of the project in which the resource belongs.
        If it is not provided, the provider project is used.
        """
        return pulumi.get(self, "project")

    @property
    @pulumi.getter(name="selfLink")
    def self_link(self) -> pulumi.Output[str]:
        """
        Output only. Server defined URL for the resource.
        """
        return pulumi.get(self, "self_link")

    @property
    @pulumi.getter
    def target(self) -> pulumi.Output['outputs.DeploymentTarget']:
        """
        Parameters that define your deployment, including the deployment
        configuration and relevant templates.
        Structure is documented below.
        """
        return pulumi.get(self, "target")

