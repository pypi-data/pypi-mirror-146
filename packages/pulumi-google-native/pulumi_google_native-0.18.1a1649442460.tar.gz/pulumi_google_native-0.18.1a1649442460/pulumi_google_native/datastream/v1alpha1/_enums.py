# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'GcsDestinationConfigGcsFileFormat',
    'JsonFileFormatCompression',
    'JsonFileFormatSchemaFileFormat',
    'StreamState',
]


class GcsDestinationConfigGcsFileFormat(str, Enum):
    """
    File format that data should be written in. Deprecated field (b/169501737) - use file_format instead.
    """
    GCS_FILE_FORMAT_UNSPECIFIED = "GCS_FILE_FORMAT_UNSPECIFIED"
    """
    Unspecified Cloud Storage file format.
    """
    AVRO = "AVRO"
    """
    Avro file format
    """


class JsonFileFormatCompression(str, Enum):
    """
    Compression of the loaded JSON file.
    """
    JSON_COMPRESSION_UNSPECIFIED = "JSON_COMPRESSION_UNSPECIFIED"
    """
    Unspecified json file compression.
    """
    NO_COMPRESSION = "NO_COMPRESSION"
    """
    Do not compress JSON file.
    """
    GZIP = "GZIP"
    """
    Gzip compression.
    """


class JsonFileFormatSchemaFileFormat(str, Enum):
    """
    The schema file format along JSON data files.
    """
    SCHEMA_FILE_FORMAT_UNSPECIFIED = "SCHEMA_FILE_FORMAT_UNSPECIFIED"
    """
    Unspecified schema file format.
    """
    NO_SCHEMA_FILE = "NO_SCHEMA_FILE"
    """
    Do not attach schema file.
    """
    AVRO_SCHEMA_FILE = "AVRO_SCHEMA_FILE"
    """
    Avro schema format.
    """


class StreamState(str, Enum):
    """
    The state of the stream.
    """
    STATE_UNSPECIFIED = "STATE_UNSPECIFIED"
    """
    Unspecified stream state.
    """
    CREATED = "CREATED"
    """
    The stream has been created.
    """
    RUNNING = "RUNNING"
    """
    The stream is running.
    """
    PAUSED = "PAUSED"
    """
    The stream is paused.
    """
    MAINTENANCE = "MAINTENANCE"
    """
    The stream is in maintenance mode. Updates are rejected on the resource in this state.
    """
    FAILED = "FAILED"
    """
    The stream is experiencing an error that is preventing data from being streamed.
    """
    FAILED_PERMANENTLY = "FAILED_PERMANENTLY"
    """
    The stream has experienced a terminal failure.
    """
    STARTING = "STARTING"
    """
    The stream is starting, but not yet running.
    """
    DRAINING = "DRAINING"
    """
    The Stream is no longer reading new events, but still writing events in the buffer.
    """
