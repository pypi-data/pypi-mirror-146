# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from ._enums import *

__all__ = [
    'BasicLevelArgs',
    'ConditionArgs',
    'CustomLevelArgs',
    'DevicePolicyArgs',
    'ExprArgs',
    'OsConstraintArgs',
]

@pulumi.input_type
class BasicLevelArgs:
    def __init__(__self__, *,
                 conditions: pulumi.Input[Sequence[pulumi.Input['ConditionArgs']]],
                 combining_function: Optional[pulumi.Input['BasicLevelCombiningFunction']] = None):
        """
        `BasicLevel` is an `AccessLevel` using a set of recommended features.
        :param pulumi.Input[Sequence[pulumi.Input['ConditionArgs']]] conditions: A list of requirements for the `AccessLevel` to be granted.
        :param pulumi.Input['BasicLevelCombiningFunction'] combining_function: How the `conditions` list should be combined to determine if a request is granted this `AccessLevel`. If AND is used, each `Condition` in `conditions` must be satisfied for the `AccessLevel` to be applied. If OR is used, at least one `Condition` in `conditions` must be satisfied for the `AccessLevel` to be applied. Default behavior is AND.
        """
        pulumi.set(__self__, "conditions", conditions)
        if combining_function is not None:
            pulumi.set(__self__, "combining_function", combining_function)

    @property
    @pulumi.getter
    def conditions(self) -> pulumi.Input[Sequence[pulumi.Input['ConditionArgs']]]:
        """
        A list of requirements for the `AccessLevel` to be granted.
        """
        return pulumi.get(self, "conditions")

    @conditions.setter
    def conditions(self, value: pulumi.Input[Sequence[pulumi.Input['ConditionArgs']]]):
        pulumi.set(self, "conditions", value)

    @property
    @pulumi.getter(name="combiningFunction")
    def combining_function(self) -> Optional[pulumi.Input['BasicLevelCombiningFunction']]:
        """
        How the `conditions` list should be combined to determine if a request is granted this `AccessLevel`. If AND is used, each `Condition` in `conditions` must be satisfied for the `AccessLevel` to be applied. If OR is used, at least one `Condition` in `conditions` must be satisfied for the `AccessLevel` to be applied. Default behavior is AND.
        """
        return pulumi.get(self, "combining_function")

    @combining_function.setter
    def combining_function(self, value: Optional[pulumi.Input['BasicLevelCombiningFunction']]):
        pulumi.set(self, "combining_function", value)


