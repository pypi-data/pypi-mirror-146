# coding: utf-8

from __future__ import absolute_import

import datetime
import re
import importlib

import six

from huaweicloudsdkcore.client import Client, ClientBuilder
from huaweicloudsdkcore.exceptions import exceptions
from huaweicloudsdkcore.utils import http_utils
from huaweicloudsdkcore.sdk_stream_request import SdkStreamRequest


class LtsAsyncClient(Client):
    """
    :param configuration: .Configuration object for this client
    :param pool_threads: The number of threads to use for async requests
        to the API. More threads means more concurrent API requests.
    """

    PRIMITIVE_TYPES = (float, bool, bytes, six.text_type) + six.integer_types
    NATIVE_TYPES_MAPPING = {
        'int': int,
        'long': int if six.PY3 else long,
        'float': float,
        'str': str,
        'bool': bool,
        'date': datetime.date,
        'datetime': datetime.datetime,
        'object': object,
    }

    def __init__(self):
        super(LtsAsyncClient, self).__init__()
        self.model_package = importlib.import_module("huaweicloudsdklts.v2.model")
        self.preset_headers = {'User-Agent': 'HuaweiCloud-SDK-Python'}

    @classmethod
    def new_builder(cls, clazz=None):
        if clazz is None:
            return ClientBuilder(cls)

        if clazz.__name__ != "LtsClient":
            raise TypeError("client type error, support client type is LtsClient")

        return ClientBuilder(clazz)

    def create_access_config_async(self, request):
        """创建日志接入

        创建日志接入

        :param CreateAccessConfigRequest request
        :return: CreateAccessConfigResponse
        """
        return self.create_access_config_with_http_info(request)

    def create_access_config_with_http_info(self, request):
        """创建日志接入

        创建日志接入

        :param CreateAccessConfigRequest request
        :return: CreateAccessConfigResponse
        """

        all_params = ['create_access_config_request_body']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = {}

        body_params = None
        if 'body' in local_var_params:
            body_params = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json;charset=UTF-8'])

        auth_settings = []

        return self.call_api(
            resource_path='/v3/{project_id}/lts/access-config',
            method='POST',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='CreateAccessConfigResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def create_host_group_async(self, request):
        """创建主机组

        创建主机组

        :param CreateHostGroupRequest request
        :return: CreateHostGroupResponse
        """
        return self.create_host_group_with_http_info(request)

    def create_host_group_with_http_info(self, request):
        """创建主机组

        创建主机组

        :param CreateHostGroupRequest request
        :return: CreateHostGroupResponse
        """

        all_params = ['create_host_group_request_body']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = {}

        body_params = None
        if 'body' in local_var_params:
            body_params = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json;charset=UTF-8'])

        auth_settings = []

        return self.call_api(
            resource_path='/v3/{project_id}/lts/host-group',
            method='POST',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='CreateHostGroupResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def create_keywords_alarm_rule_async(self, request):
        """创建关键词告警规则

        该接口用于创建关键词告警，目前每个帐户最多可以创建共200个关键词告警与SQL告警。

        :param CreateKeywordsAlarmRuleRequest request
        :return: CreateKeywordsAlarmRuleResponse
        """
        return self.create_keywords_alarm_rule_with_http_info(request)

    def create_keywords_alarm_rule_with_http_info(self, request):
        """创建关键词告警规则

        该接口用于创建关键词告警，目前每个帐户最多可以创建共200个关键词告警与SQL告警。

        :param CreateKeywordsAlarmRuleRequest request
        :return: CreateKeywordsAlarmRuleResponse
        """

        all_params = ['create_keywords_alarm_rule_request_body']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = {}

        body_params = None
        if 'body' in local_var_params:
            body_params = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json;charset=UTF-8'])

        auth_settings = []

        return self.call_api(
            resource_path='/v2/{project_id}/lts/alarms/keywords-alarm-rule',
            method='POST',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='CreateKeywordsAlarmRuleResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def create_log_dump_obs_async(self, request):
        """创建日志转储（旧版）

        该接口用于将指定的一个或多个日志流的日志转储到OBS服务。

        :param CreateLogDumpObsRequest request
        :return: CreateLogDumpObsResponse
        """
        return self.create_log_dump_obs_with_http_info(request)

    def create_log_dump_obs_with_http_info(self, request):
        """创建日志转储（旧版）

        该接口用于将指定的一个或多个日志流的日志转储到OBS服务。

        :param CreateLogDumpObsRequest request
        :return: CreateLogDumpObsResponse
        """

        all_params = ['create_log_dump_obs_request_body']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = {}

        body_params = None
        if 'body' in local_var_params:
            body_params = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json'])

        auth_settings = []

        return self.call_api(
            resource_path='/v2/{project_id}/log-dump/obs',
            method='POST',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='CreateLogDumpObsResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def create_log_group_async(self, request):
        """创建日志组

        该接口用于创建一个日志组

        :param CreateLogGroupRequest request
        :return: CreateLogGroupResponse
        """
        return self.create_log_group_with_http_info(request)

    def create_log_group_with_http_info(self, request):
        """创建日志组

        该接口用于创建一个日志组

        :param CreateLogGroupRequest request
        :return: CreateLogGroupResponse
        """

        all_params = ['create_log_group_request_body']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = {}

        body_params = None
        if 'body' in local_var_params:
            body_params = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json'])

        auth_settings = []

        return self.call_api(
            resource_path='/v2/{project_id}/groups',
            method='POST',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='CreateLogGroupResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def create_log_stream_async(self, request):
        """创建日志流

        该接口用于创建某个指定日志组下的日志流

        :param CreateLogStreamRequest request
        :return: CreateLogStreamResponse
        """
        return self.create_log_stream_with_http_info(request)

    def create_log_stream_with_http_info(self, request):
        """创建日志流

        该接口用于创建某个指定日志组下的日志流

        :param CreateLogStreamRequest request
        :return: CreateLogStreamResponse
        """

        all_params = ['log_group_id', 'create_log_stream_request_body']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'log_group_id' in local_var_params:
            path_params['log_group_id'] = local_var_params['log_group_id']

        query_params = []

        header_params = {}

        form_params = {}

        body_params = None
        if 'body' in local_var_params:
            body_params = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json'])

        auth_settings = []

        return self.call_api(
            resource_path='/v2/{project_id}/groups/{log_group_id}/streams',
            method='POST',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='CreateLogStreamResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def create_notification_template_async(self, request):
        """创建消息模板

        该接口用于创建通知模板，目前每个帐户最多可以创建共100个通知模板，创建后名称不可修改。

        :param CreateNotificationTemplateRequest request
        :return: CreateNotificationTemplateResponse
        """
        return self.create_notification_template_with_http_info(request)

    def create_notification_template_with_http_info(self, request):
        """创建消息模板

        该接口用于创建通知模板，目前每个帐户最多可以创建共100个通知模板，创建后名称不可修改。

        :param CreateNotificationTemplateRequest request
        :return: CreateNotificationTemplateResponse
        """

        all_params = ['domain_id', 'create_notification_template_request_body']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'domain_id' in local_var_params:
            path_params['domain_id'] = local_var_params['domain_id']

        query_params = []

        header_params = {}

        form_params = {}

        body_params = None
        if 'body' in local_var_params:
            body_params = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json;charset=UTF-8'])

        auth_settings = []

        return self.call_api(
            resource_path='/v2/{project_id}/{domain_id}/lts/events/notification/templates',
            method='POST',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='CreateNotificationTemplateResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def create_struct_config_async(self, request):
        """通过结构化模板创建结构化配置（新）

        该接口通过结构化模板创建结构化配置。

        :param CreateStructConfigRequest request
        :return: CreateStructConfigResponse
        """
        return self.create_struct_config_with_http_info(request)

    def create_struct_config_with_http_info(self, request):
        """通过结构化模板创建结构化配置（新）

        该接口通过结构化模板创建结构化配置。

        :param CreateStructConfigRequest request
        :return: CreateStructConfigResponse
        """

        all_params = ['create_struct_config_request_body']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = {}

        body_params = None
        if 'body' in local_var_params:
            body_params = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json;charset=UTF-8'])

        auth_settings = []

        return self.call_api(
            resource_path='/v3/{project_id}/lts/struct/template',
            method='POST',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='CreateStructConfigResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def create_struct_template_async(self, request):
        """创建结构化配置

        该接口用于创建指定日志流下的结构化配置。

        :param CreateStructTemplateRequest request
        :return: CreateStructTemplateResponse
        """
        return self.create_struct_template_with_http_info(request)

    def create_struct_template_with_http_info(self, request):
        """创建结构化配置

        该接口用于创建指定日志流下的结构化配置。

        :param CreateStructTemplateRequest request
        :return: CreateStructTemplateResponse
        """

        all_params = ['create_struct_template_request_body']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = {}

        body_params = None
        if 'body' in local_var_params:
            body_params = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json'])

        auth_settings = []

        return self.call_api(
            resource_path='/v2/{project_id}/lts/struct/template',
            method='POST',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='CreateStructTemplateResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def create_transfer_async(self, request):
        """创建日志转储（新版）

        该接口用于创建OBS转储，DIS转储，DMS转储。

        :param CreateTransferRequest request
        :return: CreateTransferResponse
        """
        return self.create_transfer_with_http_info(request)

    def create_transfer_with_http_info(self, request):
        """创建日志转储（新版）

        该接口用于创建OBS转储，DIS转储，DMS转储。

        :param CreateTransferRequest request
        :return: CreateTransferResponse
        """

        all_params = ['create_transfer_request_body']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = {}

        body_params = None
        if 'body' in local_var_params:
            body_params = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json;charset=UTF-8'])

        auth_settings = []

        return self.call_api(
            resource_path='/v2/{project_id}/transfers',
            method='POST',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='CreateTransferResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def delete_access_config_async(self, request):
        """删除日志接入

        删除日志接入

        :param DeleteAccessConfigRequest request
        :return: DeleteAccessConfigResponse
        """
        return self.delete_access_config_with_http_info(request)

    def delete_access_config_with_http_info(self, request):
        """删除日志接入

        删除日志接入

        :param DeleteAccessConfigRequest request
        :return: DeleteAccessConfigResponse
        """

        all_params = ['delete_access_config_request_body']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = {}

        body_params = None
        if 'body' in local_var_params:
            body_params = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json;charset=UTF-8'])

        auth_settings = []

        return self.call_api(
            resource_path='/v3/{project_id}/lts/access-config',
            method='DELETE',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='DeleteAccessConfigResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def delete_active_alarms_async(self, request):
        """删除活动告警

        该接口用于删除活动告警

        :param DeleteActiveAlarmsRequest request
        :return: DeleteActiveAlarmsResponse
        """
        return self.delete_active_alarms_with_http_info(request)

    def delete_active_alarms_with_http_info(self, request):
        """删除活动告警

        该接口用于删除活动告警

        :param DeleteActiveAlarmsRequest request
        :return: DeleteActiveAlarmsResponse
        """

        all_params = ['domain_id', 'delete_active_alarms_request_body']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'domain_id' in local_var_params:
            path_params['domain_id'] = local_var_params['domain_id']

        query_params = []

        header_params = {}

        form_params = {}

        body_params = None
        if 'body' in local_var_params:
            body_params = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json;charset=UTF-8'])

        auth_settings = []

        return self.call_api(
            resource_path='/v2/{project_id}/{domain_id}/lts/alarms/sql-alarm/clear',
            method='POST',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='DeleteActiveAlarmsResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def delete_host_group_async(self, request):
        """删除主机组

        删除主机组

        :param DeleteHostGroupRequest request
        :return: DeleteHostGroupResponse
        """
        return self.delete_host_group_with_http_info(request)

    def delete_host_group_with_http_info(self, request):
        """删除主机组

        删除主机组

        :param DeleteHostGroupRequest request
        :return: DeleteHostGroupResponse
        """

        all_params = ['delete_host_group_request_body']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = {}

        body_params = None
        if 'body' in local_var_params:
            body_params = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json;charset=UTF-8'])

        auth_settings = []

        return self.call_api(
            resource_path='/v3/{project_id}/lts/host-group',
            method='DELETE',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='DeleteHostGroupResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def delete_keywords_alarm_rule_async(self, request):
        """删除关键词告警规则

        该接口用于删除关键词告警。

        :param DeleteKeywordsAlarmRuleRequest request
        :return: DeleteKeywordsAlarmRuleResponse
        """
        return self.delete_keywords_alarm_rule_with_http_info(request)

    def delete_keywords_alarm_rule_with_http_info(self, request):
        """删除关键词告警规则

        该接口用于删除关键词告警。

        :param DeleteKeywordsAlarmRuleRequest request
        :return: DeleteKeywordsAlarmRuleResponse
        """

        all_params = ['keywords_alarm_rule_id']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'keywords_alarm_rule_id' in local_var_params:
            path_params['keywords_alarm_rule_id'] = local_var_params['keywords_alarm_rule_id']

        query_params = []

        header_params = {}

        form_params = {}

        body_params = None
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json'])

        auth_settings = []

        return self.call_api(
            resource_path='/v2/{project_id}/lts/alarms/keywords-alarm-rule/{keywords_alarm_rule_id}',
            method='DELETE',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='DeleteKeywordsAlarmRuleResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def delete_log_group_async(self, request):
        """删除日志组

        该接口用于删除指定日志组。当日志组中的日志流配置了日志转储，需要取消日志转储后才可删除。

        :param DeleteLogGroupRequest request
        :return: DeleteLogGroupResponse
        """
        return self.delete_log_group_with_http_info(request)

    def delete_log_group_with_http_info(self, request):
        """删除日志组

        该接口用于删除指定日志组。当日志组中的日志流配置了日志转储，需要取消日志转储后才可删除。

        :param DeleteLogGroupRequest request
        :return: DeleteLogGroupResponse
        """

        all_params = ['log_group_id']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'log_group_id' in local_var_params:
            path_params['log_group_id'] = local_var_params['log_group_id']

        query_params = []

        header_params = {}

        form_params = {}

        body_params = None
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json'])

        auth_settings = []

        return self.call_api(
            resource_path='/v2/{project_id}/groups/{log_group_id}',
            method='DELETE',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='DeleteLogGroupResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def delete_log_stream_async(self, request):
        """删除日志流

        该接口用于删除指定日志组下的指定日志流。当该日志流配置了日志转储，需要取消日志转储后才可删除。

        :param DeleteLogStreamRequest request
        :return: DeleteLogStreamResponse
        """
        return self.delete_log_stream_with_http_info(request)

    def delete_log_stream_with_http_info(self, request):
        """删除日志流

        该接口用于删除指定日志组下的指定日志流。当该日志流配置了日志转储，需要取消日志转储后才可删除。

        :param DeleteLogStreamRequest request
        :return: DeleteLogStreamResponse
        """

        all_params = ['log_group_id', 'log_stream_id']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'log_group_id' in local_var_params:
            path_params['log_group_id'] = local_var_params['log_group_id']
        if 'log_stream_id' in local_var_params:
            path_params['log_stream_id'] = local_var_params['log_stream_id']

        query_params = []

        header_params = {}

        form_params = {}

        body_params = None
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json'])

        auth_settings = []

        return self.call_api(
            resource_path='/v2/{project_id}/groups/{log_group_id}/streams/{log_stream_id}',
            method='DELETE',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='DeleteLogStreamResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def delete_notification_template_async(self, request):
        """删除消息模板

        该接口用于删除通知模板。

        :param DeleteNotificationTemplateRequest request
        :return: DeleteNotificationTemplateResponse
        """
        return self.delete_notification_template_with_http_info(request)

    def delete_notification_template_with_http_info(self, request):
        """删除消息模板

        该接口用于删除通知模板。

        :param DeleteNotificationTemplateRequest request
        :return: DeleteNotificationTemplateResponse
        """

        all_params = ['domain_id', 'delete_notification_template_request_body']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'domain_id' in local_var_params:
            path_params['domain_id'] = local_var_params['domain_id']

        query_params = []

        header_params = {}

        form_params = {}

        body_params = None
        if 'body' in local_var_params:
            body_params = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json;charset=UTF-8'])

        auth_settings = []

        return self.call_api(
            resource_path='/v2/{project_id}/{domain_id}/lts/events/notification/templates',
            method='DELETE',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='DeleteNotificationTemplateResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def delete_struct_template_async(self, request):
        """删除结构化配置

        该接口用于删除指定日志流下的结构化配置。

        :param DeleteStructTemplateRequest request
        :return: DeleteStructTemplateResponse
        """
        return self.delete_struct_template_with_http_info(request)

    def delete_struct_template_with_http_info(self, request):
        """删除结构化配置

        该接口用于删除指定日志流下的结构化配置。

        :param DeleteStructTemplateRequest request
        :return: DeleteStructTemplateResponse
        """

        all_params = ['delete_struct_template_request_body']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = {}

        body_params = None
        if 'body' in local_var_params:
            body_params = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json;charset=UTF-8'])

        auth_settings = []

        return self.call_api(
            resource_path='/v2/{project_id}/lts/struct/template',
            method='DELETE',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='DeleteStructTemplateResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def delete_transfer_async(self, request):
        """删除日志转储

        该接口用于删除OBS转储，DIS转储，DMS转储。

        :param DeleteTransferRequest request
        :return: DeleteTransferResponse
        """
        return self.delete_transfer_with_http_info(request)

    def delete_transfer_with_http_info(self, request):
        """删除日志转储

        该接口用于删除OBS转储，DIS转储，DMS转储。

        :param DeleteTransferRequest request
        :return: DeleteTransferResponse
        """

        all_params = ['log_transfer_id']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'log_transfer_id' in local_var_params:
            query_params.append(('log_transfer_id', local_var_params['log_transfer_id']))

        header_params = {}

        form_params = {}

        body_params = None
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json'])

        auth_settings = []

        return self.call_api(
            resource_path='/v2/{project_id}/transfers',
            method='DELETE',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='DeleteTransferResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def disable_log_collection_async(self, request):
        """关闭超额采集开关

        该接口用于将超额采集日志功能关闭。

        :param DisableLogCollectionRequest request
        :return: DisableLogCollectionResponse
        """
        return self.disable_log_collection_with_http_info(request)

    def disable_log_collection_with_http_info(self, request):
        """关闭超额采集开关

        该接口用于将超额采集日志功能关闭。

        :param DisableLogCollectionRequest request
        :return: DisableLogCollectionResponse
        """

        all_params = []
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = {}

        body_params = None
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json'])

        auth_settings = []

        return self.call_api(
            resource_path='/v2/{project_id}/collection/disable',
            method='POST',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='DisableLogCollectionResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def enable_log_collection_async(self, request):
        """打开超额采集开关

        该接口用于将超额采集日志功能打开。

        :param EnableLogCollectionRequest request
        :return: EnableLogCollectionResponse
        """
        return self.enable_log_collection_with_http_info(request)

    def enable_log_collection_with_http_info(self, request):
        """打开超额采集开关

        该接口用于将超额采集日志功能打开。

        :param EnableLogCollectionRequest request
        :return: EnableLogCollectionResponse
        """

        all_params = []
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = {}

        body_params = None
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json'])

        auth_settings = []

        return self.call_api(
            resource_path='/v2/{project_id}/collection/enable',
            method='POST',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='EnableLogCollectionResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def list_access_config_async(self, request):
        """查询日志接入

        查询日志接入列表

        :param ListAccessConfigRequest request
        :return: ListAccessConfigResponse
        """
        return self.list_access_config_with_http_info(request)

    def list_access_config_with_http_info(self, request):
        """查询日志接入

        查询日志接入列表

        :param ListAccessConfigRequest request
        :return: ListAccessConfigResponse
        """

        all_params = ['list_access_config_request_body']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = {}

        body_params = None
        if 'body' in local_var_params:
            body_params = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json;charset=UTF-8'])

        auth_settings = []

        return self.call_api(
            resource_path='/v3/{project_id}/lts/access-config-list',
            method='POST',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ListAccessConfigResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def list_active_or_history_alarms_async(self, request):
        """查询活动或历史告警列表

        该接口用于查询告警列表

        :param ListActiveOrHistoryAlarmsRequest request
        :return: ListActiveOrHistoryAlarmsResponse
        """
        return self.list_active_or_history_alarms_with_http_info(request)

    def list_active_or_history_alarms_with_http_info(self, request):
        """查询活动或历史告警列表

        该接口用于查询告警列表

        :param ListActiveOrHistoryAlarmsRequest request
        :return: ListActiveOrHistoryAlarmsResponse
        """

        all_params = ['domain_id', 'type', 'list_active_or_history_alarms_request_body', 'marker', 'limit']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'domain_id' in local_var_params:
            path_params['domain_id'] = local_var_params['domain_id']

        query_params = []
        if 'type' in local_var_params:
            query_params.append(('type', local_var_params['type']))
        if 'marker' in local_var_params:
            query_params.append(('marker', local_var_params['marker']))
        if 'limit' in local_var_params:
            query_params.append(('limit', local_var_params['limit']))

        header_params = {}

        form_params = {}

        body_params = None
        if 'body' in local_var_params:
            body_params = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json;charset=UTF-8'])

        auth_settings = []

        return self.call_api(
            resource_path='/v2/{project_id}/{domain_id}/lts/alarms/sql-alarm/query',
            method='POST',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ListActiveOrHistoryAlarmsResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def list_breif_struct_template_async(self, request):
        """查询结构化模板简略列表

        该接口用于查询结构化模板简略列表。

        :param ListBreifStructTemplateRequest request
        :return: ListBreifStructTemplateResponse
        """
        return self.list_breif_struct_template_with_http_info(request)

    def list_breif_struct_template_with_http_info(self, request):
        """查询结构化模板简略列表

        该接口用于查询结构化模板简略列表。

        :param ListBreifStructTemplateRequest request
        :return: ListBreifStructTemplateResponse
        """

        all_params = []
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = {}

        body_params = None
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json'])

        auth_settings = []

        return self.call_api(
            resource_path='/v3/{project_id}/lts/struct/customtemplate/list',
            method='GET',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ListBreifStructTemplateResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def list_charts_async(self, request):
        """查询日志流图表

        该接口用于查询日志流图表

        :param ListChartsRequest request
        :return: ListChartsResponse
        """
        return self.list_charts_with_http_info(request)

    def list_charts_with_http_info(self, request):
        """查询日志流图表

        该接口用于查询日志流图表

        :param ListChartsRequest request
        :return: ListChartsResponse
        """

        all_params = ['log_group_id', 'log_stream_id', 'offset', 'limit']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'log_group_id' in local_var_params:
            path_params['log_group_id'] = local_var_params['log_group_id']
        if 'log_stream_id' in local_var_params:
            path_params['log_stream_id'] = local_var_params['log_stream_id']

        query_params = []
        if 'offset' in local_var_params:
            query_params.append(('offset', local_var_params['offset']))
        if 'limit' in local_var_params:
            query_params.append(('limit', local_var_params['limit']))

        header_params = {}

        form_params = {}

        body_params = None
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json'])

        auth_settings = []

        return self.call_api(
            resource_path='/v2/{project_id}/groups/{log_group_id}/streams/{log_stream_id}/charts',
            method='GET',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ListChartsResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def list_host_async(self, request):
        """查询主机信息

        查询主机列表

        :param ListHostRequest request
        :return: ListHostResponse
        """
        return self.list_host_with_http_info(request)

    def list_host_with_http_info(self, request):
        """查询主机信息

        查询主机列表

        :param ListHostRequest request
        :return: ListHostResponse
        """

        all_params = ['list_host_request_body']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = {}

        body_params = None
        if 'body' in local_var_params:
            body_params = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json;charset=UTF-8'])

        auth_settings = []

        return self.call_api(
            resource_path='/v3/{project_id}/lts/host-list',
            method='POST',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ListHostResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def list_host_group_async(self, request):
        """查询主机组

        查询主机组列表

        :param ListHostGroupRequest request
        :return: ListHostGroupResponse
        """
        return self.list_host_group_with_http_info(request)

    def list_host_group_with_http_info(self, request):
        """查询主机组

        查询主机组列表

        :param ListHostGroupRequest request
        :return: ListHostGroupResponse
        """

        all_params = ['list_host_group_request_body']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = {}

        body_params = None
        if 'body' in local_var_params:
            body_params = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json;charset=UTF-8'])

        auth_settings = []

        return self.call_api(
            resource_path='/v3/{project_id}/lts/host-group-list',
            method='POST',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ListHostGroupResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def list_keywords_alarm_rules_async(self, request):
        """查询关键词告警规则

        该接口用于查询关键词告警。

        :param ListKeywordsAlarmRulesRequest request
        :return: ListKeywordsAlarmRulesResponse
        """
        return self.list_keywords_alarm_rules_with_http_info(request)

    def list_keywords_alarm_rules_with_http_info(self, request):
        """查询关键词告警规则

        该接口用于查询关键词告警。

        :param ListKeywordsAlarmRulesRequest request
        :return: ListKeywordsAlarmRulesResponse
        """

        all_params = []
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = {}

        body_params = None
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json'])

        auth_settings = []

        return self.call_api(
            resource_path='/v2/{project_id}/lts/alarms/keywords-alarm-rule',
            method='GET',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ListKeywordsAlarmRulesResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def list_log_groups_async(self, request):
        """查询账号下所有日志组

        该接口用于查询账号下所有日志组。

        :param ListLogGroupsRequest request
        :return: ListLogGroupsResponse
        """
        return self.list_log_groups_with_http_info(request)

    def list_log_groups_with_http_info(self, request):
        """查询账号下所有日志组

        该接口用于查询账号下所有日志组。

        :param ListLogGroupsRequest request
        :return: ListLogGroupsResponse
        """

        all_params = []
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = {}

        body_params = None
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json'])

        auth_settings = []

        return self.call_api(
            resource_path='/v2/{project_id}/groups',
            method='GET',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ListLogGroupsResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def list_log_histogram_async(self, request):
        """查询日志直方图

        查询关键词搜索条数

        :param ListLogHistogramRequest request
        :return: ListLogHistogramResponse
        """
        return self.list_log_histogram_with_http_info(request)

    def list_log_histogram_with_http_info(self, request):
        """查询日志直方图

        查询关键词搜索条数

        :param ListLogHistogramRequest request
        :return: ListLogHistogramResponse
        """

        all_params = ['list_log_histogram_request_body']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = {}

        body_params = None
        if 'body' in local_var_params:
            body_params = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json;charset=UTF-8'])

        auth_settings = []

        return self.call_api(
            resource_path='/v2/{project_id}/lts/keyword-count',
            method='POST',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ListLogHistogramResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def list_log_stream_async(self, request):
        """查询指定日志组下的所有日志流

        该接口用于查询指定日志组下的所有日志流信息。

        :param ListLogStreamRequest request
        :return: ListLogStreamResponse
        """
        return self.list_log_stream_with_http_info(request)

    def list_log_stream_with_http_info(self, request):
        """查询指定日志组下的所有日志流

        该接口用于查询指定日志组下的所有日志流信息。

        :param ListLogStreamRequest request
        :return: ListLogStreamResponse
        """

        all_params = ['log_group_id', 'tag']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'log_group_id' in local_var_params:
            path_params['log_group_id'] = local_var_params['log_group_id']

        query_params = []
        if 'tag' in local_var_params:
            query_params.append(('tag', local_var_params['tag']))

        header_params = {}

        form_params = {}

        body_params = None
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json'])

        auth_settings = []

        return self.call_api(
            resource_path='/v2/{project_id}/groups/{log_group_id}/streams',
            method='GET',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ListLogStreamResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def list_log_streams_async(self, request):
        """查询日志流信息

        该接口用于查询LTS日志流信息。

        :param ListLogStreamsRequest request
        :return: ListLogStreamsResponse
        """
        return self.list_log_streams_with_http_info(request)

    def list_log_streams_with_http_info(self, request):
        """查询日志流信息

        该接口用于查询LTS日志流信息。

        :param ListLogStreamsRequest request
        :return: ListLogStreamsResponse
        """

        all_params = ['log_group_name', 'log_stream_name', 'offset', 'limit']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'log_group_name' in local_var_params:
            query_params.append(('log_group_name', local_var_params['log_group_name']))
        if 'log_stream_name' in local_var_params:
            query_params.append(('log_stream_name', local_var_params['log_stream_name']))
        if 'offset' in local_var_params:
            query_params.append(('offset', local_var_params['offset']))
        if 'limit' in local_var_params:
            query_params.append(('limit', local_var_params['limit']))

        header_params = {}

        form_params = {}

        body_params = None
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json'])

        auth_settings = []

        return self.call_api(
            resource_path='/v2/{project_id}/log-streams',
            method='GET',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ListLogStreamsResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def list_logs_async(self, request):
        """查询日志

        该接口用于查询指定日志流下的日志内容。

        :param ListLogsRequest request
        :return: ListLogsResponse
        """
        return self.list_logs_with_http_info(request)

    def list_logs_with_http_info(self, request):
        """查询日志

        该接口用于查询指定日志流下的日志内容。

        :param ListLogsRequest request
        :return: ListLogsResponse
        """

        all_params = ['log_group_id', 'log_stream_id', 'list_logs_request_body']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'log_group_id' in local_var_params:
            path_params['log_group_id'] = local_var_params['log_group_id']
        if 'log_stream_id' in local_var_params:
            path_params['log_stream_id'] = local_var_params['log_stream_id']

        query_params = []

        header_params = {}

        form_params = {}

        body_params = None
        if 'body' in local_var_params:
            body_params = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json'])

        auth_settings = []

        return self.call_api(
            resource_path='/v2/{project_id}/groups/{log_group_id}/streams/{log_stream_id}/content/query',
            method='POST',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ListLogsResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def list_notification_template_async(self, request):
        """预览消息模板邮件格式

        该接口用于预览通知模板邮件格式

        :param ListNotificationTemplateRequest request
        :return: ListNotificationTemplateResponse
        """
        return self.list_notification_template_with_http_info(request)

    def list_notification_template_with_http_info(self, request):
        """预览消息模板邮件格式

        该接口用于预览通知模板邮件格式

        :param ListNotificationTemplateRequest request
        :return: ListNotificationTemplateResponse
        """

        all_params = ['domain_id', 'preview_notification_template_request_body']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'domain_id' in local_var_params:
            path_params['domain_id'] = local_var_params['domain_id']

        query_params = []

        header_params = {}

        form_params = {}

        body_params = None
        if 'body' in local_var_params:
            body_params = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json;charset=UTF-8'])

        auth_settings = []

        return self.call_api(
            resource_path='/v2/{project_id}/{domain_id}/lts/events/notification/templates/view',
            method='POST',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ListNotificationTemplateResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def list_notification_templates_async(self, request):
        """查询消息模板

        该接口用于查询通知模板。

        :param ListNotificationTemplatesRequest request
        :return: ListNotificationTemplatesResponse
        """
        return self.list_notification_templates_with_http_info(request)

    def list_notification_templates_with_http_info(self, request):
        """查询消息模板

        该接口用于查询通知模板。

        :param ListNotificationTemplatesRequest request
        :return: ListNotificationTemplatesResponse
        """

        all_params = ['domain_id', 'offset', 'limit']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'domain_id' in local_var_params:
            path_params['domain_id'] = local_var_params['domain_id']

        query_params = []
        if 'offset' in local_var_params:
            query_params.append(('offset', local_var_params['offset']))
        if 'limit' in local_var_params:
            query_params.append(('limit', local_var_params['limit']))

        header_params = {}

        form_params = {}

        body_params = None
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json'])

        auth_settings = []

        return self.call_api(
            resource_path='/v2/{project_id}/{domain_id}/lts/events/notification/templates',
            method='GET',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ListNotificationTemplatesResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def list_notification_topics_async(self, request):
        """查询SMN主题

        该接口用于查询SMN主题

        :param ListNotificationTopicsRequest request
        :return: ListNotificationTopicsResponse
        """
        return self.list_notification_topics_with_http_info(request)

    def list_notification_topics_with_http_info(self, request):
        """查询SMN主题

        该接口用于查询SMN主题

        :param ListNotificationTopicsRequest request
        :return: ListNotificationTopicsResponse
        """

        all_params = ['offset', 'limit']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'offset' in local_var_params:
            query_params.append(('offset', local_var_params['offset']))
        if 'limit' in local_var_params:
            query_params.append(('limit', local_var_params['limit']))

        header_params = {}

        form_params = {}

        body_params = None
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json'])

        auth_settings = []

        return self.call_api(
            resource_path='/v2/{project_id}/lts/notifications/topics',
            method='GET',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ListNotificationTopicsResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def list_query_structured_logs_async(self, request):
        """查询结构化日志

        该接口用于查询指定日志流下的结构化日志内容。

        :param ListQueryStructuredLogsRequest request
        :return: ListQueryStructuredLogsResponse
        """
        return self.list_query_structured_logs_with_http_info(request)

    def list_query_structured_logs_with_http_info(self, request):
        """查询结构化日志

        该接口用于查询指定日志流下的结构化日志内容。

        :param ListQueryStructuredLogsRequest request
        :return: ListQueryStructuredLogsResponse
        """

        all_params = ['log_group_id', 'log_stream_id', 'list_query_structured_logs_request_body']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'log_group_id' in local_var_params:
            path_params['log_group_id'] = local_var_params['log_group_id']
        if 'log_stream_id' in local_var_params:
            path_params['log_stream_id'] = local_var_params['log_stream_id']

        query_params = []

        header_params = {}

        form_params = {}

        body_params = None
        if 'body' in local_var_params:
            body_params = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json'])

        auth_settings = []

        return self.call_api(
            resource_path='/v2/{project_id}/groups/{log_group_id}/streams/{log_stream_id}/struct-content/query',
            method='POST',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ListQueryStructuredLogsResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def list_struct_template_async(self, request):
        """查询结构化模板

        该接口用于查询结构化模板。

        :param ListStructTemplateRequest request
        :return: ListStructTemplateResponse
        """
        return self.list_struct_template_with_http_info(request)

    def list_struct_template_with_http_info(self, request):
        """查询结构化模板

        该接口用于查询结构化模板。

        :param ListStructTemplateRequest request
        :return: ListStructTemplateResponse
        """

        all_params = ['id']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'id' in local_var_params:
            query_params.append(('id', local_var_params['id']))

        header_params = {}

        form_params = {}

        body_params = None
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json'])

        auth_settings = []

        return self.call_api(
            resource_path='/v3/{project_id}/lts/struct/customtemplate',
            method='GET',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ListStructTemplateResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def list_structured_logs_with_time_range_async(self, request):
        """查询结构化日志（新版）

        该接口用于查询指定日志流下的结构化日志内容（新版）。

        :param ListStructuredLogsWithTimeRangeRequest request
        :return: ListStructuredLogsWithTimeRangeResponse
        """
        return self.list_structured_logs_with_time_range_with_http_info(request)

    def list_structured_logs_with_time_range_with_http_info(self, request):
        """查询结构化日志（新版）

        该接口用于查询指定日志流下的结构化日志内容（新版）。

        :param ListStructuredLogsWithTimeRangeRequest request
        :return: ListStructuredLogsWithTimeRangeResponse
        """

        all_params = ['log_stream_id', 'list_structured_logs_with_time_range_request_body']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'log_stream_id' in local_var_params:
            path_params['log_stream_id'] = local_var_params['log_stream_id']

        query_params = []

        header_params = {}

        form_params = {}

        body_params = None
        if 'body' in local_var_params:
            body_params = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json'])

        auth_settings = []

        return self.call_api(
            resource_path='/v2/{project_id}/streams/{log_stream_id}/struct-content/query',
            method='POST',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ListStructuredLogsWithTimeRangeResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def list_transfers_async(self, request):
        """查询日志转储

        该接口用于查询OBS转储，DIS转储，DMS转储配置。

        :param ListTransfersRequest request
        :return: ListTransfersResponse
        """
        return self.list_transfers_with_http_info(request)

    def list_transfers_with_http_info(self, request):
        """查询日志转储

        该接口用于查询OBS转储，DIS转储，DMS转储配置。

        :param ListTransfersRequest request
        :return: ListTransfersResponse
        """

        all_params = ['log_transfer_type', 'log_group_name', 'log_stream_name', 'offset', 'limit']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'log_transfer_type' in local_var_params:
            query_params.append(('log_transfer_type', local_var_params['log_transfer_type']))
        if 'log_group_name' in local_var_params:
            query_params.append(('log_group_name', local_var_params['log_group_name']))
        if 'log_stream_name' in local_var_params:
            query_params.append(('log_stream_name', local_var_params['log_stream_name']))
        if 'offset' in local_var_params:
            query_params.append(('offset', local_var_params['offset']))
        if 'limit' in local_var_params:
            query_params.append(('limit', local_var_params['limit']))

        header_params = {}

        form_params = {}

        body_params = None
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json'])

        auth_settings = []

        return self.call_api(
            resource_path='/v2/{project_id}/transfers',
            method='GET',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ListTransfersResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def register_dms_kafka_instance_async(self, request):
        """注册DMS kafka实例

        该接口用于注册DMS kafka实例。

        :param RegisterDmsKafkaInstanceRequest request
        :return: RegisterDmsKafkaInstanceResponse
        """
        return self.register_dms_kafka_instance_with_http_info(request)

    def register_dms_kafka_instance_with_http_info(self, request):
        """注册DMS kafka实例

        该接口用于注册DMS kafka实例。

        :param RegisterDmsKafkaInstanceRequest request
        :return: RegisterDmsKafkaInstanceResponse
        """

        all_params = ['register_dms_kafka_instance_request_body']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = {}

        body_params = None
        if 'body' in local_var_params:
            body_params = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json;charset=UTF-8'])

        auth_settings = []

        return self.call_api(
            resource_path='/v2/{project_id}/lts/dms/kafka-instance',
            method='POST',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='RegisterDmsKafkaInstanceResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def show_notification_template_async(self, request):
        """查询单个消息模板

        该接口用于查询单个通知模板

        :param ShowNotificationTemplateRequest request
        :return: ShowNotificationTemplateResponse
        """
        return self.show_notification_template_with_http_info(request)

    def show_notification_template_with_http_info(self, request):
        """查询单个消息模板

        该接口用于查询单个通知模板

        :param ShowNotificationTemplateRequest request
        :return: ShowNotificationTemplateResponse
        """

        all_params = ['domain_id', 'template_name']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'domain_id' in local_var_params:
            path_params['domain_id'] = local_var_params['domain_id']
        if 'template_name' in local_var_params:
            path_params['template_name'] = local_var_params['template_name']

        query_params = []

        header_params = {}

        form_params = {}

        body_params = None
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json'])

        auth_settings = []

        return self.call_api(
            resource_path='/v2/{project_id}/{domain_id}/lts/events/notification/template/{template_name}',
            method='GET',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ShowNotificationTemplateResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def show_struct_template_async(self, request):
        """查询结构化配置

        该接口用于查询指定日志流下的结构化配置内容。

        :param ShowStructTemplateRequest request
        :return: ShowStructTemplateResponse
        """
        return self.show_struct_template_with_http_info(request)

    def show_struct_template_with_http_info(self, request):
        """查询结构化配置

        该接口用于查询指定日志流下的结构化配置内容。

        :param ShowStructTemplateRequest request
        :return: ShowStructTemplateResponse
        """

        all_params = ['log_group_id', 'log_stream_id']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'log_group_id' in local_var_params:
            query_params.append(('logGroupId', local_var_params['log_group_id']))
        if 'log_stream_id' in local_var_params:
            query_params.append(('logStreamId', local_var_params['log_stream_id']))

        header_params = {}

        form_params = {}

        body_params = None
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json'])

        auth_settings = []

        return self.call_api(
            resource_path='/v2/{project_id}/lts/struct/template',
            method='GET',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ShowStructTemplateResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def update_access_config_async(self, request):
        """修改日志接入

        修改日志接入

        :param UpdateAccessConfigRequest request
        :return: UpdateAccessConfigResponse
        """
        return self.update_access_config_with_http_info(request)

    def update_access_config_with_http_info(self, request):
        """修改日志接入

        修改日志接入

        :param UpdateAccessConfigRequest request
        :return: UpdateAccessConfigResponse
        """

        all_params = ['update_access_config_request_body']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = {}

        body_params = None
        if 'body' in local_var_params:
            body_params = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json;charset=UTF-8'])

        auth_settings = []

        return self.call_api(
            resource_path='/v3/{project_id}/lts/access-config',
            method='PUT',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='UpdateAccessConfigResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def update_host_group_async(self, request):
        """修改主机组

        修改主机组

        :param UpdateHostGroupRequest request
        :return: UpdateHostGroupResponse
        """
        return self.update_host_group_with_http_info(request)

    def update_host_group_with_http_info(self, request):
        """修改主机组

        修改主机组

        :param UpdateHostGroupRequest request
        :return: UpdateHostGroupResponse
        """

        all_params = ['update_host_group_request_body']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = {}

        body_params = None
        if 'body' in local_var_params:
            body_params = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json;charset=UTF-8'])

        auth_settings = []

        return self.call_api(
            resource_path='/v3/{project_id}/lts/host-group',
            method='PUT',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='UpdateHostGroupResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def update_keywords_alarm_rule_async(self, request):
        """修改关键词告警规则

        该接口用于修改关键词告警。

        :param UpdateKeywordsAlarmRuleRequest request
        :return: UpdateKeywordsAlarmRuleResponse
        """
        return self.update_keywords_alarm_rule_with_http_info(request)

    def update_keywords_alarm_rule_with_http_info(self, request):
        """修改关键词告警规则

        该接口用于修改关键词告警。

        :param UpdateKeywordsAlarmRuleRequest request
        :return: UpdateKeywordsAlarmRuleResponse
        """

        all_params = ['update_keywords_alarm_rule_request_body']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = {}

        body_params = None
        if 'body' in local_var_params:
            body_params = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json;charset=UTF-8'])

        auth_settings = []

        return self.call_api(
            resource_path='/v2/{project_id}/lts/alarms/keywords-alarm-rule',
            method='PUT',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='UpdateKeywordsAlarmRuleResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def update_log_group_async(self, request):
        """修改日志组

        该接口用于修改指定日志组下的日志存储时长。

        :param UpdateLogGroupRequest request
        :return: UpdateLogGroupResponse
        """
        return self.update_log_group_with_http_info(request)

    def update_log_group_with_http_info(self, request):
        """修改日志组

        该接口用于修改指定日志组下的日志存储时长。

        :param UpdateLogGroupRequest request
        :return: UpdateLogGroupResponse
        """

        all_params = ['log_group_id', 'update_log_group_request_body']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'log_group_id' in local_var_params:
            path_params['log_group_id'] = local_var_params['log_group_id']

        query_params = []

        header_params = {}

        form_params = {}

        body_params = None
        if 'body' in local_var_params:
            body_params = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json'])

        auth_settings = []

        return self.call_api(
            resource_path='/v2/{project_id}/groups/{log_group_id}',
            method='POST',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='UpdateLogGroupResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def update_notification_template_async(self, request):
        """修改消息模板

        该接口用于修改通知模板,根据名称进行修改。

        :param UpdateNotificationTemplateRequest request
        :return: UpdateNotificationTemplateResponse
        """
        return self.update_notification_template_with_http_info(request)

    def update_notification_template_with_http_info(self, request):
        """修改消息模板

        该接口用于修改通知模板,根据名称进行修改。

        :param UpdateNotificationTemplateRequest request
        :return: UpdateNotificationTemplateResponse
        """

        all_params = ['domain_id', 'update_notification_template_request_body']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'domain_id' in local_var_params:
            path_params['domain_id'] = local_var_params['domain_id']

        query_params = []

        header_params = {}

        form_params = {}

        body_params = None
        if 'body' in local_var_params:
            body_params = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json;charset=UTF-8'])

        auth_settings = []

        return self.call_api(
            resource_path='/v2/{project_id}/{domain_id}/lts/events/notification/templates',
            method='PUT',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='UpdateNotificationTemplateResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def update_struct_config_async(self, request):
        """通过结构化模板修改结构化配置（新）

        该接口通过结构化模板修改结构化配置

        :param UpdateStructConfigRequest request
        :return: UpdateStructConfigResponse
        """
        return self.update_struct_config_with_http_info(request)

    def update_struct_config_with_http_info(self, request):
        """通过结构化模板修改结构化配置（新）

        该接口通过结构化模板修改结构化配置

        :param UpdateStructConfigRequest request
        :return: UpdateStructConfigResponse
        """

        all_params = ['update_struct_config_request_body']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = {}

        body_params = None
        if 'body' in local_var_params:
            body_params = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json;charset=UTF-8'])

        auth_settings = []

        return self.call_api(
            resource_path='/v3/{project_id}/lts/struct/template',
            method='PUT',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='UpdateStructConfigResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def update_struct_template_async(self, request):
        """修改结构化配置

        该接口用于修改指定日志流下的结构化配置。

        :param UpdateStructTemplateRequest request
        :return: UpdateStructTemplateResponse
        """
        return self.update_struct_template_with_http_info(request)

    def update_struct_template_with_http_info(self, request):
        """修改结构化配置

        该接口用于修改指定日志流下的结构化配置。

        :param UpdateStructTemplateRequest request
        :return: UpdateStructTemplateResponse
        """

        all_params = ['update_struct_template_request_body']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = {}

        body_params = None
        if 'body' in local_var_params:
            body_params = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json'])

        auth_settings = []

        return self.call_api(
            resource_path='/v2/{project_id}/lts/struct/template',
            method='PUT',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='UpdateStructTemplateResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def update_transfer_async(self, request):
        """更新日志转储

        该接口用于更新OBS转储，DIS转储，DMS转储。

        :param UpdateTransferRequest request
        :return: UpdateTransferResponse
        """
        return self.update_transfer_with_http_info(request)

    def update_transfer_with_http_info(self, request):
        """更新日志转储

        该接口用于更新OBS转储，DIS转储，DMS转储。

        :param UpdateTransferRequest request
        :return: UpdateTransferResponse
        """

        all_params = ['update_transfer_request_body']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = {}

        body_params = None
        if 'body' in local_var_params:
            body_params = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json;charset=UTF-8'])

        auth_settings = []

        return self.call_api(
            resource_path='/v2/{project_id}/transfers',
            method='PUT',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='UpdateTransferResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def create_aom_mapping_rules_async(self, request):
        """创建接入规则

        该接口用于创建aom日志接入lts规则

        :param CreateAomMappingRulesRequest request
        :return: CreateAomMappingRulesResponse
        """
        return self.create_aom_mapping_rules_with_http_info(request)

    def create_aom_mapping_rules_with_http_info(self, request):
        """创建接入规则

        该接口用于创建aom日志接入lts规则

        :param CreateAomMappingRulesRequest request
        :return: CreateAomMappingRulesResponse
        """

        all_params = ['is_batch', 'create_aom_mapping_rules_request_body']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'is_batch' in local_var_params:
            query_params.append(('isBatch', local_var_params['is_batch']))

        header_params = {}

        form_params = {}

        body_params = None
        if 'body' in local_var_params:
            body_params = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json'])

        auth_settings = []

        return self.call_api(
            resource_path='/v2/{project_id}/lts/aom-mapping',
            method='POST',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='CreateAomMappingRulesResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def delete_aom_mapping_rules_async(self, request):
        """删除接入规则

        该接口用于删除lts接入规则。

        :param DeleteAomMappingRulesRequest request
        :return: DeleteAomMappingRulesResponse
        """
        return self.delete_aom_mapping_rules_with_http_info(request)

    def delete_aom_mapping_rules_with_http_info(self, request):
        """删除接入规则

        该接口用于删除lts接入规则。

        :param DeleteAomMappingRulesRequest request
        :return: DeleteAomMappingRulesResponse
        """

        all_params = ['id']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'id' in local_var_params:
            query_params.append(('id', local_var_params['id']))

        header_params = {}

        form_params = {}

        body_params = None
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json'])

        auth_settings = []

        return self.call_api(
            resource_path='/v2/{project_id}/lts/aom-mapping',
            method='DELETE',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='DeleteAomMappingRulesResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def show_aom_mapping_rule_async(self, request):
        """查询单个接入规则

        该接口用于查询单个aom日志接入lts

        :param ShowAomMappingRuleRequest request
        :return: ShowAomMappingRuleResponse
        """
        return self.show_aom_mapping_rule_with_http_info(request)

    def show_aom_mapping_rule_with_http_info(self, request):
        """查询单个接入规则

        该接口用于查询单个aom日志接入lts

        :param ShowAomMappingRuleRequest request
        :return: ShowAomMappingRuleResponse
        """

        all_params = ['rule_id']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'rule_id' in local_var_params:
            path_params['rule_id'] = local_var_params['rule_id']

        query_params = []

        header_params = {}

        form_params = {}

        body_params = None
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json'])

        auth_settings = []

        return self.call_api(
            resource_path='/v2/{project_id}/lts/aom-mapping/{rule_id}',
            method='GET',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ShowAomMappingRuleResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def show_aom_mapping_rules_async(self, request):
        """查询所有接入规则

        该接口用于查询aom日志所有接入lts规则

        :param ShowAomMappingRulesRequest request
        :return: ShowAomMappingRulesResponse
        """
        return self.show_aom_mapping_rules_with_http_info(request)

    def show_aom_mapping_rules_with_http_info(self, request):
        """查询所有接入规则

        该接口用于查询aom日志所有接入lts规则

        :param ShowAomMappingRulesRequest request
        :return: ShowAomMappingRulesResponse
        """

        all_params = []
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = {}

        body_params = None
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json'])

        auth_settings = []

        return self.call_api(
            resource_path='/v2/{project_id}/lts/aom-mapping',
            method='GET',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ShowAomMappingRulesResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def update_aom_mapping_rules_async(self, request):
        """修改接入规则

        该接口用于修改接入规则

        :param UpdateAomMappingRulesRequest request
        :return: UpdateAomMappingRulesResponse
        """
        return self.update_aom_mapping_rules_with_http_info(request)

    def update_aom_mapping_rules_with_http_info(self, request):
        """修改接入规则

        该接口用于修改接入规则

        :param UpdateAomMappingRulesRequest request
        :return: UpdateAomMappingRulesResponse
        """

        all_params = ['update_aom_mapping_rules_request_body']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = {}

        body_params = None
        if 'body' in local_var_params:
            body_params = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json'])

        auth_settings = []

        return self.call_api(
            resource_path='/v2/{project_id}/lts/aom-mapping',
            method='PUT',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='UpdateAomMappingRulesResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def create_sql_alarm_rule_async(self, request):
        """创建SQL告警规则

        该接口用于创建SQL告警，目前每个帐户最多可以创建共200个关键词告警与SQL告警

        :param CreateSqlAlarmRuleRequest request
        :return: CreateSqlAlarmRuleResponse
        """
        return self.create_sql_alarm_rule_with_http_info(request)

    def create_sql_alarm_rule_with_http_info(self, request):
        """创建SQL告警规则

        该接口用于创建SQL告警，目前每个帐户最多可以创建共200个关键词告警与SQL告警

        :param CreateSqlAlarmRuleRequest request
        :return: CreateSqlAlarmRuleResponse
        """

        all_params = ['create_sql_alarm_rule_request_body']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = {}

        body_params = None
        if 'body' in local_var_params:
            body_params = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json;charset=UTF-8'])

        auth_settings = []

        return self.call_api(
            resource_path='/v2/{project_id}/lts/alarms/sql-alarm-rule',
            method='POST',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='CreateSqlAlarmRuleResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def delete_sql_alarm_rule_async(self, request):
        """删除SQL告警规则

        该接口用于删除SQL告警

        :param DeleteSqlAlarmRuleRequest request
        :return: DeleteSqlAlarmRuleResponse
        """
        return self.delete_sql_alarm_rule_with_http_info(request)

    def delete_sql_alarm_rule_with_http_info(self, request):
        """删除SQL告警规则

        该接口用于删除SQL告警

        :param DeleteSqlAlarmRuleRequest request
        :return: DeleteSqlAlarmRuleResponse
        """

        all_params = ['sql_alarm_rule_id']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'sql_alarm_rule_id' in local_var_params:
            path_params['sql_alarm_rule_id'] = local_var_params['sql_alarm_rule_id']

        query_params = []

        header_params = {}

        form_params = {}

        body_params = None
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json'])

        auth_settings = []

        return self.call_api(
            resource_path='/v2/{project_id}/lts/alarms/sql-alarm-rule/{sql_alarm_rule_id}',
            method='DELETE',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='DeleteSqlAlarmRuleResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def list_sql_alarm_rules_async(self, request):
        """查询SQL告警规则

        该接口用于查询SQL告警

        :param ListSqlAlarmRulesRequest request
        :return: ListSqlAlarmRulesResponse
        """
        return self.list_sql_alarm_rules_with_http_info(request)

    def list_sql_alarm_rules_with_http_info(self, request):
        """查询SQL告警规则

        该接口用于查询SQL告警

        :param ListSqlAlarmRulesRequest request
        :return: ListSqlAlarmRulesResponse
        """

        all_params = []
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = {}

        body_params = None
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json'])

        auth_settings = []

        return self.call_api(
            resource_path='/v2/{project_id}/lts/alarms/sql-alarm-rule',
            method='GET',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ListSqlAlarmRulesResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def update_alarm_rule_status_async(self, request):
        """切换告警规则状态

        改变告警规则状态

        :param UpdateAlarmRuleStatusRequest request
        :return: UpdateAlarmRuleStatusResponse
        """
        return self.update_alarm_rule_status_with_http_info(request)

    def update_alarm_rule_status_with_http_info(self, request):
        """切换告警规则状态

        改变告警规则状态

        :param UpdateAlarmRuleStatusRequest request
        :return: UpdateAlarmRuleStatusResponse
        """

        all_params = ['change_alarm_rule_status']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = {}

        body_params = None
        if 'body' in local_var_params:
            body_params = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json;charset=UTF-8'])

        auth_settings = []

        return self.call_api(
            resource_path='/v2/{project_id}/lts/alarms/status',
            method='PUT',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='UpdateAlarmRuleStatusResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def update_sql_alarm_rule_async(self, request):
        """修改SQL告警规则

        该接口用于修改SQL告警

        :param UpdateSqlAlarmRuleRequest request
        :return: UpdateSqlAlarmRuleResponse
        """
        return self.update_sql_alarm_rule_with_http_info(request)

    def update_sql_alarm_rule_with_http_info(self, request):
        """修改SQL告警规则

        该接口用于修改SQL告警

        :param UpdateSqlAlarmRuleRequest request
        :return: UpdateSqlAlarmRuleResponse
        """

        all_params = ['update_sql_alarm_rule_request_body']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = {}

        body_params = None
        if 'body' in local_var_params:
            body_params = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json;charset=UTF-8'])

        auth_settings = []

        return self.call_api(
            resource_path='/v2/{project_id}/lts/alarms/sql-alarm-rule',
            method='PUT',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='UpdateSqlAlarmRuleResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def call_api(self, resource_path, method, path_params=None, query_params=None, header_params=None, body=None,
                 post_params=None, response_type=None, response_headers=None, auth_settings=None,
                 collection_formats=None, request_type=None):
        """Makes the HTTP request and returns deserialized data.

        :param resource_path: Path to method endpoint.
        :param method: Method to call.
        :param path_params: Path parameters in the url.
        :param query_params: Query parameters in the url.
        :param header_params: Header parameters to be
            placed in the request header.
        :param body: Request body.
        :param post_params dict: Request post form parameters,
            for `application/x-www-form-urlencoded`, `multipart/form-data`.
        :param auth_settings list: Auth Settings names for the request.
        :param response_type: Response data type.
        :param response_headers: Header should be added to response data.
        :param collection_formats: dict of collection formats for path, query,
            header, and post parameters.
        :param request_type: Request data type.
        :return:
            Return the response directly.
        """
        return self.do_http_request(
            method=method,
            resource_path=resource_path,
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body,
            post_params=post_params,
            response_type=response_type,
            response_headers=response_headers,
            collection_formats=collection_formats,
            request_type=request_type,
	    async_request=True)
