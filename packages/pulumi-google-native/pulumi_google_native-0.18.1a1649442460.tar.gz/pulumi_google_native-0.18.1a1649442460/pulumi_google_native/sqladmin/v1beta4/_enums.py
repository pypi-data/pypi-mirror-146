# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'BackupRetentionSettingsRetentionUnit',
    'BackupRunBackupKind',
    'BackupRunStatus',
    'BackupRunType',
    'InstanceBackendType',
    'InstanceDatabaseVersion',
    'InstanceInstanceType',
    'InstanceState',
    'InstanceSuspensionReasonItem',
    'IpMappingType',
    'MaintenanceWindowUpdateTrack',
    'PasswordValidationPolicyComplexity',
    'SettingsActivationPolicy',
    'SettingsAvailabilityType',
    'SettingsDataDiskType',
    'SettingsPricingPlan',
    'SettingsReplicationType',
    'SqlOutOfDiskReportSqlOutOfDiskState',
]


class BackupRetentionSettingsRetentionUnit(str, Enum):
    """
    The unit that 'retained_backups' represents.
    """
    RETENTION_UNIT_UNSPECIFIED = "RETENTION_UNIT_UNSPECIFIED"
    """
    Backup retention unit is unspecified, will be treated as COUNT.
    """
    COUNT = "COUNT"
    """
    Retention will be by count, eg. "retain the most recent 7 backups".
    """


class BackupRunBackupKind(str, Enum):
    """
    Specifies the kind of backup, PHYSICAL or DEFAULT_SNAPSHOT.
    """
    SQL_BACKUP_KIND_UNSPECIFIED = "SQL_BACKUP_KIND_UNSPECIFIED"
    """
    This is an unknown BackupKind.
    """
    SNAPSHOT = "SNAPSHOT"
    """
    The snapshot based backups
    """
    PHYSICAL = "PHYSICAL"
    """
    Physical backups
    """


class BackupRunStatus(str, Enum):
    """
    The status of this run.
    """
    SQL_BACKUP_RUN_STATUS_UNSPECIFIED = "SQL_BACKUP_RUN_STATUS_UNSPECIFIED"
    """
    The status of the run is unknown.
    """
    ENQUEUED = "ENQUEUED"
    """
    The backup operation was enqueued.
    """
    OVERDUE = "OVERDUE"
    """
    The backup is overdue across a given backup window. Indicates a problem. Example: Long-running operation in progress during the whole window.
    """
    RUNNING = "RUNNING"
    """
    The backup is in progress.
    """
    FAILED = "FAILED"
    """
    The backup failed.
    """
    SUCCESSFUL = "SUCCESSFUL"
    """
    The backup was successful.
    """
    SKIPPED = "SKIPPED"
    """
    The backup was skipped (without problems) for a given backup window. Example: Instance was idle.
    """
    DELETION_PENDING = "DELETION_PENDING"
    """
    The backup is about to be deleted.
    """
    DELETION_FAILED = "DELETION_FAILED"
    """
    The backup deletion failed.
    """
    DELETED = "DELETED"
    """
    The backup has been deleted.
    """


class BackupRunType(str, Enum):
    """
    The type of this run; can be either "AUTOMATED" or "ON_DEMAND". This field defaults to "ON_DEMAND" and is ignored, when specified for insert requests.
    """
    SQL_BACKUP_RUN_TYPE_UNSPECIFIED = "SQL_BACKUP_RUN_TYPE_UNSPECIFIED"
    """
    This is an unknown BackupRun type.
    """
    AUTOMATED = "AUTOMATED"
    """
    The backup schedule automatically triggers a backup.
    """
    ON_DEMAND = "ON_DEMAND"
    """
    The user manually triggers a backup.
    """


class InstanceBackendType(str, Enum):
    """
    The backend type. `SECOND_GEN`: Cloud SQL database instance. `EXTERNAL`: A database server that is not managed by Google. This property is read-only; use the `tier` property in the `settings` object to determine the database type.
    """
    SQL_BACKEND_TYPE_UNSPECIFIED = "SQL_BACKEND_TYPE_UNSPECIFIED"
    """
    This is an unknown backend type for instance.
    """
    FIRST_GEN = "FIRST_GEN"
    """
    V1 speckle instance.
    """
    SECOND_GEN = "SECOND_GEN"
    """
    V2 speckle instance.
    """
    EXTERNAL = "EXTERNAL"
    """
    On premises instance.
    """


