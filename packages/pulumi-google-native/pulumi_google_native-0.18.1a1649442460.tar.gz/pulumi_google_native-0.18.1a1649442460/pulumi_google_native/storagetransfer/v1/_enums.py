# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'LoggingConfigLogActionStatesItem',
    'LoggingConfigLogActionsItem',
    'MetadataOptionsAcl',
    'MetadataOptionsGid',
    'MetadataOptionsKmsKey',
    'MetadataOptionsMode',
    'MetadataOptionsStorageClass',
    'MetadataOptionsSymlink',
    'MetadataOptionsTemporaryHold',
    'MetadataOptionsTimeCreated',
    'MetadataOptionsUid',
    'NotificationConfigEventTypesItem',
    'NotificationConfigPayloadFormat',
    'TransferJobStatus',
    'TransferOptionsOverwriteWhen',
]


class LoggingConfigLogActionStatesItem(str, Enum):
    LOGGABLE_ACTION_STATE_UNSPECIFIED = "LOGGABLE_ACTION_STATE_UNSPECIFIED"
    """
    Default value. This value is unused.
    """
    SUCCEEDED = "SUCCEEDED"
    """
    `LoggableAction` completed successfully. `SUCCEEDED` actions are logged as INFO.
    """
    FAILED = "FAILED"
    """
    `LoggableAction` terminated in an error state. `FAILED` actions are logged as ERROR.
    """


class LoggingConfigLogActionsItem(str, Enum):
    LOGGABLE_ACTION_UNSPECIFIED = "LOGGABLE_ACTION_UNSPECIFIED"
    """
    Default value. This value is unused.
    """
    FIND = "FIND"
    """
    Listing objects in a bucket.
    """
    DELETE = "DELETE"
    """
    Deleting objects at the source or the destination.
    """
    COPY = "COPY"
    """
    Copying objects to Google Cloud Storage.
    """


class MetadataOptionsAcl(str, Enum):
    """
    Specifies how each object's ACLs should be preserved for transfers between Google Cloud Storage buckets. If unspecified, the default behavior is the same as ACL_DESTINATION_BUCKET_DEFAULT.
    """
    ACL_UNSPECIFIED = "ACL_UNSPECIFIED"
    """
    ACL behavior is unspecified.
    """
    ACL_DESTINATION_BUCKET_DEFAULT = "ACL_DESTINATION_BUCKET_DEFAULT"
    """
    Use the destination bucket's default object ACLS, if applicable.
    """
    ACL_PRESERVE = "ACL_PRESERVE"
    """
    Preserve the object's original ACLs. This requires the service account to have `storage.objects.getIamPolicy` permission for the source object. [Uniform bucket-level access](https://cloud.google.com/storage/docs/uniform-bucket-level-access) must not be enabled on either the source or destination buckets.
    """


class MetadataOptionsGid(str, Enum):
    """
    Specifies how each file's POSIX group ID (GID) attribute should be handled by the transfer. By default, GID is not preserved. Only applicable to transfers involving POSIX file systems, and ignored for other transfers.
    """
    GID_UNSPECIFIED = "GID_UNSPECIFIED"
    """
    GID behavior is unspecified.
    """
    GID_SKIP = "GID_SKIP"
    """
    Do not preserve GID during a transfer job.
    """
    GID_NUMBER = "GID_NUMBER"
    """
    Preserve GID during a transfer job.
    """


class MetadataOptionsKmsKey(str, Enum):
    """
    Specifies how each object's Cloud KMS customer-managed encryption key (CMEK) is preserved for transfers between Google Cloud Storage buckets. If unspecified, the default behavior is the same as KMS_KEY_DESTINATION_BUCKET_DEFAULT.
    """
    KMS_KEY_UNSPECIFIED = "KMS_KEY_UNSPECIFIED"
    """
    KmsKey behavior is unspecified.
    """
    KMS_KEY_DESTINATION_BUCKET_DEFAULT = "KMS_KEY_DESTINATION_BUCKET_DEFAULT"
    """
    Use the destination bucket's default encryption settings.
    """
    KMS_KEY_PRESERVE = "KMS_KEY_PRESERVE"
    """
    Preserve the object's original Cloud KMS customer-managed encryption key (CMEK) if present. Objects that do not use a Cloud KMS encryption key will be encrypted using the destination bucket's encryption settings.
    """