@pulumi.input_type
class ConditionArgs:
    def __init__(__self__, *,
                 device_policy: Optional[pulumi.Input['DevicePolicyArgs']] = None,
                 ip_subnetworks: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 members: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 negate: Optional[pulumi.Input[bool]] = None,
                 regions: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 required_access_levels: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        A condition necessary for an `AccessLevel` to be granted. The Condition is an AND over its fields. So a Condition is true if: 1) the request IP is from one of the listed subnetworks AND 2) the originating device complies with the listed device policy AND 3) all listed access levels are granted AND 4) the request was sent at a time allowed by the DateTimeRestriction.
        :param pulumi.Input['DevicePolicyArgs'] device_policy: Device specific restrictions, all restrictions must hold for the Condition to be true. If not specified, all devices are allowed.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] ip_subnetworks: CIDR block IP subnetwork specification. May be IPv4 or IPv6. Note that for a CIDR IP address block, the specified IP address portion must be properly truncated (i.e. all the host bits must be zero) or the input is considered malformed. For example, "192.0.2.0/24" is accepted but "192.0.2.1/24" is not. Similarly, for IPv6, "2001:db8::/32" is accepted whereas "2001:db8::1/32" is not. The originating IP of a request must be in one of the listed subnets in order for this Condition to be true. If empty, all IP addresses are allowed.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] members: The request must be made by one of the provided user or service accounts. Groups are not supported. Syntax: `user:{emailid}` `serviceAccount:{emailid}` If not specified, a request may come from any user.
        :param pulumi.Input[bool] negate: Whether to negate the Condition. If true, the Condition becomes a NAND over its non-empty fields, each field must be false for the Condition overall to be satisfied. Defaults to false.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] regions: The request must originate from one of the provided countries/regions. Must be valid ISO 3166-1 alpha-2 codes.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] required_access_levels: A list of other access levels defined in the same `Policy`, referenced by resource name. Referencing an `AccessLevel` which does not exist is an error. All access levels listed must be granted for the Condition to be true. Example: "`accessPolicies/MY_POLICY/accessLevels/LEVEL_NAME"`
        """
        if device_policy is not None:
            pulumi.set(__self__, "device_policy", device_policy)
        if ip_subnetworks is not None:
            pulumi.set(__self__, "ip_subnetworks", ip_subnetworks)
        if members is not None:
            pulumi.set(__self__, "members", members)
        if negate is not None:
            pulumi.set(__self__, "negate", negate)
        if regions is not None:
            pulumi.set(__self__, "regions", regions)
        if required_access_levels is not None:
            pulumi.set(__self__, "required_access_levels", required_access_levels)

    @property
    @pulumi.getter(name="devicePolicy")
    def device_policy(self) -> Optional[pulumi.Input['DevicePolicyArgs']]:
        """
        Device specific restrictions, all restrictions must hold for the Condition to be true. If not specified, all devices are allowed.
        """
        return pulumi.get(self, "device_policy")

    @device_policy.setter
    def device_policy(self, value: Optional[pulumi.Input['DevicePolicyArgs']]):
        pulumi.set(self, "device_policy", value)

    @property
    @pulumi.getter(name="ipSubnetworks")
    def ip_subnetworks(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        CIDR block IP subnetwork specification. May be IPv4 or IPv6. Note that for a CIDR IP address block, the specified IP address portion must be properly truncated (i.e. all the host bits must be zero) or the input is considered malformed. For example, "192.0.2.0/24" is accepted but "192.0.2.1/24" is not. Similarly, for IPv6, "2001:db8::/32" is accepted whereas "2001:db8::1/32" is not. The originating IP of a request must be in one of the listed subnets in order for this Condition to be true. If empty, all IP addresses are allowed.
        """
        return pulumi.get(self, "ip_subnetworks")

    @ip_subnetworks.setter
    def ip_subnetworks(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "ip_subnetworks", value)

    @property
    @pulumi.getter
    def members(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The request must be made by one of the provided user or service accounts. Groups are not supported. Syntax: `user:{emailid}` `serviceAccount:{emailid}` If not specified, a request may come from any user.
        """
        return pulumi.get(self, "members")

    @members.setter
    def members(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "members", value)

    @property
    @pulumi.getter
    def negate(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether to negate the Condition. If true, the Condition becomes a NAND over its non-empty fields, each field must be false for the Condition overall to be satisfied. Defaults to false.
        """
        return pulumi.get(self, "negate")

    @negate.setter
    def negate(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "negate", value)

    @property
    @pulumi.getter
    def regions(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The request must originate from one of the provided countries/regions. Must be valid ISO 3166-1 alpha-2 codes.
        """
        return pulumi.get(self, "regions")

    @regions.setter
    def regions(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "regions", value)

    @property
    @pulumi.getter(name="requiredAccessLevels")
    def required_access_levels(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of other access levels defined in the same `Policy`, referenced by resource name. Referencing an `AccessLevel` which does not exist is an error. All access levels listed must be granted for the Condition to be true. Example: "`accessPolicies/MY_POLICY/accessLevels/LEVEL_NAME"`
        """
        return pulumi.get(self, "required_access_levels")

    @required_access_levels.setter
    def required_access_levels(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "required_access_levels", value)


@pulumi.input_type
class CustomLevelArgs:
    def __init__(__self__, *,
                 expr: pulumi.Input['ExprArgs']):
        """
        `CustomLevel` is an `AccessLevel` using the Cloud Common Expression Language to represent the necessary conditions for the level to apply to a request. See CEL spec at: https://github.com/google/cel-spec
        :param pulumi.Input['ExprArgs'] expr: A Cloud CEL expression evaluating to a boolean.
        """
        pulumi.set(__self__, "expr", expr)

    @property
    @pulumi.getter
    def expr(self) -> pulumi.Input['ExprArgs']:
        """
        A Cloud CEL expression evaluating to a boolean.
        """
        return pulumi.get(self, "expr")

    @expr.setter
    def expr(self, value: pulumi.Input['ExprArgs']):
        pulumi.set(self, "expr", value)


@pulumi.input_type
class DevicePolicyArgs:
    def __init__(__self__, *,
                 allowed_device_management_levels: Optional[pulumi.Input[Sequence[pulumi.Input['DevicePolicyAllowedDeviceManagementLevelsItem']]]] = None,
                 allowed_encryption_statuses: Optional[pulumi.Input[Sequence[pulumi.Input['DevicePolicyAllowedEncryptionStatusesItem']]]] = None,
                 os_constraints: Optional[pulumi.Input[Sequence[pulumi.Input['OsConstraintArgs']]]] = None,
                 require_admin_approval: Optional[pulumi.Input[bool]] = None,
                 require_corp_owned: Optional[pulumi.Input[bool]] = None,
                 require_screenlock: Optional[pulumi.Input[bool]] = None):
        """
        `DevicePolicy` specifies device specific restrictions necessary to acquire a given access level. A `DevicePolicy` specifies requirements for requests from devices to be granted access levels, it does not do any enforcement on the device. `DevicePolicy` acts as an AND over all specified fields, and each repeated field is an OR over its elements. Any unset fields are ignored. For example, if the proto is { os_type : DESKTOP_WINDOWS, os_type : DESKTOP_LINUX, encryption_status: ENCRYPTED}, then the DevicePolicy will be true for requests originating from encrypted Linux desktops and encrypted Windows desktops.
        :param pulumi.Input[Sequence[pulumi.Input['DevicePolicyAllowedDeviceManagementLevelsItem']]] allowed_device_management_levels: Allowed device management levels, an empty list allows all management levels.
        :param pulumi.Input[Sequence[pulumi.Input['DevicePolicyAllowedEncryptionStatusesItem']]] allowed_encryption_statuses: Allowed encryptions statuses, an empty list allows all statuses.
        :param pulumi.Input[Sequence[pulumi.Input['OsConstraintArgs']]] os_constraints: Allowed OS versions, an empty list allows all types and all versions.
        :param pulumi.Input[bool] require_admin_approval: Whether the device needs to be approved by the customer admin.
        :param pulumi.Input[bool] require_corp_owned: Whether the device needs to be corp owned.
        :param pulumi.Input[bool] require_screenlock: Whether or not screenlock is required for the DevicePolicy to be true. Defaults to `false`.
        """
        if allowed_device_management_levels is not None:
            pulumi.set(__self__, "allowed_device_management_levels", allowed_device_management_levels)
        if allowed_encryption_statuses is not None:
            pulumi.set(__self__, "allowed_encryption_statuses", allowed_encryption_statuses)
        if os_constraints is not None:
            pulumi.set(__self__, "os_constraints", os_constraints)
        if require_admin_approval is not None:
            pulumi.set(__self__, "require_admin_approval", require_admin_approval)
        if require_corp_owned is not None:
            pulumi.set(__self__, "require_corp_owned", require_corp_owned)
        if require_screenlock is not None:
            pulumi.set(__self__, "require_screenlock", require_screenlock)

    @property
    @pulumi.getter(name="allowedDeviceManagementLevels")
    def allowed_device_management_levels(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['DevicePolicyAllowedDeviceManagementLevelsItem']]]]:
        """
        Allowed device management levels, an empty list allows all management levels.
        """
        return pulumi.get(self, "allowed_device_management_levels")

    @allowed_device_management_levels.setter
    def allowed_device_management_levels(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['DevicePolicyAllowedDeviceManagementLevelsItem']]]]):
        pulumi.set(self, "allowed_device_management_levels", value)

    @property
    @pulumi.getter(name="allowedEncryptionStatuses")
    def allowed_encryption_statuses(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['DevicePolicyAllowedEncryptionStatusesItem']]]]:
        """
        Allowed encryptions statuses, an empty list allows all statuses.
        """
        return pulumi.get(self, "allowed_encryption_statuses")

    @allowed_encryption_statuses.setter
    def allowed_encryption_statuses(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['DevicePolicyAllowedEncryptionStatusesItem']]]]):
        pulumi.set(self, "allowed_encryption_statuses", value)

    @property
    @pulumi.getter(name="osConstraints")
    def os_constraints(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['OsConstraintArgs']]]]:
        """
        Allowed OS versions, an empty list allows all types and all versions.
        """
        return pulumi.get(self, "os_constraints")

    @os_constraints.setter
    def os_constraints(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['OsConstraintArgs']]]]):
        pulumi.set(self, "os_constraints", value)

    @property
    @pulumi.getter(name="requireAdminApproval")
    def require_admin_approval(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether the device needs to be approved by the customer admin.
        """
        return pulumi.get(self, "require_admin_approval")

    @require_admin_approval.setter
    def require_admin_approval(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "require_admin_approval", value)

    @property
    @pulumi.getter(name="requireCorpOwned")
    def require_corp_owned(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether the device needs to be corp owned.
        """
        return pulumi.get(self, "require_corp_owned")

    @require_corp_owned.setter
    def require_corp_owned(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "require_corp_owned", value)

    @property
    @pulumi.getter(name="requireScreenlock")
    def require_screenlock(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether or not screenlock is required for the DevicePolicy to be true. Defaults to `false`.
        """
        return pulumi.get(self, "require_screenlock")

    @require_screenlock.setter
    def require_screenlock(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "require_screenlock", value)


@pulumi.input_type
class ExprArgs:
    def __init__(__self__, *,
                 description: Optional[pulumi.Input[str]] = None,
                 expression: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 title: Optional[pulumi.Input[str]] = None):
        """
        Represents a textual expression in the Common Expression Language (CEL) syntax. CEL is a C-like expression language. The syntax and semantics of CEL are documented at https://github.com/google/cel-spec. Example (Comparison): title: "Summary size limit" description: "Determines if a summary is less than 100 chars" expression: "document.summary.size() < 100" Example (Equality): title: "Requestor is owner" description: "Determines if requestor is the document owner" expression: "document.owner == request.auth.claims.email" Example (Logic): title: "Public documents" description: "Determine whether the document should be publicly visible" expression: "document.type != 'private' && document.type != 'internal'" Example (Data Manipulation): title: "Notification string" description: "Create a notification string with a timestamp." expression: "'New message received at ' + string(document.create_time)" The exact variables and functions that may be referenced within an expression are determined by the service that evaluates it. See the service documentation for additional information.
        :param pulumi.Input[str] description: Optional. Description of the expression. This is a longer text which describes the expression, e.g. when hovered over it in a UI.
        :param pulumi.Input[str] expression: Textual representation of an expression in Common Expression Language syntax.
        :param pulumi.Input[str] location: Optional. String indicating the location of the expression for error reporting, e.g. a file name and a position in the file.
        :param pulumi.Input[str] title: Optional. Title for the expression, i.e. a short string describing its purpose. This can be used e.g. in UIs which allow to enter the expression.
        """
        if description is not None:
            pulumi.set(__self__, "description", description)
        if expression is not None:
            pulumi.set(__self__, "expression", expression)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if title is not None:
            pulumi.set(__self__, "title", title)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Optional. Description of the expression. This is a longer text which describes the expression, e.g. when hovered over it in a UI.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def expression(self) -> Optional[pulumi.Input[str]]:
        """
        Textual representation of an expression in Common Expression Language syntax.
        """
        return pulumi.get(self, "expression")

    @expression.setter
    def expression(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "expression", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Optional. String indicating the location of the expression for error reporting, e.g. a file name and a position in the file.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def title(self) -> Optional[pulumi.Input[str]]:
        """
        Optional. Title for the expression, i.e. a short string describing its purpose. This can be used e.g. in UIs which allow to enter the expression.
        """
        return pulumi.get(self, "title")

    @title.setter
    def title(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "title", value)


@pulumi.input_type
class OsConstraintArgs:
    def __init__(__self__, *,
                 os_type: pulumi.Input['OsConstraintOsType'],
                 minimum_version: Optional[pulumi.Input[str]] = None,
                 require_verified_chrome_os: Optional[pulumi.Input[bool]] = None):
        """
        A restriction on the OS type and version of devices making requests.
        :param pulumi.Input['OsConstraintOsType'] os_type: The allowed OS type.
        :param pulumi.Input[str] minimum_version: The minimum allowed OS version. If not set, any version of this OS satisfies the constraint. Format: `"major.minor.patch"`. Examples: `"10.5.301"`, `"9.2.1"`.
        :param pulumi.Input[bool] require_verified_chrome_os: Only allows requests from devices with a verified Chrome OS. Verifications includes requirements that the device is enterprise-managed, conformant to domain policies, and the caller has permission to call the API targeted by the request.
        """
        pulumi.set(__self__, "os_type", os_type)
        if minimum_version is not None:
            pulumi.set(__self__, "minimum_version", minimum_version)
        if require_verified_chrome_os is not None:
            pulumi.set(__self__, "require_verified_chrome_os", require_verified_chrome_os)

    @property
    @pulumi.getter(name="osType")
    def os_type(self) -> pulumi.Input['OsConstraintOsType']:
        """
        The allowed OS type.
        """
        return pulumi.get(self, "os_type")

    @os_type.setter
    def os_type(self, value: pulumi.Input['OsConstraintOsType']):
        pulumi.set(self, "os_type", value)

    @property
    @pulumi.getter(name="minimumVersion")
    def minimum_version(self) -> Optional[pulumi.Input[str]]:
        """
        The minimum allowed OS version. If not set, any version of this OS satisfies the constraint. Format: `"major.minor.patch"`. Examples: `"10.5.301"`, `"9.2.1"`.
        """
        return pulumi.get(self, "minimum_version")

    @minimum_version.setter
    def minimum_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "minimum_version", value)

    @property
    @pulumi.getter(name="requireVerifiedChromeOs")
    def require_verified_chrome_os(self) -> Optional[pulumi.Input[bool]]:
        """
        Only allows requests from devices with a verified Chrome OS. Verifications includes requirements that the device is enterprise-managed, conformant to domain policies, and the caller has permission to call the API targeted by the request.
        """
        return pulumi.get(self, "require_verified_chrome_os")

    @require_verified_chrome_os.setter
    def require_verified_chrome_os(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "require_verified_chrome_os", value)


