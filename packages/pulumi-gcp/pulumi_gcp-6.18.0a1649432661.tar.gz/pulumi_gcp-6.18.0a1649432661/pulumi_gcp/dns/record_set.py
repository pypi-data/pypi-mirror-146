# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['RecordSetArgs', 'RecordSet']

@pulumi.input_type
class RecordSetArgs:
    def __init__(__self__, *,
                 managed_zone: pulumi.Input[str],
                 name: pulumi.Input[str],
                 rrdatas: pulumi.Input[Sequence[pulumi.Input[str]]],
                 type: pulumi.Input[str],
                 project: Optional[pulumi.Input[str]] = None,
                 ttl: Optional[pulumi.Input[int]] = None):
        """
        The set of arguments for constructing a RecordSet resource.
        :param pulumi.Input[str] managed_zone: The name of the zone in which this record set will
               reside.
        :param pulumi.Input[str] name: The DNS name this record set will apply to.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] rrdatas: The string data for the records in this record set whose meaning depends on the DNS type. For TXT record, if the string
               data contains spaces, add surrounding \" if you don't want your string to get split on spaces. To specify a single
               record value longer than 255 characters such as a TXT record for DKIM, add \"\" inside the Terraform configuration
               string (e.g. "first255characters\"\"morecharacters").
        :param pulumi.Input[str] type: The DNS record set type.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs. If it
               is not provided, the provider project is used.
        :param pulumi.Input[int] ttl: The time-to-live of this record set (seconds).
        """
        pulumi.set(__self__, "managed_zone", managed_zone)
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "rrdatas", rrdatas)
        pulumi.set(__self__, "type", type)
        if project is not None:
            pulumi.set(__self__, "project", project)
        if ttl is not None:
            pulumi.set(__self__, "ttl", ttl)

    @property
    @pulumi.getter(name="managedZone")
    def managed_zone(self) -> pulumi.Input[str]:
        """
        The name of the zone in which this record set will
        reside.
        """
        return pulumi.get(self, "managed_zone")

    @managed_zone.setter
    def managed_zone(self, value: pulumi.Input[str]):
        pulumi.set(self, "managed_zone", value)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        The DNS name this record set will apply to.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def rrdatas(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        The string data for the records in this record set whose meaning depends on the DNS type. For TXT record, if the string
        data contains spaces, add surrounding \" if you don't want your string to get split on spaces. To specify a single
        record value longer than 255 characters such as a TXT record for DKIM, add \"\" inside the Terraform configuration
        string (e.g. "first255characters\"\"morecharacters").
        """
        return pulumi.get(self, "rrdatas")

    @rrdatas.setter
    def rrdatas(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "rrdatas", value)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input[str]:
        """
        The DNS record set type.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: pulumi.Input[str]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter
    def project(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the project in which the resource belongs. If it
        is not provided, the provider project is used.
        """
        return pulumi.get(self, "project")

    @project.setter
    def project(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "project", value)

    @property
    @pulumi.getter
    def ttl(self) -> Optional[pulumi.Input[int]]:
        """
        The time-to-live of this record set (seconds).
        """
        return pulumi.get(self, "ttl")

    @ttl.setter
    def ttl(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "ttl", value)


@pulumi.input_type
class _RecordSetState:
    def __init__(__self__, *,
                 managed_zone: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 rrdatas: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 ttl: Optional[pulumi.Input[int]] = None,
                 type: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering RecordSet resources.
        :param pulumi.Input[str] managed_zone: The name of the zone in which this record set will
               reside.
        :param pulumi.Input[str] name: The DNS name this record set will apply to.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs. If it
               is not provided, the provider project is used.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] rrdatas: The string data for the records in this record set whose meaning depends on the DNS type. For TXT record, if the string
               data contains spaces, add surrounding \" if you don't want your string to get split on spaces. To specify a single
               record value longer than 255 characters such as a TXT record for DKIM, add \"\" inside the Terraform configuration
               string (e.g. "first255characters\"\"morecharacters").
        :param pulumi.Input[int] ttl: The time-to-live of this record set (seconds).
        :param pulumi.Input[str] type: The DNS record set type.
        """
        if managed_zone is not None:
            pulumi.set(__self__, "managed_zone", managed_zone)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if project is not None:
            pulumi.set(__self__, "project", project)
        if rrdatas is not None:
            pulumi.set(__self__, "rrdatas", rrdatas)
        if ttl is not None:
            pulumi.set(__self__, "ttl", ttl)
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="managedZone")
    def managed_zone(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the zone in which this record set will
        reside.
        """
        return pulumi.get(self, "managed_zone")

    @managed_zone.setter
    def managed_zone(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "managed_zone", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The DNS name this record set will apply to.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def project(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the project in which the resource belongs. If it
        is not provided, the provider project is used.
        """
        return pulumi.get(self, "project")

    @project.setter
    def project(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "project", value)

    @property
    @pulumi.getter
    def rrdatas(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The string data for the records in this record set whose meaning depends on the DNS type. For TXT record, if the string
        data contains spaces, add surrounding \" if you don't want your string to get split on spaces. To specify a single
        record value longer than 255 characters such as a TXT record for DKIM, add \"\" inside the Terraform configuration
        string (e.g. "first255characters\"\"morecharacters").
        """
        return pulumi.get(self, "rrdatas")

    @rrdatas.setter
    def rrdatas(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "rrdatas", value)

    @property
    @pulumi.getter
    def ttl(self) -> Optional[pulumi.Input[int]]:
        """
        The time-to-live of this record set (seconds).
        """
        return pulumi.get(self, "ttl")

    @ttl.setter
    def ttl(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "ttl", value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[str]]:
        """
        The DNS record set type.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "type", value)


class RecordSet(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 managed_zone: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 rrdatas: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 ttl: Optional[pulumi.Input[int]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        ## Example Usage
        ### Binding a DNS name to the ephemeral IP of a new instance:

        ```python
        import pulumi
        import pulumi_gcp as gcp

        frontend_instance = gcp.compute.Instance("frontendInstance",
            machine_type="g1-small",
            zone="us-central1-b",
            boot_disk=gcp.compute.InstanceBootDiskArgs(
                initialize_params=gcp.compute.InstanceBootDiskInitializeParamsArgs(
                    image="debian-cloud/debian-9",
                ),
            ),
            network_interfaces=[gcp.compute.InstanceNetworkInterfaceArgs(
                network="default",
                access_configs=[gcp.compute.InstanceNetworkInterfaceAccessConfigArgs()],
            )])
        prod = gcp.dns.ManagedZone("prod", dns_name="prod.mydomain.com.")
        frontend_record_set = gcp.dns.RecordSet("frontendRecordSet",
            name=prod.dns_name.apply(lambda dns_name: f"frontend.{dns_name}"),
            type="A",
            ttl=300,
            managed_zone=prod.name,
            rrdatas=[frontend_instance.network_interfaces[0].access_configs[0].nat_ip])
        ```
        ### Adding an A record

        ```python
        import pulumi
        import pulumi_gcp as gcp

        prod = gcp.dns.ManagedZone("prod", dns_name="prod.mydomain.com.")
        record_set = gcp.dns.RecordSet("recordSet",
            name=prod.dns_name.apply(lambda dns_name: f"backend.{dns_name}"),
            managed_zone=prod.name,
            type="A",
            ttl=300,
            rrdatas=["8.8.8.8"])
        ```
        ### Adding an MX record

        ```python
        import pulumi
        import pulumi_gcp as gcp

        prod = gcp.dns.ManagedZone("prod", dns_name="prod.mydomain.com.")
        mx = gcp.dns.RecordSet("mx",
            name=prod.dns_name,
            managed_zone=prod.name,
            type="MX",
            ttl=3600,
            rrdatas=[
                "1 aspmx.l.google.com.",
                "5 alt1.aspmx.l.google.com.",
                "5 alt2.aspmx.l.google.com.",
                "10 alt3.aspmx.l.google.com.",
                "10 alt4.aspmx.l.google.com.",
            ])
        ```
        ### Adding an SPF record

        Quotes (`""`) must be added around your `rrdatas` for a SPF record. Otherwise `rrdatas` string gets split on spaces.

        ```python
        import pulumi
        import pulumi_gcp as gcp

        prod = gcp.dns.ManagedZone("prod", dns_name="prod.mydomain.com.")
        spf = gcp.dns.RecordSet("spf",
            name=prod.dns_name.apply(lambda dns_name: f"frontend.{dns_name}"),
            managed_zone=prod.name,
            type="TXT",
            ttl=300,
            rrdatas=["\"v=spf1 ip4:111.111.111.111 include:backoff.email-example.com -all\""])
        ```
        ### Adding a CNAME record

         The list of `rrdatas` should only contain a single string corresponding to the Canonical Name intended.

        ```python
        import pulumi
        import pulumi_gcp as gcp

        prod = gcp.dns.ManagedZone("prod", dns_name="prod.mydomain.com.")
        cname = gcp.dns.RecordSet("cname",
            name=prod.dns_name.apply(lambda dns_name: f"frontend.{dns_name}"),
            managed_zone=prod.name,
            type="CNAME",
            ttl=300,
            rrdatas=["frontend.mydomain.com."])
        ```

        ## Import

        DNS record sets can be imported using either of these accepted formats

        ```sh
         $ pulumi import gcp:dns/recordSet:RecordSet frontend projects/{{project}}/managedZones/{{zone}}/rrsets/{{name}}/{{type}}
        ```

        ```sh
         $ pulumi import gcp:dns/recordSet:RecordSet frontend {{project}}/{{zone}}/{{name}}/{{type}}
        ```

        ```sh
         $ pulumi import gcp:dns/recordSet:RecordSet frontend {{zone}}/{{name}}/{{type}}
        ```

         NoteThe record name must include the trailing dot at the end.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] managed_zone: The name of the zone in which this record set will
               reside.
        :param pulumi.Input[str] name: The DNS name this record set will apply to.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs. If it
               is not provided, the provider project is used.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] rrdatas: The string data for the records in this record set whose meaning depends on the DNS type. For TXT record, if the string
               data contains spaces, add surrounding \" if you don't want your string to get split on spaces. To specify a single
               record value longer than 255 characters such as a TXT record for DKIM, add \"\" inside the Terraform configuration
               string (e.g. "first255characters\"\"morecharacters").
        :param pulumi.Input[int] ttl: The time-to-live of this record set (seconds).
        :param pulumi.Input[str] type: The DNS record set type.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: RecordSetArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        ## Example Usage
        ### Binding a DNS name to the ephemeral IP of a new instance:

        ```python
        import pulumi
        import pulumi_gcp as gcp

        frontend_instance = gcp.compute.Instance("frontendInstance",
            machine_type="g1-small",
            zone="us-central1-b",
            boot_disk=gcp.compute.InstanceBootDiskArgs(
                initialize_params=gcp.compute.InstanceBootDiskInitializeParamsArgs(
                    image="debian-cloud/debian-9",
                ),
            ),
            network_interfaces=[gcp.compute.InstanceNetworkInterfaceArgs(
                network="default",
                access_configs=[gcp.compute.InstanceNetworkInterfaceAccessConfigArgs()],
            )])
        prod = gcp.dns.ManagedZone("prod", dns_name="prod.mydomain.com.")
        frontend_record_set = gcp.dns.RecordSet("frontendRecordSet",
            name=prod.dns_name.apply(lambda dns_name: f"frontend.{dns_name}"),
            type="A",
            ttl=300,
            managed_zone=prod.name,
            rrdatas=[frontend_instance.network_interfaces[0].access_configs[0].nat_ip])
        ```
        ### Adding an A record

        ```python
        import pulumi
        import pulumi_gcp as gcp

        prod = gcp.dns.ManagedZone("prod", dns_name="prod.mydomain.com.")
        record_set = gcp.dns.RecordSet("recordSet",
            name=prod.dns_name.apply(lambda dns_name: f"backend.{dns_name}"),
            managed_zone=prod.name,
            type="A",
            ttl=300,
            rrdatas=["8.8.8.8"])
        ```
        ### Adding an MX record

        ```python
        import pulumi
        import pulumi_gcp as gcp

        prod = gcp.dns.ManagedZone("prod", dns_name="prod.mydomain.com.")
        mx = gcp.dns.RecordSet("mx",
            name=prod.dns_name,
            managed_zone=prod.name,
            type="MX",
            ttl=3600,
            rrdatas=[
                "1 aspmx.l.google.com.",
                "5 alt1.aspmx.l.google.com.",
                "5 alt2.aspmx.l.google.com.",
                "10 alt3.aspmx.l.google.com.",
                "10 alt4.aspmx.l.google.com.",
            ])
        ```
        ### Adding an SPF record

        Quotes (`""`) must be added around your `rrdatas` for a SPF record. Otherwise `rrdatas` string gets split on spaces.

        ```python
        import pulumi
        import pulumi_gcp as gcp

        prod = gcp.dns.ManagedZone("prod", dns_name="prod.mydomain.com.")
        spf = gcp.dns.RecordSet("spf",
            name=prod.dns_name.apply(lambda dns_name: f"frontend.{dns_name}"),
            managed_zone=prod.name,
            type="TXT",
            ttl=300,
            rrdatas=["\"v=spf1 ip4:111.111.111.111 include:backoff.email-example.com -all\""])
        ```
        ### Adding a CNAME record

         The list of `rrdatas` should only contain a single string corresponding to the Canonical Name intended.

        ```python
        import pulumi
        import pulumi_gcp as gcp

        prod = gcp.dns.ManagedZone("prod", dns_name="prod.mydomain.com.")
        cname = gcp.dns.RecordSet("cname",
            name=prod.dns_name.apply(lambda dns_name: f"frontend.{dns_name}"),
            managed_zone=prod.name,
            type="CNAME",
            ttl=300,
            rrdatas=["frontend.mydomain.com."])
        ```

        ## Import

        DNS record sets can be imported using either of these accepted formats

        ```sh
         $ pulumi import gcp:dns/recordSet:RecordSet frontend projects/{{project}}/managedZones/{{zone}}/rrsets/{{name}}/{{type}}
        ```

        ```sh
         $ pulumi import gcp:dns/recordSet:RecordSet frontend {{project}}/{{zone}}/{{name}}/{{type}}
        ```

        ```sh
         $ pulumi import gcp:dns/recordSet:RecordSet frontend {{zone}}/{{name}}/{{type}}
        ```

         NoteThe record name must include the trailing dot at the end.

        :param str resource_name: The name of the resource.
        :param RecordSetArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(RecordSetArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 managed_zone: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 rrdatas: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 ttl: Optional[pulumi.Input[int]] = None,
                 type: Optional[pulumi.Input[str]] = None,
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
            __props__ = RecordSetArgs.__new__(RecordSetArgs)

            if managed_zone is None and not opts.urn:
                raise TypeError("Missing required property 'managed_zone'")
            __props__.__dict__["managed_zone"] = managed_zone
            if name is None and not opts.urn:
                raise TypeError("Missing required property 'name'")
            __props__.__dict__["name"] = name
            __props__.__dict__["project"] = project
            if rrdatas is None and not opts.urn:
                raise TypeError("Missing required property 'rrdatas'")
            __props__.__dict__["rrdatas"] = rrdatas
            __props__.__dict__["ttl"] = ttl
            if type is None and not opts.urn:
                raise TypeError("Missing required property 'type'")
            __props__.__dict__["type"] = type
        super(RecordSet, __self__).__init__(
            'gcp:dns/recordSet:RecordSet',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            managed_zone: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            project: Optional[pulumi.Input[str]] = None,
            rrdatas: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            ttl: Optional[pulumi.Input[int]] = None,
            type: Optional[pulumi.Input[str]] = None) -> 'RecordSet':
        """
        Get an existing RecordSet resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] managed_zone: The name of the zone in which this record set will
               reside.
        :param pulumi.Input[str] name: The DNS name this record set will apply to.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs. If it
               is not provided, the provider project is used.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] rrdatas: The string data for the records in this record set whose meaning depends on the DNS type. For TXT record, if the string
               data contains spaces, add surrounding \" if you don't want your string to get split on spaces. To specify a single
               record value longer than 255 characters such as a TXT record for DKIM, add \"\" inside the Terraform configuration
               string (e.g. "first255characters\"\"morecharacters").
        :param pulumi.Input[int] ttl: The time-to-live of this record set (seconds).
        :param pulumi.Input[str] type: The DNS record set type.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _RecordSetState.__new__(_RecordSetState)

        __props__.__dict__["managed_zone"] = managed_zone
        __props__.__dict__["name"] = name
        __props__.__dict__["project"] = project
        __props__.__dict__["rrdatas"] = rrdatas
        __props__.__dict__["ttl"] = ttl
        __props__.__dict__["type"] = type
        return RecordSet(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="managedZone")
    def managed_zone(self) -> pulumi.Output[str]:
        """
        The name of the zone in which this record set will
        reside.
        """
        return pulumi.get(self, "managed_zone")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The DNS name this record set will apply to.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def project(self) -> pulumi.Output[str]:
        """
        The ID of the project in which the resource belongs. If it
        is not provided, the provider project is used.
        """
        return pulumi.get(self, "project")

    @property
    @pulumi.getter
    def rrdatas(self) -> pulumi.Output[Sequence[str]]:
        """
        The string data for the records in this record set whose meaning depends on the DNS type. For TXT record, if the string
        data contains spaces, add surrounding \" if you don't want your string to get split on spaces. To specify a single
        record value longer than 255 characters such as a TXT record for DKIM, add \"\" inside the Terraform configuration
        string (e.g. "first255characters\"\"morecharacters").
        """
        return pulumi.get(self, "rrdatas")

    @property
    @pulumi.getter
    def ttl(self) -> pulumi.Output[Optional[int]]:
        """
        The time-to-live of this record set (seconds).
        """
        return pulumi.get(self, "ttl")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The DNS record set type.
        """
        return pulumi.get(self, "type")

