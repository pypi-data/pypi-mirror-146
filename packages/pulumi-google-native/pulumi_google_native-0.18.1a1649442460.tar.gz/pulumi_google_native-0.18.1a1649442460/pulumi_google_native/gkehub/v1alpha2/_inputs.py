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
    'AuditConfigArgs',
    'AuditLogConfigArgs',
    'AuthorityArgs',
    'BindingArgs',
    'EdgeClusterArgs',
    'ExprArgs',
    'GkeClusterArgs',
    'KubernetesResourceArgs',
    'MembershipEndpointArgs',
    'MultiCloudClusterArgs',
    'OnPremClusterArgs',
    'ResourceOptionsArgs',
]

@pulumi.input_type
class AuditConfigArgs:
    def __init__(__self__, *,
                 audit_log_configs: Optional[pulumi.Input[Sequence[pulumi.Input['AuditLogConfigArgs']]]] = None,
                 service: Optional[pulumi.Input[str]] = None):
        """
        Specifies the audit configuration for a service. The configuration determines which permission types are logged, and what identities, if any, are exempted from logging. An AuditConfig must have one or more AuditLogConfigs. If there are AuditConfigs for both `allServices` and a specific service, the union of the two AuditConfigs is used for that service: the log_types specified in each AuditConfig are enabled, and the exempted_members in each AuditLogConfig are exempted. Example Policy with multiple AuditConfigs: { "audit_configs": [ { "service": "allServices", "audit_log_configs": [ { "log_type": "DATA_READ", "exempted_members": [ "user:jose@example.com" ] }, { "log_type": "DATA_WRITE" }, { "log_type": "ADMIN_READ" } ] }, { "service": "sampleservice.googleapis.com", "audit_log_configs": [ { "log_type": "DATA_READ" }, { "log_type": "DATA_WRITE", "exempted_members": [ "user:aliya@example.com" ] } ] } ] } For sampleservice, this policy enables DATA_READ, DATA_WRITE and ADMIN_READ logging. It also exempts jose@example.com from DATA_READ logging, and aliya@example.com from DATA_WRITE logging.
        :param pulumi.Input[Sequence[pulumi.Input['AuditLogConfigArgs']]] audit_log_configs: The configuration for logging of each type of permission.
        :param pulumi.Input[str] service: Specifies a service that will be enabled for audit logging. For example, `storage.googleapis.com`, `cloudsql.googleapis.com`. `allServices` is a special value that covers all services.
        """
        if audit_log_configs is not None:
            pulumi.set(__self__, "audit_log_configs", audit_log_configs)
        if service is not None:
            pulumi.set(__self__, "service", service)

    @property
    @pulumi.getter(name="auditLogConfigs")
    def audit_log_configs(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['AuditLogConfigArgs']]]]:
        """
        The configuration for logging of each type of permission.
        """
        return pulumi.get(self, "audit_log_configs")

    @audit_log_configs.setter
    def audit_log_configs(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['AuditLogConfigArgs']]]]):
        pulumi.set(self, "audit_log_configs", value)

    @property
    @pulumi.getter
    def service(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies a service that will be enabled for audit logging. For example, `storage.googleapis.com`, `cloudsql.googleapis.com`. `allServices` is a special value that covers all services.
        """
        return pulumi.get(self, "service")

    @service.setter
    def service(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "service", value)


@pulumi.input_type
class AuditLogConfigArgs:
    def __init__(__self__, *,
                 exempted_members: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 log_type: Optional[pulumi.Input['AuditLogConfigLogType']] = None):
        """
        Provides the configuration for logging a type of permissions. Example: { "audit_log_configs": [ { "log_type": "DATA_READ", "exempted_members": [ "user:jose@example.com" ] }, { "log_type": "DATA_WRITE" } ] } This enables 'DATA_READ' and 'DATA_WRITE' logging, while exempting jose@example.com from DATA_READ logging.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] exempted_members: Specifies the identities that do not cause logging for this type of permission. Follows the same format of Binding.members.
        :param pulumi.Input['AuditLogConfigLogType'] log_type: The log type that this config enables.
        """
        if exempted_members is not None:
            pulumi.set(__self__, "exempted_members", exempted_members)
        if log_type is not None:
            pulumi.set(__self__, "log_type", log_type)

    @property
    @pulumi.getter(name="exemptedMembers")
    def exempted_members(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Specifies the identities that do not cause logging for this type of permission. Follows the same format of Binding.members.
        """
        return pulumi.get(self, "exempted_members")

    @exempted_members.setter
    def exempted_members(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "exempted_members", value)

    @property
    @pulumi.getter(name="logType")
    def log_type(self) -> Optional[pulumi.Input['AuditLogConfigLogType']]:
        """
        The log type that this config enables.
        """
        return pulumi.get(self, "log_type")

    @log_type.setter
    def log_type(self, value: Optional[pulumi.Input['AuditLogConfigLogType']]):
        pulumi.set(self, "log_type", value)


