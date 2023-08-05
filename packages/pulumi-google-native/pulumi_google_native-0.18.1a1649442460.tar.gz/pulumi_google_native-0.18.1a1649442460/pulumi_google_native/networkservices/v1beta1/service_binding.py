# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities

__all__ = ['ServiceBindingArgs', 'ServiceBinding']

@pulumi.input_type
class ServiceBindingArgs:
    def __init__(__self__, *,
                 service: pulumi.Input[str],
                 service_binding_id: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None,
                 endpoint_filter: Optional[pulumi.Input[str]] = None,
                 labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a ServiceBinding resource.
        :param pulumi.Input[str] service: The full service directory service name of the format /projects/*/locations/*/namespaces/*/services/*
        :param pulumi.Input[str] service_binding_id: Required. Short name of the ServiceBinding resource to be created.
        :param pulumi.Input[str] description: Optional. A free-text description of the resource. Max length 1024 characters.
        :param pulumi.Input[str] endpoint_filter: Optional. The endpoint filter associated with the Service Binding. The syntax is described in http://cloud/service-directory/docs/reference/rpc/google.cloud.servicedirectory.v1#google.cloud.servicedirectory.v1.ResolveServiceRequest
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: Optional. Set of label tags associated with the ServiceBinding resource.
        :param pulumi.Input[str] name: Name of the ServiceBinding resource. It matches pattern `projects/*/locations/global/serviceBindings/service_binding_name>`.
        """
        pulumi.set(__self__, "service", service)
        pulumi.set(__self__, "service_binding_id", service_binding_id)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if endpoint_filter is not None:
            pulumi.set(__self__, "endpoint_filter", endpoint_filter)
        if labels is not None:
            pulumi.set(__self__, "labels", labels)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if project is not None:
            pulumi.set(__self__, "project", project)

    @property
    @pulumi.getter
    def service(self) -> pulumi.Input[str]:
        """
        The full service directory service name of the format /projects/*/locations/*/namespaces/*/services/*
        """
        return pulumi.get(self, "service")

    @service.setter
    def service(self, value: pulumi.Input[str]):
        pulumi.set(self, "service", value)

    @property
    @pulumi.getter(name="serviceBindingId")
    def service_binding_id(self) -> pulumi.Input[str]:
        """
        Required. Short name of the ServiceBinding resource to be created.
        """
        return pulumi.get(self, "service_binding_id")

    @service_binding_id.setter
    def service_binding_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "service_binding_id", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Optional. A free-text description of the resource. Max length 1024 characters.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="endpointFilter")
    def endpoint_filter(self) -> Optional[pulumi.Input[str]]:
        """
        Optional. The endpoint filter associated with the Service Binding. The syntax is described in http://cloud/service-directory/docs/reference/rpc/google.cloud.servicedirectory.v1#google.cloud.servicedirectory.v1.ResolveServiceRequest
        """
        return pulumi.get(self, "endpoint_filter")

    @endpoint_filter.setter
    def endpoint_filter(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "endpoint_filter", value)

    @property
    @pulumi.getter
    def labels(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Optional. Set of label tags associated with the ServiceBinding resource.
        """
        return pulumi.get(self, "labels")

    @labels.setter
    def labels(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "labels", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the ServiceBinding resource. It matches pattern `projects/*/locations/global/serviceBindings/service_binding_name>`.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def project(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "project")

    @project.setter
    def project(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "project", value)


class ServiceBinding(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 endpoint_filter: Optional[pulumi.Input[str]] = None,
                 labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 service: Optional[pulumi.Input[str]] = None,
                 service_binding_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Creates a new ServiceBinding in a given project and location.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: Optional. A free-text description of the resource. Max length 1024 characters.
        :param pulumi.Input[str] endpoint_filter: Optional. The endpoint filter associated with the Service Binding. The syntax is described in http://cloud/service-directory/docs/reference/rpc/google.cloud.servicedirectory.v1#google.cloud.servicedirectory.v1.ResolveServiceRequest
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: Optional. Set of label tags associated with the ServiceBinding resource.
        :param pulumi.Input[str] name: Name of the ServiceBinding resource. It matches pattern `projects/*/locations/global/serviceBindings/service_binding_name>`.
        :param pulumi.Input[str] service: The full service directory service name of the format /projects/*/locations/*/namespaces/*/services/*
        :param pulumi.Input[str] service_binding_id: Required. Short name of the ServiceBinding resource to be created.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ServiceBindingArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Creates a new ServiceBinding in a given project and location.

        :param str resource_name: The name of the resource.
        :param ServiceBindingArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ServiceBindingArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 endpoint_filter: Optional[pulumi.Input[str]] = None,
                 labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 service: Optional[pulumi.Input[str]] = None,
                 service_binding_id: Optional[pulumi.Input[str]] = None,
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
            __props__ = ServiceBindingArgs.__new__(ServiceBindingArgs)

            __props__.__dict__["description"] = description
            __props__.__dict__["endpoint_filter"] = endpoint_filter
            __props__.__dict__["labels"] = labels
            __props__.__dict__["location"] = location
            __props__.__dict__["name"] = name
            __props__.__dict__["project"] = project
            if service is None and not opts.urn:
                raise TypeError("Missing required property 'service'")
            __props__.__dict__["service"] = service
            if service_binding_id is None and not opts.urn:
                raise TypeError("Missing required property 'service_binding_id'")
            __props__.__dict__["service_binding_id"] = service_binding_id
            __props__.__dict__["create_time"] = None
            __props__.__dict__["update_time"] = None
        super(ServiceBinding, __self__).__init__(
            'google-native:networkservices/v1beta1:ServiceBinding',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ServiceBinding':
        """
        Get an existing ServiceBinding resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ServiceBindingArgs.__new__(ServiceBindingArgs)

        __props__.__dict__["create_time"] = None
        __props__.__dict__["description"] = None
        __props__.__dict__["endpoint_filter"] = None
        __props__.__dict__["labels"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["service"] = None
        __props__.__dict__["update_time"] = None
        return ServiceBinding(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> pulumi.Output[str]:
        """
        The timestamp when the resource was created.
        """
        return pulumi.get(self, "create_time")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[str]:
        """
        Optional. A free-text description of the resource. Max length 1024 characters.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="endpointFilter")
    def endpoint_filter(self) -> pulumi.Output[str]:
        """
        Optional. The endpoint filter associated with the Service Binding. The syntax is described in http://cloud/service-directory/docs/reference/rpc/google.cloud.servicedirectory.v1#google.cloud.servicedirectory.v1.ResolveServiceRequest
        """
        return pulumi.get(self, "endpoint_filter")

    @property
    @pulumi.getter
    def labels(self) -> pulumi.Output[Mapping[str, str]]:
        """
        Optional. Set of label tags associated with the ServiceBinding resource.
        """
        return pulumi.get(self, "labels")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Name of the ServiceBinding resource. It matches pattern `projects/*/locations/global/serviceBindings/service_binding_name>`.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def service(self) -> pulumi.Output[str]:
        """
        The full service directory service name of the format /projects/*/locations/*/namespaces/*/services/*
        """
        return pulumi.get(self, "service")

    @property
    @pulumi.getter(name="updateTime")
    def update_time(self) -> pulumi.Output[str]:
        """
        The timestamp when the resource was updated.
        """
        return pulumi.get(self, "update_time")

