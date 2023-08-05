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
    'GetCryptoKeyResult',
    'AwaitableGetCryptoKeyResult',
    'get_crypto_key',
    'get_crypto_key_output',
]

@pulumi.output_type
class GetCryptoKeyResult:
    def __init__(__self__, create_time=None, crypto_key_backend=None, destroy_scheduled_duration=None, import_only=None, labels=None, name=None, next_rotation_time=None, primary=None, purpose=None, rotation_period=None, version_template=None):
        if create_time and not isinstance(create_time, str):
            raise TypeError("Expected argument 'create_time' to be a str")
        pulumi.set(__self__, "create_time", create_time)
        if crypto_key_backend and not isinstance(crypto_key_backend, str):
            raise TypeError("Expected argument 'crypto_key_backend' to be a str")
        pulumi.set(__self__, "crypto_key_backend", crypto_key_backend)
        if destroy_scheduled_duration and not isinstance(destroy_scheduled_duration, str):
            raise TypeError("Expected argument 'destroy_scheduled_duration' to be a str")
        pulumi.set(__self__, "destroy_scheduled_duration", destroy_scheduled_duration)
        if import_only and not isinstance(import_only, bool):
            raise TypeError("Expected argument 'import_only' to be a bool")
        pulumi.set(__self__, "import_only", import_only)
        if labels and not isinstance(labels, dict):
            raise TypeError("Expected argument 'labels' to be a dict")
        pulumi.set(__self__, "labels", labels)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if next_rotation_time and not isinstance(next_rotation_time, str):
            raise TypeError("Expected argument 'next_rotation_time' to be a str")
        pulumi.set(__self__, "next_rotation_time", next_rotation_time)
        if primary and not isinstance(primary, dict):
            raise TypeError("Expected argument 'primary' to be a dict")
        pulumi.set(__self__, "primary", primary)
        if purpose and not isinstance(purpose, str):
            raise TypeError("Expected argument 'purpose' to be a str")
        pulumi.set(__self__, "purpose", purpose)
        if rotation_period and not isinstance(rotation_period, str):
            raise TypeError("Expected argument 'rotation_period' to be a str")
        pulumi.set(__self__, "rotation_period", rotation_period)
        if version_template and not isinstance(version_template, dict):
            raise TypeError("Expected argument 'version_template' to be a dict")
        pulumi.set(__self__, "version_template", version_template)

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> str:
        """
        The time at which this CryptoKey was created.
        """
        return pulumi.get(self, "create_time")

    @property
    @pulumi.getter(name="cryptoKeyBackend")
    def crypto_key_backend(self) -> str:
        """
        Immutable. The resource name of the backend environment where the key material for all CryptoKeyVersions associated with this CryptoKey reside and where all related cryptographic operations are performed. Only applicable if CryptoKeyVersions have a ProtectionLevel of EXTERNAL_VPC, with the resource name in the format `projects/*/locations/*/ekmConnections/*`. Note, this list is non-exhaustive and may apply to additional ProtectionLevels in the future.
        """
        return pulumi.get(self, "crypto_key_backend")

    @property
    @pulumi.getter(name="destroyScheduledDuration")
    def destroy_scheduled_duration(self) -> str:
        """
        Immutable. The period of time that versions of this key spend in the DESTROY_SCHEDULED state before transitioning to DESTROYED. If not specified at creation time, the default duration is 24 hours.
        """
        return pulumi.get(self, "destroy_scheduled_duration")

    @property
    @pulumi.getter(name="importOnly")
    def import_only(self) -> bool:
        """
        Immutable. Whether this key may contain imported versions only.
        """
        return pulumi.get(self, "import_only")

    @property
    @pulumi.getter
    def labels(self) -> Mapping[str, str]:
        """
        Labels with user-defined metadata. For more information, see [Labeling Keys](https://cloud.google.com/kms/docs/labeling-keys).
        """
        return pulumi.get(self, "labels")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The resource name for this CryptoKey in the format `projects/*/locations/*/keyRings/*/cryptoKeys/*`.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="nextRotationTime")
    def next_rotation_time(self) -> str:
        """
        At next_rotation_time, the Key Management Service will automatically: 1. Create a new version of this CryptoKey. 2. Mark the new version as primary. Key rotations performed manually via CreateCryptoKeyVersion and UpdateCryptoKeyPrimaryVersion do not affect next_rotation_time. Keys with purpose ENCRYPT_DECRYPT support automatic rotation. For other keys, this field must be omitted.
        """
        return pulumi.get(self, "next_rotation_time")

    @property
    @pulumi.getter
    def primary(self) -> 'outputs.CryptoKeyVersionResponse':
        """
        A copy of the "primary" CryptoKeyVersion that will be used by Encrypt when this CryptoKey is given in EncryptRequest.name. The CryptoKey's primary version can be updated via UpdateCryptoKeyPrimaryVersion. Keys with purpose ENCRYPT_DECRYPT may have a primary. For other keys, this field will be omitted.
        """
        return pulumi.get(self, "primary")

    @property
    @pulumi.getter
    def purpose(self) -> str:
        """
        Immutable. The immutable purpose of this CryptoKey.
        """
        return pulumi.get(self, "purpose")

    @property
    @pulumi.getter(name="rotationPeriod")
    def rotation_period(self) -> str:
        """
        next_rotation_time will be advanced by this period when the service automatically rotates a key. Must be at least 24 hours and at most 876,000 hours. If rotation_period is set, next_rotation_time must also be set. Keys with purpose ENCRYPT_DECRYPT support automatic rotation. For other keys, this field must be omitted.
        """
        return pulumi.get(self, "rotation_period")

    @property
    @pulumi.getter(name="versionTemplate")
    def version_template(self) -> 'outputs.CryptoKeyVersionTemplateResponse':
        """
        A template describing settings for new CryptoKeyVersion instances. The properties of new CryptoKeyVersion instances created by either CreateCryptoKeyVersion or auto-rotation are controlled by this template.
        """
        return pulumi.get(self, "version_template")


