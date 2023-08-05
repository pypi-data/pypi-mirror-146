# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'GetSSLPolicyResult',
    'AwaitableGetSSLPolicyResult',
    'get_ssl_policy',
    'get_ssl_policy_output',
]

@pulumi.output_type
class GetSSLPolicyResult:
    """
    A collection of values returned by getSSLPolicy.
    """
    def __init__(__self__, creation_timestamp=None, custom_features=None, description=None, enabled_features=None, fingerprint=None, id=None, min_tls_version=None, name=None, profile=None, project=None, self_link=None):
        if creation_timestamp and not isinstance(creation_timestamp, str):
            raise TypeError("Expected argument 'creation_timestamp' to be a str")
        pulumi.set(__self__, "creation_timestamp", creation_timestamp)
        if custom_features and not isinstance(custom_features, list):
            raise TypeError("Expected argument 'custom_features' to be a list")
        pulumi.set(__self__, "custom_features", custom_features)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if enabled_features and not isinstance(enabled_features, list):
            raise TypeError("Expected argument 'enabled_features' to be a list")
        pulumi.set(__self__, "enabled_features", enabled_features)
        if fingerprint and not isinstance(fingerprint, str):
            raise TypeError("Expected argument 'fingerprint' to be a str")
        pulumi.set(__self__, "fingerprint", fingerprint)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if min_tls_version and not isinstance(min_tls_version, str):
            raise TypeError("Expected argument 'min_tls_version' to be a str")
        pulumi.set(__self__, "min_tls_version", min_tls_version)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if profile and not isinstance(profile, str):
            raise TypeError("Expected argument 'profile' to be a str")
        pulumi.set(__self__, "profile", profile)
        if project and not isinstance(project, str):
            raise TypeError("Expected argument 'project' to be a str")
        pulumi.set(__self__, "project", project)
        if self_link and not isinstance(self_link, str):
            raise TypeError("Expected argument 'self_link' to be a str")
        pulumi.set(__self__, "self_link", self_link)

    @property
    @pulumi.getter(name="creationTimestamp")
    def creation_timestamp(self) -> str:
        return pulumi.get(self, "creation_timestamp")

    @property
    @pulumi.getter(name="customFeatures")
    def custom_features(self) -> Sequence[str]:
        """
        If the `profile` is `CUSTOM`, these are the custom encryption
        ciphers supported by the profile. If the `profile` is *not* `CUSTOM`, this
        attribute will be empty.
        """
        return pulumi.get(self, "custom_features")

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        Description of this SSL Policy.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="enabledFeatures")
    def enabled_features(self) -> Sequence[str]:
        """
        The set of enabled encryption ciphers as a result of the policy config
        """
        return pulumi.get(self, "enabled_features")

    @property
    @pulumi.getter
    def fingerprint(self) -> str:
        """
        Fingerprint of this resource.
        """
        return pulumi.get(self, "fingerprint")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="minTlsVersion")
    def min_tls_version(self) -> str:
        """
        The minimum supported TLS version of this policy.
        """
        return pulumi.get(self, "min_tls_version")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def profile(self) -> str:
        """
        The Google-curated or custom profile used by this policy.
        """
        return pulumi.get(self, "profile")

    @property
    @pulumi.getter
    def project(self) -> Optional[str]:
        return pulumi.get(self, "project")

    @property
    @pulumi.getter(name="selfLink")
    def self_link(self) -> str:
        """
        The URI of the created resource.
        """
        return pulumi.get(self, "self_link")


class AwaitableGetSSLPolicyResult(GetSSLPolicyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSSLPolicyResult(
            creation_timestamp=self.creation_timestamp,
            custom_features=self.custom_features,
            description=self.description,
            enabled_features=self.enabled_features,
            fingerprint=self.fingerprint,
            id=self.id,
            min_tls_version=self.min_tls_version,
            name=self.name,
            profile=self.profile,
            project=self.project,
            self_link=self.self_link)


def get_ssl_policy(name: Optional[str] = None,
                   project: Optional[str] = None,
                   opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSSLPolicyResult:
    """
    Gets an SSL Policy within GCE from its name, for use with Target HTTPS and Target SSL Proxies.
        For more information see [the official documentation](https://cloud.google.com/compute/docs/load-balancing/ssl-policies).

    ## Example Usage

    ```python
    import pulumi
    import pulumi_gcp as gcp

    my_ssl_policy = gcp.compute.get_ssl_policy(name="production-ssl-policy")
    ```


    :param str name: The name of the SSL Policy.
    :param str project: The ID of the project in which the resource belongs. If it
           is not provided, the provider project is used.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['project'] = project
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('gcp:compute/getSSLPolicy:getSSLPolicy', __args__, opts=opts, typ=GetSSLPolicyResult).value

    return AwaitableGetSSLPolicyResult(
        creation_timestamp=__ret__.creation_timestamp,
        custom_features=__ret__.custom_features,
        description=__ret__.description,
        enabled_features=__ret__.enabled_features,
        fingerprint=__ret__.fingerprint,
        id=__ret__.id,
        min_tls_version=__ret__.min_tls_version,
        name=__ret__.name,
        profile=__ret__.profile,
        project=__ret__.project,
        self_link=__ret__.self_link)


@_utilities.lift_output_func(get_ssl_policy)
def get_ssl_policy_output(name: Optional[pulumi.Input[str]] = None,
                          project: Optional[pulumi.Input[Optional[str]]] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetSSLPolicyResult]:
    """
    Gets an SSL Policy within GCE from its name, for use with Target HTTPS and Target SSL Proxies.
        For more information see [the official documentation](https://cloud.google.com/compute/docs/load-balancing/ssl-policies).

    ## Example Usage

    ```python
    import pulumi
    import pulumi_gcp as gcp

    my_ssl_policy = gcp.compute.get_ssl_policy(name="production-ssl-policy")
    ```


    :param str name: The name of the SSL Policy.
    :param str project: The ID of the project in which the resource belongs. If it
           is not provided, the provider project is used.
    """
    ...
