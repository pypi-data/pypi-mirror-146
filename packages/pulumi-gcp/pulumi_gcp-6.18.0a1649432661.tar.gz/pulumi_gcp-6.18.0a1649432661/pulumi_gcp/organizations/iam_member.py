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

__all__ = ['IAMMemberArgs', 'IAMMember']

@pulumi.input_type
class IAMMemberArgs:
    def __init__(__self__, *,
                 member: pulumi.Input[str],
                 org_id: pulumi.Input[str],
                 role: pulumi.Input[str],
                 condition: Optional[pulumi.Input['IAMMemberConditionArgs']] = None):
        """
        The set of arguments for constructing a IAMMember resource.
        :param pulumi.Input[str] org_id: The organization ID. If not specified for `organizations.IAMBinding`, `organizations.IAMMember`, or `organizations.IamAuditConfig`, uses the ID of the organization configured with the provider.
               Required for `organizations.IAMPolicy` - you must explicitly set the organization, and it
               will not be inferred from the provider.
        :param pulumi.Input[str] role: The role that should be applied. Only one
               `organizations.IAMBinding` can be used per role. Note that custom roles must be of the format
               `organizations/{{org_id}}/roles/{{role_id}}`.
        :param pulumi.Input['IAMMemberConditionArgs'] condition: An [IAM Condition](https://cloud.google.com/iam/docs/conditions-overview) for a given binding.
               Structure is documented below.
        """
        pulumi.set(__self__, "member", member)
        pulumi.set(__self__, "org_id", org_id)
        pulumi.set(__self__, "role", role)
        if condition is not None:
            pulumi.set(__self__, "condition", condition)

    @property
    @pulumi.getter
    def member(self) -> pulumi.Input[str]:
        return pulumi.get(self, "member")

    @member.setter
    def member(self, value: pulumi.Input[str]):
        pulumi.set(self, "member", value)

    @property
    @pulumi.getter(name="orgId")
    def org_id(self) -> pulumi.Input[str]:
        """
        The organization ID. If not specified for `organizations.IAMBinding`, `organizations.IAMMember`, or `organizations.IamAuditConfig`, uses the ID of the organization configured with the provider.
        Required for `organizations.IAMPolicy` - you must explicitly set the organization, and it
        will not be inferred from the provider.
        """
        return pulumi.get(self, "org_id")

    @org_id.setter
    def org_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "org_id", value)

    @property
    @pulumi.getter
    def role(self) -> pulumi.Input[str]:
        """
        The role that should be applied. Only one
        `organizations.IAMBinding` can be used per role. Note that custom roles must be of the format
        `organizations/{{org_id}}/roles/{{role_id}}`.
        """
        return pulumi.get(self, "role")

    @role.setter
    def role(self, value: pulumi.Input[str]):
        pulumi.set(self, "role", value)

    @property
    @pulumi.getter
    def condition(self) -> Optional[pulumi.Input['IAMMemberConditionArgs']]:
        """
        An [IAM Condition](https://cloud.google.com/iam/docs/conditions-overview) for a given binding.
        Structure is documented below.
        """
        return pulumi.get(self, "condition")

    @condition.setter
    def condition(self, value: Optional[pulumi.Input['IAMMemberConditionArgs']]):
        pulumi.set(self, "condition", value)