class InstanceDatabaseVersion(str, Enum):
    """
    The database engine type and version. The `databaseVersion` field cannot be changed after instance creation.
    """
    SQL_DATABASE_VERSION_UNSPECIFIED = "SQL_DATABASE_VERSION_UNSPECIFIED"
    """
    This is an unknown database version.
    """
    MYSQL51 = "MYSQL_5_1"
    """
    The database version is MySQL 5.1.
    """
    MYSQL55 = "MYSQL_5_5"
    """
    The database version is MySQL 5.5.
    """
    MYSQL56 = "MYSQL_5_6"
    """
    The database version is MySQL 5.6.
    """
    MYSQL57 = "MYSQL_5_7"
    """
    The database version is MySQL 5.7.
    """
    POSTGRES96 = "POSTGRES_9_6"
    """
    The database version is PostgreSQL 9.6.
    """
    POSTGRES11 = "POSTGRES_11"
    """
    The database version is PostgreSQL 11.
    """
    SQLSERVER2017_STANDARD = "SQLSERVER_2017_STANDARD"
    """
    The database version is SQL Server 2017 Standard.
    """
    SQLSERVER2017_ENTERPRISE = "SQLSERVER_2017_ENTERPRISE"
    """
    The database version is SQL Server 2017 Enterprise.
    """
    SQLSERVER2017_EXPRESS = "SQLSERVER_2017_EXPRESS"
    """
    The database version is SQL Server 2017 Express.
    """
    SQLSERVER2017_WEB = "SQLSERVER_2017_WEB"
    """
    The database version is SQL Server 2017 Web.
    """
    POSTGRES10 = "POSTGRES_10"
    """
    The database version is PostgreSQL 10.
    """
    POSTGRES12 = "POSTGRES_12"
    """
    The database version is PostgreSQL 12.
    """
    MYSQL80 = "MYSQL_8_0"
    """
    The database version is MySQL 8.
    """
    MYSQL8018 = "MYSQL_8_0_18"
    """
    The database major version is MySQL 8.0 and the minor version is 18.
    """
    MYSQL8026 = "MYSQL_8_0_26"
    """
    The database major version is MySQL 8.0 and the minor version is 26.
    """
    MYSQL8027 = "MYSQL_8_0_27"
    """
    The database major version is MySQL 8.0 and the minor version is 27.
    """
    MYSQL8028 = "MYSQL_8_0_28"
    """
    The database major version is MySQL 8.0 and the minor version is 28.
    """
    POSTGRES13 = "POSTGRES_13"
    """
    The database version is PostgreSQL 13.
    """
    POSTGRES14 = "POSTGRES_14"
    """
    The database version is PostgreSQL 14.
    """
    SQLSERVER2019_STANDARD = "SQLSERVER_2019_STANDARD"
    """
    The database version is SQL Server 2019 Standard.
    """
    SQLSERVER2019_ENTERPRISE = "SQLSERVER_2019_ENTERPRISE"
    """
    The database version is SQL Server 2019 Enterprise.
    """
    SQLSERVER2019_EXPRESS = "SQLSERVER_2019_EXPRESS"
    """
    The database version is SQL Server 2019 Express.
    """
    SQLSERVER2019_WEB = "SQLSERVER_2019_WEB"
    """
    The database version is SQL Server 2019 Web.
    """


class InstanceInstanceType(str, Enum):
    """
    The instance type.
    """
    SQL_INSTANCE_TYPE_UNSPECIFIED = "SQL_INSTANCE_TYPE_UNSPECIFIED"
    """
    This is an unknown Cloud SQL instance type.
    """
    CLOUD_SQL_INSTANCE = "CLOUD_SQL_INSTANCE"
    """
    A regular Cloud SQL instance that is not replicating from a primary instance.
    """
    ON_PREMISES_INSTANCE = "ON_PREMISES_INSTANCE"
    """
    An instance running on the customer's premises that is not managed by Cloud SQL.
    """
    READ_REPLICA_INSTANCE = "READ_REPLICA_INSTANCE"
    """
    A Cloud SQL instance acting as a read-replica.
    """