@pulumi.input_type
class AuthorityArgs:
    def __init__(__self__, *,
                 issuer: Optional[pulumi.Input[str]] = None,
                 oidc_jwks: Optional[pulumi.Input[str]] = None):
        """
        Authority encodes how Google will recognize identities from this Membership. See the workload identity documentation for more details: https://cloud.google.com/kubernetes-engine/docs/how-to/workload-identity
        :param pulumi.Input[str] issuer: Optional. A JSON Web Token (JWT) issuer URI. `issuer` must start with `https://` and be a valid URL with length <2000 characters. If set, then Google will allow valid OIDC tokens from this issuer to authenticate within the workload_identity_pool. OIDC discovery will be performed on this URI to validate tokens from the issuer, unless `oidc_jwks` is set. Clearing `issuer` disables Workload Identity. `issuer` cannot be directly modified; it must be cleared (and Workload Identity disabled) before using a new issuer (and re-enabling Workload Identity).
        :param pulumi.Input[str] oidc_jwks: Optional. OIDC verification keys for this Membership in JWKS format (RFC 7517). When this field is set, OIDC discovery will NOT be performed on `issuer`, and instead OIDC tokens will be validated using this field.
        """
        if issuer is not None:
            pulumi.set(__self__, "issuer", issuer)
        if oidc_jwks is not None:
            pulumi.set(__self__, "oidc_jwks", oidc_jwks)

    @property
    @pulumi.getter
    def issuer(self) -> Optional[pulumi.Input[str]]:
        """
        Optional. A JSON Web Token (JWT) issuer URI. `issuer` must start with `https://` and be a valid URL with length <2000 characters. If set, then Google will allow valid OIDC tokens from this issuer to authenticate within the workload_identity_pool. OIDC discovery will be performed on this URI to validate tokens from the issuer, unless `oidc_jwks` is set. Clearing `issuer` disables Workload Identity. `issuer` cannot be directly modified; it must be cleared (and Workload Identity disabled) before using a new issuer (and re-enabling Workload Identity).
        """
        return pulumi.get(self, "issuer")

    @issuer.setter
    def issuer(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "issuer", value)

    @property
    @pulumi.getter(name="oidcJwks")
    def oidc_jwks(self) -> Optional[pulumi.Input[str]]:
        """
        Optional. OIDC verification keys for this Membership in JWKS format (RFC 7517). When this field is set, OIDC discovery will NOT be performed on `issuer`, and instead OIDC tokens will be validated using this field.
        """
        return pulumi.get(self, "oidc_jwks")

    @oidc_jwks.setter
    def oidc_jwks(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "oidc_jwks", value)


