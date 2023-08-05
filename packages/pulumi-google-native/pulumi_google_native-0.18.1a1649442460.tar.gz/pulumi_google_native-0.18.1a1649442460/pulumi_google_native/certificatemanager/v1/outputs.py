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

__all__ = [
    'AuthorizationAttemptInfoResponse',
    'DnsResourceRecordResponse',
    'GclbTargetResponse',
    'IpConfigResponse',
    'ManagedCertificateResponse',
    'ProvisioningIssueResponse',
    'SelfManagedCertificateResponse',
]

@pulumi.output_type
class AuthorizationAttemptInfoResponse(dict):
    """
    State of the latest attempt to authorize a domain for certificate issuance.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "failureReason":
            suggest = "failure_reason"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in AuthorizationAttemptInfoResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        AuthorizationAttemptInfoResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        AuthorizationAttemptInfoResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 details: str,
                 domain: str,
                 failure_reason: str,
                 state: str):
        """
        State of the latest attempt to authorize a domain for certificate issuance.
        :param str details: Human readable explanation for reaching the state. Provided to help address the configuration issues. Not guaranteed to be stable. For programmatic access use Reason enum.
        :param str domain: Domain name of the authorization attempt.
        :param str failure_reason: Reason for failure of the authorization attempt for the domain.
        :param str state: State of the domain for managed certificate issuance.
        """
        pulumi.set(__self__, "details", details)
        pulumi.set(__self__, "domain", domain)
        pulumi.set(__self__, "failure_reason", failure_reason)
        pulumi.set(__self__, "state", state)

    @property
    @pulumi.getter
    def details(self) -> str:
        """
        Human readable explanation for reaching the state. Provided to help address the configuration issues. Not guaranteed to be stable. For programmatic access use Reason enum.
        """
        return pulumi.get(self, "details")

    @property
    @pulumi.getter
    def domain(self) -> str:
        """
        Domain name of the authorization attempt.
        """
        return pulumi.get(self, "domain")

    @property
    @pulumi.getter(name="failureReason")
    def failure_reason(self) -> str:
        """
        Reason for failure of the authorization attempt for the domain.
        """
        return pulumi.get(self, "failure_reason")

    @property
    @pulumi.getter
    def state(self) -> str:
        """
        State of the domain for managed certificate issuance.
        """
        return pulumi.get(self, "state")


@pulumi.output_type
class DnsResourceRecordResponse(dict):
    """
    The structure describing the DNS Resource Record that needs to be added to DNS configuration for the authorization to be usable by certificate.
    """
    def __init__(__self__, *,
                 data: str,
                 name: str,
                 type: str):
        """
        The structure describing the DNS Resource Record that needs to be added to DNS configuration for the authorization to be usable by certificate.
        :param str data: Data of the DNS Resource Record.
        :param str name: Fully qualified name of the DNS Resource Record. e.g. `_acme-challenge.example.com`
        :param str type: Type of the DNS Resource Record. Currently always set to "CNAME".
        """
        pulumi.set(__self__, "data", data)
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def data(self) -> str:
        """
        Data of the DNS Resource Record.
        """
        return pulumi.get(self, "data")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Fully qualified name of the DNS Resource Record. e.g. `_acme-challenge.example.com`
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Type of the DNS Resource Record. Currently always set to "CNAME".
        """
        return pulumi.get(self, "type")


