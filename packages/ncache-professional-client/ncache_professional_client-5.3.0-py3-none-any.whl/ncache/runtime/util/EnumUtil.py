from ncache.client.enum.CacheItemPriority import CacheItemPriority
from ncache.client.enum.CacheItemRemovedReason import CacheItemRemovedReason
from ncache.client.enum.CacheStatusNotificationType import CacheStatusNotificationType
from ncache.client.enum.ClientCacheSyncMode import ClientCacheSyncMode
from ncache.client.enum.CmdParamsType import CmdParamsType
from ncache.client.enum.CommandType import CommandType
from ncache.client.enum.DeliveryMode import DeliveryMode
from ncache.client.enum.DeliveryOption import DeliveryOption
from ncache.client.enum.EventDataFilter import EventDataFilter
from ncache.client.enum.EventType import EventType
from ncache.client.enum.ExpirationType import ExpirationType
from ncache.client.enum.IsolationLevel import IsolationLevel
from ncache.client.enum.LogLevel import LogLevel
from ncache.client.enum.MessgeFailureReason import MessageFailureReason
from ncache.client.enum.SubscriptionPolicy import SubscriptionPolicy
from ncache.client.enum.TopicPriority import TopicPriority
from ncache.client.enum.TopicSearchOptions import TopicSearchOptions
from ncache.util.TypeCaster import TypeCaster
from ncache.util.ValidateType import ValidateType

from ncache.util.JavaInstancesFactory import JavaInstancesFactory