@pulumi.input_type
class BindingArgs:
    def __init__(__self__, *,
                 condition: Optional[pulumi.Input['ExprArgs']] = None,
                 members: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 role: Optional[pulumi.Input[str]] = None):
        """
        Associates `members`, or principals, with a `role`.
        :param pulumi.Input['ExprArgs'] condition: The condition that is associated with this binding. If the condition evaluates to `true`, then this binding applies to the current request. If the condition evaluates to `false`, then this binding does not apply to the current request. However, a different role binding might grant the same role to one or more of the principals in this binding. To learn which resources support conditions in their IAM policies, see the [IAM documentation](https://cloud.google.com/iam/help/conditions/resource-policies).
        :param pulumi.Input[Sequence[pulumi.Input[str]]] members: Specifies the principals requesting access for a Cloud Platform resource. `members` can have the following values: * `allUsers`: A special identifier that represents anyone who is on the internet; with or without a Google account. * `allAuthenticatedUsers`: A special identifier that represents anyone who is authenticated with a Google account or a service account. * `user:{emailid}`: An email address that represents a specific Google account. For example, `alice@example.com` . * `serviceAccount:{emailid}`: An email address that represents a service account. For example, `my-other-app@appspot.gserviceaccount.com`. * `group:{emailid}`: An email address that represents a Google group. For example, `admins@example.com`. * `deleted:user:{emailid}?uid={uniqueid}`: An email address (plus unique identifier) representing a user that has been recently deleted. For example, `alice@example.com?uid=123456789012345678901`. If the user is recovered, this value reverts to `user:{emailid}` and the recovered user retains the role in the binding. * `deleted:serviceAccount:{emailid}?uid={uniqueid}`: An email address (plus unique identifier) representing a service account that has been recently deleted. For example, `my-other-app@appspot.gserviceaccount.com?uid=123456789012345678901`. If the service account is undeleted, this value reverts to `serviceAccount:{emailid}` and the undeleted service account retains the role in the binding. * `deleted:group:{emailid}?uid={uniqueid}`: An email address (plus unique identifier) representing a Google group that has been recently deleted. For example, `admins@example.com?uid=123456789012345678901`. If the group is recovered, this value reverts to `group:{emailid}` and the recovered group retains the role in the binding. * `domain:{domain}`: The G Suite domain (primary) that represents all the users of that domain. For example, `google.com` or `example.com`. 
        :param pulumi.Input[str] role: Role that is assigned to the list of `members`, or principals. For example, `roles/viewer`, `roles/editor`, or `roles/owner`.
        """
        if condition is not None:
            pulumi.set(__self__, "condition", condition)
        if members is not None:
            pulumi.set(__self__, "members", members)
        if role is not None:
            pulumi.set(__self__, "role", role)

    @property
    @pulumi.getter
    def condition(self) -> Optional[pulumi.Input['ExprArgs']]:
        """
        The condition that is associated with this binding. If the condition evaluates to `true`, then this binding applies to the current request. If the condition evaluates to `false`, then this binding does not apply to the current request. However, a different role binding might grant the same role to one or more of the principals in this binding. To learn which resources support conditions in their IAM policies, see the [IAM documentation](https://cloud.google.com/iam/help/conditions/resource-policies).
        """
        return pulumi.get(self, "condition")

    @condition.setter
    def condition(self, value: Optional[pulumi.Input['ExprArgs']]):
        pulumi.set(self, "condition", value)

    @property
    @pulumi.getter
    def members(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Specifies the principals requesting access for a Cloud Platform resource. `members` can have the following values: * `allUsers`: A special identifier that represents anyone who is on the internet; with or without a Google account. * `allAuthenticatedUsers`: A special identifier that represents anyone who is authenticated with a Google account or a service account. * `user:{emailid}`: An email address that represents a specific Google account. For example, `alice@example.com` . * `serviceAccount:{emailid}`: An email address that represents a service account. For example, `my-other-app@appspot.gserviceaccount.com`. * `group:{emailid}`: An email address that represents a Google group. For example, `admins@example.com`. * `deleted:user:{emailid}?uid={uniqueid}`: An email address (plus unique identifier) representing a user that has been recently deleted. For example, `alice@example.com?uid=123456789012345678901`. If the user is recovered, this value reverts to `user:{emailid}` and the recovered user retains the role in the binding. * `deleted:serviceAccount:{emailid}?uid={uniqueid}`: An email address (plus unique identifier) representing a service account that has been recently deleted. For example, `my-other-app@appspot.gserviceaccount.com?uid=123456789012345678901`. If the service account is undeleted, this value reverts to `serviceAccount:{emailid}` and the undeleted service account retains the role in the binding. * `deleted:group:{emailid}?uid={uniqueid}`: An email address (plus unique identifier) representing a Google group that has been recently deleted. For example, `admins@example.com?uid=123456789012345678901`. If the group is recovered, this value reverts to `group:{emailid}` and the recovered group retains the role in the binding. * `domain:{domain}`: The G Suite domain (primary) that represents all the users of that domain. For example, `google.com` or `example.com`. 
        """
        return pulumi.get(self, "members")

    @members.setter
    def members(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "members", value)

    @property
    @pulumi.getter
    def role(self) -> Optional[pulumi.Input[str]]:
        """
        Role that is assigned to the list of `members`, or principals. For example, `roles/viewer`, `roles/editor`, or `roles/owner`.
        """
        return pulumi.get(self, "role")

    @role.setter
    def role(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "role", value)


@pulumi.input_type
class EdgeClusterArgs:
    def __init__(__self__, *,
                 resource_link: Optional[pulumi.Input[str]] = None):
        """
        EdgeCluster contains information specific to Google Edge Clusters.
        :param pulumi.Input[str] resource_link: Immutable. Self-link of the GCP resource for the Edge Cluster. For example: //edgecontainer.googleapis.com/projects/my-project/locations/us-west1-a/clusters/my-cluster
        """
        if resource_link is not None:
            pulumi.set(__self__, "resource_link", resource_link)

    @property
    @pulumi.getter(name="resourceLink")
    def resource_link(self) -> Optional[pulumi.Input[str]]:
        """
        Immutable. Self-link of the GCP resource for the Edge Cluster. For example: //edgecontainer.googleapis.com/projects/my-project/locations/us-west1-a/clusters/my-cluster
        """
        return pulumi.get(self, "resource_link")

    @resource_link.setter
    def resource_link(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_link", value)


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
class GkeClusterArgs:
    def __init__(__self__, *,
                 resource_link: Optional[pulumi.Input[str]] = None):
        """
        GkeCluster contains information specific to GKE clusters.
        :param pulumi.Input[str] resource_link: Immutable. Self-link of the GCP resource for the GKE cluster. For example: //container.googleapis.com/projects/my-project/locations/us-west1-a/clusters/my-cluster Zonal clusters are also supported.
        """
        if resource_link is not None:
            pulumi.set(__self__, "resource_link", resource_link)

    @property
    @pulumi.getter(name="resourceLink")
    def resource_link(self) -> Optional[pulumi.Input[str]]:
        """
        Immutable. Self-link of the GCP resource for the GKE cluster. For example: //container.googleapis.com/projects/my-project/locations/us-west1-a/clusters/my-cluster Zonal clusters are also supported.
        """
        return pulumi.get(self, "resource_link")

    @resource_link.setter
    def resource_link(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_link", value)


@pulumi.input_type
class KubernetesResourceArgs:
    def __init__(__self__, *,
                 membership_cr_manifest: Optional[pulumi.Input[str]] = None,
                 resource_options: Optional[pulumi.Input['ResourceOptionsArgs']] = None):
        """
        KubernetesResource contains the YAML manifests and configuration for Membership Kubernetes resources in the cluster. After CreateMembership or UpdateMembership, these resources should be re-applied in the cluster.
        :param pulumi.Input[str] membership_cr_manifest: Input only. The YAML representation of the Membership CR. This field is ignored for GKE clusters where Hub can read the CR directly. Callers should provide the CR that is currently present in the cluster during Create or Update, or leave this field empty if none exists. The CR manifest is used to validate the cluster has not been registered with another Membership.
        :param pulumi.Input['ResourceOptionsArgs'] resource_options: Optional. Options for Kubernetes resource generation.
        """
        if membership_cr_manifest is not None:
            pulumi.set(__self__, "membership_cr_manifest", membership_cr_manifest)
        if resource_options is not None:
            pulumi.set(__self__, "resource_options", resource_options)

    @property
    @pulumi.getter(name="membershipCrManifest")
    def membership_cr_manifest(self) -> Optional[pulumi.Input[str]]:
        """
        Input only. The YAML representation of the Membership CR. This field is ignored for GKE clusters where Hub can read the CR directly. Callers should provide the CR that is currently present in the cluster during Create or Update, or leave this field empty if none exists. The CR manifest is used to validate the cluster has not been registered with another Membership.
        """
        return pulumi.get(self, "membership_cr_manifest")

    @membership_cr_manifest.setter
    def membership_cr_manifest(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "membership_cr_manifest", value)

    @property
    @pulumi.getter(name="resourceOptions")
    def resource_options(self) -> Optional[pulumi.Input['ResourceOptionsArgs']]:
        """
        Optional. Options for Kubernetes resource generation.
        """
        return pulumi.get(self, "resource_options")

    @resource_options.setter
    def resource_options(self, value: Optional[pulumi.Input['ResourceOptionsArgs']]):
        pulumi.set(self, "resource_options", value)


@pulumi.input_type
class MembershipEndpointArgs:
    def __init__(__self__, *,
                 edge_cluster: Optional[pulumi.Input['EdgeClusterArgs']] = None,
                 gke_cluster: Optional[pulumi.Input['GkeClusterArgs']] = None,
                 kubernetes_resource: Optional[pulumi.Input['KubernetesResourceArgs']] = None,
                 multi_cloud_cluster: Optional[pulumi.Input['MultiCloudClusterArgs']] = None,
                 on_prem_cluster: Optional[pulumi.Input['OnPremClusterArgs']] = None):
        """
        MembershipEndpoint contains information needed to contact a Kubernetes API, endpoint and any additional Kubernetes metadata.
        :param pulumi.Input['EdgeClusterArgs'] edge_cluster: Optional. Specific information for a Google Edge cluster.
        :param pulumi.Input['GkeClusterArgs'] gke_cluster: Optional. Specific information for a GKE-on-GCP cluster.
        :param pulumi.Input['KubernetesResourceArgs'] kubernetes_resource: Optional. The in-cluster Kubernetes Resources that should be applied for a correctly registered cluster, in the steady state. These resources: * Ensure that the cluster is exclusively registered to one and only one Hub Membership. * Propagate Workload Pool Information available in the Membership Authority field. * Ensure proper initial configuration of default Hub Features.
        :param pulumi.Input['MultiCloudClusterArgs'] multi_cloud_cluster: Optional. Specific information for a GKE Multi-Cloud cluster.
        :param pulumi.Input['OnPremClusterArgs'] on_prem_cluster: Optional. Specific information for a GKE On-Prem cluster. An onprem user-cluster who has no resourceLink is not allowed to use this field, it should have a nil "type" instead.
        """
        if edge_cluster is not None:
            pulumi.set(__self__, "edge_cluster", edge_cluster)
        if gke_cluster is not None:
            pulumi.set(__self__, "gke_cluster", gke_cluster)
        if kubernetes_resource is not None:
            pulumi.set(__self__, "kubernetes_resource", kubernetes_resource)
        if multi_cloud_cluster is not None:
            pulumi.set(__self__, "multi_cloud_cluster", multi_cloud_cluster)
        if on_prem_cluster is not None:
            pulumi.set(__self__, "on_prem_cluster", on_prem_cluster)

    @property
    @pulumi.getter(name="edgeCluster")
    def edge_cluster(self) -> Optional[pulumi.Input['EdgeClusterArgs']]:
        """
        Optional. Specific information for a Google Edge cluster.
        """
        return pulumi.get(self, "edge_cluster")

    @edge_cluster.setter
    def edge_cluster(self, value: Optional[pulumi.Input['EdgeClusterArgs']]):
        pulumi.set(self, "edge_cluster", value)

    @property
    @pulumi.getter(name="gkeCluster")
    def gke_cluster(self) -> Optional[pulumi.Input['GkeClusterArgs']]:
        """
        Optional. Specific information for a GKE-on-GCP cluster.
        """
        return pulumi.get(self, "gke_cluster")

    @gke_cluster.setter
    def gke_cluster(self, value: Optional[pulumi.Input['GkeClusterArgs']]):
        pulumi.set(self, "gke_cluster", value)

    @property
    @pulumi.getter(name="kubernetesResource")
    def kubernetes_resource(self) -> Optional[pulumi.Input['KubernetesResourceArgs']]:
        """
        Optional. The in-cluster Kubernetes Resources that should be applied for a correctly registered cluster, in the steady state. These resources: * Ensure that the cluster is exclusively registered to one and only one Hub Membership. * Propagate Workload Pool Information available in the Membership Authority field. * Ensure proper initial configuration of default Hub Features.
        """
        return pulumi.get(self, "kubernetes_resource")

    @kubernetes_resource.setter
    def kubernetes_resource(self, value: Optional[pulumi.Input['KubernetesResourceArgs']]):
        pulumi.set(self, "kubernetes_resource", value)

    @property
    @pulumi.getter(name="multiCloudCluster")
    def multi_cloud_cluster(self) -> Optional[pulumi.Input['MultiCloudClusterArgs']]:
        """
        Optional. Specific information for a GKE Multi-Cloud cluster.
        """
        return pulumi.get(self, "multi_cloud_cluster")

    @multi_cloud_cluster.setter
    def multi_cloud_cluster(self, value: Optional[pulumi.Input['MultiCloudClusterArgs']]):
        pulumi.set(self, "multi_cloud_cluster", value)

    @property
    @pulumi.getter(name="onPremCluster")
    def on_prem_cluster(self) -> Optional[pulumi.Input['OnPremClusterArgs']]:
        """
        Optional. Specific information for a GKE On-Prem cluster. An onprem user-cluster who has no resourceLink is not allowed to use this field, it should have a nil "type" instead.
        """
        return pulumi.get(self, "on_prem_cluster")

    @on_prem_cluster.setter
    def on_prem_cluster(self, value: Optional[pulumi.Input['OnPremClusterArgs']]):
        pulumi.set(self, "on_prem_cluster", value)


@pulumi.input_type
class MultiCloudClusterArgs:
    def __init__(__self__, *,
                 resource_link: Optional[pulumi.Input[str]] = None):
        """
        MultiCloudCluster contains information specific to GKE Multi-Cloud clusters.
        :param pulumi.Input[str] resource_link: Immutable. Self-link of the GCP resource for the GKE Multi-Cloud cluster. For example: //gkemulticloud.googleapis.com/projects/my-project/locations/us-west1-a/awsClusters/my-cluster //gkemulticloud.googleapis.com/projects/my-project/locations/us-west1-a/azureClusters/my-cluster
        """
        if resource_link is not None:
            pulumi.set(__self__, "resource_link", resource_link)

    @property
    @pulumi.getter(name="resourceLink")
    def resource_link(self) -> Optional[pulumi.Input[str]]:
        """
        Immutable. Self-link of the GCP resource for the GKE Multi-Cloud cluster. For example: //gkemulticloud.googleapis.com/projects/my-project/locations/us-west1-a/awsClusters/my-cluster //gkemulticloud.googleapis.com/projects/my-project/locations/us-west1-a/azureClusters/my-cluster
        """
        return pulumi.get(self, "resource_link")

    @resource_link.setter
    def resource_link(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_link", value)


@pulumi.input_type
class OnPremClusterArgs:
    def __init__(__self__, *,
                 admin_cluster: Optional[pulumi.Input[bool]] = None,
                 resource_link: Optional[pulumi.Input[str]] = None):
        """
        OnPremCluster contains information specific to GKE On-Prem clusters.
        :param pulumi.Input[bool] admin_cluster: Immutable. Whether the cluster is an admin cluster.
        :param pulumi.Input[str] resource_link: Immutable. Self-link of the GCP resource for the GKE On-Prem cluster. For example: //gkeonprem.googleapis.com/projects/my-project/locations/us-west1-a/vmwareClusters/my-cluster //gkeonprem.googleapis.com/projects/my-project/locations/us-west1-a/bareMetalClusters/my-cluster
        """
        if admin_cluster is not None:
            pulumi.set(__self__, "admin_cluster", admin_cluster)
        if resource_link is not None:
            pulumi.set(__self__, "resource_link", resource_link)

    @property
    @pulumi.getter(name="adminCluster")
    def admin_cluster(self) -> Optional[pulumi.Input[bool]]:
        """
        Immutable. Whether the cluster is an admin cluster.
        """
        return pulumi.get(self, "admin_cluster")

    @admin_cluster.setter
    def admin_cluster(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "admin_cluster", value)

    @property
    @pulumi.getter(name="resourceLink")
    def resource_link(self) -> Optional[pulumi.Input[str]]:
        """
        Immutable. Self-link of the GCP resource for the GKE On-Prem cluster. For example: //gkeonprem.googleapis.com/projects/my-project/locations/us-west1-a/vmwareClusters/my-cluster //gkeonprem.googleapis.com/projects/my-project/locations/us-west1-a/bareMetalClusters/my-cluster
        """
        return pulumi.get(self, "resource_link")

    @resource_link.setter
    def resource_link(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_link", value)


@pulumi.input_type
class ResourceOptionsArgs:
    def __init__(__self__, *,
                 connect_version: Optional[pulumi.Input[str]] = None,
                 k8s_version: Optional[pulumi.Input[str]] = None,
                 v1beta1_crd: Optional[pulumi.Input[bool]] = None):
        """
        ResourceOptions represent options for Kubernetes resource generation.
        :param pulumi.Input[str] connect_version: Optional. The Connect agent version to use for connect_resources. Defaults to the latest GKE Connect version. The version must be a currently supported version, obsolete versions will be rejected.
        :param pulumi.Input[str] k8s_version: Optional. Major version of the Kubernetes cluster. This is only used to determine which version to use for the CustomResourceDefinition resources, `apiextensions/v1beta1` or`apiextensions/v1`.
        :param pulumi.Input[bool] v1beta1_crd: Optional. Use `apiextensions/v1beta1` instead of `apiextensions/v1` for CustomResourceDefinition resources. This option should be set for clusters with Kubernetes apiserver versions <1.16.
        """
        if connect_version is not None:
            pulumi.set(__self__, "connect_version", connect_version)
        if k8s_version is not None:
            pulumi.set(__self__, "k8s_version", k8s_version)
        if v1beta1_crd is not None:
            pulumi.set(__self__, "v1beta1_crd", v1beta1_crd)

    @property
    @pulumi.getter(name="connectVersion")
    def connect_version(self) -> Optional[pulumi.Input[str]]:
        """
        Optional. The Connect agent version to use for connect_resources. Defaults to the latest GKE Connect version. The version must be a currently supported version, obsolete versions will be rejected.
        """
        return pulumi.get(self, "connect_version")

    @connect_version.setter
    def connect_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "connect_version", value)

    @property
    @pulumi.getter(name="k8sVersion")
    def k8s_version(self) -> Optional[pulumi.Input[str]]:
        """
        Optional. Major version of the Kubernetes cluster. This is only used to determine which version to use for the CustomResourceDefinition resources, `apiextensions/v1beta1` or`apiextensions/v1`.
        """
        return pulumi.get(self, "k8s_version")

    @k8s_version.setter
    def k8s_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "k8s_version", value)

    @property
    @pulumi.getter(name="v1beta1Crd")
    def v1beta1_crd(self) -> Optional[pulumi.Input[bool]]:
        """
        Optional. Use `apiextensions/v1beta1` instead of `apiextensions/v1` for CustomResourceDefinition resources. This option should be set for clusters with Kubernetes apiserver versions <1.16.
        """
        return pulumi.get(self, "v1beta1_crd")

    @v1beta1_crd.setter
    def v1beta1_crd(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "v1beta1_crd", value)