class InstanceState(str, Enum):
    """
    The current serving state of the Cloud SQL instance.
    """
    SQL_INSTANCE_STATE_UNSPECIFIED = "SQL_INSTANCE_STATE_UNSPECIFIED"
    """
    The state of the instance is unknown.
    """
    RUNNABLE = "RUNNABLE"
    """
    The instance is running, or has been stopped by owner.
    """
    SUSPENDED = "SUSPENDED"
    """
    The instance is not available, for example due to problems with billing.
    """
    PENDING_DELETE = "PENDING_DELETE"
    """
    The instance is being deleted.
    """
    PENDING_CREATE = "PENDING_CREATE"
    """
    The instance is being created.
    """
    MAINTENANCE = "MAINTENANCE"
    """
    The instance is down for maintenance.
    """
    FAILED = "FAILED"
    """
    The creation of the instance failed or a fatal error occurred during maintenance.
    """
    ONLINE_MAINTENANCE = "ONLINE_MAINTENANCE"
    """
    Deprecated
    """


class InstanceSuspensionReasonItem(str, Enum):
    SQL_SUSPENSION_REASON_UNSPECIFIED = "SQL_SUSPENSION_REASON_UNSPECIFIED"
    """
    This is an unknown suspension reason.
    """
    BILLING_ISSUE = "BILLING_ISSUE"
    """
    The instance is suspended due to billing issues (for example:, GCP account issue)
    """
    LEGAL_ISSUE = "LEGAL_ISSUE"
    """
    The instance is suspended due to illegal content (for example:, child pornography, copyrighted material, etc.).
    """
    OPERATIONAL_ISSUE = "OPERATIONAL_ISSUE"
    """
    The instance is causing operational issues (for example:, causing the database to crash).
    """
    KMS_KEY_ISSUE = "KMS_KEY_ISSUE"
    """
    The KMS key used by the instance is either revoked or denied access to
    """


class IpMappingType(str, Enum):
    """
    The type of this IP address. A `PRIMARY` address is a public address that can accept incoming connections. A `PRIVATE` address is a private address that can accept incoming connections. An `OUTGOING` address is the source address of connections originating from the instance, if supported.
    """
    SQL_IP_ADDRESS_TYPE_UNSPECIFIED = "SQL_IP_ADDRESS_TYPE_UNSPECIFIED"
    """
    This is an unknown IP address type.
    """
    PRIMARY = "PRIMARY"
    """
    IP address the customer is supposed to connect to. Usually this is the load balancer's IP address
    """
    OUTGOING = "OUTGOING"
    """
    Source IP address of the connection a read replica establishes to its external primary instance. This IP address can be allowlisted by the customer in case it has a firewall that filters incoming connection to its on premises primary instance.
    """
    PRIVATE = "PRIVATE"
    """
    Private IP used when using private IPs and network peering.
    """
    MIGRATED1ST_GEN = "MIGRATED_1ST_GEN"
    """
    V1 IP of a migrated instance. We want the user to decommission this IP as soon as the migration is complete. Note: V1 instances with V1 ip addresses will be counted as PRIMARY.
    """


class MaintenanceWindowUpdateTrack(str, Enum):
    """
    Maintenance timing setting: `canary` (Earlier) or `stable` (Later). [Learn more](https://cloud.google.com/sql/docs/mysql/instance-settings#maintenance-timing-2ndgen).
    """
    SQL_UPDATE_TRACK_UNSPECIFIED = "SQL_UPDATE_TRACK_UNSPECIFIED"
    """
    This is an unknown maintenance timing preference.
    """
    CANARY = "canary"
    """
    For instance update that requires a restart, this update track indicates your instance prefer to restart for new version early in maintenance window.
    """
    STABLE = "stable"
    """
    For instance update that requires a restart, this update track indicates your instance prefer to let Cloud SQL choose the timing of restart (within its Maintenance window, if applicable).
    """


class PasswordValidationPolicyComplexity(str, Enum):
    """
    The complexity of the password.
    """
    COMPLEXITY_UNSPECIFIED = "COMPLEXITY_UNSPECIFIED"
    """
    Complexity check is not specified.
    """
    COMPLEXITY_DEFAULT = "COMPLEXITY_DEFAULT"
    """
    A combination of lowercase, uppercase, numeric, and non-alphanumeric characters.
    """


