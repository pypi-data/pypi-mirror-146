# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities

__all__ = ['TagKeyArgs', 'TagKey']

@pulumi.input_type
class TagKeyArgs:
    def __init__(__self__, *,
                 short_name: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None,
                 etag: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 parent: Optional[pulumi.Input[str]] = None,
                 validate_only: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a TagKey resource.
        :param pulumi.Input[str] short_name: Immutable. The user friendly name for a TagKey. The short name should be unique for TagKeys within the same tag namespace. The short name must be 1-63 characters, beginning and ending with an alphanumeric character ([a-z0-9A-Z]) with dashes (-), underscores (_), dots (.), and alphanumerics between.
        :param pulumi.Input[str] description: Optional. User-assigned description of the TagKey. Must not exceed 256 characters. Read-write.
        :param pulumi.Input[str] etag: Optional. Entity tag which users can pass to prevent race conditions. This field is always set in server responses. See UpdateTagKeyRequest for details.
        :param pulumi.Input[str] name: Immutable. The resource name for a TagKey. Must be in the format `tagKeys/{tag_key_id}`, where `tag_key_id` is the generated numeric id for the TagKey.
        :param pulumi.Input[str] parent: Immutable. The resource name of the new TagKey's parent. Must be of the form `organizations/{org_id}`.
        :param pulumi.Input[str] validate_only: Optional. Set to true to perform validations necessary for creating the resource, but not actually perform the action.
        """
        pulumi.set(__self__, "short_name", short_name)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if etag is not None:
            pulumi.set(__self__, "etag", etag)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if parent is not None:
            pulumi.set(__self__, "parent", parent)
        if validate_only is not None:
            pulumi.set(__self__, "validate_only", validate_only)

    @property
    @pulumi.getter(name="shortName")
    def short_name(self) -> pulumi.Input[str]:
        """
        Immutable. The user friendly name for a TagKey. The short name should be unique for TagKeys within the same tag namespace. The short name must be 1-63 characters, beginning and ending with an alphanumeric character ([a-z0-9A-Z]) with dashes (-), underscores (_), dots (.), and alphanumerics between.
        """
        return pulumi.get(self, "short_name")

    @short_name.setter
    def short_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "short_name", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Optional. User-assigned description of the TagKey. Must not exceed 256 characters. Read-write.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def etag(self) -> Optional[pulumi.Input[str]]:
        """
        Optional. Entity tag which users can pass to prevent race conditions. This field is always set in server responses. See UpdateTagKeyRequest for details.
        """
        return pulumi.get(self, "etag")

    @etag.setter
    def etag(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "etag", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Immutable. The resource name for a TagKey. Must be in the format `tagKeys/{tag_key_id}`, where `tag_key_id` is the generated numeric id for the TagKey.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def parent(self) -> Optional[pulumi.Input[str]]:
        """
        Immutable. The resource name of the new TagKey's parent. Must be of the form `organizations/{org_id}`.
        """
        return pulumi.get(self, "parent")

    @parent.setter
    def parent(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "parent", value)

    @property
    @pulumi.getter(name="validateOnly")
    def validate_only(self) -> Optional[pulumi.Input[str]]:
        """
        Optional. Set to true to perform validations necessary for creating the resource, but not actually perform the action.
        """
        return pulumi.get(self, "validate_only")

    @validate_only.setter
    def validate_only(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "validate_only", value)


class TagKey(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 etag: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 parent: Optional[pulumi.Input[str]] = None,
                 short_name: Optional[pulumi.Input[str]] = None,
                 validate_only: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Creates a new TagKey. If another request with the same parameters is sent while the original request is in process, the second request will receive an error. A maximum of 300 TagKeys can exist under a parent at any given time.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: Optional. User-assigned description of the TagKey. Must not exceed 256 characters. Read-write.
        :param pulumi.Input[str] etag: Optional. Entity tag which users can pass to prevent race conditions. This field is always set in server responses. See UpdateTagKeyRequest for details.
        :param pulumi.Input[str] name: Immutable. The resource name for a TagKey. Must be in the format `tagKeys/{tag_key_id}`, where `tag_key_id` is the generated numeric id for the TagKey.
        :param pulumi.Input[str] parent: Immutable. The resource name of the new TagKey's parent. Must be of the form `organizations/{org_id}`.
        :param pulumi.Input[str] short_name: Immutable. The user friendly name for a TagKey. The short name should be unique for TagKeys within the same tag namespace. The short name must be 1-63 characters, beginning and ending with an alphanumeric character ([a-z0-9A-Z]) with dashes (-), underscores (_), dots (.), and alphanumerics between.
        :param pulumi.Input[str] validate_only: Optional. Set to true to perform validations necessary for creating the resource, but not actually perform the action.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: TagKeyArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Creates a new TagKey. If another request with the same parameters is sent while the original request is in process, the second request will receive an error. A maximum of 300 TagKeys can exist under a parent at any given time.

        :param str resource_name: The name of the resource.
        :param TagKeyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(TagKeyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 etag: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 parent: Optional[pulumi.Input[str]] = None,
                 short_name: Optional[pulumi.Input[str]] = None,
                 validate_only: Optional[pulumi.Input[str]] = None,
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
            __props__ = TagKeyArgs.__new__(TagKeyArgs)

            __props__.__dict__["description"] = description
            __props__.__dict__["etag"] = etag
            __props__.__dict__["name"] = name
            __props__.__dict__["parent"] = parent
            if short_name is None and not opts.urn:
                raise TypeError("Missing required property 'short_name'")
            __props__.__dict__["short_name"] = short_name
            __props__.__dict__["validate_only"] = validate_only
            __props__.__dict__["create_time"] = None
            __props__.__dict__["namespaced_name"] = None
            __props__.__dict__["update_time"] = None
        super(TagKey, __self__).__init__(
            'google-native:cloudresourcemanager/v3:TagKey',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'TagKey':
        """
        Get an existing TagKey resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = TagKeyArgs.__new__(TagKeyArgs)

        __props__.__dict__["create_time"] = None
        __props__.__dict__["description"] = None
        __props__.__dict__["etag"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["namespaced_name"] = None
        __props__.__dict__["parent"] = None
        __props__.__dict__["short_name"] = None
        __props__.__dict__["update_time"] = None
        return TagKey(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> pulumi.Output[str]:
        """
        Creation time.
        """
        return pulumi.get(self, "create_time")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[str]:
        """
        Optional. User-assigned description of the TagKey. Must not exceed 256 characters. Read-write.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[str]:
        """
        Optional. Entity tag which users can pass to prevent race conditions. This field is always set in server responses. See UpdateTagKeyRequest for details.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Immutable. The resource name for a TagKey. Must be in the format `tagKeys/{tag_key_id}`, where `tag_key_id` is the generated numeric id for the TagKey.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="namespacedName")
    def namespaced_name(self) -> pulumi.Output[str]:
        """
        Immutable. Namespaced name of the TagKey.
        """
        return pulumi.get(self, "namespaced_name")

    @property
    @pulumi.getter
    def parent(self) -> pulumi.Output[str]:
        """
        Immutable. The resource name of the new TagKey's parent. Must be of the form `organizations/{org_id}`.
        """
        return pulumi.get(self, "parent")

    @property
    @pulumi.getter(name="shortName")
    def short_name(self) -> pulumi.Output[str]:
        """
        Immutable. The user friendly name for a TagKey. The short name should be unique for TagKeys within the same tag namespace. The short name must be 1-63 characters, beginning and ending with an alphanumeric character ([a-z0-9A-Z]) with dashes (-), underscores (_), dots (.), and alphanumerics between.
        """
        return pulumi.get(self, "short_name")

    @property
    @pulumi.getter(name="updateTime")
    def update_time(self) -> pulumi.Output[str]:
        """
        Update time.
        """
        return pulumi.get(self, "update_time")