@pulumi.output_type
class GclbTargetResponse(dict):
    """
    Describes a Target Proxy which uses this Certificate Map.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "ipConfigs":
            suggest = "ip_configs"
        elif key == "targetHttpsProxy":
            suggest = "target_https_proxy"
        elif key == "targetSslProxy":
            suggest = "target_ssl_proxy"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in GclbTargetResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        GclbTargetResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        GclbTargetResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 ip_configs: Sequence['outputs.IpConfigResponse'],
                 target_https_proxy: str,
                 target_ssl_proxy: str):
        """
        Describes a Target Proxy which uses this Certificate Map.
        :param Sequence['IpConfigResponse'] ip_configs: IP configurations for this Target Proxy where the Certificate Map is serving.
        :param str target_https_proxy: A name must be in the format `projects/*/locations/*/targetHttpsProxies/*`.
        :param str target_ssl_proxy: A name must be in the format `projects/*/locations/*/targetSslProxies/*`.
        """
        pulumi.set(__self__, "ip_configs", ip_configs)
        pulumi.set(__self__, "target_https_proxy", target_https_proxy)
        pulumi.set(__self__, "target_ssl_proxy", target_ssl_proxy)

    @property
    @pulumi.getter(name="ipConfigs")
    def ip_configs(self) -> Sequence['outputs.IpConfigResponse']:
        """
        IP configurations for this Target Proxy where the Certificate Map is serving.
        """
        return pulumi.get(self, "ip_configs")

    @property
    @pulumi.getter(name="targetHttpsProxy")
    def target_https_proxy(self) -> str:
        """
        A name must be in the format `projects/*/locations/*/targetHttpsProxies/*`.
        """
        return pulumi.get(self, "target_https_proxy")

    @property
    @pulumi.getter(name="targetSslProxy")
    def target_ssl_proxy(self) -> str:
        """
        A name must be in the format `projects/*/locations/*/targetSslProxies/*`.
        """
        return pulumi.get(self, "target_ssl_proxy")


@pulumi.output_type
class IpConfigResponse(dict):
    """
    Defines IP configuration where this Certificate Map is serving.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "ipAddress":
            suggest = "ip_address"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in IpConfigResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        IpConfigResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        IpConfigResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 ip_address: str,
                 ports: Sequence[int]):
        """
        Defines IP configuration where this Certificate Map is serving.
        :param str ip_address: An external IP address.
        :param Sequence[int] ports: Ports.
        """
        pulumi.set(__self__, "ip_address", ip_address)
        pulumi.set(__self__, "ports", ports)

    @property
    @pulumi.getter(name="ipAddress")
    def ip_address(self) -> str:
        """
        An external IP address.
        """
        return pulumi.get(self, "ip_address")

    @property
    @pulumi.getter
    def ports(self) -> Sequence[int]:
        """
        Ports.
        """
        return pulumi.get(self, "ports")