@pulumi.input_type
class _IAMMemberState:
    def __init__(__self__, *,
                 condition: Optional[pulumi.Input['IAMMemberConditionArgs']] = None,
                 etag: Optional[pulumi.Input[str]] = None,
                 member: Optional[pulumi.Input[str]] = None,
                 org_id: Optional[pulumi.Input[str]] = None,
                 role: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering IAMMember resources.
        :param pulumi.Input['IAMMemberConditionArgs'] condition: An [IAM Condition](https://cloud.google.com/iam/docs/conditions-overview) for a given binding.
               Structure is documented below.
        :param pulumi.Input[str] etag: (Computed) The etag of the organization's IAM policy.
        :param pulumi.Input[str] org_id: The organization ID. If not specified for `organizations.IAMBinding`, `organizations.IAMMember`, or `organizations.IamAuditConfig`, uses the ID of the organization configured with the provider.
               Required for `organizations.IAMPolicy` - you must explicitly set the organization, and it
               will not be inferred from the provider.
        :param pulumi.Input[str] role: The role that should be applied. Only one
               `organizations.IAMBinding` can be used per role. Note that custom roles must be of the format
               `organizations/{{org_id}}/roles/{{role_id}}`.
        """
        if condition is not None:
            pulumi.set(__self__, "condition", condition)
        if etag is not None:
            pulumi.set(__self__, "etag", etag)
        if member is not None:
            pulumi.set(__self__, "member", member)
        if org_id is not None:
            pulumi.set(__self__, "org_id", org_id)
        if role is not None:
            pulumi.set(__self__, "role", role)

    @property
    @pulumi.getter
    def condition(self) -> Optional[pulumi.Input['IAMMemberConditionArgs']]:
        """
        An [IAM Condition](https://cloud.google.com/iam/docs/conditions-overview) for a given binding.
        Structure is documented below.
        """
        return pulumi.get(self, "condition")

    @condition.setter
    def condition(self, value: Optional[pulumi.Input['IAMMemberConditionArgs']]):
        pulumi.set(self, "condition", value)

    @property
    @pulumi.getter
    def etag(self) -> Optional[pulumi.Input[str]]:
        """
        (Computed) The etag of the organization's IAM policy.
        """
        return pulumi.get(self, "etag")

    @etag.setter
    def etag(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "etag", value)

    @property
    @pulumi.getter
    def member(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "member")

    @member.setter
    def member(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "member", value)

    @property
    @pulumi.getter(name="orgId")
    def org_id(self) -> Optional[pulumi.Input[str]]:
        """
        The organization ID. If not specified for `organizations.IAMBinding`, `organizations.IAMMember`, or `organizations.IamAuditConfig`, uses the ID of the organization configured with the provider.
        Required for `organizations.IAMPolicy` - you must explicitly set the organization, and it
        will not be inferred from the provider.
        """
        return pulumi.get(self, "org_id")

    @org_id.setter
    def org_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "org_id", value)

    @property
    @pulumi.getter
    def role(self) -> Optional[pulumi.Input[str]]:
        """
        The role that should be applied. Only one
        `organizations.IAMBinding` can be used per role. Note that custom roles must be of the format
        `organizations/{{org_id}}/roles/{{role_id}}`.
        """
        return pulumi.get(self, "role")

    @role.setter
    def role(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "role", value)


class IAMMember(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 condition: Optional[pulumi.Input[pulumi.InputType['IAMMemberConditionArgs']]] = None,
                 member: Optional[pulumi.Input[str]] = None,
                 org_id: Optional[pulumi.Input[str]] = None,
                 role: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Four different resources help you manage your IAM policy for a organization. Each of these resources serves a different use case:

        * `organizations.IAMPolicy`: Authoritative. Sets the IAM policy for the organization and replaces any existing policy already attached.
        * `organizations.IAMBinding`: Authoritative for a given role. Updates the IAM policy to grant a role to a list of members. Other roles within the IAM policy for the organization are preserved.
        * `organizations.IAMMember`: Non-authoritative. Updates the IAM policy to grant a role to a new member. Other members for the role for the organization are preserved.
        * `organizations.IamAuditConfig`: Authoritative for a given service. Updates the IAM policy to enable audit logging for the given service.

        > **Note:** `organizations.IAMPolicy` **cannot** be used in conjunction with `organizations.IAMBinding`, `organizations.IAMMember`, or `organizations.IamAuditConfig` or they will fight over what your policy should be.

        > **Note:** `organizations.IAMBinding` resources **can be** used in conjunction with `organizations.IAMMember` resources **only if** they do not grant privilege to the same role.

        ## google\_organization\_iam\_policy

        !> **Warning:** New organizations have several default policies which will,
           without extreme caution, be **overwritten** by use of this resource.
           The safest alternative is to use multiple `organizations.IAMBinding`
           resources. This resource makes it easy to remove your own access to
           an organization, which will require a call to Google Support to have
           fixed, and can take multiple days to resolve.

           In general, this resource should only be used with organizations
           fully managed by this provider.I f you do use this resource,
           the best way to be sure that you are not making dangerous changes is to start
           by **importing** your existing policy, and examining the diff very closely.

        ```python
        import pulumi
        import pulumi_gcp as gcp

        admin = gcp.organizations.get_iam_policy(bindings=[gcp.organizations.GetIAMPolicyBindingArgs(
            role="roles/editor",
            members=["user:jane@example.com"],
        )])
        organization = gcp.organizations.IAMPolicy("organization",
            org_id="your-organization-id",
            policy_data=admin.policy_data)
        ```

        With IAM Conditions:

        ```python
        import pulumi
        import pulumi_gcp as gcp

        admin = gcp.organizations.get_iam_policy(bindings=[gcp.organizations.GetIAMPolicyBindingArgs(
            condition=gcp.organizations.GetIAMPolicyBindingConditionArgs(
                description="Expiring at midnight of 2019-12-31",
                expression="request.time < timestamp(\"2020-01-01T00:00:00Z\")",
                title="expires_after_2019_12_31",
            ),
            members=["user:jane@example.com"],
            role="roles/editor",
        )])
        organization = gcp.organizations.IAMPolicy("organization",
            org_id="your-organization-id",
            policy_data=admin.policy_data)
        ```

        ## google\_organization\_iam\_binding

        > **Note:** If `role` is set to `roles/owner` and you don't specify a user or service account you have access to in `members`, you can lock yourself out of your organization.

        ```python
        import pulumi
        import pulumi_gcp as gcp

        organization = gcp.organizations.IAMBinding("organization",
            members=["user:jane@example.com"],
            org_id="your-organization-id",
            role="roles/editor")
        ```

        With IAM Conditions:

        ```python
        import pulumi
        import pulumi_gcp as gcp

        organization = gcp.organizations.IAMBinding("organization",
            condition=gcp.organizations.IAMBindingConditionArgs(
                description="Expiring at midnight of 2019-12-31",
                expression="request.time < timestamp(\"2020-01-01T00:00:00Z\")",
                title="expires_after_2019_12_31",
            ),
            members=["user:jane@example.com"],
            org_id="your-organization-id",
            role="roles/editor")
        ```

        ## google\_organization\_iam\_member

        ```python
        import pulumi
        import pulumi_gcp as gcp

        organization = gcp.organizations.IAMMember("organization",
            member="user:jane@example.com",
            org_id="your-organization-id",
            role="roles/editor")
        ```

        With IAM Conditions:

        ```python
        import pulumi
        import pulumi_gcp as gcp

        organization = gcp.organizations.IAMMember("organization",
            condition=gcp.organizations.IAMMemberConditionArgs(
                description="Expiring at midnight of 2019-12-31",
                expression="request.time < timestamp(\"2020-01-01T00:00:00Z\")",
                title="expires_after_2019_12_31",
            ),
            member="user:jane@example.com",
            org_id="your-organization-id",
            role="roles/editor")
        ```

        ## google\_organization\_iam\_audit\_config

        ```python
        import pulumi
        import pulumi_gcp as gcp

        organization = gcp.organizations.IamAuditConfig("organization",
            audit_log_configs=[
                gcp.organizations.IamAuditConfigAuditLogConfigArgs(
                    log_type="ADMIN_READ",
                ),
                gcp.organizations.IamAuditConfigAuditLogConfigArgs(
                    exempted_members=["user:joebloggs@hashicorp.com"],
                    log_type="DATA_READ",
                ),
            ],
            org_id="your-organization-id",
            service="allServices")
        ```

        ## Import

        IAM member imports use space-delimited identifiers; the resource in question, the role, and the account.

        This member resource can be imported using the `org_id`, role, and member e.g.

        ```sh
         $ pulumi import gcp:organizations/iAMMember:IAMMember my_organization "your-orgid roles/viewer user:foo@example.com"
        ```

         IAM binding imports use space-delimited identifiers; the resource in question and the role.

        This binding resource can be imported using the `org_id` and role, e.g.

        ```sh
         $ pulumi import gcp:organizations/iAMMember:IAMMember my_organization "your-org-id roles/viewer"
        ```

         IAM policy imports use the identifier of the resource in question.

        This policy resource can be imported using the `org_id`.

        ```sh
         $ pulumi import gcp:organizations/iAMMember:IAMMember my_organization your-org-id
        ```

         IAM audit config imports use the identifier of the resource in question and the service, e.g.

        ```sh
         $ pulumi import gcp:organizations/iAMMember:IAMMember my_organization "your-organization-id foo.googleapis.com"
        ```

         -> **Custom Roles**If you're importing a IAM resource with a custom role, make sure to use the

        full name of the custom role, e.g. `organizations/{{org_id}}/roles/{{role_id}}`.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['IAMMemberConditionArgs']] condition: An [IAM Condition](https://cloud.google.com/iam/docs/conditions-overview) for a given binding.
               Structure is documented below.
        :param pulumi.Input[str] org_id: The organization ID. If not specified for `organizations.IAMBinding`, `organizations.IAMMember`, or `organizations.IamAuditConfig`, uses the ID of the organization configured with the provider.
               Required for `organizations.IAMPolicy` - you must explicitly set the organization, and it
               will not be inferred from the provider.
        :param pulumi.Input[str] role: The role that should be applied. Only one
               `organizations.IAMBinding` can be used per role. Note that custom roles must be of the format
               `organizations/{{org_id}}/roles/{{role_id}}`.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: IAMMemberArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Four different resources help you manage your IAM policy for a organization. Each of these resources serves a different use case:

        * `organizations.IAMPolicy`: Authoritative. Sets the IAM policy for the organization and replaces any existing policy already attached.
        * `organizations.IAMBinding`: Authoritative for a given role. Updates the IAM policy to grant a role to a list of members. Other roles within the IAM policy for the organization are preserved.
        * `organizations.IAMMember`: Non-authoritative. Updates the IAM policy to grant a role to a new member. Other members for the role for the organization are preserved.
        * `organizations.IamAuditConfig`: Authoritative for a given service. Updates the IAM policy to enable audit logging for the given service.

        > **Note:** `organizations.IAMPolicy` **cannot** be used in conjunction with `organizations.IAMBinding`, `organizations.IAMMember`, or `organizations.IamAuditConfig` or they will fight over what your policy should be.

        > **Note:** `organizations.IAMBinding` resources **can be** used in conjunction with `organizations.IAMMember` resources **only if** they do not grant privilege to the same role.

        ## google\_organization\_iam\_policy

        !> **Warning:** New organizations have several default policies which will,
           without extreme caution, be **overwritten** by use of this resource.
           The safest alternative is to use multiple `organizations.IAMBinding`
           resources. This resource makes it easy to remove your own access to
           an organization, which will require a call to Google Support to have
           fixed, and can take multiple days to resolve.

           In general, this resource should only be used with organizations
           fully managed by this provider.I f you do use this resource,
           the best way to be sure that you are not making dangerous changes is to start
           by **importing** your existing policy, and examining the diff very closely.

        ```python
        import pulumi
        import pulumi_gcp as gcp

        admin = gcp.organizations.get_iam_policy(bindings=[gcp.organizations.GetIAMPolicyBindingArgs(
            role="roles/editor",
            members=["user:jane@example.com"],
        )])
        organization = gcp.organizations.IAMPolicy("organization",
            org_id="your-organization-id",
            policy_data=admin.policy_data)
        ```

        With IAM Conditions:

        ```python
        import pulumi
        import pulumi_gcp as gcp

        admin = gcp.organizations.get_iam_policy(bindings=[gcp.organizations.GetIAMPolicyBindingArgs(
            condition=gcp.organizations.GetIAMPolicyBindingConditionArgs(
                description="Expiring at midnight of 2019-12-31",
                expression="request.time < timestamp(\"2020-01-01T00:00:00Z\")",
                title="expires_after_2019_12_31",
            ),
            members=["user:jane@example.com"],
            role="roles/editor",
        )])
        organization = gcp.organizations.IAMPolicy("organization",
            org_id="your-organization-id",
            policy_data=admin.policy_data)
        ```

        ## google\_organization\_iam\_binding

        > **Note:** If `role` is set to `roles/owner` and you don't specify a user or service account you have access to in `members`, you can lock yourself out of your organization.

        ```python
        import pulumi
        import pulumi_gcp as gcp

        organization = gcp.organizations.IAMBinding("organization",
            members=["user:jane@example.com"],
            org_id="your-organization-id",
            role="roles/editor")
        ```

        With IAM Conditions:

        ```python
        import pulumi
        import pulumi_gcp as gcp

        organization = gcp.organizations.IAMBinding("organization",
            condition=gcp.organizations.IAMBindingConditionArgs(
                description="Expiring at midnight of 2019-12-31",
                expression="request.time < timestamp(\"2020-01-01T00:00:00Z\")",
                title="expires_after_2019_12_31",
            ),
            members=["user:jane@example.com"],
            org_id="your-organization-id",
            role="roles/editor")
        ```

        ## google\_organization\_iam\_member

        ```python
        import pulumi
        import pulumi_gcp as gcp

        organization = gcp.organizations.IAMMember("organization",
            member="user:jane@example.com",
            org_id="your-organization-id",
            role="roles/editor")
        ```

        With IAM Conditions:

        ```python
        import pulumi
        import pulumi_gcp as gcp

        organization = gcp.organizations.IAMMember("organization",
            condition=gcp.organizations.IAMMemberConditionArgs(
                description="Expiring at midnight of 2019-12-31",
                expression="request.time < timestamp(\"2020-01-01T00:00:00Z\")",
                title="expires_after_2019_12_31",
            ),
            member="user:jane@example.com",
            org_id="your-organization-id",
            role="roles/editor")
        ```

        ## google\_organization\_iam\_audit\_config

        ```python
        import pulumi
        import pulumi_gcp as gcp

        organization = gcp.organizations.IamAuditConfig("organization",
            audit_log_configs=[
                gcp.organizations.IamAuditConfigAuditLogConfigArgs(
                    log_type="ADMIN_READ",
                ),
                gcp.organizations.IamAuditConfigAuditLogConfigArgs(
                    exempted_members=["user:joebloggs@hashicorp.com"],
                    log_type="DATA_READ",
                ),
            ],
            org_id="your-organization-id",
            service="allServices")
        ```

        ## Import

        IAM member imports use space-delimited identifiers; the resource in question, the role, and the account.

        This member resource can be imported using the `org_id`, role, and member e.g.

        ```sh
         $ pulumi import gcp:organizations/iAMMember:IAMMember my_organization "your-orgid roles/viewer user:foo@example.com"
        ```

         IAM binding imports use space-delimited identifiers; the resource in question and the role.

        This binding resource can be imported using the `org_id` and role, e.g.

        ```sh
         $ pulumi import gcp:organizations/iAMMember:IAMMember my_organization "your-org-id roles/viewer"
        ```

         IAM policy imports use the identifier of the resource in question.

        This policy resource can be imported using the `org_id`.

        ```sh
         $ pulumi import gcp:organizations/iAMMember:IAMMember my_organization your-org-id
        ```

         IAM audit config imports use the identifier of the resource in question and the service, e.g.

        ```sh
         $ pulumi import gcp:organizations/iAMMember:IAMMember my_organization "your-organization-id foo.googleapis.com"
        ```

         -> **Custom Roles**If you're importing a IAM resource with a custom role, make sure to use the

        full name of the custom role, e.g. `organizations/{{org_id}}/roles/{{role_id}}`.

        :param str resource_name: The name of the resource.
        :param IAMMemberArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(IAMMemberArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 condition: Optional[pulumi.Input[pulumi.InputType['IAMMemberConditionArgs']]] = None,
                 member: Optional[pulumi.Input[str]] = None,
                 org_id: Optional[pulumi.Input[str]] = None,
                 role: Optional[pulumi.Input[str]] = None,
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
            __props__ = IAMMemberArgs.__new__(IAMMemberArgs)

            __props__.__dict__["condition"] = condition
            if member is None and not opts.urn:
                raise TypeError("Missing required property 'member'")
            __props__.__dict__["member"] = member
            if org_id is None and not opts.urn:
                raise TypeError("Missing required property 'org_id'")
            __props__.__dict__["org_id"] = org_id
            if role is None and not opts.urn:
                raise TypeError("Missing required property 'role'")
            __props__.__dict__["role"] = role
            __props__.__dict__["etag"] = None
        super(IAMMember, __self__).__init__(
            'gcp:organizations/iAMMember:IAMMember',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            condition: Optional[pulumi.Input[pulumi.InputType['IAMMemberConditionArgs']]] = None,
            etag: Optional[pulumi.Input[str]] = None,
            member: Optional[pulumi.Input[str]] = None,
            org_id: Optional[pulumi.Input[str]] = None,
            role: Optional[pulumi.Input[str]] = None) -> 'IAMMember':
        """
        Get an existing IAMMember resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['IAMMemberConditionArgs']] condition: An [IAM Condition](https://cloud.google.com/iam/docs/conditions-overview) for a given binding.
               Structure is documented below.
        :param pulumi.Input[str] etag: (Computed) The etag of the organization's IAM policy.
        :param pulumi.Input[str] org_id: The organization ID. If not specified for `organizations.IAMBinding`, `organizations.IAMMember`, or `organizations.IamAuditConfig`, uses the ID of the organization configured with the provider.
               Required for `organizations.IAMPolicy` - you must explicitly set the organization, and it
               will not be inferred from the provider.
        :param pulumi.Input[str] role: The role that should be applied. Only one
               `organizations.IAMBinding` can be used per role. Note that custom roles must be of the format
               `organizations/{{org_id}}/roles/{{role_id}}`.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _IAMMemberState.__new__(_IAMMemberState)

        __props__.__dict__["condition"] = condition
        __props__.__dict__["etag"] = etag
        __props__.__dict__["member"] = member
        __props__.__dict__["org_id"] = org_id
        __props__.__dict__["role"] = role
        return IAMMember(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def condition(self) -> pulumi.Output[Optional['outputs.IAMMemberCondition']]:
        """
        An [IAM Condition](https://cloud.google.com/iam/docs/conditions-overview) for a given binding.
        Structure is documented below.
        """
        return pulumi.get(self, "condition")

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[str]:
        """
        (Computed) The etag of the organization's IAM policy.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def member(self) -> pulumi.Output[str]:
        return pulumi.get(self, "member")

    @property
    @pulumi.getter(name="orgId")
    def org_id(self) -> pulumi.Output[str]:
        """
        The organization ID. If not specified for `organizations.IAMBinding`, `organizations.IAMMember`, or `organizations.IamAuditConfig`, uses the ID of the organization configured with the provider.
        Required for `organizations.IAMPolicy` - you must explicitly set the organization, and it
        will not be inferred from the provider.
        """
        return pulumi.get(self, "org_id")

    @property
    @pulumi.getter
    def role(self) -> pulumi.Output[str]:
        """
        The role that should be applied. Only one
        `organizations.IAMBinding` can be used per role. Note that custom roles must be of the format
        `organizations/{{org_id}}/roles/{{role_id}}`.
        """
        return pulumi.get(self, "role")

