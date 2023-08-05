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
    'GoogleCloudBillingBudgetsV1BudgetAmountArgs',
    'GoogleCloudBillingBudgetsV1CustomPeriodArgs',
    'GoogleCloudBillingBudgetsV1FilterArgs',
    'GoogleCloudBillingBudgetsV1LastPeriodAmountArgs',
    'GoogleCloudBillingBudgetsV1NotificationsRuleArgs',
    'GoogleCloudBillingBudgetsV1ThresholdRuleArgs',
    'GoogleTypeDateArgs',
    'GoogleTypeMoneyArgs',
]

@pulumi.input_type
class GoogleCloudBillingBudgetsV1BudgetAmountArgs:
    def __init__(__self__, *,
                 last_period_amount: Optional[pulumi.Input['GoogleCloudBillingBudgetsV1LastPeriodAmountArgs']] = None,
                 specified_amount: Optional[pulumi.Input['GoogleTypeMoneyArgs']] = None):
        """
        The budgeted amount for each usage period.
        :param pulumi.Input['GoogleCloudBillingBudgetsV1LastPeriodAmountArgs'] last_period_amount: Use the last period's actual spend as the budget for the present period. LastPeriodAmount can only be set when the budget's time period is a Filter.calendar_period. It cannot be set in combination with Filter.custom_period.
        :param pulumi.Input['GoogleTypeMoneyArgs'] specified_amount: A specified amount to use as the budget. `currency_code` is optional. If specified when creating a budget, it must match the currency of the billing account. If specified when updating a budget, it must match the currency_code of the existing budget. The `currency_code` is provided on output.
        """
        if last_period_amount is not None:
            pulumi.set(__self__, "last_period_amount", last_period_amount)
        if specified_amount is not None:
            pulumi.set(__self__, "specified_amount", specified_amount)

    @property
    @pulumi.getter(name="lastPeriodAmount")
    def last_period_amount(self) -> Optional[pulumi.Input['GoogleCloudBillingBudgetsV1LastPeriodAmountArgs']]:
        """
        Use the last period's actual spend as the budget for the present period. LastPeriodAmount can only be set when the budget's time period is a Filter.calendar_period. It cannot be set in combination with Filter.custom_period.
        """
        return pulumi.get(self, "last_period_amount")

    @last_period_amount.setter
    def last_period_amount(self, value: Optional[pulumi.Input['GoogleCloudBillingBudgetsV1LastPeriodAmountArgs']]):
        pulumi.set(self, "last_period_amount", value)

    @property
    @pulumi.getter(name="specifiedAmount")
    def specified_amount(self) -> Optional[pulumi.Input['GoogleTypeMoneyArgs']]:
        """
        A specified amount to use as the budget. `currency_code` is optional. If specified when creating a budget, it must match the currency of the billing account. If specified when updating a budget, it must match the currency_code of the existing budget. The `currency_code` is provided on output.
        """
        return pulumi.get(self, "specified_amount")

    @specified_amount.setter
    def specified_amount(self, value: Optional[pulumi.Input['GoogleTypeMoneyArgs']]):
        pulumi.set(self, "specified_amount", value)


@pulumi.input_type
class GoogleCloudBillingBudgetsV1CustomPeriodArgs:
    def __init__(__self__, *,
                 start_date: pulumi.Input['GoogleTypeDateArgs'],
                 end_date: Optional[pulumi.Input['GoogleTypeDateArgs']] = None):
        """
        All date times begin at 12 AM US and Canadian Pacific Time (UTC-8).
        :param pulumi.Input['GoogleTypeDateArgs'] start_date: The start date must be after January 1, 2017.
        :param pulumi.Input['GoogleTypeDateArgs'] end_date: Optional. The end date of the time period. Budgets with elapsed end date won't be processed. If unset, specifies to track all usage incurred since the start_date.
        """
        pulumi.set(__self__, "start_date", start_date)
        if end_date is not None:
            pulumi.set(__self__, "end_date", end_date)

    @property
    @pulumi.getter(name="startDate")
    def start_date(self) -> pulumi.Input['GoogleTypeDateArgs']:
        """
        The start date must be after January 1, 2017.
        """
        return pulumi.get(self, "start_date")

    @start_date.setter
    def start_date(self, value: pulumi.Input['GoogleTypeDateArgs']):
        pulumi.set(self, "start_date", value)

    @property
    @pulumi.getter(name="endDate")
    def end_date(self) -> Optional[pulumi.Input['GoogleTypeDateArgs']]:
        """
        Optional. The end date of the time period. Budgets with elapsed end date won't be processed. If unset, specifies to track all usage incurred since the start_date.
        """
        return pulumi.get(self, "end_date")

    @end_date.setter
    def end_date(self, value: Optional[pulumi.Input['GoogleTypeDateArgs']]):
        pulumi.set(self, "end_date", value)


