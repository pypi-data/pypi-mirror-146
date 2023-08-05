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
    'GoogleDevtoolsRemotebuildexecutionAdminV1alphaAcceleratorConfigArgs',
    'GoogleDevtoolsRemotebuildexecutionAdminV1alphaAutoscaleArgs',
    'GoogleDevtoolsRemotebuildexecutionAdminV1alphaFeaturePolicyFeatureArgs',
    'GoogleDevtoolsRemotebuildexecutionAdminV1alphaFeaturePolicyArgs',
    'GoogleDevtoolsRemotebuildexecutionAdminV1alphaWorkerConfigArgs',
]

@pulumi.input_type
class GoogleDevtoolsRemotebuildexecutionAdminV1alphaAcceleratorConfigArgs:
    def __init__(__self__, *,
                 accelerator_count: Optional[pulumi.Input[str]] = None,
                 accelerator_type: Optional[pulumi.Input[str]] = None):
        """
        AcceleratorConfig defines the accelerator cards to attach to the VM.
        :param pulumi.Input[str] accelerator_count: The number of guest accelerator cards exposed to each VM.
        :param pulumi.Input[str] accelerator_type: The type of accelerator to attach to each VM, e.g. "nvidia-tesla-k80" for nVidia Tesla K80.
        """
        if accelerator_count is not None:
            pulumi.set(__self__, "accelerator_count", accelerator_count)
        if accelerator_type is not None:
            pulumi.set(__self__, "accelerator_type", accelerator_type)

    @property
    @pulumi.getter(name="acceleratorCount")
    def accelerator_count(self) -> Optional[pulumi.Input[str]]:
        """
        The number of guest accelerator cards exposed to each VM.
        """
        return pulumi.get(self, "accelerator_count")

    @accelerator_count.setter
    def accelerator_count(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "accelerator_count", value)

    @property
    @pulumi.getter(name="acceleratorType")
    def accelerator_type(self) -> Optional[pulumi.Input[str]]:
        """
        The type of accelerator to attach to each VM, e.g. "nvidia-tesla-k80" for nVidia Tesla K80.
        """
        return pulumi.get(self, "accelerator_type")

    @accelerator_type.setter
    def accelerator_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "accelerator_type", value)


@pulumi.input_type
class GoogleDevtoolsRemotebuildexecutionAdminV1alphaAutoscaleArgs:
    def __init__(__self__, *,
                 max_size: Optional[pulumi.Input[str]] = None,
                 min_size: Optional[pulumi.Input[str]] = None):
        """
        Autoscale defines the autoscaling policy of a worker pool.
        :param pulumi.Input[str] max_size: The maximal number of workers. Must be equal to or greater than min_size.
        :param pulumi.Input[str] min_size: The minimal number of workers. Must be greater than 0.
        """
        if max_size is not None:
            pulumi.set(__self__, "max_size", max_size)
        if min_size is not None:
            pulumi.set(__self__, "min_size", min_size)

    @property
    @pulumi.getter(name="maxSize")
    def max_size(self) -> Optional[pulumi.Input[str]]:
        """
        The maximal number of workers. Must be equal to or greater than min_size.
        """
        return pulumi.get(self, "max_size")

    @max_size.setter
    def max_size(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "max_size", value)

    @property
    @pulumi.getter(name="minSize")
    def min_size(self) -> Optional[pulumi.Input[str]]:
        """
        The minimal number of workers. Must be greater than 0.
        """
        return pulumi.get(self, "min_size")

    @min_size.setter
    def min_size(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "min_size", value)


