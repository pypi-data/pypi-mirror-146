# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from ._enums import *

__all__ = ['AttributeDefinitionArgs', 'AttributeDefinition']

@pulumi.input_type
class AttributeDefinitionArgs:
    def __init__(__self__, *,
                 allowed_values: pulumi.Input[Sequence[pulumi.Input[str]]],
                 attribute_definition_id: pulumi.Input[str],
                 category: pulumi.Input['AttributeDefinitionCategory'],
                 consent_store_id: pulumi.Input[str],
                 dataset_id: pulumi.Input[str],
                 consent_default_values: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 data_mapping_default_value: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a AttributeDefinition resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] allowed_values: Possible values for the attribute. The number of allowed values must not exceed 500. An empty list is invalid. The list can only be expanded after creation.
        :param pulumi.Input[str] attribute_definition_id: Required. The ID of the Attribute definition to create. The string must match the following regex: `_a-zA-Z{0,255}` and must not be a reserved keyword within the Common Expression Language as listed on https://github.com/google/cel-spec/blob/master/doc/langdef.md.
        :param pulumi.Input['AttributeDefinitionCategory'] category: The category of the attribute. The value of this field cannot be changed after creation.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] consent_default_values: Optional. Default values of the attribute in Consents. If no default values are specified, it defaults to an empty value.
        :param pulumi.Input[str] data_mapping_default_value: Optional. Default value of the attribute in User data mappings. If no default value is specified, it defaults to an empty value. This field is only applicable to attributes of the category `RESOURCE`.
        :param pulumi.Input[str] description: Optional. A description of the attribute.
        :param pulumi.Input[str] name: Resource name of the Attribute definition, of the form `projects/{project_id}/locations/{location_id}/datasets/{dataset_id}/consentStores/{consent_store_id}/attributeDefinitions/{attribute_definition_id}`. Cannot be changed after creation.
        """
        pulumi.set(__self__, "allowed_values", allowed_values)
        pulumi.set(__self__, "attribute_definition_id", attribute_definition_id)
        pulumi.set(__self__, "category", category)
        pulumi.set(__self__, "consent_store_id", consent_store_id)
        pulumi.set(__self__, "dataset_id", dataset_id)
        if consent_default_values is not None:
            pulumi.set(__self__, "consent_default_values", consent_default_values)
        if data_mapping_default_value is not None:
            pulumi.set(__self__, "data_mapping_default_value", data_mapping_default_value)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if project is not None:
            pulumi.set(__self__, "project", project)

    @property
    @pulumi.getter(name="allowedValues")
    def allowed_values(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        Possible values for the attribute. The number of allowed values must not exceed 500. An empty list is invalid. The list can only be expanded after creation.
        """
        return pulumi.get(self, "allowed_values")

    @allowed_values.setter
    def allowed_values(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "allowed_values", value)

    @property
    @pulumi.getter(name="attributeDefinitionId")
    def attribute_definition_id(self) -> pulumi.Input[str]:
        """
        Required. The ID of the Attribute definition to create. The string must match the following regex: `_a-zA-Z{0,255}` and must not be a reserved keyword within the Common Expression Language as listed on https://github.com/google/cel-spec/blob/master/doc/langdef.md.
        """
        return pulumi.get(self, "attribute_definition_id")

    @attribute_definition_id.setter
    def attribute_definition_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "attribute_definition_id", value)

    @property
    @pulumi.getter
    def category(self) -> pulumi.Input['AttributeDefinitionCategory']:
        """
        The category of the attribute. The value of this field cannot be changed after creation.
        """
        return pulumi.get(self, "category")

    @category.setter
    def category(self, value: pulumi.Input['AttributeDefinitionCategory']):
        pulumi.set(self, "category", value)

    @property
    @pulumi.getter(name="consentStoreId")
    def consent_store_id(self) -> pulumi.Input[str]:
        return pulumi.get(self, "consent_store_id")

    @consent_store_id.setter
    def consent_store_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "consent_store_id", value)

    @property
    @pulumi.getter(name="datasetId")
    def dataset_id(self) -> pulumi.Input[str]:
        return pulumi.get(self, "dataset_id")

    @dataset_id.setter
    def dataset_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "dataset_id", value)

    @property
    @pulumi.getter(name="consentDefaultValues")
    def consent_default_values(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Optional. Default values of the attribute in Consents. If no default values are specified, it defaults to an empty value.
        """
        return pulumi.get(self, "consent_default_values")

    @consent_default_values.setter
    def consent_default_values(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "consent_default_values", value)

    @property
    @pulumi.getter(name="dataMappingDefaultValue")
    def data_mapping_default_value(self) -> Optional[pulumi.Input[str]]:
        """
        Optional. Default value of the attribute in User data mappings. If no default value is specified, it defaults to an empty value. This field is only applicable to attributes of the category `RESOURCE`.
        """
        return pulumi.get(self, "data_mapping_default_value")

    @data_mapping_default_value.setter
    def data_mapping_default_value(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "data_mapping_default_value", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Optional. A description of the attribute.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

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
        Resource name of the Attribute definition, of the form `projects/{project_id}/locations/{location_id}/datasets/{dataset_id}/consentStores/{consent_store_id}/attributeDefinitions/{attribute_definition_id}`. Cannot be changed after creation.
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


class AttributeDefinition(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 allowed_values: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 attribute_definition_id: Optional[pulumi.Input[str]] = None,
                 category: Optional[pulumi.Input['AttributeDefinitionCategory']] = None,
                 consent_default_values: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 consent_store_id: Optional[pulumi.Input[str]] = None,
                 data_mapping_default_value: Optional[pulumi.Input[str]] = None,
                 dataset_id: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Creates a new Attribute definition in the parent consent store.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] allowed_values: Possible values for the attribute. The number of allowed values must not exceed 500. An empty list is invalid. The list can only be expanded after creation.
        :param pulumi.Input[str] attribute_definition_id: Required. The ID of the Attribute definition to create. The string must match the following regex: `_a-zA-Z{0,255}` and must not be a reserved keyword within the Common Expression Language as listed on https://github.com/google/cel-spec/blob/master/doc/langdef.md.
        :param pulumi.Input['AttributeDefinitionCategory'] category: The category of the attribute. The value of this field cannot be changed after creation.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] consent_default_values: Optional. Default values of the attribute in Consents. If no default values are specified, it defaults to an empty value.
        :param pulumi.Input[str] data_mapping_default_value: Optional. Default value of the attribute in User data mappings. If no default value is specified, it defaults to an empty value. This field is only applicable to attributes of the category `RESOURCE`.
        :param pulumi.Input[str] description: Optional. A description of the attribute.
        :param pulumi.Input[str] name: Resource name of the Attribute definition, of the form `projects/{project_id}/locations/{location_id}/datasets/{dataset_id}/consentStores/{consent_store_id}/attributeDefinitions/{attribute_definition_id}`. Cannot be changed after creation.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: AttributeDefinitionArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Creates a new Attribute definition in the parent consent store.

        :param str resource_name: The name of the resource.
        :param AttributeDefinitionArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AttributeDefinitionArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 allowed_values: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 attribute_definition_id: Optional[pulumi.Input[str]] = None,
                 category: Optional[pulumi.Input['AttributeDefinitionCategory']] = None,
                 consent_default_values: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 consent_store_id: Optional[pulumi.Input[str]] = None,
                 data_mapping_default_value: Optional[pulumi.Input[str]] = None,
                 dataset_id: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
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
            __props__ = AttributeDefinitionArgs.__new__(AttributeDefinitionArgs)

            if allowed_values is None and not opts.urn:
                raise TypeError("Missing required property 'allowed_values'")
            __props__.__dict__["allowed_values"] = allowed_values
            if attribute_definition_id is None and not opts.urn:
                raise TypeError("Missing required property 'attribute_definition_id'")
            __props__.__dict__["attribute_definition_id"] = attribute_definition_id
            if category is None and not opts.urn:
                raise TypeError("Missing required property 'category'")
            __props__.__dict__["category"] = category
            __props__.__dict__["consent_default_values"] = consent_default_values
            if consent_store_id is None and not opts.urn:
                raise TypeError("Missing required property 'consent_store_id'")
            __props__.__dict__["consent_store_id"] = consent_store_id
            __props__.__dict__["data_mapping_default_value"] = data_mapping_default_value
            if dataset_id is None and not opts.urn:
                raise TypeError("Missing required property 'dataset_id'")
            __props__.__dict__["dataset_id"] = dataset_id
            __props__.__dict__["description"] = description
            __props__.__dict__["location"] = location
            __props__.__dict__["name"] = name
            __props__.__dict__["project"] = project
        super(AttributeDefinition, __self__).__init__(
            'google-native:healthcare/v1:AttributeDefinition',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'AttributeDefinition':
        """
        Get an existing AttributeDefinition resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = AttributeDefinitionArgs.__new__(AttributeDefinitionArgs)

        __props__.__dict__["allowed_values"] = None
        __props__.__dict__["category"] = None
        __props__.__dict__["consent_default_values"] = None
        __props__.__dict__["data_mapping_default_value"] = None
        __props__.__dict__["description"] = None
        __props__.__dict__["name"] = None
        return AttributeDefinition(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="allowedValues")
    def allowed_values(self) -> pulumi.Output[Sequence[str]]:
        """
        Possible values for the attribute. The number of allowed values must not exceed 500. An empty list is invalid. The list can only be expanded after creation.
        """
        return pulumi.get(self, "allowed_values")

    @property
    @pulumi.getter
    def category(self) -> pulumi.Output[str]:
        """
        The category of the attribute. The value of this field cannot be changed after creation.
        """
        return pulumi.get(self, "category")

    @property
    @pulumi.getter(name="consentDefaultValues")
    def consent_default_values(self) -> pulumi.Output[Sequence[str]]:
        """
        Optional. Default values of the attribute in Consents. If no default values are specified, it defaults to an empty value.
        """
        return pulumi.get(self, "consent_default_values")

    @property
    @pulumi.getter(name="dataMappingDefaultValue")
    def data_mapping_default_value(self) -> pulumi.Output[str]:
        """
        Optional. Default value of the attribute in User data mappings. If no default value is specified, it defaults to an empty value. This field is only applicable to attributes of the category `RESOURCE`.
        """
        return pulumi.get(self, "data_mapping_default_value")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[str]:
        """
        Optional. A description of the attribute.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name of the Attribute definition, of the form `projects/{project_id}/locations/{location_id}/datasets/{dataset_id}/consentStores/{consent_store_id}/attributeDefinitions/{attribute_definition_id}`. Cannot be changed after creation.
        """
        return pulumi.get(self, "name")