@pulumi.output_type
class ManagedCertificateResponse(dict):
    """
    Configuration and state of a Managed Certificate. Certificate Manager provisions and renews Managed Certificates automatically, for as long as it's authorized to do so.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "authorizationAttemptInfo":
            suggest = "authorization_attempt_info"
        elif key == "dnsAuthorizations":
            suggest = "dns_authorizations"
        elif key == "provisioningIssue":
            suggest = "provisioning_issue"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ManagedCertificateResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ManagedCertificateResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ManagedCertificateResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 authorization_attempt_info: Sequence['outputs.AuthorizationAttemptInfoResponse'],
                 dns_authorizations: Sequence[str],
                 domains: Sequence[str],
                 provisioning_issue: 'outputs.ProvisioningIssueResponse',
                 state: str):
        """
        Configuration and state of a Managed Certificate. Certificate Manager provisions and renews Managed Certificates automatically, for as long as it's authorized to do so.
        :param Sequence['AuthorizationAttemptInfoResponse'] authorization_attempt_info: Detailed state of the latest authorization attempt for each domain specified for managed certificate resource.
        :param Sequence[str] dns_authorizations: Immutable. Authorizations that will be used for performing domain authorization.
        :param Sequence[str] domains: Immutable. The domains for which a managed SSL certificate will be generated. Wildcard domains are only supported with DNS challenge resolution.
        :param 'ProvisioningIssueResponse' provisioning_issue: Information about issues with provisioning a Managed Certificate.
        :param str state: State of the managed certificate resource.
        """
        pulumi.set(__self__, "authorization_attempt_info", authorization_attempt_info)
        pulumi.set(__self__, "dns_authorizations", dns_authorizations)
        pulumi.set(__self__, "domains", domains)
        pulumi.set(__self__, "provisioning_issue", provisioning_issue)
        pulumi.set(__self__, "state", state)

    @property
    @pulumi.getter(name="authorizationAttemptInfo")
    def authorization_attempt_info(self) -> Sequence['outputs.AuthorizationAttemptInfoResponse']:
        """
        Detailed state of the latest authorization attempt for each domain specified for managed certificate resource.
        """
        return pulumi.get(self, "authorization_attempt_info")

    @property
    @pulumi.getter(name="dnsAuthorizations")
    def dns_authorizations(self) -> Sequence[str]:
        """
        Immutable. Authorizations that will be used for performing domain authorization.
        """
        return pulumi.get(self, "dns_authorizations")

    @property
    @pulumi.getter
    def domains(self) -> Sequence[str]:
        """
        Immutable. The domains for which a managed SSL certificate will be generated. Wildcard domains are only supported with DNS challenge resolution.
        """
        return pulumi.get(self, "domains")

    @property
    @pulumi.getter(name="provisioningIssue")
    def provisioning_issue(self) -> 'outputs.ProvisioningIssueResponse':
        """
        Information about issues with provisioning a Managed Certificate.
        """
        return pulumi.get(self, "provisioning_issue")

    @property
    @pulumi.getter
    def state(self) -> str:
        """
        State of the managed certificate resource.
        """
        return pulumi.get(self, "state")


@pulumi.output_type
class ProvisioningIssueResponse(dict):
    """
    Information about issues with provisioning a Managed Certificate.
    """
    def __init__(__self__, *,
                 details: str,
                 reason: str):
        """
        Information about issues with provisioning a Managed Certificate.
        :param str details: Human readable explanation about the issue. Provided to help address the configuration issues. Not guaranteed to be stable. For programmatic access use Reason enum.
        :param str reason: Reason for provisioning failures.
        """
        pulumi.set(__self__, "details", details)
        pulumi.set(__self__, "reason", reason)

    @property
    @pulumi.getter
    def details(self) -> str:
        """
        Human readable explanation about the issue. Provided to help address the configuration issues. Not guaranteed to be stable. For programmatic access use Reason enum.
        """
        return pulumi.get(self, "details")

    @property
    @pulumi.getter
    def reason(self) -> str:
        """
        Reason for provisioning failures.
        """
        return pulumi.get(self, "reason")


@pulumi.output_type
class SelfManagedCertificateResponse(dict):
    """
    Certificate data for a SelfManaged Certificate. SelfManaged Certificates are uploaded by the user. Updating such certificates before they expire remains the user's responsibility.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "pemCertificate":
            suggest = "pem_certificate"
        elif key == "pemPrivateKey":
            suggest = "pem_private_key"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in SelfManagedCertificateResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        SelfManagedCertificateResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        SelfManagedCertificateResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 pem_certificate: str,
                 pem_private_key: str):
        """
        Certificate data for a SelfManaged Certificate. SelfManaged Certificates are uploaded by the user. Updating such certificates before they expire remains the user's responsibility.
        :param str pem_certificate: Input only. The PEM-encoded certificate chain. Leaf certificate comes first, followed by intermediate ones if any.
        :param str pem_private_key: Input only. The PEM-encoded private key of the leaf certificate.
        """
        pulumi.set(__self__, "pem_certificate", pem_certificate)
        pulumi.set(__self__, "pem_private_key", pem_private_key)

    @property
    @pulumi.getter(name="pemCertificate")
    def pem_certificate(self) -> str:
        """
        Input only. The PEM-encoded certificate chain. Leaf certificate comes first, followed by intermediate ones if any.
        """
        return pulumi.get(self, "pem_certificate")

    @property
    @pulumi.getter(name="pemPrivateKey")
    def pem_private_key(self) -> str:
        """
        Input only. The PEM-encoded private key of the leaf certificate.
        """
        return pulumi.get(self, "pem_private_key")