class AwaitableGetCryptoKeyResult(GetCryptoKeyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetCryptoKeyResult(
            create_time=self.create_time,
            crypto_key_backend=self.crypto_key_backend,
            destroy_scheduled_duration=self.destroy_scheduled_duration,
            import_only=self.import_only,
            labels=self.labels,
            name=self.name,
            next_rotation_time=self.next_rotation_time,
            primary=self.primary,
            purpose=self.purpose,
            rotation_period=self.rotation_period,
            version_template=self.version_template)


def get_crypto_key(crypto_key_id: Optional[str] = None,
                   key_ring_id: Optional[str] = None,
                   location: Optional[str] = None,
                   project: Optional[str] = None,
                   opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetCryptoKeyResult:
    """
    Returns metadata for a given CryptoKey, as well as its primary CryptoKeyVersion.
    """
    __args__ = dict()
    __args__['cryptoKeyId'] = crypto_key_id
    __args__['keyRingId'] = key_ring_id
    __args__['location'] = location
    __args__['project'] = project
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('google-native:cloudkms/v1:getCryptoKey', __args__, opts=opts, typ=GetCryptoKeyResult).value

    return AwaitableGetCryptoKeyResult(
        create_time=__ret__.create_time,
        crypto_key_backend=__ret__.crypto_key_backend,
        destroy_scheduled_duration=__ret__.destroy_scheduled_duration,
        import_only=__ret__.import_only,
        labels=__ret__.labels,
        name=__ret__.name,
        next_rotation_time=__ret__.next_rotation_time,
        primary=__ret__.primary,
        purpose=__ret__.purpose,
        rotation_period=__ret__.rotation_period,
        version_template=__ret__.version_template)


@_utilities.lift_output_func(get_crypto_key)
def get_crypto_key_output(crypto_key_id: Optional[pulumi.Input[str]] = None,
                          key_ring_id: Optional[pulumi.Input[str]] = None,
                          location: Optional[pulumi.Input[str]] = None,
                          project: Optional[pulumi.Input[Optional[str]]] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetCryptoKeyResult]:
    """
    Returns metadata for a given CryptoKey, as well as its primary CryptoKeyVersion.
    """
    ...
