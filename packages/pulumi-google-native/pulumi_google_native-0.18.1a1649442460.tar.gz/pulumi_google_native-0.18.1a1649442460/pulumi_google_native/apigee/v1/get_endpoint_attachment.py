# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities

__all__ = [
    'GetEndpointAttachmentResult',
    'AwaitableGetEndpointAttachmentResult',
    'get_endpoint_attachment',
    'get_endpoint_attachment_output',
]

@pulumi.output_type
class GetEndpointAttachmentResult:
    def __init__(__self__, host=None, location=None, name=None, service_attachment=None, state=None):
        if host and not isinstance(host, str):
            raise TypeError("Expected argument 'host' to be a str")
        pulumi.set(__self__, "host", host)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if service_attachment and not isinstance(service_attachment, str):
            raise TypeError("Expected argument 'service_attachment' to be a str")
        pulumi.set(__self__, "service_attachment", service_attachment)
        if state and not isinstance(state, str):
            raise TypeError("Expected argument 'state' to be a str")
        pulumi.set(__self__, "state", state)

    @property
    @pulumi.getter
    def host(self) -> str:
        """
        Host that can be used in either the HTTP target endpoint directly or as the host in target server.
        """
        return pulumi.get(self, "host")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        Location of the endpoint attachment.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Name of the endpoint attachment. Use the following structure in your request: `organizations/{org}/endpointAttachments/{endpoint_attachment}`
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="serviceAttachment")
    def service_attachment(self) -> str:
        """
        Format: projects/*/regions/*/serviceAttachments/*
        """
        return pulumi.get(self, "service_attachment")

    @property
    @pulumi.getter
    def state(self) -> str:
        """
        State of the endpoint attachment. Values other than `ACTIVE` mean the resource is not ready to use.
        """
        return pulumi.get(self, "state")


class AwaitableGetEndpointAttachmentResult(GetEndpointAttachmentResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetEndpointAttachmentResult(
            host=self.host,
            location=self.location,
            name=self.name,
            service_attachment=self.service_attachment,
            state=self.state)


def get_endpoint_attachment(endpoint_attachment_id: Optional[str] = None,
                            organization_id: Optional[str] = None,
                            opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetEndpointAttachmentResult:
    """
    Gets the endpoint attachment.
    """
    __args__ = dict()
    __args__['endpointAttachmentId'] = endpoint_attachment_id
    __args__['organizationId'] = organization_id
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('google-native:apigee/v1:getEndpointAttachment', __args__, opts=opts, typ=GetEndpointAttachmentResult).value

    return AwaitableGetEndpointAttachmentResult(
        host=__ret__.host,
        location=__ret__.location,
        name=__ret__.name,
        service_attachment=__ret__.service_attachment,
        state=__ret__.state)


@_utilities.lift_output_func(get_endpoint_attachment)
def get_endpoint_attachment_output(endpoint_attachment_id: Optional[pulumi.Input[str]] = None,
                                   organization_id: Optional[pulumi.Input[str]] = None,
                                   opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetEndpointAttachmentResult]:
    """
    Gets the endpoint attachment.
    """
    ...
