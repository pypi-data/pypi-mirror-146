# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'GoogleCloudRunV2RevisionTemplateExecutionEnvironment',
    'GoogleCloudRunV2TrafficTargetType',
    'GoogleCloudRunV2VpcAccessEgress',
    'GoogleIamV1AuditLogConfigLogType',
    'ServiceIngress',
    'ServiceLaunchStage',
]


class GoogleCloudRunV2RevisionTemplateExecutionEnvironment(str, Enum):
    """
    The sandbox environment to host this Revision.
    """
    EXECUTION_ENVIRONMENT_UNSPECIFIED = "EXECUTION_ENVIRONMENT_UNSPECIFIED"
    """
    Unspecified
    """
    EXECUTION_ENVIRONMENT_DEFAULT = "EXECUTION_ENVIRONMENT_DEFAULT"
    """
    Uses the Google-default environment.
    """
    EXECUTION_ENVIRONMENT_GEN2 = "EXECUTION_ENVIRONMENT_GEN2"
    """
    Uses Second Generation environment.
    """


class GoogleCloudRunV2TrafficTargetType(str, Enum):
    """
    The allocation type for this traffic target.
    """
    TRAFFIC_TARGET_ALLOCATION_TYPE_UNSPECIFIED = "TRAFFIC_TARGET_ALLOCATION_TYPE_UNSPECIFIED"
    """
    Unspecified instance allocation type.
    """
    TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
    """
    Allocates instances to the Service's latest ready Revision.
    """
    TRAFFIC_TARGET_ALLOCATION_TYPE_REVISION = "TRAFFIC_TARGET_ALLOCATION_TYPE_REVISION"
    """
    Allocates instances to a Revision by name.
    """


class GoogleCloudRunV2VpcAccessEgress(str, Enum):
    """
    Traffic VPC egress settings.
    """
    VPC_EGRESS_UNSPECIFIED = "VPC_EGRESS_UNSPECIFIED"
    """
    Unspecified
    """
    ALL_TRAFFIC = "ALL_TRAFFIC"
    """
    All outbound traffic is routed through the VPC connector.
    """
    PRIVATE_RANGES_ONLY = "PRIVATE_RANGES_ONLY"
    """
    Only private IP ranges are routed through the VPC connector.
    """


class GoogleIamV1AuditLogConfigLogType(str, Enum):
    """
    The log type that this config enables.
    """
    LOG_TYPE_UNSPECIFIED = "LOG_TYPE_UNSPECIFIED"
    """
    Default case. Should never be this.
    """
    ADMIN_READ = "ADMIN_READ"
    """
    Admin reads. Example: CloudIAM getIamPolicy
    """
    DATA_WRITE = "DATA_WRITE"
    """
    Data writes. Example: CloudSQL Users create
    """
    DATA_READ = "DATA_READ"
    """
    Data reads. Example: CloudSQL Users list
    """


class ServiceIngress(str, Enum):
    """
    Provides the ingress settings for this Service. On output, returns the currently observed ingress settings, or INGRESS_TRAFFIC_UNSPECIFIED if no revision is active.
    """
    INGRESS_TRAFFIC_UNSPECIFIED = "INGRESS_TRAFFIC_UNSPECIFIED"
    """
    Unspecified
    """
    INGRESS_TRAFFIC_ALL = "INGRESS_TRAFFIC_ALL"
    """
    All inbound traffic is allowed.
    """
    INGRESS_TRAFFIC_INTERNAL_ONLY = "INGRESS_TRAFFIC_INTERNAL_ONLY"
    """
    Only internal traffic is allowed.
    """
    INGRESS_TRAFFIC_INTERNAL_LOAD_BALANCER = "INGRESS_TRAFFIC_INTERNAL_LOAD_BALANCER"
    """
    Both internal and Google Cloud Load Balancer traffic is allowed.
    """


class ServiceLaunchStage(str, Enum):
    """
    The launch stage as defined by [Google Cloud Platform Launch Stages](https://cloud.google.com/terms/launch-stages). Cloud Run supports `ALPHA`, `BETA`, and `GA`. If no value is specified, GA is assumed.
    """
    LAUNCH_STAGE_UNSPECIFIED = "LAUNCH_STAGE_UNSPECIFIED"
    """
    Do not use this default value.
    """
    UNIMPLEMENTED = "UNIMPLEMENTED"
    """
    The feature is not yet implemented. Users can not use it.
    """
    PRELAUNCH = "PRELAUNCH"
    """
    Prelaunch features are hidden from users and are only visible internally.
    """
    EARLY_ACCESS = "EARLY_ACCESS"
    """
    Early Access features are limited to a closed group of testers. To use these features, you must sign up in advance and sign a Trusted Tester agreement (which includes confidentiality provisions). These features may be unstable, changed in backward-incompatible ways, and are not guaranteed to be released.
    """
    ALPHA = "ALPHA"
    """
    Alpha is a limited availability test for releases before they are cleared for widespread use. By Alpha, all significant design issues are resolved and we are in the process of verifying functionality. Alpha customers need to apply for access, agree to applicable terms, and have their projects allowlisted. Alpha releases don't have to be feature complete, no SLAs are provided, and there are no technical support obligations, but they will be far enough along that customers can actually use them in test environments or for limited-use tests -- just like they would in normal production cases.
    """
    BETA = "BETA"
    """
    Beta is the point at which we are ready to open a release for any customer to use. There are no SLA or technical support obligations in a Beta release. Products will be complete from a feature perspective, but may have some open outstanding issues. Beta releases are suitable for limited production use cases.
    """
    GA = "GA"
    """
    GA features are open to all developers and are considered stable and fully qualified for production use.
    """
    DEPRECATED = "DEPRECATED"
    """
    Deprecated features are scheduled to be shut down and removed. For more information, see the "Deprecation Policy" section of our [Terms of Service](https://cloud.google.com/terms/) and the [Google Cloud Platform Subject to the Deprecation Policy](https://cloud.google.com/terms/deprecation) documentation.
    """