class MetadataOptionsMode(str, Enum):
    """
    Specifies how each file's mode attribute should be handled by the transfer. By default, mode is not preserved. Only applicable to transfers involving POSIX file systems, and ignored for other transfers.
    """
    MODE_UNSPECIFIED = "MODE_UNSPECIFIED"
    """
    Mode behavior is unspecified.
    """
    MODE_SKIP = "MODE_SKIP"
    """
    Do not preserve mode during a transfer job.
    """
    MODE_PRESERVE = "MODE_PRESERVE"
    """
    Preserve mode during a transfer job.
    """


class MetadataOptionsStorageClass(str, Enum):
    """
    Specifies the storage class to set on objects being transferred to Google Cloud Storage buckets. If unspecified, the default behavior is the same as STORAGE_CLASS_DESTINATION_BUCKET_DEFAULT.
    """
    STORAGE_CLASS_UNSPECIFIED = "STORAGE_CLASS_UNSPECIFIED"
    """
    Storage class behavior is unspecified.
    """
    STORAGE_CLASS_DESTINATION_BUCKET_DEFAULT = "STORAGE_CLASS_DESTINATION_BUCKET_DEFAULT"
    """
    Use the destination bucket's default storage class.
    """
    STORAGE_CLASS_PRESERVE = "STORAGE_CLASS_PRESERVE"
    """
    Preserve the object's original storage class. This is only supported for transfers from Google Cloud Storage buckets.
    """
    STORAGE_CLASS_STANDARD = "STORAGE_CLASS_STANDARD"
    """
    Set the storage class to STANDARD.
    """
    STORAGE_CLASS_NEARLINE = "STORAGE_CLASS_NEARLINE"
    """
    Set the storage class to NEARLINE.
    """
    STORAGE_CLASS_COLDLINE = "STORAGE_CLASS_COLDLINE"
    """
    Set the storage class to COLDLINE.
    """
    STORAGE_CLASS_ARCHIVE = "STORAGE_CLASS_ARCHIVE"
    """
    Set the storage class to ARCHIVE.
    """


class MetadataOptionsSymlink(str, Enum):
    """
    Specifies how symlinks should be handled by the transfer. By default, symlinks are not preserved. Only applicable to transfers involving POSIX file systems, and ignored for other transfers.
    """
    SYMLINK_UNSPECIFIED = "SYMLINK_UNSPECIFIED"
    """
    Symlink behavior is unspecified.
    """
    SYMLINK_SKIP = "SYMLINK_SKIP"
    """
    Do not preserve symlinks during a transfer job.
    """
    SYMLINK_PRESERVE = "SYMLINK_PRESERVE"
    """
    Preserve symlinks during a transfer job.
    """


class MetadataOptionsTemporaryHold(str, Enum):
    """
    Specifies how each object's temporary hold status should be preserved for transfers between Google Cloud Storage buckets. If unspecified, the default behavior is the same as TEMPORARY_HOLD_PRESERVE.
    """
    TEMPORARY_HOLD_UNSPECIFIED = "TEMPORARY_HOLD_UNSPECIFIED"
    """
    Temporary hold behavior is unspecified.
    """
    TEMPORARY_HOLD_SKIP = "TEMPORARY_HOLD_SKIP"
    """
    Do not set a temporary hold on the destination object.
    """
    TEMPORARY_HOLD_PRESERVE = "TEMPORARY_HOLD_PRESERVE"
    """
    Preserve the object's original temporary hold status.
    """


