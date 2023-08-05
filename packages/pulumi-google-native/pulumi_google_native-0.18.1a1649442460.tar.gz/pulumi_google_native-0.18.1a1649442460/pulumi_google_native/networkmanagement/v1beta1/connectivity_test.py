# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
from ._enums import *
from ._inputs import *

__all__ = ['ConnectivityTestArgs', 'ConnectivityTest']

@pulumi.input_type
class ConnectivityTestArgs:
    def __init__(__self__, *,
                 destination: pulumi.Input['EndpointArgs'],
                 name: pulumi.Input[str],
                 source: pulumi.Input['EndpointArgs'],
                 test_id: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None,
                 labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 protocol: Optional[pulumi.Input[str]] = None,
                 related_projects: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a ConnectivityTest resource.
        :param pulumi.Input['EndpointArgs'] destination: Destination specification of the Connectivity Test. You can use a combination of destination IP address, Compute Engine VM instance, or VPC network to uniquely identify the destination location. Even if the destination IP address is not unique, the source IP location is unique. Usually, the analysis can infer the destination endpoint from route information. If the destination you specify is a VM instance and the instance has multiple network interfaces, then you must also specify either a destination IP address or VPC network to identify the destination interface. A reachability analysis proceeds even if the destination location is ambiguous. However, the result can include endpoints that you don't intend to test.
        :param pulumi.Input[str] name: Unique name of the resource using the form: `projects/{project_id}/locations/global/connectivityTests/{test}`
        :param pulumi.Input['EndpointArgs'] source: Source specification of the Connectivity Test. You can use a combination of source IP address, virtual machine (VM) instance, or Compute Engine network to uniquely identify the source location. Examples: If the source IP address is an internal IP address within a Google Cloud Virtual Private Cloud (VPC) network, then you must also specify the VPC network. Otherwise, specify the VM instance, which already contains its internal IP address and VPC network information. If the source of the test is within an on-premises network, then you must provide the destination VPC network. If the source endpoint is a Compute Engine VM instance with multiple network interfaces, the instance itself is not sufficient to identify the endpoint. So, you must also specify the source IP address or VPC network. A reachability analysis proceeds even if the source location is ambiguous. However, the test result may include endpoints that you don't intend to test.
        :param pulumi.Input[str] test_id: Required. The logical name of the Connectivity Test in your project with the following restrictions: * Must contain only lowercase letters, numbers, and hyphens. * Must start with a letter. * Must be between 1-40 characters. * Must end with a number or a letter. * Must be unique within the customer project
        :param pulumi.Input[str] description: The user-supplied description of the Connectivity Test. Maximum of 512 characters.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: Resource labels to represent user-provided metadata.
        :param pulumi.Input[str] protocol: IP Protocol of the test. When not provided, "TCP" is assumed.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] related_projects: Other projects that may be relevant for reachability analysis. This is applicable to scenarios where a test can cross project boundaries.
        """
        pulumi.set(__self__, "destination", destination)
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "source", source)
        pulumi.set(__self__, "test_id", test_id)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if labels is not None:
            pulumi.set(__self__, "labels", labels)
        if project is not None:
            pulumi.set(__self__, "project", project)
        if protocol is not None:
            pulumi.set(__self__, "protocol", protocol)
        if related_projects is not None:
            pulumi.set(__self__, "related_projects", related_projects)

    @property
    @pulumi.getter
    def destination(self) -> pulumi.Input['EndpointArgs']:
        """
        Destination specification of the Connectivity Test. You can use a combination of destination IP address, Compute Engine VM instance, or VPC network to uniquely identify the destination location. Even if the destination IP address is not unique, the source IP location is unique. Usually, the analysis can infer the destination endpoint from route information. If the destination you specify is a VM instance and the instance has multiple network interfaces, then you must also specify either a destination IP address or VPC network to identify the destination interface. A reachability analysis proceeds even if the destination location is ambiguous. However, the result can include endpoints that you don't intend to test.
        """
        return pulumi.get(self, "destination")

    @destination.setter
    def destination(self, value: pulumi.Input['EndpointArgs']):
        pulumi.set(self, "destination", value)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        Unique name of the resource using the form: `projects/{project_id}/locations/global/connectivityTests/{test}`
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def source(self) -> pulumi.Input['EndpointArgs']:
        """
        Source specification of the Connectivity Test. You can use a combination of source IP address, virtual machine (VM) instance, or Compute Engine network to uniquely identify the source location. Examples: If the source IP address is an internal IP address within a Google Cloud Virtual Private Cloud (VPC) network, then you must also specify the VPC network. Otherwise, specify the VM instance, which already contains its internal IP address and VPC network information. If the source of the test is within an on-premises network, then you must provide the destination VPC network. If the source endpoint is a Compute Engine VM instance with multiple network interfaces, the instance itself is not sufficient to identify the endpoint. So, you must also specify the source IP address or VPC network. A reachability analysis proceeds even if the source location is ambiguous. However, the test result may include endpoints that you don't intend to test.
        """
        return pulumi.get(self, "source")

    @source.setter
    def source(self, value: pulumi.Input['EndpointArgs']):
        pulumi.set(self, "source", value)

    @property
    @pulumi.getter(name="testId")
    def test_id(self) -> pulumi.Input[str]:
        """
        Required. The logical name of the Connectivity Test in your project with the following restrictions: * Must contain only lowercase letters, numbers, and hyphens. * Must start with a letter. * Must be between 1-40 characters. * Must end with a number or a letter. * Must be unique within the customer project
        """
        return pulumi.get(self, "test_id")

    @test_id.setter
    def test_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "test_id", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The user-supplied description of the Connectivity Test. Maximum of 512 characters.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def labels(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Resource labels to represent user-provided metadata.
        """
        return pulumi.get(self, "labels")

    @labels.setter
    def labels(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "labels", value)

    @property
    @pulumi.getter
    def project(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "project")

    @project.setter
    def project(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "project", value)

    @property
    @pulumi.getter
    def protocol(self) -> Optional[pulumi.Input[str]]:
        """
        IP Protocol of the test. When not provided, "TCP" is assumed.
        """
        return pulumi.get(self, "protocol")

    @protocol.setter
    def protocol(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "protocol", value)

    @property
    @pulumi.getter(name="relatedProjects")
    def related_projects(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Other projects that may be relevant for reachability analysis. This is applicable to scenarios where a test can cross project boundaries.
        """
        return pulumi.get(self, "related_projects")

    @related_projects.setter
    def related_projects(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "related_projects", value)


class ConnectivityTest(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 destination: Optional[pulumi.Input[pulumi.InputType['EndpointArgs']]] = None,
                 labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 protocol: Optional[pulumi.Input[str]] = None,
                 related_projects: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 source: Optional[pulumi.Input[pulumi.InputType['EndpointArgs']]] = None,
                 test_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Creates a new Connectivity Test. After you create a test, the reachability analysis is performed as part of the long running operation, which completes when the analysis completes. If the endpoint specifications in `ConnectivityTest` are invalid (for example, containing non-existent resources in the network, or you don't have read permissions to the network configurations of listed projects), then the reachability result returns a value of `UNKNOWN`. If the endpoint specifications in `ConnectivityTest` are incomplete, the reachability result returns a value of AMBIGUOUS. For more information, see the Connectivity Test documentation.
        Auto-naming is currently not supported for this resource.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: The user-supplied description of the Connectivity Test. Maximum of 512 characters.
        :param pulumi.Input[pulumi.InputType['EndpointArgs']] destination: Destination specification of the Connectivity Test. You can use a combination of destination IP address, Compute Engine VM instance, or VPC network to uniquely identify the destination location. Even if the destination IP address is not unique, the source IP location is unique. Usually, the analysis can infer the destination endpoint from route information. If the destination you specify is a VM instance and the instance has multiple network interfaces, then you must also specify either a destination IP address or VPC network to identify the destination interface. A reachability analysis proceeds even if the destination location is ambiguous. However, the result can include endpoints that you don't intend to test.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: Resource labels to represent user-provided metadata.
        :param pulumi.Input[str] name: Unique name of the resource using the form: `projects/{project_id}/locations/global/connectivityTests/{test}`
        :param pulumi.Input[str] protocol: IP Protocol of the test. When not provided, "TCP" is assumed.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] related_projects: Other projects that may be relevant for reachability analysis. This is applicable to scenarios where a test can cross project boundaries.
        :param pulumi.Input[pulumi.InputType['EndpointArgs']] source: Source specification of the Connectivity Test. You can use a combination of source IP address, virtual machine (VM) instance, or Compute Engine network to uniquely identify the source location. Examples: If the source IP address is an internal IP address within a Google Cloud Virtual Private Cloud (VPC) network, then you must also specify the VPC network. Otherwise, specify the VM instance, which already contains its internal IP address and VPC network information. If the source of the test is within an on-premises network, then you must provide the destination VPC network. If the source endpoint is a Compute Engine VM instance with multiple network interfaces, the instance itself is not sufficient to identify the endpoint. So, you must also specify the source IP address or VPC network. A reachability analysis proceeds even if the source location is ambiguous. However, the test result may include endpoints that you don't intend to test.
        :param pulumi.Input[str] test_id: Required. The logical name of the Connectivity Test in your project with the following restrictions: * Must contain only lowercase letters, numbers, and hyphens. * Must start with a letter. * Must be between 1-40 characters. * Must end with a number or a letter. * Must be unique within the customer project
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ConnectivityTestArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Creates a new Connectivity Test. After you create a test, the reachability analysis is performed as part of the long running operation, which completes when the analysis completes. If the endpoint specifications in `ConnectivityTest` are invalid (for example, containing non-existent resources in the network, or you don't have read permissions to the network configurations of listed projects), then the reachability result returns a value of `UNKNOWN`. If the endpoint specifications in `ConnectivityTest` are incomplete, the reachability result returns a value of AMBIGUOUS. For more information, see the Connectivity Test documentation.
        Auto-naming is currently not supported for this resource.

        :param str resource_name: The name of the resource.
        :param ConnectivityTestArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ConnectivityTestArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 destination: Optional[pulumi.Input[pulumi.InputType['EndpointArgs']]] = None,
                 labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 protocol: Optional[pulumi.Input[str]] = None,
                 related_projects: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 source: Optional[pulumi.Input[pulumi.InputType['EndpointArgs']]] = None,
                 test_id: Optional[pulumi.Input[str]] = None,
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
            __props__ = ConnectivityTestArgs.__new__(ConnectivityTestArgs)

            __props__.__dict__["description"] = description
            if destination is None and not opts.urn:
                raise TypeError("Missing required property 'destination'")
            __props__.__dict__["destination"] = destination
            __props__.__dict__["labels"] = labels
            if name is None and not opts.urn:
                raise TypeError("Missing required property 'name'")
            __props__.__dict__["name"] = name
            __props__.__dict__["project"] = project
            __props__.__dict__["protocol"] = protocol
            __props__.__dict__["related_projects"] = related_projects
            if source is None and not opts.urn:
                raise TypeError("Missing required property 'source'")
            __props__.__dict__["source"] = source
            if test_id is None and not opts.urn:
                raise TypeError("Missing required property 'test_id'")
            __props__.__dict__["test_id"] = test_id
            __props__.__dict__["create_time"] = None
            __props__.__dict__["display_name"] = None
            __props__.__dict__["probing_details"] = None
            __props__.__dict__["reachability_details"] = None
            __props__.__dict__["update_time"] = None
        super(ConnectivityTest, __self__).__init__(
            'google-native:networkmanagement/v1beta1:ConnectivityTest',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ConnectivityTest':
        """
        Get an existing ConnectivityTest resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ConnectivityTestArgs.__new__(ConnectivityTestArgs)

        __props__.__dict__["create_time"] = None
        __props__.__dict__["description"] = None
        __props__.__dict__["destination"] = None
        __props__.__dict__["display_name"] = None
        __props__.__dict__["labels"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["probing_details"] = None
        __props__.__dict__["protocol"] = None
        __props__.__dict__["reachability_details"] = None
        __props__.__dict__["related_projects"] = None
        __props__.__dict__["source"] = None
        __props__.__dict__["update_time"] = None
        return ConnectivityTest(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> pulumi.Output[str]:
        """
        The time the test was created.
        """
        return pulumi.get(self, "create_time")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[str]:
        """
        The user-supplied description of the Connectivity Test. Maximum of 512 characters.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def destination(self) -> pulumi.Output['outputs.EndpointResponse']:
        """
        Destination specification of the Connectivity Test. You can use a combination of destination IP address, Compute Engine VM instance, or VPC network to uniquely identify the destination location. Even if the destination IP address is not unique, the source IP location is unique. Usually, the analysis can infer the destination endpoint from route information. If the destination you specify is a VM instance and the instance has multiple network interfaces, then you must also specify either a destination IP address or VPC network to identify the destination interface. A reachability analysis proceeds even if the destination location is ambiguous. However, the result can include endpoints that you don't intend to test.
        """
        return pulumi.get(self, "destination")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> pulumi.Output[str]:
        """
        The display name of a Connectivity Test.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter
    def labels(self) -> pulumi.Output[Mapping[str, str]]:
        """
        Resource labels to represent user-provided metadata.
        """
        return pulumi.get(self, "labels")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Unique name of the resource using the form: `projects/{project_id}/locations/global/connectivityTests/{test}`
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="probingDetails")
    def probing_details(self) -> pulumi.Output['outputs.ProbingDetailsResponse']:
        """
        The probing details of this test from the latest run, present for applicable tests only. The details are updated when creating a new test, updating an existing test, or triggering a one-time rerun of an existing test.
        """
        return pulumi.get(self, "probing_details")

    @property
    @pulumi.getter
    def protocol(self) -> pulumi.Output[str]:
        """
        IP Protocol of the test. When not provided, "TCP" is assumed.
        """
        return pulumi.get(self, "protocol")

    @property
    @pulumi.getter(name="reachabilityDetails")
    def reachability_details(self) -> pulumi.Output['outputs.ReachabilityDetailsResponse']:
        """
        The reachability details of this test from the latest run. The details are updated when creating a new test, updating an existing test, or triggering a one-time rerun of an existing test.
        """
        return pulumi.get(self, "reachability_details")

    @property
    @pulumi.getter(name="relatedProjects")
    def related_projects(self) -> pulumi.Output[Sequence[str]]:
        """
        Other projects that may be relevant for reachability analysis. This is applicable to scenarios where a test can cross project boundaries.
        """
        return pulumi.get(self, "related_projects")

    @property
    @pulumi.getter
    def source(self) -> pulumi.Output['outputs.EndpointResponse']:
        """
        Source specification of the Connectivity Test. You can use a combination of source IP address, virtual machine (VM) instance, or Compute Engine network to uniquely identify the source location. Examples: If the source IP address is an internal IP address within a Google Cloud Virtual Private Cloud (VPC) network, then you must also specify the VPC network. Otherwise, specify the VM instance, which already contains its internal IP address and VPC network information. If the source of the test is within an on-premises network, then you must provide the destination VPC network. If the source endpoint is a Compute Engine VM instance with multiple network interfaces, the instance itself is not sufficient to identify the endpoint. So, you must also specify the source IP address or VPC network. A reachability analysis proceeds even if the source location is ambiguous. However, the test result may include endpoints that you don't intend to test.
        """
        return pulumi.get(self, "source")

    @property
    @pulumi.getter(name="updateTime")
    def update_time(self) -> pulumi.Output[str]:
        """
        The time the test's configuration was updated.
        """
        return pulumi.get(self, "update_time")

