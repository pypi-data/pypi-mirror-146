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
    'ModelStateResponse',
    'OperationResponse',
    'StatusResponse',
    'TfLiteModelResponse',
]

@pulumi.output_type
class ModelStateResponse(dict):
    """
    State common to all model types. Includes publishing and validation information.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "validationError":
            suggest = "validation_error"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ModelStateResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ModelStateResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ModelStateResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 published: bool,
                 validation_error: 'outputs.StatusResponse'):
        """
        State common to all model types. Includes publishing and validation information.
        :param bool published: Indicates if this model has been published.
        :param 'StatusResponse' validation_error: Indicates the latest validation error on the model if any. A model may have validation errors if there were problems during the model creation/update. e.g. in the case of a TfLiteModel, if a tflite model file was missing or in the wrong format. This field will be empty for valid models.
        """
        pulumi.set(__self__, "published", published)
        pulumi.set(__self__, "validation_error", validation_error)

    @property
    @pulumi.getter
    def published(self) -> bool:
        """
        Indicates if this model has been published.
        """
        return pulumi.get(self, "published")

    @property
    @pulumi.getter(name="validationError")
    def validation_error(self) -> 'outputs.StatusResponse':
        """
        Indicates the latest validation error on the model if any. A model may have validation errors if there were problems during the model creation/update. e.g. in the case of a TfLiteModel, if a tflite model file was missing or in the wrong format. This field will be empty for valid models.
        """
        return pulumi.get(self, "validation_error")


@pulumi.output_type
class OperationResponse(dict):
    """
    This resource represents a long-running operation that is the result of a network API call.
    """
    def __init__(__self__, *,
                 done: bool,
                 error: 'outputs.StatusResponse',
                 metadata: Mapping[str, str],
                 name: str,
                 response: Mapping[str, str]):
        """
        This resource represents a long-running operation that is the result of a network API call.
        :param bool done: If the value is `false`, it means the operation is still in progress. If `true`, the operation is completed, and either `error` or `response` is available.
        :param 'StatusResponse' error: The error result of the operation in case of failure or cancellation.
        :param Mapping[str, str] metadata: Service-specific metadata associated with the operation. It typically contains progress information and common metadata such as create time. Some services might not provide such metadata. Any method that returns a long-running operation should document the metadata type, if any.
        :param str name: The server-assigned name, which is only unique within the same service that originally returns it. If you use the default HTTP mapping, the `name` should be a resource name ending with `operations/{unique_id}`.
        :param Mapping[str, str] response: The normal response of the operation in case of success. If the original method returns no data on success, such as `Delete`, the response is `google.protobuf.Empty`. If the original method is standard `Get`/`Create`/`Update`, the response should be the resource. For other methods, the response should have the type `XxxResponse`, where `Xxx` is the original method name. For example, if the original method name is `TakeSnapshot()`, the inferred response type is `TakeSnapshotResponse`.
        """
        pulumi.set(__self__, "done", done)
        pulumi.set(__self__, "error", error)
        pulumi.set(__self__, "metadata", metadata)
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "response", response)

    @property
    @pulumi.getter
    def done(self) -> bool:
        """
        If the value is `false`, it means the operation is still in progress. If `true`, the operation is completed, and either `error` or `response` is available.
        """
        return pulumi.get(self, "done")

    @property
    @pulumi.getter
    def error(self) -> 'outputs.StatusResponse':
        """
        The error result of the operation in case of failure or cancellation.
        """
        return pulumi.get(self, "error")

    @property
    @pulumi.getter
    def metadata(self) -> Mapping[str, str]:
        """
        Service-specific metadata associated with the operation. It typically contains progress information and common metadata such as create time. Some services might not provide such metadata. Any method that returns a long-running operation should document the metadata type, if any.
        """
        return pulumi.get(self, "metadata")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The server-assigned name, which is only unique within the same service that originally returns it. If you use the default HTTP mapping, the `name` should be a resource name ending with `operations/{unique_id}`.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def response(self) -> Mapping[str, str]:
        """
        The normal response of the operation in case of success. If the original method returns no data on success, such as `Delete`, the response is `google.protobuf.Empty`. If the original method is standard `Get`/`Create`/`Update`, the response should be the resource. For other methods, the response should have the type `XxxResponse`, where `Xxx` is the original method name. For example, if the original method name is `TakeSnapshot()`, the inferred response type is `TakeSnapshotResponse`.
        """
        return pulumi.get(self, "response")


@pulumi.output_type
class StatusResponse(dict):
    """
    The `Status` type defines a logical error model that is suitable for different programming environments, including REST APIs and RPC APIs. It is used by [gRPC](https://github.com/grpc). Each `Status` message contains three pieces of data: error code, error message, and error details. You can find out more about this error model and how to work with it in the [API Design Guide](https://cloud.google.com/apis/design/errors).
    """
    def __init__(__self__, *,
                 code: int,
                 details: Sequence[Mapping[str, str]],
                 message: str):
        """
        The `Status` type defines a logical error model that is suitable for different programming environments, including REST APIs and RPC APIs. It is used by [gRPC](https://github.com/grpc). Each `Status` message contains three pieces of data: error code, error message, and error details. You can find out more about this error model and how to work with it in the [API Design Guide](https://cloud.google.com/apis/design/errors).
        :param int code: The status code, which should be an enum value of google.rpc.Code.
        :param Sequence[Mapping[str, str]] details: A list of messages that carry the error details. There is a common set of message types for APIs to use.
        :param str message: A developer-facing error message, which should be in English. Any user-facing error message should be localized and sent in the google.rpc.Status.details field, or localized by the client.
        """
        pulumi.set(__self__, "code", code)
        pulumi.set(__self__, "details", details)
        pulumi.set(__self__, "message", message)

    @property
    @pulumi.getter
    def code(self) -> int:
        """
        The status code, which should be an enum value of google.rpc.Code.
        """
        return pulumi.get(self, "code")

    @property
    @pulumi.getter
    def details(self) -> Sequence[Mapping[str, str]]:
        """
        A list of messages that carry the error details. There is a common set of message types for APIs to use.
        """
        return pulumi.get(self, "details")

    @property
    @pulumi.getter
    def message(self) -> str:
        """
        A developer-facing error message, which should be in English. Any user-facing error message should be localized and sent in the google.rpc.Status.details field, or localized by the client.
        """
        return pulumi.get(self, "message")


@pulumi.output_type
class TfLiteModelResponse(dict):
    """
    Information that is specific to TfLite models.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "automlModel":
            suggest = "automl_model"
        elif key == "gcsTfliteUri":
            suggest = "gcs_tflite_uri"
        elif key == "sizeBytes":
            suggest = "size_bytes"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in TfLiteModelResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        TfLiteModelResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        TfLiteModelResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 automl_model: str,
                 gcs_tflite_uri: str,
                 size_bytes: str):
        """
        Information that is specific to TfLite models.
        :param str automl_model: The AutoML model id referencing a model you created with the AutoML API. The name should have format 'projects//locations//models/' (This is the model resource name returned from the AutoML API)
        :param str gcs_tflite_uri: The TfLite file containing the model. (Stored in Google Cloud). The gcs_tflite_uri should have form: gs://some-bucket/some-model.tflite Note: If you update the file in the original location, it is necessary to call UpdateModel for ML to pick up and validate the updated file.
        :param str size_bytes: The size of the TFLite model
        """
        pulumi.set(__self__, "automl_model", automl_model)
        pulumi.set(__self__, "gcs_tflite_uri", gcs_tflite_uri)
        pulumi.set(__self__, "size_bytes", size_bytes)

    @property
    @pulumi.getter(name="automlModel")
    def automl_model(self) -> str:
        """
        The AutoML model id referencing a model you created with the AutoML API. The name should have format 'projects//locations//models/' (This is the model resource name returned from the AutoML API)
        """
        return pulumi.get(self, "automl_model")

    @property
    @pulumi.getter(name="gcsTfliteUri")
    def gcs_tflite_uri(self) -> str:
        """
        The TfLite file containing the model. (Stored in Google Cloud). The gcs_tflite_uri should have form: gs://some-bucket/some-model.tflite Note: If you update the file in the original location, it is necessary to call UpdateModel for ML to pick up and validate the updated file.
        """
        return pulumi.get(self, "gcs_tflite_uri")

    @property
    @pulumi.getter(name="sizeBytes")
    def size_bytes(self) -> str:
        """
        The size of the TFLite model
        """
        return pulumi.get(self, "size_bytes")