class MetadataOptionsTimeCreated(str, Enum):
    """
    Specifies how each object's `timeCreated` metadata is preserved for transfers between Google Cloud Storage buckets. If unspecified, the default behavior is the same as TIME_CREATED_SKIP.
    """
    TIME_CREATED_UNSPECIFIED = "TIME_CREATED_UNSPECIFIED"
    """
    TimeCreated behavior is unspecified.
    """
    TIME_CREATED_SKIP = "TIME_CREATED_SKIP"
    """
    Do not preserve the `timeCreated` metadata from the source object.
    """
    TIME_CREATED_PRESERVE_AS_CUSTOM_TIME = "TIME_CREATED_PRESERVE_AS_CUSTOM_TIME"
    """
    Preserves the source object's `timeCreated` metadata in the `customTime` field in the destination object. Note that any value stored in the source object's `customTime` field will not be propagated to the destination object.
    """


class MetadataOptionsUid(str, Enum):
    """
    Specifies how each file's POSIX user ID (UID) attribute should be handled by the transfer. By default, UID is not preserved. Only applicable to transfers involving POSIX file systems, and ignored for other transfers.
    """
    UID_UNSPECIFIED = "UID_UNSPECIFIED"
    """
    UID behavior is unspecified.
    """
    UID_SKIP = "UID_SKIP"
    """
    Do not preserve UID during a transfer job.
    """
    UID_NUMBER = "UID_NUMBER"
    """
    Preserve UID during a transfer job.
    """


class NotificationConfigEventTypesItem(str, Enum):
    EVENT_TYPE_UNSPECIFIED = "EVENT_TYPE_UNSPECIFIED"
    """
    Illegal value, to avoid allowing a default.
    """
    TRANSFER_OPERATION_SUCCESS = "TRANSFER_OPERATION_SUCCESS"
    """
    `TransferOperation` completed with status SUCCESS.
    """
    TRANSFER_OPERATION_FAILED = "TRANSFER_OPERATION_FAILED"
    """
    `TransferOperation` completed with status FAILED.
    """
    TRANSFER_OPERATION_ABORTED = "TRANSFER_OPERATION_ABORTED"
    """
    `TransferOperation` completed with status ABORTED.
    """


class NotificationConfigPayloadFormat(str, Enum):
    """
    Required. The desired format of the notification message payloads.
    """
    PAYLOAD_FORMAT_UNSPECIFIED = "PAYLOAD_FORMAT_UNSPECIFIED"
    """
    Illegal value, to avoid allowing a default.
    """
    NONE = "NONE"
    """
    No payload is included with the notification.
    """
    JSON = "JSON"
    """
    `TransferOperation` is [formatted as a JSON response](https://developers.google.com/protocol-buffers/docs/proto3#json), in application/json.
    """


class TransferJobStatus(str, Enum):
    """
    Status of the job. This value MUST be specified for `CreateTransferJobRequests`. **Note:** The effect of the new job status takes place during a subsequent job run. For example, if you change the job status from ENABLED to DISABLED, and an operation spawned by the transfer is running, the status change would not affect the current operation.
    """
    STATUS_UNSPECIFIED = "STATUS_UNSPECIFIED"
    """
    Zero is an illegal value.
    """
    ENABLED = "ENABLED"
    """
    New transfers are performed based on the schedule.
    """
    DISABLED = "DISABLED"
    """
    New transfers are not scheduled.
    """
    DELETED = "DELETED"
    """
    This is a soft delete state. After a transfer job is set to this state, the job and all the transfer executions are subject to garbage collection. Transfer jobs become eligible for garbage collection 30 days after their status is set to `DELETED`.
    """


class TransferOptionsOverwriteWhen(str, Enum):
    """
    When to overwrite objects that already exist in the sink. If not set overwrite behavior is determined by overwrite_objects_already_existing_in_sink.
    """
    OVERWRITE_WHEN_UNSPECIFIED = "OVERWRITE_WHEN_UNSPECIFIED"
    """
    Indicate the option is not set.
    """
    DIFFERENT = "DIFFERENT"
    """
    Overwrite destination object with source if the two objects are different.
    """
    NEVER = "NEVER"
    """
    Never overwrite destination object.
    """
    ALWAYS = "ALWAYS"
    """
    Always overwrite destination object.
    """