class EnumUtil:
    @staticmethod
    def get_expiration_type(value):
        ValidateType.type_check(value, int)
        value = TypeCaster.to_java_primitive_type(value - 1)

        return JavaInstancesFactory.get_java_instance("EnumUtil").getExpirationType(value)

    @staticmethod
    def get_expiration_type_value(optype):
        ValidateType.is_none(optype)

        value = int(JavaInstancesFactory.get_java_instance("EnumUtil").getExpirationTypeValue(optype))
        return ExpirationType(value + 1)

    @staticmethod
    def get_topic_priority(value):
        value = TypeCaster.to_java_primitive_type(value - 1)

        return JavaInstancesFactory.get_java_instance("EnumUtil").getTopicPriority(value)

    @staticmethod
    def get_topic_priority_value(priority):
        value = str(JavaInstancesFactory.get_java_instance("EnumUtil").getTopicPriorityValue(priority))

        if value == 'Low':
            value = 1
        elif value == 'Normal':
            value = 2
        elif value == 'High':
            value = 3

        return TopicPriority(value)

    @staticmethod
    def get_cache_item_priority(value):
        ValidateType.type_check(value, int)
        value = TypeCaster.to_java_primitive_type(value - 1)

        return JavaInstancesFactory.get_java_instance("EnumUtil").getCacheItemPriority(value)

    @staticmethod
    def get_cache_item_priority_value(priority):
        ValidateType.is_none(priority)

        value = int(JavaInstancesFactory.get_java_instance("EnumUtil").getCacheItemPriorityValue(priority))
        return CacheItemPriority(value + 1)

    @staticmethod
    def get_event_type(value):
        ValidateType.type_check(value, int)
        value = TypeCaster.to_java_primitive_type(value - 1)

        return JavaInstancesFactory.get_java_instance("EnumUtil").getEventType(value)

    @staticmethod
    def get_event_type_value(eventtype):
        ValidateType.is_none(eventtype)

        value = str(JavaInstancesFactory.get_java_instance("EnumUtil").getEventTypeValue(eventtype))

        if value == 'ItemAdded':
            value = 1
        elif value == 'ItemUpdated':
            value = 2
        elif value == 'ItemRemoved':
            value = 3

        return EventType(value)

    @staticmethod
    def get_event_data_filter(value):
        ValidateType.type_check(value, int)
        value = TypeCaster.to_java_primitive_type(value - 1)

        return JavaInstancesFactory.get_java_instance("EnumUtil").getEventDataFilter(value)

    @staticmethod
    def get_event_data_filter_value(datafilter):
        ValidateType.is_none(datafilter)

        value = str(JavaInstancesFactory.get_java_instance("EnumUtil").getEventDataFilterValue(datafilter))

        if value == 'None':
            value = 1
        elif value == 'Metadata':
            value = 2
        elif value == 'DataWithMetadata':
            value = 4

        return EventDataFilter(value)

    @staticmethod
    def get_topic_search_options(value):
        ValidateType.type_check(value, int)
        value = TypeCaster.to_java_primitive_type(value - 1)

        return JavaInstancesFactory.get_java_instance("EnumUtil").getTopicSearchOptions(value)

    @staticmethod
    def get_topic_search_options_value(options):
        ValidateType.is_none(options)

        value = str(JavaInstancesFactory.get_java_instance("EnumUtil").getTopicSearchOptionsValue(options))

        if value == 'ByName':
            value = 1
        elif value == 'ByPattern':
            value = 2

        return TopicSearchOptions(value)

    @staticmethod
    def enum_set_cache_status(statustype):
        pass

    @staticmethod
    def get_isolation_level(value):
        ValidateType.type_check(value, int)
        value = TypeCaster.to_java_primitive_type(value - 1)

        return JavaInstancesFactory.get_java_instance("ClientEnumUtil").getIsolationLevel(value)

    @staticmethod
    def get_isolation_level_value(options):
        ValidateType.is_none(options)

        value = int(JavaInstancesFactory.get_java_instance("ClientEnumUtil").getIsolationLevelValue(options))
        return IsolationLevel(value + 1)

    @staticmethod
    def get_log_level(value):
        ValidateType.type_check(value, int)
        value = TypeCaster.to_java_primitive_type(value - 1)

        return JavaInstancesFactory.get_java_instance("ClientEnumUtil").getLogLevel(value)

    @staticmethod
    def get_log_level_value(options):
        ValidateType.is_none(options)

        value = int(JavaInstancesFactory.get_java_instance("ClientEnumUtil").getLogLevelValue(options))
        return LogLevel(value + 1)

    @staticmethod
    def get_client_cache_sync_mode(value):
        ValidateType.type_check(value, int)
        value = TypeCaster.to_java_primitive_type(value - 1)

        return JavaInstancesFactory.get_java_instance("ClientEnumUtil").getCacheClientSyncMode(value)

    @staticmethod
    def get_client_cache_sync_mode_value(mode):
        ValidateType.is_none(mode)

        value = int(JavaInstancesFactory.get_java_instance("ClientEnumUtil").getClientCacheSyncModeValue(mode))
        return ClientCacheSyncMode(value + 1)

    @staticmethod
    def get_cache_status_notification_type(value):
        value = value.name

        if value == 'MEMBER_JOINED':
            value = 'MemberJoined'
        elif value == 'MEMBER_LEFT':
            value = 'MemberLeft'
        elif value == 'CACHE_STOPPED':
            value = 'CacheStopped'
        else:
            value = 'ALL'

        value = TypeCaster.to_java_primitive_type(value)

        return JavaInstancesFactory.get_java_instance("ClientEnumUtil").getCacheStatusNotificationType(value)

    @staticmethod
    def get_cache_status_notification_type_value(notificationtype):
        ValidateType.is_none(notificationtype)

        value = str(JavaInstancesFactory.get_java_instance("ClientEnumUtil").getCacheStatusNotificationTypeValue(notificationtype))

        if value == 'MemberJoined':
            value = 1
        elif value == 'MemberLeft':
            value = 2
        elif value == 'CacheStopped':
            value = 3
        elif value == 'ALL':
            value = 4

        return CacheStatusNotificationType(value)

    @staticmethod
    def get_delivery_option(value):
        ValidateType.type_check(value, int)
        value = TypeCaster.to_java_primitive_type(value - 1)

        return JavaInstancesFactory.get_java_instance("ClientEnumUtil").getDeliveryOption(value)

    @staticmethod
    def get_delivery_option_value(value):
        ValidateType.is_none(value)

        value = str(JavaInstancesFactory.get_java_instance("ClientEnumUtil").getDeliveryOptionValue(value))

        if value == 'All':
            value = 1
        elif value == 'Any':
            value = 2

        return DeliveryOption(value)

    @staticmethod
    def get_subscription_policy(value):
        ValidateType.type_check(value, int)
        value = TypeCaster.to_java_primitive_type(value - 1)

        return JavaInstancesFactory.get_java_instance("ClientEnumUtil").getSubscriptionPolicy(value)

    @staticmethod
    def get_subscription_policy_value(policy):
        ValidateType.is_none(policy)

        value = str(JavaInstancesFactory.get_java_instance("ClientEnumUtil").getSubscriptionPolicyValue(policy))

        if value == 'Shared':
            value = 1
        elif value == 'Exclusive':
            value = 2

        return SubscriptionPolicy(value)

    @staticmethod
    def get_delivery_mode(value):
        if value == 'ASYNC':
            value = 'Async'
        elif value == 'SYNC':
            value = 'Sync'

        value = TypeCaster.to_java_primitive_type(value)

        return JavaInstancesFactory.get_java_instance("ClientEnumUtil").getDeliveryMode(value)
    
    @staticmethod
    def get_delivery_mode_value(mode):
        ValidateType.is_none(mode)

        value = str(JavaInstancesFactory.get_java_instance("ClientEnumUtil").getDeliveryModeValue(mode))

        if value == 'Async':
            value = 1
        elif value == 'Sync':
            value = 2

        return DeliveryMode(value)

    @staticmethod
    def get_tag_search_options(value):
        ValidateType.type_check(value, int)
        value = TypeCaster.to_java_primitive_type(value - 1)

        return JavaInstancesFactory.get_java_instance("ClientEnumUtil").getTagSearchOptions(value)

    @staticmethod
    def get_cache_item_removed_reason(value):
        ValidateType.type_check(value, int)
        value = TypeCaster.to_java_primitive_type(value - 1)

        return JavaInstancesFactory.get_java_instance("ClientEnumUtil").getCacheItemRemovedReason(value)

    @staticmethod
    def get_cache_item_removed_reason_value(reason):
        ValidateType.is_none(reason)

        value = str(JavaInstancesFactory.get_java_instance("ClientEnumUtil").getCacheItemRemovedReasonValue(reason))

        if value == 'DependencyChanged':
            value = 1
        elif value == 'Expired':
            value = 2
        elif value == 'Removed':
            value = 3
        elif value == 'Underused':
            value = 4
        elif value == 'DependencyInvalid':
            value = 5

        return CacheItemRemovedReason(value)

    @staticmethod
    def get_message_failure_reason(value):
        ValidateType.type_check(value, int)
        value = TypeCaster.to_java_primitive_type(value - 1)

        return JavaInstancesFactory.get_java_instance("EnumUtil").getSubscriptionPolicy(value)

    @staticmethod
    def get_message_failure_reason_value(reason):
        ValidateType.is_none(reason)

        value = str(JavaInstancesFactory.get_java_instance("ClientEnumUtil").getSubscriptionPolicyValue(reason))

        if value == 'Expired':
            value = 1
        elif value == 'Evicted':
            value = 2

        return MessageFailureReason(value)

    @staticmethod
    def get_command_type(value):
        ValidateType.type_check(value, int)
        value = TypeCaster.to_java_primitive_type(value)

        return JavaInstancesFactory.get_java_instance("EnumUtil").getCommandType(value)

    @staticmethod
    def get_command_type_value(options):
        ValidateType.is_none(options)

        value = str(JavaInstancesFactory.get_java_instance("EnumUtil").getCommandTypeValue(options))

        if value == 'Text':
            value = 1
        elif value == 'StoredProcedure':
            value = 4
        elif value == 'TableDirect':
            value = 512

        return CommandType(value)



    @staticmethod
    def get_cmd_params_type(value):
        ValidateType.type_check(value, int)
        value = TypeCaster.to_java_primitive_type(value - 1)

        return JavaInstancesFactory.get_java_instance("EnumUtil").getCmdParamsType(value)

    @staticmethod
    def get_cmd_params_type_value(options):
        ValidateType.is_none(options)

        value = str(JavaInstancesFactory.get_java_instance("EnumUtil").getCmdParamsTypeValue(options))

        value = EnumUtil.get_cmd_params_type_number_for_name(value)

        return CmdParamsType(value)

    @staticmethod
    def get_cmd_params_type_number_for_name(name):
        if name == 'BigInt':
            return 1
        elif name == 'Binary':
            return 2
        elif name == 'Bit':
            return 3
        elif name == 'Char':
            return 4
        elif name == 'DateTime':
            return 5
        elif name == 'Decimal':
            return 6
        elif name == 'Float':
            return 7
        elif name == 'Int':
            return 9
        elif name == 'Money':
            return 10
        elif name == 'NChar':
            return 11
        elif name == 'NVarChar':
            return 13
        elif name == 'Real':
            return 14
        elif name == 'UniqueIdentifier':
            return 15
        elif name == 'SmallDateTime':
            return 16
        elif name == 'SmallInt':
            return 17
        elif name == 'SmallMoney':
            return 18
        elif name == 'Timestamp':
            return 20
        elif name == 'TinyInt':
            return 21
        elif name == 'VarBinary':
            return 22
        elif name == 'VarChar':
            return 23
        elif name == 'Variant':
            return 24
        elif name == 'Xml':
            return 26
        elif name == 'Udt':
            return 30
        elif name == 'Structured':
            return 31
        elif name == 'Date':
            return 32
        elif name == 'Time':
            return 33
        elif name == 'DateTime2':
            return 34
        elif name == 'DateTimeOffset':
            return 35

