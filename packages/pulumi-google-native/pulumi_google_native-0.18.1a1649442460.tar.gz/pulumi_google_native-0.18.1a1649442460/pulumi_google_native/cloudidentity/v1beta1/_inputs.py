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
    'DynamicGroupMetadataArgs',
    'DynamicGroupQueryArgs',
    'EntityKeyArgs',
    'ExpiryDetailArgs',
    'MembershipRoleRestrictionEvaluationArgs',
    'MembershipRoleArgs',
    'PosixGroupArgs',
    'RestrictionEvaluationsArgs',
]

@pulumi.input_type
class DynamicGroupMetadataArgs:
    def __init__(__self__, *,
                 queries: Optional[pulumi.Input[Sequence[pulumi.Input['DynamicGroupQueryArgs']]]] = None):
        """
        Dynamic group metadata like queries and status.
        :param pulumi.Input[Sequence[pulumi.Input['DynamicGroupQueryArgs']]] queries: Memberships will be the union of all queries. Only one entry with USER resource is currently supported. Customers can create up to 100 dynamic groups.
        """
        if queries is not None:
            pulumi.set(__self__, "queries", queries)

    @property
    @pulumi.getter
    def queries(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['DynamicGroupQueryArgs']]]]:
        """
        Memberships will be the union of all queries. Only one entry with USER resource is currently supported. Customers can create up to 100 dynamic groups.
        """
        return pulumi.get(self, "queries")

    @queries.setter
    def queries(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['DynamicGroupQueryArgs']]]]):
        pulumi.set(self, "queries", value)


@pulumi.input_type
class DynamicGroupQueryArgs:
    def __init__(__self__, *,
                 query: Optional[pulumi.Input[str]] = None,
                 resource_type: Optional[pulumi.Input['DynamicGroupQueryResourceType']] = None):
        """
        Defines a query on a resource.
        :param pulumi.Input[str] query: Query that determines the memberships of the dynamic group. Examples: All users with at least one `organizations.department` of engineering. `user.organizations.exists(org, org.department=='engineering')` All users with at least one location that has `area` of `foo` and `building_id` of `bar`. `user.locations.exists(loc, loc.area=='foo' && loc.building_id=='bar')` All users with any variation of the name John Doe (case-insensitive queries add `equalsIgnoreCase()` to the value being queried). `user.name.value.equalsIgnoreCase('jOhn DoE')`
        """
        if query is not None:
            pulumi.set(__self__, "query", query)
        if resource_type is not None:
            pulumi.set(__self__, "resource_type", resource_type)

    @property
    @pulumi.getter
    def query(self) -> Optional[pulumi.Input[str]]:
        """
        Query that determines the memberships of the dynamic group. Examples: All users with at least one `organizations.department` of engineering. `user.organizations.exists(org, org.department=='engineering')` All users with at least one location that has `area` of `foo` and `building_id` of `bar`. `user.locations.exists(loc, loc.area=='foo' && loc.building_id=='bar')` All users with any variation of the name John Doe (case-insensitive queries add `equalsIgnoreCase()` to the value being queried). `user.name.value.equalsIgnoreCase('jOhn DoE')`
        """
        return pulumi.get(self, "query")

    @query.setter
    def query(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "query", value)

    @property
    @pulumi.getter(name="resourceType")
    def resource_type(self) -> Optional[pulumi.Input['DynamicGroupQueryResourceType']]:
        return pulumi.get(self, "resource_type")

    @resource_type.setter
    def resource_type(self, value: Optional[pulumi.Input['DynamicGroupQueryResourceType']]):
        pulumi.set(self, "resource_type", value)