@pulumi.input_type
class GoogleCloudBillingBudgetsV1FilterArgs:
    def __init__(__self__, *,
                 calendar_period: Optional[pulumi.Input['GoogleCloudBillingBudgetsV1FilterCalendarPeriod']] = None,
                 credit_types: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 credit_types_treatment: Optional[pulumi.Input['GoogleCloudBillingBudgetsV1FilterCreditTypesTreatment']] = None,
                 custom_period: Optional[pulumi.Input['GoogleCloudBillingBudgetsV1CustomPeriodArgs']] = None,
                 labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 projects: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 services: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 subaccounts: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        A filter for a budget, limiting the scope of the cost to calculate.
        :param pulumi.Input['GoogleCloudBillingBudgetsV1FilterCalendarPeriod'] calendar_period: Optional. Specifies to track usage for recurring calendar period. For example, assume that CalendarPeriod.QUARTER is set. The budget tracks usage from April 1 to June 30, when the current calendar month is April, May, June. After that, it tracks usage from July 1 to September 30 when the current calendar month is July, August, September, so on.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] credit_types: Optional. If Filter.credit_types_treatment is INCLUDE_SPECIFIED_CREDITS, this is a list of credit types to be subtracted from gross cost to determine the spend for threshold calculations. See [a list of acceptable credit type values](https://cloud.google.com/billing/docs/how-to/export-data-bigquery-tables#credits-type). If Filter.credit_types_treatment is **not** INCLUDE_SPECIFIED_CREDITS, this field must be empty.
        :param pulumi.Input['GoogleCloudBillingBudgetsV1FilterCreditTypesTreatment'] credit_types_treatment: Optional. If not set, default behavior is `INCLUDE_ALL_CREDITS`.
        :param pulumi.Input['GoogleCloudBillingBudgetsV1CustomPeriodArgs'] custom_period: Optional. Specifies to track usage from any start date (required) to any end date (optional). This time period is static, it does not recur.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: Optional. A single label and value pair specifying that usage from only this set of labeled resources should be included in the budget. If omitted, the report includes all labeled and unlabeled usage. An object containing a single `"key": value` pair. Example: `{ "name": "wrench" }`. _Currently, multiple entries or multiple values per entry are not allowed._
        :param pulumi.Input[Sequence[pulumi.Input[str]]] projects: Optional. A set of projects of the form `projects/{project}`, specifying that usage from only this set of projects should be included in the budget. If omitted, the report includes all usage for the billing account, regardless of which project the usage occurred on. Only zero or one project can be specified currently.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] services: Optional. A set of services of the form `services/{service_id}`, specifying that usage from only this set of services should be included in the budget. If omitted, the report includes usage for all the services. The service names are available through the Catalog API: https://cloud.google.com/billing/v1/how-tos/catalog-api.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] subaccounts: Optional. A set of subaccounts of the form `billingAccounts/{account_id}`, specifying that usage from only this set of subaccounts should be included in the budget. If a subaccount is set to the name of the parent account, usage from the parent account is included. If the field is omitted, the report includes usage from the parent account and all subaccounts, if they exist.
        """
        if calendar_period is not None:
            pulumi.set(__self__, "calendar_period", calendar_period)
        if credit_types is not None:
            pulumi.set(__self__, "credit_types", credit_types)
        if credit_types_treatment is not None:
            pulumi.set(__self__, "credit_types_treatment", credit_types_treatment)
        if custom_period is not None:
            pulumi.set(__self__, "custom_period", custom_period)
        if labels is not None:
            pulumi.set(__self__, "labels", labels)
        if projects is not None:
            pulumi.set(__self__, "projects", projects)
        if services is not None:
            pulumi.set(__self__, "services", services)
        if subaccounts is not None:
            pulumi.set(__self__, "subaccounts", subaccounts)

    @property
    @pulumi.getter(name="calendarPeriod")
    def calendar_period(self) -> Optional[pulumi.Input['GoogleCloudBillingBudgetsV1FilterCalendarPeriod']]:
        """
        Optional. Specifies to track usage for recurring calendar period. For example, assume that CalendarPeriod.QUARTER is set. The budget tracks usage from April 1 to June 30, when the current calendar month is April, May, June. After that, it tracks usage from July 1 to September 30 when the current calendar month is July, August, September, so on.
        """
        return pulumi.get(self, "calendar_period")

    @calendar_period.setter
    def calendar_period(self, value: Optional[pulumi.Input['GoogleCloudBillingBudgetsV1FilterCalendarPeriod']]):
        pulumi.set(self, "calendar_period", value)

    @property
    @pulumi.getter(name="creditTypes")
    def credit_types(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Optional. If Filter.credit_types_treatment is INCLUDE_SPECIFIED_CREDITS, this is a list of credit types to be subtracted from gross cost to determine the spend for threshold calculations. See [a list of acceptable credit type values](https://cloud.google.com/billing/docs/how-to/export-data-bigquery-tables#credits-type). If Filter.credit_types_treatment is **not** INCLUDE_SPECIFIED_CREDITS, this field must be empty.
        """
        return pulumi.get(self, "credit_types")

    @credit_types.setter
    def credit_types(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "credit_types", value)

    @property
    @pulumi.getter(name="creditTypesTreatment")
    def credit_types_treatment(self) -> Optional[pulumi.Input['GoogleCloudBillingBudgetsV1FilterCreditTypesTreatment']]:
        """
        Optional. If not set, default behavior is `INCLUDE_ALL_CREDITS`.
        """
        return pulumi.get(self, "credit_types_treatment")

    @credit_types_treatment.setter
    def credit_types_treatment(self, value: Optional[pulumi.Input['GoogleCloudBillingBudgetsV1FilterCreditTypesTreatment']]):
        pulumi.set(self, "credit_types_treatment", value)

    @property
    @pulumi.getter(name="customPeriod")
    def custom_period(self) -> Optional[pulumi.Input['GoogleCloudBillingBudgetsV1CustomPeriodArgs']]:
        """
        Optional. Specifies to track usage from any start date (required) to any end date (optional). This time period is static, it does not recur.
        """
        return pulumi.get(self, "custom_period")

    @custom_period.setter
    def custom_period(self, value: Optional[pulumi.Input['GoogleCloudBillingBudgetsV1CustomPeriodArgs']]):
        pulumi.set(self, "custom_period", value)

    @property
    @pulumi.getter
    def labels(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Optional. A single label and value pair specifying that usage from only this set of labeled resources should be included in the budget. If omitted, the report includes all labeled and unlabeled usage. An object containing a single `"key": value` pair. Example: `{ "name": "wrench" }`. _Currently, multiple entries or multiple values per entry are not allowed._
        """
        return pulumi.get(self, "labels")

    @labels.setter
    def labels(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "labels", value)

    @property
    @pulumi.getter
    def projects(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Optional. A set of projects of the form `projects/{project}`, specifying that usage from only this set of projects should be included in the budget. If omitted, the report includes all usage for the billing account, regardless of which project the usage occurred on. Only zero or one project can be specified currently.
        """
        return pulumi.get(self, "projects")

    @projects.setter
    def projects(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "projects", value)

    @property
    @pulumi.getter
    def services(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Optional. A set of services of the form `services/{service_id}`, specifying that usage from only this set of services should be included in the budget. If omitted, the report includes usage for all the services. The service names are available through the Catalog API: https://cloud.google.com/billing/v1/how-tos/catalog-api.
        """
        return pulumi.get(self, "services")

    @services.setter
    def services(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "services", value)

    @property
    @pulumi.getter
    def subaccounts(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Optional. A set of subaccounts of the form `billingAccounts/{account_id}`, specifying that usage from only this set of subaccounts should be included in the budget. If a subaccount is set to the name of the parent account, usage from the parent account is included. If the field is omitted, the report includes usage from the parent account and all subaccounts, if they exist.
        """
        return pulumi.get(self, "subaccounts")

    @subaccounts.setter
    def subaccounts(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "subaccounts", value)


@pulumi.input_type
class GoogleCloudBillingBudgetsV1LastPeriodAmountArgs:
    def __init__(__self__):
        """
        Describes a budget amount targeted to the last Filter.calendar_period spend. At this time, the amount is automatically 100% of the last calendar period's spend; that is, there are no other options yet. LastPeriodAmount cannot be set for a budget configured with a Filter.custom_period.
        """
        pass


@pulumi.input_type
class GoogleCloudBillingBudgetsV1NotificationsRuleArgs:
    def __init__(__self__, *,
                 disable_default_iam_recipients: Optional[pulumi.Input[bool]] = None,
                 monitoring_notification_channels: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 pubsub_topic: Optional[pulumi.Input[str]] = None,
                 schema_version: Optional[pulumi.Input[str]] = None):
        """
        NotificationsRule defines notifications that are sent based on budget spend and thresholds.
        :param pulumi.Input[bool] disable_default_iam_recipients: Optional. When set to true, disables default notifications sent when a threshold is exceeded. Default notifications are sent to those with Billing Account Administrator and Billing Account User IAM roles for the target account.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] monitoring_notification_channels: Optional. Email targets to send notifications to when a threshold is exceeded. This is in addition to the `DefaultIamRecipients` who receive alert emails based on their billing account IAM role. The value is the full REST resource name of a Cloud Monitoring email notification channel with the form `projects/{project_id}/notificationChannels/{channel_id}`. A maximum of 5 email notifications are allowed. To customize budget alert email recipients with monitoring notification channels, you _must create the monitoring notification channels before you link them to a budget_. For guidance on setting up notification channels to use with budgets, see [Customize budget alert email recipients](https://cloud.google.com/billing/docs/how-to/budgets-notification-recipients). For Cloud Billing budget alerts, you _must use email notification channels_. The other types of notification channels are _not_ supported, such as Slack, SMS, or PagerDuty. If you want to [send budget notifications to Slack](https://cloud.google.com/billing/docs/how-to/notify#send_notifications_to_slack), use a pubsubTopic and configure [programmatic notifications](https://cloud.google.com/billing/docs/how-to/budgets-programmatic-notifications).
        :param pulumi.Input[str] pubsub_topic: Optional. The name of the Pub/Sub topic where budget-related messages are published, in the form `projects/{project_id}/topics/{topic_id}`. Updates are sent to the topic at regular intervals; the timing of the updates is not dependent on the [threshold rules](#thresholdrule) you've set. Note that if you want your [Pub/Sub JSON object](https://cloud.google.com/billing/docs/how-to/budgets-programmatic-notifications#notification_format) to contain data for `alertThresholdExceeded`, you need at least one [alert threshold rule](#thresholdrule). When you set threshold rules, you must also enable at least one of the email notification options, either using the default IAM recipients or Cloud Monitoring email notification channels. To use Pub/Sub topics with budgets, you must do the following: 1. Create the Pub/Sub topic before connecting it to your budget. For guidance, see [Manage programmatic budget alert notifications](https://cloud.google.com/billing/docs/how-to/budgets-programmatic-notifications). 2. Grant the API caller the `pubsub.topics.setIamPolicy` permission on the Pub/Sub topic. If not set, the API call fails with PERMISSION_DENIED. For additional details on Pub/Sub roles and permissions, see [Permissions required for this task](https://cloud.google.com/billing/docs/how-to/budgets-programmatic-notifications#permissions_required_for_this_task).
        :param pulumi.Input[str] schema_version: Optional. Required when NotificationsRule.pubsub_topic is set. The schema version of the notification sent to NotificationsRule.pubsub_topic. Only "1.0" is accepted. It represents the JSON schema as defined in https://cloud.google.com/billing/docs/how-to/budgets-programmatic-notifications#notification_format.
        """
        if disable_default_iam_recipients is not None:
            pulumi.set(__self__, "disable_default_iam_recipients", disable_default_iam_recipients)
        if monitoring_notification_channels is not None:
            pulumi.set(__self__, "monitoring_notification_channels", monitoring_notification_channels)
        if pubsub_topic is not None:
            pulumi.set(__self__, "pubsub_topic", pubsub_topic)
        if schema_version is not None:
            pulumi.set(__self__, "schema_version", schema_version)

    @property
    @pulumi.getter(name="disableDefaultIamRecipients")
    def disable_default_iam_recipients(self) -> Optional[pulumi.Input[bool]]:
        """
        Optional. When set to true, disables default notifications sent when a threshold is exceeded. Default notifications are sent to those with Billing Account Administrator and Billing Account User IAM roles for the target account.
        """
        return pulumi.get(self, "disable_default_iam_recipients")

    @disable_default_iam_recipients.setter
    def disable_default_iam_recipients(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "disable_default_iam_recipients", value)

    @property
    @pulumi.getter(name="monitoringNotificationChannels")
    def monitoring_notification_channels(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Optional. Email targets to send notifications to when a threshold is exceeded. This is in addition to the `DefaultIamRecipients` who receive alert emails based on their billing account IAM role. The value is the full REST resource name of a Cloud Monitoring email notification channel with the form `projects/{project_id}/notificationChannels/{channel_id}`. A maximum of 5 email notifications are allowed. To customize budget alert email recipients with monitoring notification channels, you _must create the monitoring notification channels before you link them to a budget_. For guidance on setting up notification channels to use with budgets, see [Customize budget alert email recipients](https://cloud.google.com/billing/docs/how-to/budgets-notification-recipients). For Cloud Billing budget alerts, you _must use email notification channels_. The other types of notification channels are _not_ supported, such as Slack, SMS, or PagerDuty. If you want to [send budget notifications to Slack](https://cloud.google.com/billing/docs/how-to/notify#send_notifications_to_slack), use a pubsubTopic and configure [programmatic notifications](https://cloud.google.com/billing/docs/how-to/budgets-programmatic-notifications).
        """
        return pulumi.get(self, "monitoring_notification_channels")

    @monitoring_notification_channels.setter
    def monitoring_notification_channels(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "monitoring_notification_channels", value)

    @property
    @pulumi.getter(name="pubsubTopic")
    def pubsub_topic(self) -> Optional[pulumi.Input[str]]:
        """
        Optional. The name of the Pub/Sub topic where budget-related messages are published, in the form `projects/{project_id}/topics/{topic_id}`. Updates are sent to the topic at regular intervals; the timing of the updates is not dependent on the [threshold rules](#thresholdrule) you've set. Note that if you want your [Pub/Sub JSON object](https://cloud.google.com/billing/docs/how-to/budgets-programmatic-notifications#notification_format) to contain data for `alertThresholdExceeded`, you need at least one [alert threshold rule](#thresholdrule). When you set threshold rules, you must also enable at least one of the email notification options, either using the default IAM recipients or Cloud Monitoring email notification channels. To use Pub/Sub topics with budgets, you must do the following: 1. Create the Pub/Sub topic before connecting it to your budget. For guidance, see [Manage programmatic budget alert notifications](https://cloud.google.com/billing/docs/how-to/budgets-programmatic-notifications). 2. Grant the API caller the `pubsub.topics.setIamPolicy` permission on the Pub/Sub topic. If not set, the API call fails with PERMISSION_DENIED. For additional details on Pub/Sub roles and permissions, see [Permissions required for this task](https://cloud.google.com/billing/docs/how-to/budgets-programmatic-notifications#permissions_required_for_this_task).
        """
        return pulumi.get(self, "pubsub_topic")

    @pubsub_topic.setter
    def pubsub_topic(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "pubsub_topic", value)

    @property
    @pulumi.getter(name="schemaVersion")
    def schema_version(self) -> Optional[pulumi.Input[str]]:
        """
        Optional. Required when NotificationsRule.pubsub_topic is set. The schema version of the notification sent to NotificationsRule.pubsub_topic. Only "1.0" is accepted. It represents the JSON schema as defined in https://cloud.google.com/billing/docs/how-to/budgets-programmatic-notifications#notification_format.
        """
        return pulumi.get(self, "schema_version")

    @schema_version.setter
    def schema_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "schema_version", value)


@pulumi.input_type
class GoogleCloudBillingBudgetsV1ThresholdRuleArgs:
    def __init__(__self__, *,
                 threshold_percent: pulumi.Input[float],
                 spend_basis: Optional[pulumi.Input['GoogleCloudBillingBudgetsV1ThresholdRuleSpendBasis']] = None):
        """
        ThresholdRule contains the definition of a threshold. Threshold rules define the triggering events used to generate a budget notification email. When a threshold is crossed (spend exceeds the specified percentages of the budget), budget alert emails are sent to the email recipients you specify in the [NotificationsRule](#notificationsrule). Threshold rules also affect the fields included in the [JSON data object](https://cloud.google.com/billing/docs/how-to/budgets-programmatic-notifications#notification_format) sent to a Pub/Sub topic. Threshold rules are _required_ if using email notifications. Threshold rules are _optional_ if only setting a [`pubsubTopic` NotificationsRule](#NotificationsRule), unless you want your JSON data object to include data about the thresholds you set. For more information, see [set budget threshold rules and actions](https://cloud.google.com/billing/docs/how-to/budgets#budget-actions).
        :param pulumi.Input[float] threshold_percent: Send an alert when this threshold is exceeded. This is a 1.0-based percentage, so 0.5 = 50%. Validation: non-negative number.
        :param pulumi.Input['GoogleCloudBillingBudgetsV1ThresholdRuleSpendBasis'] spend_basis: Optional. The type of basis used to determine if spend has passed the threshold. Behavior defaults to CURRENT_SPEND if not set.
        """
        pulumi.set(__self__, "threshold_percent", threshold_percent)
        if spend_basis is not None:
            pulumi.set(__self__, "spend_basis", spend_basis)

    @property
    @pulumi.getter(name="thresholdPercent")
    def threshold_percent(self) -> pulumi.Input[float]:
        """
        Send an alert when this threshold is exceeded. This is a 1.0-based percentage, so 0.5 = 50%. Validation: non-negative number.
        """
        return pulumi.get(self, "threshold_percent")

    @threshold_percent.setter
    def threshold_percent(self, value: pulumi.Input[float]):
        pulumi.set(self, "threshold_percent", value)

    @property
    @pulumi.getter(name="spendBasis")
    def spend_basis(self) -> Optional[pulumi.Input['GoogleCloudBillingBudgetsV1ThresholdRuleSpendBasis']]:
        """
        Optional. The type of basis used to determine if spend has passed the threshold. Behavior defaults to CURRENT_SPEND if not set.
        """
        return pulumi.get(self, "spend_basis")

    @spend_basis.setter
    def spend_basis(self, value: Optional[pulumi.Input['GoogleCloudBillingBudgetsV1ThresholdRuleSpendBasis']]):
        pulumi.set(self, "spend_basis", value)


@pulumi.input_type
class GoogleTypeDateArgs:
    def __init__(__self__, *,
                 day: Optional[pulumi.Input[int]] = None,
                 month: Optional[pulumi.Input[int]] = None,
                 year: Optional[pulumi.Input[int]] = None):
        """
        Represents a whole or partial calendar date, such as a birthday. The time of day and time zone are either specified elsewhere or are insignificant. The date is relative to the Gregorian Calendar. This can represent one of the following: * A full date, with non-zero year, month, and day values. * A month and day, with a zero year (for example, an anniversary). * A year on its own, with a zero month and a zero day. * A year and month, with a zero day (for example, a credit card expiration date). Related types: * google.type.TimeOfDay * google.type.DateTime * google.protobuf.Timestamp
        :param pulumi.Input[int] day: Day of a month. Must be from 1 to 31 and valid for the year and month, or 0 to specify a year by itself or a year and month where the day isn't significant.
        :param pulumi.Input[int] month: Month of a year. Must be from 1 to 12, or 0 to specify a year without a month and day.
        :param pulumi.Input[int] year: Year of the date. Must be from 1 to 9999, or 0 to specify a date without a year.
        """
        if day is not None:
            pulumi.set(__self__, "day", day)
        if month is not None:
            pulumi.set(__self__, "month", month)
        if year is not None:
            pulumi.set(__self__, "year", year)

    @property
    @pulumi.getter
    def day(self) -> Optional[pulumi.Input[int]]:
        """
        Day of a month. Must be from 1 to 31 and valid for the year and month, or 0 to specify a year by itself or a year and month where the day isn't significant.
        """
        return pulumi.get(self, "day")

    @day.setter
    def day(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "day", value)

    @property
    @pulumi.getter
    def month(self) -> Optional[pulumi.Input[int]]:
        """
        Month of a year. Must be from 1 to 12, or 0 to specify a year without a month and day.
        """
        return pulumi.get(self, "month")

    @month.setter
    def month(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "month", value)

    @property
    @pulumi.getter
    def year(self) -> Optional[pulumi.Input[int]]:
        """
        Year of the date. Must be from 1 to 9999, or 0 to specify a date without a year.
        """
        return pulumi.get(self, "year")

    @year.setter
    def year(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "year", value)


@pulumi.input_type
class GoogleTypeMoneyArgs:
    def __init__(__self__, *,
                 currency_code: Optional[pulumi.Input[str]] = None,
                 nanos: Optional[pulumi.Input[int]] = None,
                 units: Optional[pulumi.Input[str]] = None):
        """
        Represents an amount of money with its currency type.
        :param pulumi.Input[str] currency_code: The three-letter currency code defined in ISO 4217.
        :param pulumi.Input[int] nanos: Number of nano (10^-9) units of the amount. The value must be between -999,999,999 and +999,999,999 inclusive. If `units` is positive, `nanos` must be positive or zero. If `units` is zero, `nanos` can be positive, zero, or negative. If `units` is negative, `nanos` must be negative or zero. For example $-1.75 is represented as `units`=-1 and `nanos`=-750,000,000.
        :param pulumi.Input[str] units: The whole units of the amount. For example if `currencyCode` is `"USD"`, then 1 unit is one US dollar.
        """
        if currency_code is not None:
            pulumi.set(__self__, "currency_code", currency_code)
        if nanos is not None:
            pulumi.set(__self__, "nanos", nanos)
        if units is not None:
            pulumi.set(__self__, "units", units)

    @property
    @pulumi.getter(name="currencyCode")
    def currency_code(self) -> Optional[pulumi.Input[str]]:
        """
        The three-letter currency code defined in ISO 4217.
        """
        return pulumi.get(self, "currency_code")

    @currency_code.setter
    def currency_code(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "currency_code", value)

    @property
    @pulumi.getter
    def nanos(self) -> Optional[pulumi.Input[int]]:
        """
        Number of nano (10^-9) units of the amount. The value must be between -999,999,999 and +999,999,999 inclusive. If `units` is positive, `nanos` must be positive or zero. If `units` is zero, `nanos` can be positive, zero, or negative. If `units` is negative, `nanos` must be negative or zero. For example $-1.75 is represented as `units`=-1 and `nanos`=-750,000,000.
        """
        return pulumi.get(self, "nanos")

    @nanos.setter
    def nanos(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "nanos", value)

    @property
    @pulumi.getter
    def units(self) -> Optional[pulumi.Input[str]]:
        """
        The whole units of the amount. For example if `currencyCode` is `"USD"`, then 1 unit is one US dollar.
        """
        return pulumi.get(self, "units")

    @units.setter
    def units(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "units", value)