@pulumi.input_type
class GoogleDevtoolsRemotebuildexecutionAdminV1alphaFeaturePolicyFeatureArgs:
    def __init__(__self__, *,
                 allowed_values: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 policy: Optional[pulumi.Input['GoogleDevtoolsRemotebuildexecutionAdminV1alphaFeaturePolicyFeaturePolicy']] = None):
        """
        Defines whether a feature can be used or what values are accepted.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] allowed_values: A list of acceptable values. Only effective when the policy is `RESTRICTED`.
        :param pulumi.Input['GoogleDevtoolsRemotebuildexecutionAdminV1alphaFeaturePolicyFeaturePolicy'] policy: The policy of the feature.
        """
        if allowed_values is not None:
            pulumi.set(__self__, "allowed_values", allowed_values)
        if policy is not None:
            pulumi.set(__self__, "policy", policy)

    @property
    @pulumi.getter(name="allowedValues")
    def allowed_values(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of acceptable values. Only effective when the policy is `RESTRICTED`.
        """
        return pulumi.get(self, "allowed_values")

    @allowed_values.setter
    def allowed_values(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "allowed_values", value)

    @property
    @pulumi.getter
    def policy(self) -> Optional[pulumi.Input['GoogleDevtoolsRemotebuildexecutionAdminV1alphaFeaturePolicyFeaturePolicy']]:
        """
        The policy of the feature.
        """
        return pulumi.get(self, "policy")

    @policy.setter
    def policy(self, value: Optional[pulumi.Input['GoogleDevtoolsRemotebuildexecutionAdminV1alphaFeaturePolicyFeaturePolicy']]):
        pulumi.set(self, "policy", value)


@pulumi.input_type
class GoogleDevtoolsRemotebuildexecutionAdminV1alphaFeaturePolicyArgs:
    def __init__(__self__, *,
                 container_image_sources: Optional[pulumi.Input['GoogleDevtoolsRemotebuildexecutionAdminV1alphaFeaturePolicyFeatureArgs']] = None,
                 docker_add_capabilities: Optional[pulumi.Input['GoogleDevtoolsRemotebuildexecutionAdminV1alphaFeaturePolicyFeatureArgs']] = None,
                 docker_chroot_path: Optional[pulumi.Input['GoogleDevtoolsRemotebuildexecutionAdminV1alphaFeaturePolicyFeatureArgs']] = None,
                 docker_network: Optional[pulumi.Input['GoogleDevtoolsRemotebuildexecutionAdminV1alphaFeaturePolicyFeatureArgs']] = None,
                 docker_privileged: Optional[pulumi.Input['GoogleDevtoolsRemotebuildexecutionAdminV1alphaFeaturePolicyFeatureArgs']] = None,
                 docker_run_as_root: Optional[pulumi.Input['GoogleDevtoolsRemotebuildexecutionAdminV1alphaFeaturePolicyFeatureArgs']] = None,
                 docker_runtime: Optional[pulumi.Input['GoogleDevtoolsRemotebuildexecutionAdminV1alphaFeaturePolicyFeatureArgs']] = None,
                 docker_sibling_containers: Optional[pulumi.Input['GoogleDevtoolsRemotebuildexecutionAdminV1alphaFeaturePolicyFeatureArgs']] = None,
                 linux_isolation: Optional[pulumi.Input['GoogleDevtoolsRemotebuildexecutionAdminV1alphaFeaturePolicyLinuxIsolation']] = None):
        """
        FeaturePolicy defines features allowed to be used on RBE instances, as well as instance-wide behavior changes that take effect without opt-in or opt-out at usage time.
        :param pulumi.Input['GoogleDevtoolsRemotebuildexecutionAdminV1alphaFeaturePolicyFeatureArgs'] container_image_sources: Which container image sources are allowed. Currently only RBE-supported registry (gcr.io) is allowed. One can allow all repositories under a project or one specific repository only. E.g. container_image_sources { policy: RESTRICTED allowed_values: [ "gcr.io/project-foo", "gcr.io/project-bar/repo-baz", ] } will allow any repositories under "gcr.io/project-foo" plus the repository "gcr.io/project-bar/repo-baz". Default (UNSPECIFIED) is equivalent to any source is allowed.
        :param pulumi.Input['GoogleDevtoolsRemotebuildexecutionAdminV1alphaFeaturePolicyFeatureArgs'] docker_add_capabilities: Whether dockerAddCapabilities can be used or what capabilities are allowed.
        :param pulumi.Input['GoogleDevtoolsRemotebuildexecutionAdminV1alphaFeaturePolicyFeatureArgs'] docker_chroot_path: Whether dockerChrootPath can be used.
        :param pulumi.Input['GoogleDevtoolsRemotebuildexecutionAdminV1alphaFeaturePolicyFeatureArgs'] docker_network: Whether dockerNetwork can be used or what network modes are allowed. E.g. one may allow `off` value only via `allowed_values`.
        :param pulumi.Input['GoogleDevtoolsRemotebuildexecutionAdminV1alphaFeaturePolicyFeatureArgs'] docker_privileged: Whether dockerPrivileged can be used.
        :param pulumi.Input['GoogleDevtoolsRemotebuildexecutionAdminV1alphaFeaturePolicyFeatureArgs'] docker_run_as_root: Whether dockerRunAsRoot can be used.
        :param pulumi.Input['GoogleDevtoolsRemotebuildexecutionAdminV1alphaFeaturePolicyFeatureArgs'] docker_runtime: Whether dockerRuntime is allowed to be set or what runtimes are allowed. Note linux_isolation takes precedence, and if set, docker_runtime values may be rejected if they are incompatible with the selected isolation.
        :param pulumi.Input['GoogleDevtoolsRemotebuildexecutionAdminV1alphaFeaturePolicyFeatureArgs'] docker_sibling_containers: Whether dockerSiblingContainers can be used.
        :param pulumi.Input['GoogleDevtoolsRemotebuildexecutionAdminV1alphaFeaturePolicyLinuxIsolation'] linux_isolation: linux_isolation allows overriding the docker runtime used for containers started on Linux.
        """
        if container_image_sources is not None:
            pulumi.set(__self__, "container_image_sources", container_image_sources)
        if docker_add_capabilities is not None:
            pulumi.set(__self__, "docker_add_capabilities", docker_add_capabilities)
        if docker_chroot_path is not None:
            pulumi.set(__self__, "docker_chroot_path", docker_chroot_path)
        if docker_network is not None:
            pulumi.set(__self__, "docker_network", docker_network)
        if docker_privileged is not None:
            pulumi.set(__self__, "docker_privileged", docker_privileged)
        if docker_run_as_root is not None:
            pulumi.set(__self__, "docker_run_as_root", docker_run_as_root)
        if docker_runtime is not None:
            pulumi.set(__self__, "docker_runtime", docker_runtime)
        if docker_sibling_containers is not None:
            pulumi.set(__self__, "docker_sibling_containers", docker_sibling_containers)
        if linux_isolation is not None:
            pulumi.set(__self__, "linux_isolation", linux_isolation)

    @property
    @pulumi.getter(name="containerImageSources")
    def container_image_sources(self) -> Optional[pulumi.Input['GoogleDevtoolsRemotebuildexecutionAdminV1alphaFeaturePolicyFeatureArgs']]:
        """
        Which container image sources are allowed. Currently only RBE-supported registry (gcr.io) is allowed. One can allow all repositories under a project or one specific repository only. E.g. container_image_sources { policy: RESTRICTED allowed_values: [ "gcr.io/project-foo", "gcr.io/project-bar/repo-baz", ] } will allow any repositories under "gcr.io/project-foo" plus the repository "gcr.io/project-bar/repo-baz". Default (UNSPECIFIED) is equivalent to any source is allowed.
        """
        return pulumi.get(self, "container_image_sources")

    @container_image_sources.setter
    def container_image_sources(self, value: Optional[pulumi.Input['GoogleDevtoolsRemotebuildexecutionAdminV1alphaFeaturePolicyFeatureArgs']]):
        pulumi.set(self, "container_image_sources", value)

    @property
    @pulumi.getter(name="dockerAddCapabilities")
    def docker_add_capabilities(self) -> Optional[pulumi.Input['GoogleDevtoolsRemotebuildexecutionAdminV1alphaFeaturePolicyFeatureArgs']]:
        """
        Whether dockerAddCapabilities can be used or what capabilities are allowed.
        """
        return pulumi.get(self, "docker_add_capabilities")

    @docker_add_capabilities.setter
    def docker_add_capabilities(self, value: Optional[pulumi.Input['GoogleDevtoolsRemotebuildexecutionAdminV1alphaFeaturePolicyFeatureArgs']]):
        pulumi.set(self, "docker_add_capabilities", value)

    @property
    @pulumi.getter(name="dockerChrootPath")
    def docker_chroot_path(self) -> Optional[pulumi.Input['GoogleDevtoolsRemotebuildexecutionAdminV1alphaFeaturePolicyFeatureArgs']]:
        """
        Whether dockerChrootPath can be used.
        """
        return pulumi.get(self, "docker_chroot_path")

    @docker_chroot_path.setter
    def docker_chroot_path(self, value: Optional[pulumi.Input['GoogleDevtoolsRemotebuildexecutionAdminV1alphaFeaturePolicyFeatureArgs']]):
        pulumi.set(self, "docker_chroot_path", value)

    @property
    @pulumi.getter(name="dockerNetwork")
    def docker_network(self) -> Optional[pulumi.Input['GoogleDevtoolsRemotebuildexecutionAdminV1alphaFeaturePolicyFeatureArgs']]:
        """
        Whether dockerNetwork can be used or what network modes are allowed. E.g. one may allow `off` value only via `allowed_values`.
        """
        return pulumi.get(self, "docker_network")

    @docker_network.setter
    def docker_network(self, value: Optional[pulumi.Input['GoogleDevtoolsRemotebuildexecutionAdminV1alphaFeaturePolicyFeatureArgs']]):
        pulumi.set(self, "docker_network", value)

    @property
    @pulumi.getter(name="dockerPrivileged")
    def docker_privileged(self) -> Optional[pulumi.Input['GoogleDevtoolsRemotebuildexecutionAdminV1alphaFeaturePolicyFeatureArgs']]:
        """
        Whether dockerPrivileged can be used.
        """
        return pulumi.get(self, "docker_privileged")

    @docker_privileged.setter
    def docker_privileged(self, value: Optional[pulumi.Input['GoogleDevtoolsRemotebuildexecutionAdminV1alphaFeaturePolicyFeatureArgs']]):
        pulumi.set(self, "docker_privileged", value)

    @property
    @pulumi.getter(name="dockerRunAsRoot")
    def docker_run_as_root(self) -> Optional[pulumi.Input['GoogleDevtoolsRemotebuildexecutionAdminV1alphaFeaturePolicyFeatureArgs']]:
        """
        Whether dockerRunAsRoot can be used.
        """
        return pulumi.get(self, "docker_run_as_root")

    @docker_run_as_root.setter
    def docker_run_as_root(self, value: Optional[pulumi.Input['GoogleDevtoolsRemotebuildexecutionAdminV1alphaFeaturePolicyFeatureArgs']]):
        pulumi.set(self, "docker_run_as_root", value)

    @property
    @pulumi.getter(name="dockerRuntime")
    def docker_runtime(self) -> Optional[pulumi.Input['GoogleDevtoolsRemotebuildexecutionAdminV1alphaFeaturePolicyFeatureArgs']]:
        """
        Whether dockerRuntime is allowed to be set or what runtimes are allowed. Note linux_isolation takes precedence, and if set, docker_runtime values may be rejected if they are incompatible with the selected isolation.
        """
        return pulumi.get(self, "docker_runtime")

    @docker_runtime.setter
    def docker_runtime(self, value: Optional[pulumi.Input['GoogleDevtoolsRemotebuildexecutionAdminV1alphaFeaturePolicyFeatureArgs']]):
        pulumi.set(self, "docker_runtime", value)

    @property
    @pulumi.getter(name="dockerSiblingContainers")
    def docker_sibling_containers(self) -> Optional[pulumi.Input['GoogleDevtoolsRemotebuildexecutionAdminV1alphaFeaturePolicyFeatureArgs']]:
        """
        Whether dockerSiblingContainers can be used.
        """
        return pulumi.get(self, "docker_sibling_containers")

    @docker_sibling_containers.setter
    def docker_sibling_containers(self, value: Optional[pulumi.Input['GoogleDevtoolsRemotebuildexecutionAdminV1alphaFeaturePolicyFeatureArgs']]):
        pulumi.set(self, "docker_sibling_containers", value)

    @property
    @pulumi.getter(name="linuxIsolation")
    def linux_isolation(self) -> Optional[pulumi.Input['GoogleDevtoolsRemotebuildexecutionAdminV1alphaFeaturePolicyLinuxIsolation']]:
        """
        linux_isolation allows overriding the docker runtime used for containers started on Linux.
        """
        return pulumi.get(self, "linux_isolation")

    @linux_isolation.setter
    def linux_isolation(self, value: Optional[pulumi.Input['GoogleDevtoolsRemotebuildexecutionAdminV1alphaFeaturePolicyLinuxIsolation']]):
        pulumi.set(self, "linux_isolation", value)


@pulumi.input_type
class GoogleDevtoolsRemotebuildexecutionAdminV1alphaWorkerConfigArgs:
    def __init__(__self__, *,
                 disk_size_gb: pulumi.Input[str],
                 disk_type: pulumi.Input[str],
                 machine_type: pulumi.Input[str],
                 accelerator: Optional[pulumi.Input['GoogleDevtoolsRemotebuildexecutionAdminV1alphaAcceleratorConfigArgs']] = None,
                 labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 max_concurrent_actions: Optional[pulumi.Input[str]] = None,
                 min_cpu_platform: Optional[pulumi.Input[str]] = None,
                 network_access: Optional[pulumi.Input[str]] = None,
                 reserved: Optional[pulumi.Input[bool]] = None,
                 sole_tenant_node_type: Optional[pulumi.Input[str]] = None,
                 vm_image: Optional[pulumi.Input[str]] = None):
        """
        Defines the configuration to be used for creating workers in the worker pool.
        :param pulumi.Input[str] disk_size_gb: Size of the disk attached to the worker, in GB. See https://cloud.google.com/compute/docs/disks/
        :param pulumi.Input[str] disk_type: Disk Type to use for the worker. See [Storage options](https://cloud.google.com/compute/docs/disks/#introduction). Currently only `pd-standard` and `pd-ssd` are supported.
        :param pulumi.Input[str] machine_type: Machine type of the worker, such as `e2-standard-2`. See https://cloud.google.com/compute/docs/machine-types for a list of supported machine types. Note that `f1-micro` and `g1-small` are not yet supported.
        :param pulumi.Input['GoogleDevtoolsRemotebuildexecutionAdminV1alphaAcceleratorConfigArgs'] accelerator: The accelerator card attached to each VM.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: Labels associated with the workers. Label keys and values can be no longer than 63 characters, can only contain lowercase letters, numeric characters, underscores and dashes. International letters are permitted. Label keys must start with a letter. Label values are optional. There can not be more than 64 labels per resource.
        :param pulumi.Input[str] max_concurrent_actions: The maximum number of actions a worker can execute concurrently.
        :param pulumi.Input[str] min_cpu_platform: Minimum CPU platform to use when creating the worker. See [CPU Platforms](https://cloud.google.com/compute/docs/cpu-platforms).
        :param pulumi.Input[str] network_access: Determines the type of network access granted to workers. Possible values: - "public": Workers can connect to the public internet. - "private": Workers can only connect to Google APIs and services. - "restricted-private": Workers can only connect to Google APIs that are reachable through `restricted.googleapis.com` (`199.36.153.4/30`).
        :param pulumi.Input[bool] reserved: Determines whether the worker is reserved (equivalent to a Compute Engine on-demand VM and therefore won't be preempted). See [Preemptible VMs](https://cloud.google.com/preemptible-vms/) for more details.
        :param pulumi.Input[str] sole_tenant_node_type: The node type name to be used for sole-tenant nodes.
        :param pulumi.Input[str] vm_image: The name of the image used by each VM.
        """
        pulumi.set(__self__, "disk_size_gb", disk_size_gb)
        pulumi.set(__self__, "disk_type", disk_type)
        pulumi.set(__self__, "machine_type", machine_type)
        if accelerator is not None:
            pulumi.set(__self__, "accelerator", accelerator)
        if labels is not None:
            pulumi.set(__self__, "labels", labels)
        if max_concurrent_actions is not None:
            pulumi.set(__self__, "max_concurrent_actions", max_concurrent_actions)
        if min_cpu_platform is not None:
            pulumi.set(__self__, "min_cpu_platform", min_cpu_platform)
        if network_access is not None:
            pulumi.set(__self__, "network_access", network_access)
        if reserved is not None:
            pulumi.set(__self__, "reserved", reserved)
        if sole_tenant_node_type is not None:
            pulumi.set(__self__, "sole_tenant_node_type", sole_tenant_node_type)
        if vm_image is not None:
            pulumi.set(__self__, "vm_image", vm_image)

    @property
    @pulumi.getter(name="diskSizeGb")
    def disk_size_gb(self) -> pulumi.Input[str]:
        """
        Size of the disk attached to the worker, in GB. See https://cloud.google.com/compute/docs/disks/
        """
        return pulumi.get(self, "disk_size_gb")

    @disk_size_gb.setter
    def disk_size_gb(self, value: pulumi.Input[str]):
        pulumi.set(self, "disk_size_gb", value)

    @property
    @pulumi.getter(name="diskType")
    def disk_type(self) -> pulumi.Input[str]:
        """
        Disk Type to use for the worker. See [Storage options](https://cloud.google.com/compute/docs/disks/#introduction). Currently only `pd-standard` and `pd-ssd` are supported.
        """
        return pulumi.get(self, "disk_type")

    @disk_type.setter
    def disk_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "disk_type", value)

    @property
    @pulumi.getter(name="machineType")
    def machine_type(self) -> pulumi.Input[str]:
        """
        Machine type of the worker, such as `e2-standard-2`. See https://cloud.google.com/compute/docs/machine-types for a list of supported machine types. Note that `f1-micro` and `g1-small` are not yet supported.
        """
        return pulumi.get(self, "machine_type")

    @machine_type.setter
    def machine_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "machine_type", value)

    @property
    @pulumi.getter
    def accelerator(self) -> Optional[pulumi.Input['GoogleDevtoolsRemotebuildexecutionAdminV1alphaAcceleratorConfigArgs']]:
        """
        The accelerator card attached to each VM.
        """
        return pulumi.get(self, "accelerator")

    @accelerator.setter
    def accelerator(self, value: Optional[pulumi.Input['GoogleDevtoolsRemotebuildexecutionAdminV1alphaAcceleratorConfigArgs']]):
        pulumi.set(self, "accelerator", value)

    @property
    @pulumi.getter
    def labels(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Labels associated with the workers. Label keys and values can be no longer than 63 characters, can only contain lowercase letters, numeric characters, underscores and dashes. International letters are permitted. Label keys must start with a letter. Label values are optional. There can not be more than 64 labels per resource.
        """
        return pulumi.get(self, "labels")

    @labels.setter
    def labels(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "labels", value)

    @property
    @pulumi.getter(name="maxConcurrentActions")
    def max_concurrent_actions(self) -> Optional[pulumi.Input[str]]:
        """
        The maximum number of actions a worker can execute concurrently.
        """
        return pulumi.get(self, "max_concurrent_actions")

    @max_concurrent_actions.setter
    def max_concurrent_actions(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "max_concurrent_actions", value)

    @property
    @pulumi.getter(name="minCpuPlatform")
    def min_cpu_platform(self) -> Optional[pulumi.Input[str]]:
        """
        Minimum CPU platform to use when creating the worker. See [CPU Platforms](https://cloud.google.com/compute/docs/cpu-platforms).
        """
        return pulumi.get(self, "min_cpu_platform")

    @min_cpu_platform.setter
    def min_cpu_platform(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "min_cpu_platform", value)

    @property
    @pulumi.getter(name="networkAccess")
    def network_access(self) -> Optional[pulumi.Input[str]]:
        """
        Determines the type of network access granted to workers. Possible values: - "public": Workers can connect to the public internet. - "private": Workers can only connect to Google APIs and services. - "restricted-private": Workers can only connect to Google APIs that are reachable through `restricted.googleapis.com` (`199.36.153.4/30`).
        """
        return pulumi.get(self, "network_access")

    @network_access.setter
    def network_access(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "network_access", value)

    @property
    @pulumi.getter
    def reserved(self) -> Optional[pulumi.Input[bool]]:
        """
        Determines whether the worker is reserved (equivalent to a Compute Engine on-demand VM and therefore won't be preempted). See [Preemptible VMs](https://cloud.google.com/preemptible-vms/) for more details.
        """
        return pulumi.get(self, "reserved")

    @reserved.setter
    def reserved(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "reserved", value)

    @property
    @pulumi.getter(name="soleTenantNodeType")
    def sole_tenant_node_type(self) -> Optional[pulumi.Input[str]]:
        """
        The node type name to be used for sole-tenant nodes.
        """
        return pulumi.get(self, "sole_tenant_node_type")

    @sole_tenant_node_type.setter
    def sole_tenant_node_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "sole_tenant_node_type", value)

    @property
    @pulumi.getter(name="vmImage")
    def vm_image(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the image used by each VM.
        """
        return pulumi.get(self, "vm_image")

    @vm_image.setter
    def vm_image(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "vm_image", value)