@pulumi.input_type
class EntityKeyArgs:
    def __init__(__self__, *,
                 id: Optional[pulumi.Input[str]] = None,
                 namespace: Optional[pulumi.Input[str]] = None):
        """
        A unique identifier for an entity in the Cloud Identity Groups API. An entity can represent either a group with an optional `namespace` or a user without a `namespace`. The combination of `id` and `namespace` must be unique; however, the same `id` can be used with different `namespace`s.
        :param pulumi.Input[str] id: The ID of the entity. For Google-managed entities, the `id` must be the email address of an existing group or user. For external-identity-mapped entities, the `id` must be a string conforming to the Identity Source's requirements. Must be unique within a `namespace`.
        :param pulumi.Input[str] namespace: The namespace in which the entity exists. If not specified, the `EntityKey` represents a Google-managed entity such as a Google user or a Google Group. If specified, the `EntityKey` represents an external-identity-mapped group. The namespace must correspond to an identity source created in Admin Console and must be in the form of `identitysources/{identity_source_id}`.
        """
        if id is not None:
            pulumi.set(__self__, "id", id)
        if namespace is not None:
            pulumi.set(__self__, "namespace", namespace)

    @property
    @pulumi.getter
    def id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the entity. For Google-managed entities, the `id` must be the email address of an existing group or user. For external-identity-mapped entities, the `id` must be a string conforming to the Identity Source's requirements. Must be unique within a `namespace`.
        """
        return pulumi.get(self, "id")

    @id.setter
    def id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "id", value)

    @property
    @pulumi.getter
    def namespace(self) -> Optional[pulumi.Input[str]]:
        """
        The namespace in which the entity exists. If not specified, the `EntityKey` represents a Google-managed entity such as a Google user or a Google Group. If specified, the `EntityKey` represents an external-identity-mapped group. The namespace must correspond to an identity source created in Admin Console and must be in the form of `identitysources/{identity_source_id}`.
        """
        return pulumi.get(self, "namespace")

    @namespace.setter
    def namespace(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "namespace", value)


@pulumi.input_type
class ExpiryDetailArgs:
    def __init__(__self__, *,
                 expire_time: Optional[pulumi.Input[str]] = None):
        """
        The `MembershipRole` expiry details.
        :param pulumi.Input[str] expire_time: The time at which the `MembershipRole` will expire.
        """
        if expire_time is not None:
            pulumi.set(__self__, "expire_time", expire_time)

    @property
    @pulumi.getter(name="expireTime")
    def expire_time(self) -> Optional[pulumi.Input[str]]:
        """
        The time at which the `MembershipRole` will expire.
        """
        return pulumi.get(self, "expire_time")

    @expire_time.setter
    def expire_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "expire_time", value)


@pulumi.input_type
class MembershipRoleRestrictionEvaluationArgs:
    def __init__(__self__):
        """
        The evaluated state of this restriction.
        """
        pass


@pulumi.input_type
class MembershipRoleArgs:
    def __init__(__self__, *,
                 expiry_detail: Optional[pulumi.Input['ExpiryDetailArgs']] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 restriction_evaluations: Optional[pulumi.Input['RestrictionEvaluationsArgs']] = None):
        """
        A membership role within the Cloud Identity Groups API. A `MembershipRole` defines the privileges granted to a `Membership`.
        :param pulumi.Input['ExpiryDetailArgs'] expiry_detail: The expiry details of the `MembershipRole`. Expiry details are only supported for `MEMBER` `MembershipRoles`. May be set if `name` is `MEMBER`. Must not be set if `name` is any other value.
        :param pulumi.Input[str] name: The name of the `MembershipRole`. Must be one of `OWNER`, `MANAGER`, `MEMBER`.
        :param pulumi.Input['RestrictionEvaluationsArgs'] restriction_evaluations: Evaluations of restrictions applied to parent group on this membership.
        """
        if expiry_detail is not None:
            pulumi.set(__self__, "expiry_detail", expiry_detail)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if restriction_evaluations is not None:
            pulumi.set(__self__, "restriction_evaluations", restriction_evaluations)

    @property
    @pulumi.getter(name="expiryDetail")
    def expiry_detail(self) -> Optional[pulumi.Input['ExpiryDetailArgs']]:
        """
        The expiry details of the `MembershipRole`. Expiry details are only supported for `MEMBER` `MembershipRoles`. May be set if `name` is `MEMBER`. Must not be set if `name` is any other value.
        """
        return pulumi.get(self, "expiry_detail")

    @expiry_detail.setter
    def expiry_detail(self, value: Optional[pulumi.Input['ExpiryDetailArgs']]):
        pulumi.set(self, "expiry_detail", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the `MembershipRole`. Must be one of `OWNER`, `MANAGER`, `MEMBER`.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="restrictionEvaluations")
    def restriction_evaluations(self) -> Optional[pulumi.Input['RestrictionEvaluationsArgs']]:
        """
        Evaluations of restrictions applied to parent group on this membership.
        """
        return pulumi.get(self, "restriction_evaluations")

    @restriction_evaluations.setter
    def restriction_evaluations(self, value: Optional[pulumi.Input['RestrictionEvaluationsArgs']]):
        pulumi.set(self, "restriction_evaluations", value)


@pulumi.input_type
class PosixGroupArgs:
    def __init__(__self__, *,
                 gid: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 system_id: Optional[pulumi.Input[str]] = None):
        """
        POSIX Group definition to represent a group in a POSIX compliant system.
        :param pulumi.Input[str] gid: GID of the POSIX group.
        :param pulumi.Input[str] name: Name of the POSIX group.
        :param pulumi.Input[str] system_id: System identifier for which group name and gid apply to. If not specified it will default to empty value.
        """
        if gid is not None:
            pulumi.set(__self__, "gid", gid)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if system_id is not None:
            pulumi.set(__self__, "system_id", system_id)

    @property
    @pulumi.getter
    def gid(self) -> Optional[pulumi.Input[str]]:
        """
        GID of the POSIX group.
        """
        return pulumi.get(self, "gid")

    @gid.setter
    def gid(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "gid", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the POSIX group.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="systemId")
    def system_id(self) -> Optional[pulumi.Input[str]]:
        """
        System identifier for which group name and gid apply to. If not specified it will default to empty value.
        """
        return pulumi.get(self, "system_id")

    @system_id.setter
    def system_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "system_id", value)


@pulumi.input_type
class RestrictionEvaluationsArgs:
    def __init__(__self__, *,
                 member_restriction_evaluation: Optional[pulumi.Input['MembershipRoleRestrictionEvaluationArgs']] = None):
        """
        Evaluations of restrictions applied to parent group on this membership.
        :param pulumi.Input['MembershipRoleRestrictionEvaluationArgs'] member_restriction_evaluation: Evaluation of the member restriction applied to this membership. Empty if the user lacks permission to view the restriction evaluation.
        """
        if member_restriction_evaluation is not None:
            pulumi.set(__self__, "member_restriction_evaluation", member_restriction_evaluation)

    @property
    @pulumi.getter(name="memberRestrictionEvaluation")
    def member_restriction_evaluation(self) -> Optional[pulumi.Input['MembershipRoleRestrictionEvaluationArgs']]:
        """
        Evaluation of the member restriction applied to this membership. Empty if the user lacks permission to view the restriction evaluation.
        """
        return pulumi.get(self, "member_restriction_evaluation")

    @member_restriction_evaluation.setter
    def member_restriction_evaluation(self, value: Optional[pulumi.Input['MembershipRoleRestrictionEvaluationArgs']]):
        pulumi.set(self, "member_restriction_evaluation", value)