class SettingsActivationPolicy(str, Enum):
    """
    The activation policy specifies when the instance is activated; it is applicable only when the instance state is RUNNABLE. Valid values: * `ALWAYS`: The instance is on, and remains so even in the absence of connection requests. * `NEVER`: The instance is off; it is not activated, even if a connection request arrives.
    """
    SQL_ACTIVATION_POLICY_UNSPECIFIED = "SQL_ACTIVATION_POLICY_UNSPECIFIED"
    """
    Unknown activation plan.
    """
    ALWAYS = "ALWAYS"
    """
    The instance is always up and running.
    """
    NEVER = "NEVER"
    """
    The instance never starts.
    """
    ON_DEMAND = "ON_DEMAND"
    """
    The instance starts upon receiving requests.
    """


class SettingsAvailabilityType(str, Enum):
    """
    Availability type. Potential values: * `ZONAL`: The instance serves data from only one zone. Outages in that zone affect data accessibility. * `REGIONAL`: The instance can serve data from more than one zone in a region (it is highly available)./ For more information, see [Overview of the High Availability Configuration](https://cloud.google.com/sql/docs/mysql/high-availability).
    """
    SQL_AVAILABILITY_TYPE_UNSPECIFIED = "SQL_AVAILABILITY_TYPE_UNSPECIFIED"
    """
    This is an unknown Availability type.
    """
    ZONAL = "ZONAL"
    """
    Zonal available instance.
    """
    REGIONAL = "REGIONAL"
    """
    Regional available instance.
    """


class SettingsDataDiskType(str, Enum):
    """
    The type of data disk: `PD_SSD` (default) or `PD_HDD`. Not used for First Generation instances.
    """
    SQL_DATA_DISK_TYPE_UNSPECIFIED = "SQL_DATA_DISK_TYPE_UNSPECIFIED"
    """
    This is an unknown data disk type.
    """
    PD_SSD = "PD_SSD"
    """
    An SSD data disk.
    """
    PD_HDD = "PD_HDD"
    """
    An HDD data disk.
    """
    OBSOLETE_LOCAL_SSD = "OBSOLETE_LOCAL_SSD"
    """
    This field is deprecated and will be removed from a future version of the API.
    """


class SettingsPricingPlan(str, Enum):
    """
    The pricing plan for this instance. This can be either `PER_USE` or `PACKAGE`. Only `PER_USE` is supported for Second Generation instances.
    """
    SQL_PRICING_PLAN_UNSPECIFIED = "SQL_PRICING_PLAN_UNSPECIFIED"
    """
    This is an unknown pricing plan for this instance.
    """
    PACKAGE = "PACKAGE"
    """
    The instance is billed at a monthly flat rate.
    """
    PER_USE = "PER_USE"
    """
    The instance is billed per usage.
    """


class SettingsReplicationType(str, Enum):
    """
    The type of replication this instance uses. This can be either `ASYNCHRONOUS` or `SYNCHRONOUS`. (Deprecated) This property was only applicable to First Generation instances.
    """
    SQL_REPLICATION_TYPE_UNSPECIFIED = "SQL_REPLICATION_TYPE_UNSPECIFIED"
    """
    This is an unknown replication type for a Cloud SQL instance.
    """
    SYNCHRONOUS = "SYNCHRONOUS"
    """
    The synchronous replication mode for First Generation instances. It is the default value.
    """
    ASYNCHRONOUS = "ASYNCHRONOUS"
    """
    The asynchronous replication mode for First Generation instances. It provides a slight performance gain, but if an outage occurs while this option is set to asynchronous, you can lose up to a few seconds of updates to your data.
    """


class SqlOutOfDiskReportSqlOutOfDiskState(str, Enum):
    """
    This field represents the state generated by the proactive database wellness job for OutOfDisk issues. * Writers: * the proactive database wellness job for OOD. * Readers: * the proactive database wellness job
    """
    SQL_OUT_OF_DISK_STATE_UNSPECIFIED = "SQL_OUT_OF_DISK_STATE_UNSPECIFIED"
    """
    Unspecified state
    """
    NORMAL = "NORMAL"
    """
    The instance has plenty space on data disk
    """
    SOFT_SHUTDOWN = "SOFT_SHUTDOWN"
    """
    Data disk is almost used up. It is shutdown to prevent data corruption.
    """
