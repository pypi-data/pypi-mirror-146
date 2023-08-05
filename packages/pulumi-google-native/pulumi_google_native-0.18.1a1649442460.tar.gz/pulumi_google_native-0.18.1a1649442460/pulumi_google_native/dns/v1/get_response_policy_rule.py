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
    'GetResponsePolicyRuleResult',
    'AwaitableGetResponsePolicyRuleResult',
    'get_response_policy_rule',
    'get_response_policy_rule_output',
]

@pulumi.output_type
class GetResponsePolicyRuleResult:
    def __init__(__self__, behavior=None, dns_name=None, kind=None, local_data=None, rule_name=None):
        if behavior and not isinstance(behavior, str):
            raise TypeError("Expected argument 'behavior' to be a str")
        pulumi.set(__self__, "behavior", behavior)
        if dns_name and not isinstance(dns_name, str):
            raise TypeError("Expected argument 'dns_name' to be a str")
        pulumi.set(__self__, "dns_name", dns_name)
        if kind and not isinstance(kind, str):
            raise TypeError("Expected argument 'kind' to be a str")
        pulumi.set(__self__, "kind", kind)
        if local_data and not isinstance(local_data, dict):
            raise TypeError("Expected argument 'local_data' to be a dict")
        pulumi.set(__self__, "local_data", local_data)
        if rule_name and not isinstance(rule_name, str):
            raise TypeError("Expected argument 'rule_name' to be a str")
        pulumi.set(__self__, "rule_name", rule_name)

    @property
    @pulumi.getter
    def behavior(self) -> str:
        """
        Answer this query with a behavior rather than DNS data.
        """
        return pulumi.get(self, "behavior")

    @property
    @pulumi.getter(name="dnsName")
    def dns_name(self) -> str:
        """
        The DNS name (wildcard or exact) to apply this rule to. Must be unique within the Response Policy Rule.
        """
        return pulumi.get(self, "dns_name")

    @property
    @pulumi.getter
    def kind(self) -> str:
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter(name="localData")
    def local_data(self) -> 'outputs.ResponsePolicyRuleLocalDataResponse':
        """
        Answer this query directly with DNS data. These ResourceRecordSets override any other DNS behavior for the matched name; in particular they override private zones, the public internet, and GCP internal DNS. No SOA nor NS types are allowed.
        """
        return pulumi.get(self, "local_data")

    @property
    @pulumi.getter(name="ruleName")
    def rule_name(self) -> str:
        """
        An identifier for this rule. Must be unique with the ResponsePolicy.
        """
        return pulumi.get(self, "rule_name")


class AwaitableGetResponsePolicyRuleResult(GetResponsePolicyRuleResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetResponsePolicyRuleResult(
            behavior=self.behavior,
            dns_name=self.dns_name,
            kind=self.kind,
            local_data=self.local_data,
            rule_name=self.rule_name)


def get_response_policy_rule(client_operation_id: Optional[str] = None,
                             project: Optional[str] = None,
                             response_policy: Optional[str] = None,
                             response_policy_rule: Optional[str] = None,
                             opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetResponsePolicyRuleResult:
    """
    Fetches the representation of an existing Response Policy Rule.
    """
    __args__ = dict()
    __args__['clientOperationId'] = client_operation_id
    __args__['project'] = project
    __args__['responsePolicy'] = response_policy
    __args__['responsePolicyRule'] = response_policy_rule
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('google-native:dns/v1:getResponsePolicyRule', __args__, opts=opts, typ=GetResponsePolicyRuleResult).value

    return AwaitableGetResponsePolicyRuleResult(
        behavior=__ret__.behavior,
        dns_name=__ret__.dns_name,
        kind=__ret__.kind,
        local_data=__ret__.local_data,
        rule_name=__ret__.rule_name)


@_utilities.lift_output_func(get_response_policy_rule)
def get_response_policy_rule_output(client_operation_id: Optional[pulumi.Input[Optional[str]]] = None,
                                    project: Optional[pulumi.Input[Optional[str]]] = None,
                                    response_policy: Optional[pulumi.Input[str]] = None,
                                    response_policy_rule: Optional[pulumi.Input[str]] = None,
                                    opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetResponsePolicyRuleResult]:
    """
    Fetches the representation of an existing Response Policy Rule.
    """
    ...
