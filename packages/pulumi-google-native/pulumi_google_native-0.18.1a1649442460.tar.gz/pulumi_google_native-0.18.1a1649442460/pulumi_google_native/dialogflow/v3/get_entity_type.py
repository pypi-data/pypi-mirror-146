# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs

__all__ = [
    'GetEntityTypeResult',
    'AwaitableGetEntityTypeResult',
    'get_entity_type',
    'get_entity_type_output',
]

@pulumi.output_type
class GetEntityTypeResult:
    def __init__(__self__, auto_expansion_mode=None, display_name=None, enable_fuzzy_extraction=None, entities=None, excluded_phrases=None, kind=None, name=None, redact=None):
        if auto_expansion_mode and not isinstance(auto_expansion_mode, str):
            raise TypeError("Expected argument 'auto_expansion_mode' to be a str")
        pulumi.set(__self__, "auto_expansion_mode", auto_expansion_mode)
        if display_name and not isinstance(display_name, str):
            raise TypeError("Expected argument 'display_name' to be a str")
        pulumi.set(__self__, "display_name", display_name)
        if enable_fuzzy_extraction and not isinstance(enable_fuzzy_extraction, bool):
            raise TypeError("Expected argument 'enable_fuzzy_extraction' to be a bool")
        pulumi.set(__self__, "enable_fuzzy_extraction", enable_fuzzy_extraction)
        if entities and not isinstance(entities, list):
            raise TypeError("Expected argument 'entities' to be a list")
        pulumi.set(__self__, "entities", entities)
        if excluded_phrases and not isinstance(excluded_phrases, list):
            raise TypeError("Expected argument 'excluded_phrases' to be a list")
        pulumi.set(__self__, "excluded_phrases", excluded_phrases)
        if kind and not isinstance(kind, str):
            raise TypeError("Expected argument 'kind' to be a str")
        pulumi.set(__self__, "kind", kind)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if redact and not isinstance(redact, bool):
            raise TypeError("Expected argument 'redact' to be a bool")
        pulumi.set(__self__, "redact", redact)

    @property
    @pulumi.getter(name="autoExpansionMode")
    def auto_expansion_mode(self) -> str:
        """
        Indicates whether the entity type can be automatically expanded.
        """
        return pulumi.get(self, "auto_expansion_mode")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> str:
        """
        The human-readable name of the entity type, unique within the agent.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter(name="enableFuzzyExtraction")
    def enable_fuzzy_extraction(self) -> bool:
        """
        Enables fuzzy entity extraction during classification.
        """
        return pulumi.get(self, "enable_fuzzy_extraction")

    @property
    @pulumi.getter
    def entities(self) -> Sequence['outputs.GoogleCloudDialogflowCxV3EntityTypeEntityResponse']:
        """
        The collection of entity entries associated with the entity type.
        """
        return pulumi.get(self, "entities")

    @property
    @pulumi.getter(name="excludedPhrases")
    def excluded_phrases(self) -> Sequence['outputs.GoogleCloudDialogflowCxV3EntityTypeExcludedPhraseResponse']:
        """
        Collection of exceptional words and phrases that shouldn't be matched. For example, if you have a size entity type with entry `giant`(an adjective), you might consider adding `giants`(a noun) as an exclusion. If the kind of entity type is `KIND_MAP`, then the phrases specified by entities and excluded phrases should be mutually exclusive.
        """
        return pulumi.get(self, "excluded_phrases")

    @property
    @pulumi.getter
    def kind(self) -> str:
        """
        Indicates the kind of entity type.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The unique identifier of the entity type. Required for EntityTypes.UpdateEntityType. Format: `projects//locations//agents//entityTypes/`.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def redact(self) -> bool:
        """
        Indicates whether parameters of the entity type should be redacted in log. If redaction is enabled, page parameters and intent parameters referring to the entity type will be replaced by parameter name when logging.
        """
        return pulumi.get(self, "redact")


class AwaitableGetEntityTypeResult(GetEntityTypeResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetEntityTypeResult(
            auto_expansion_mode=self.auto_expansion_mode,
            display_name=self.display_name,
            enable_fuzzy_extraction=self.enable_fuzzy_extraction,
            entities=self.entities,
            excluded_phrases=self.excluded_phrases,
            kind=self.kind,
            name=self.name,
            redact=self.redact)


def get_entity_type(agent_id: Optional[str] = None,
                    entity_type_id: Optional[str] = None,
                    language_code: Optional[str] = None,
                    location: Optional[str] = None,
                    project: Optional[str] = None,
                    opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetEntityTypeResult:
    """
    Retrieves the specified entity type.
    """
    __args__ = dict()
    __args__['agentId'] = agent_id
    __args__['entityTypeId'] = entity_type_id
    __args__['languageCode'] = language_code
    __args__['location'] = location
    __args__['project'] = project
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('google-native:dialogflow/v3:getEntityType', __args__, opts=opts, typ=GetEntityTypeResult).value

    return AwaitableGetEntityTypeResult(
        auto_expansion_mode=__ret__.auto_expansion_mode,
        display_name=__ret__.display_name,
        enable_fuzzy_extraction=__ret__.enable_fuzzy_extraction,
        entities=__ret__.entities,
        excluded_phrases=__ret__.excluded_phrases,
        kind=__ret__.kind,
        name=__ret__.name,
        redact=__ret__.redact)


@_utilities.lift_output_func(get_entity_type)
def get_entity_type_output(agent_id: Optional[pulumi.Input[str]] = None,
                           entity_type_id: Optional[pulumi.Input[str]] = None,
                           language_code: Optional[pulumi.Input[Optional[str]]] = None,
                           location: Optional[pulumi.Input[str]] = None,
                           project: Optional[pulumi.Input[Optional[str]]] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetEntityTypeResult]:
    """
    Retrieves the specified entity type.
    """
    ...
