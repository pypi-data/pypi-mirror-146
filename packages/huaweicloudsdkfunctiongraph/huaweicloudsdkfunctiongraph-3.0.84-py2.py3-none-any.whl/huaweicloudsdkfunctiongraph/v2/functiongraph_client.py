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


class FunctionGraphClient(Client):
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
        super(FunctionGraphClient, self).__init__()
        self.model_package = importlib.import_module("huaweicloudsdkfunctiongraph.v2.model")
        self.preset_headers = {'User-Agent': 'HuaweiCloud-SDK-Python'}

    @classmethod
    def new_builder(cls, clazz=None):
        if clazz is None:
            return ClientBuilder(cls)

        if clazz.__name__ != "FunctionGraphClient":
            raise TypeError("client type error, support client type is FunctionGraphClient")

        return ClientBuilder(clazz)

    def async_invoke_function(self, request):
        """异步执行函数。

        异步执行函数。

        :param AsyncInvokeFunctionRequest request
        :return: AsyncInvokeFunctionResponse
        """
        return self.async_invoke_function_with_http_info(request)

    def async_invoke_function_with_http_info(self, request):
        """异步执行函数。

        异步执行函数。

        :param AsyncInvokeFunctionRequest request
        :return: AsyncInvokeFunctionResponse
        """

        all_params = ['function_urn', 'async_invoke_function_request_body']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'function_urn' in local_var_params:
            path_params['function_urn'] = local_var_params['function_urn']

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
            resource_path='/v2/{project_id}/fgs/functions/{function_urn}/invocations-async',
            method='POST',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='AsyncInvokeFunctionResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def async_invoke_reserved_function(self, request):
        """函数异步执行并返回预留实例ID。

        函数异步执行并返回预留实例ID用于场景指客户端请求执行比较费时任务，不需要同步等待执行完成返回结果，该方法提前返回任务执行对应的预留实例ID, 如果预留实例有异常， 可以通过该实例ID把对应实例删除（该接口主要针对白名单用户）。

        :param AsyncInvokeReservedFunctionRequest request
        :return: AsyncInvokeReservedFunctionResponse
        """
        return self.async_invoke_reserved_function_with_http_info(request)

    def async_invoke_reserved_function_with_http_info(self, request):
        """函数异步执行并返回预留实例ID。

        函数异步执行并返回预留实例ID用于场景指客户端请求执行比较费时任务，不需要同步等待执行完成返回结果，该方法提前返回任务执行对应的预留实例ID, 如果预留实例有异常， 可以通过该实例ID把对应实例删除（该接口主要针对白名单用户）。

        :param AsyncInvokeReservedFunctionRequest request
        :return: AsyncInvokeReservedFunctionResponse
        """

        all_params = ['function_urn', 'async_invoke_reserved_function_request_body']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'function_urn' in local_var_params:
            path_params['function_urn'] = local_var_params['function_urn']

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
            resource_path='/v2/{project_id}/fgs/functions/{function_urn}/reserved-invocations',
            method='POST',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='AsyncInvokeReservedFunctionResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def create_dependency(self, request):
        """创建依赖包

        创建依赖包。

        :param CreateDependencyRequest request
        :return: CreateDependencyResponse
        """
        return self.create_dependency_with_http_info(request)

    def create_dependency_with_http_info(self, request):
        """创建依赖包

        创建依赖包。

        :param CreateDependencyRequest request
        :return: CreateDependencyResponse
        """

        all_params = ['create_dependency_request_body']
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
            resource_path='/v2/{project_id}/fgs/dependencies',
            method='POST',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='CreateDependencyResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def create_event(self, request):
        """创建测试事件

        创建测试事件。

        :param CreateEventRequest request
        :return: CreateEventResponse
        """
        return self.create_event_with_http_info(request)

    def create_event_with_http_info(self, request):
        """创建测试事件

        创建测试事件。

        :param CreateEventRequest request
        :return: CreateEventResponse
        """

        all_params = ['function_urn', 'create_event_request_body']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'function_urn' in local_var_params:
            path_params['function_urn'] = local_var_params['function_urn']

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
            resource_path='/v2/{project_id}/fgs/functions/{function_urn}/events',
            method='POST',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='CreateEventResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def create_function(self, request):
        """创建函数。

        创建指定的函数。

        :param CreateFunctionRequest request
        :return: CreateFunctionResponse
        """
        return self.create_function_with_http_info(request)

    def create_function_with_http_info(self, request):
        """创建函数。

        创建指定的函数。

        :param CreateFunctionRequest request
        :return: CreateFunctionResponse
        """

        all_params = ['create_function_request_body']
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
            resource_path='/v2/{project_id}/fgs/functions',
            method='POST',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='CreateFunctionResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def create_function_version(self, request):
        """发布函数版本。

        发布函数版本。

        :param CreateFunctionVersionRequest request
        :return: CreateFunctionVersionResponse
        """
        return self.create_function_version_with_http_info(request)

    def create_function_version_with_http_info(self, request):
        """发布函数版本。

        发布函数版本。

        :param CreateFunctionVersionRequest request
        :return: CreateFunctionVersionResponse
        """

        all_params = ['function_urn', 'create_function_version_request_body']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'function_urn' in local_var_params:
            path_params['function_urn'] = local_var_params['function_urn']

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
            resource_path='/v2/{project_id}/fgs/functions/{function_urn}/versions',
            method='POST',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='CreateFunctionVersionResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def create_version_alias(self, request):
        """创建函数版本别名。

        创建函数灰度版本别名。

        :param CreateVersionAliasRequest request
        :return: CreateVersionAliasResponse
        """
        return self.create_version_alias_with_http_info(request)

    def create_version_alias_with_http_info(self, request):
        """创建函数版本别名。

        创建函数灰度版本别名。

        :param CreateVersionAliasRequest request
        :return: CreateVersionAliasResponse
        """

        all_params = ['function_urn', 'create_version_alias_request_body']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'function_urn' in local_var_params:
            path_params['function_urn'] = local_var_params['function_urn']

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
            resource_path='/v2/{project_id}/fgs/functions/{function_urn}/aliases',
            method='POST',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='CreateVersionAliasResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def delete_dependency(self, request):
        """删除依赖包

        删除指定的依赖包。

        :param DeleteDependencyRequest request
        :return: DeleteDependencyResponse
        """
        return self.delete_dependency_with_http_info(request)

    def delete_dependency_with_http_info(self, request):
        """删除依赖包

        删除指定的依赖包。

        :param DeleteDependencyRequest request
        :return: DeleteDependencyResponse
        """

        all_params = ['depend_id']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'depend_id' in local_var_params:
            path_params['depend_id'] = local_var_params['depend_id']

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
            resource_path='/v2/{project_id}/fgs/dependencies/{depend_id}',
            method='DELETE',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='DeleteDependencyResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def delete_event(self, request):
        """删除测试事件

        删除测试事件。

        :param DeleteEventRequest request
        :return: DeleteEventResponse
        """
        return self.delete_event_with_http_info(request)

    def delete_event_with_http_info(self, request):
        """删除测试事件

        删除测试事件。

        :param DeleteEventRequest request
        :return: DeleteEventResponse
        """

        all_params = ['event_id', 'function_urn']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'event_id' in local_var_params:
            path_params['event_id'] = local_var_params['event_id']
        if 'function_urn' in local_var_params:
            path_params['function_urn'] = local_var_params['function_urn']

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
            resource_path='/v2/{project_id}/fgs/functions/{function_urn}/events/{event_id}',
            method='DELETE',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='DeleteEventResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def delete_function(self, request):
        """删除函数/版本。

        删除指定的函数或者特定的版本（不允许删除latest版本）。  如果URN中包含函数版本或者别名，则删除特定的函数版本或者别名指向的版本以及该版本关联的trigger。 如果URN中不包含版本或者别名，则删除整个函数，包含所有版本以及别名，触发器。

        :param DeleteFunctionRequest request
        :return: DeleteFunctionResponse
        """
        return self.delete_function_with_http_info(request)

    def delete_function_with_http_info(self, request):
        """删除函数/版本。

        删除指定的函数或者特定的版本（不允许删除latest版本）。  如果URN中包含函数版本或者别名，则删除特定的函数版本或者别名指向的版本以及该版本关联的trigger。 如果URN中不包含版本或者别名，则删除整个函数，包含所有版本以及别名，触发器。

        :param DeleteFunctionRequest request
        :return: DeleteFunctionResponse
        """

        all_params = ['function_urn']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'function_urn' in local_var_params:
            path_params['function_urn'] = local_var_params['function_urn']

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
            resource_path='/v2/{project_id}/fgs/functions/{function_urn}',
            method='DELETE',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='DeleteFunctionResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def delete_function_async_invoke_config(self, request):
        """删除函数异步配置信息。

        删除函数异步配置信息。

        :param DeleteFunctionAsyncInvokeConfigRequest request
        :return: DeleteFunctionAsyncInvokeConfigResponse
        """
        return self.delete_function_async_invoke_config_with_http_info(request)

    def delete_function_async_invoke_config_with_http_info(self, request):
        """删除函数异步配置信息。

        删除函数异步配置信息。

        :param DeleteFunctionAsyncInvokeConfigRequest request
        :return: DeleteFunctionAsyncInvokeConfigResponse
        """

        all_params = ['function_urn']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'function_urn' in local_var_params:
            path_params['function_urn'] = local_var_params['function_urn']

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
            resource_path='/v2/{project_id}/fgs/functions/{function_urn}/async-invoke-config',
            method='DELETE',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='DeleteFunctionAsyncInvokeConfigResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def delete_version_alias(self, request):
        """删除函数版本别名。

        删除函数版本别名。

        :param DeleteVersionAliasRequest request
        :return: DeleteVersionAliasResponse
        """
        return self.delete_version_alias_with_http_info(request)

    def delete_version_alias_with_http_info(self, request):
        """删除函数版本别名。

        删除函数版本别名。

        :param DeleteVersionAliasRequest request
        :return: DeleteVersionAliasResponse
        """

        all_params = ['function_urn', 'alias_name']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'function_urn' in local_var_params:
            path_params['function_urn'] = local_var_params['function_urn']
        if 'alias_name' in local_var_params:
            path_params['alias_name'] = local_var_params['alias_name']

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
            resource_path='/v2/{project_id}/fgs/functions/{function_urn}/aliases/{alias_name}',
            method='DELETE',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='DeleteVersionAliasResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def enable_lts_logs(self, request):
        """开通lts日志上报功能。

        开通lts日志上报功能。

        :param EnableLtsLogsRequest request
        :return: EnableLtsLogsResponse
        """
        return self.enable_lts_logs_with_http_info(request)

    def enable_lts_logs_with_http_info(self, request):
        """开通lts日志上报功能。

        开通lts日志上报功能。

        :param EnableLtsLogsRequest request
        :return: EnableLtsLogsResponse
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
            resource_path='/v2/{project_id}/fgs/functions/enable-lts-logs',
            method='POST',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='EnableLtsLogsResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def export_function(self, request):
        """导出函数。

        导出函数。

        :param ExportFunctionRequest request
        :return: ExportFunctionResponse
        """
        return self.export_function_with_http_info(request)

    def export_function_with_http_info(self, request):
        """导出函数。

        导出函数。

        :param ExportFunctionRequest request
        :return: ExportFunctionResponse
        """

        all_params = ['function_urn', 'config', 'code', 'type']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'function_urn' in local_var_params:
            path_params['function_urn'] = local_var_params['function_urn']

        query_params = []
        if 'config' in local_var_params:
            query_params.append(('config', local_var_params['config']))
        if 'code' in local_var_params:
            query_params.append(('code', local_var_params['code']))
        if 'type' in local_var_params:
            query_params.append(('type', local_var_params['type']))

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
            resource_path='/v2/{project_id}/fgs/functions/{function_urn}/export',
            method='GET',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ExportFunctionResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def import_function(self, request):
        """导入函数。

        导入函数。

        :param ImportFunctionRequest request
        :return: ImportFunctionResponse
        """
        return self.import_function_with_http_info(request)

    def import_function_with_http_info(self, request):
        """导入函数。

        导入函数。

        :param ImportFunctionRequest request
        :return: ImportFunctionResponse
        """

        all_params = ['import_function_request_body']
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
            resource_path='/v2/{project_id}/fgs/functions/import',
            method='POST',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ImportFunctionResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def invoke_function(self, request):
        """同步执行函数。

        同步调用指的是客户端请求需要明确等到响应结果，也就是说这样的请求必须得调用到用户的函数，并且等到调用完成才返回。

        :param InvokeFunctionRequest request
        :return: InvokeFunctionResponse
        """
        return self.invoke_function_with_http_info(request)

    def invoke_function_with_http_info(self, request):
        """同步执行函数。

        同步调用指的是客户端请求需要明确等到响应结果，也就是说这样的请求必须得调用到用户的函数，并且等到调用完成才返回。

        :param InvokeFunctionRequest request
        :return: InvokeFunctionResponse
        """

        all_params = ['function_urn', 'invoke_function_request_body', 'x_cff_log_type', 'x_cff_request_version']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'function_urn' in local_var_params:
            path_params['function_urn'] = local_var_params['function_urn']

        query_params = []

        header_params = {}
        if 'x_cff_log_type' in local_var_params:
            header_params['X-Cff-Log-Type'] = local_var_params['x_cff_log_type']
        if 'x_cff_request_version' in local_var_params:
            header_params['X-CFF-Request-Version'] = local_var_params['x_cff_request_version']

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
            resource_path='/v2/{project_id}/fgs/functions/{function_urn}/invocations',
            method='POST',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='InvokeFunctionResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def list_dependencies(self, request):
        """获取依赖包列表

        获取依赖包列表。

        :param ListDependenciesRequest request
        :return: ListDependenciesResponse
        """
        return self.list_dependencies_with_http_info(request)

    def list_dependencies_with_http_info(self, request):
        """获取依赖包列表

        获取依赖包列表。

        :param ListDependenciesRequest request
        :return: ListDependenciesResponse
        """

        all_params = ['dependency_type', 'runtime', 'name', 'marker', 'limit']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'dependency_type' in local_var_params:
            query_params.append(('dependency_type', local_var_params['dependency_type']))
        if 'runtime' in local_var_params:
            query_params.append(('runtime', local_var_params['runtime']))
        if 'name' in local_var_params:
            query_params.append(('name', local_var_params['name']))
        if 'marker' in local_var_params:
            query_params.append(('marker', local_var_params['marker']))
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
            resource_path='/v2/{project_id}/fgs/dependencies',
            method='GET',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ListDependenciesResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def list_events(self, request):
        """获取测试事件列表

        获取指定函数的测试事件列表。

        :param ListEventsRequest request
        :return: ListEventsResponse
        """
        return self.list_events_with_http_info(request)

    def list_events_with_http_info(self, request):
        """获取测试事件列表

        获取指定函数的测试事件列表。

        :param ListEventsRequest request
        :return: ListEventsResponse
        """

        all_params = ['function_urn']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'function_urn' in local_var_params:
            path_params['function_urn'] = local_var_params['function_urn']

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
            resource_path='/v2/{project_id}/fgs/functions/{function_urn}/events',
            method='GET',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ListEventsResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def list_function_async_invocations(self, request):
        """获取函数异步调用请求列表

        获取函数异步调用请求列表

        :param ListFunctionAsyncInvocationsRequest request
        :return: ListFunctionAsyncInvocationsResponse
        """
        return self.list_function_async_invocations_with_http_info(request)

    def list_function_async_invocations_with_http_info(self, request):
        """获取函数异步调用请求列表

        获取函数异步调用请求列表

        :param ListFunctionAsyncInvocationsRequest request
        :return: ListFunctionAsyncInvocationsResponse
        """

        all_params = ['function_urn', 'request_id', 'limit', 'status', 'query_begin_time', 'query_end_time']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'function_urn' in local_var_params:
            path_params['function_urn'] = local_var_params['function_urn']

        query_params = []
        if 'request_id' in local_var_params:
            query_params.append(('request_id', local_var_params['request_id']))
        if 'limit' in local_var_params:
            query_params.append(('limit', local_var_params['limit']))
        if 'status' in local_var_params:
            query_params.append(('status', local_var_params['status']))
        if 'query_begin_time' in local_var_params:
            query_params.append(('query_begin_time', local_var_params['query_begin_time']))
        if 'query_end_time' in local_var_params:
            query_params.append(('query_end_time', local_var_params['query_end_time']))

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
            resource_path='/v2/{project_id}/fgs/functions/{function_urn}/async-invocations',
            method='GET',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ListFunctionAsyncInvocationsResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def list_function_async_invoke_config(self, request):
        """获取函数异步配置列表

        获取函数异步配置列表。

        :param ListFunctionAsyncInvokeConfigRequest request
        :return: ListFunctionAsyncInvokeConfigResponse
        """
        return self.list_function_async_invoke_config_with_http_info(request)

    def list_function_async_invoke_config_with_http_info(self, request):
        """获取函数异步配置列表

        获取函数异步配置列表。

        :param ListFunctionAsyncInvokeConfigRequest request
        :return: ListFunctionAsyncInvokeConfigResponse
        """

        all_params = ['function_urn', 'marker', 'limit']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'function_urn' in local_var_params:
            path_params['function_urn'] = local_var_params['function_urn']

        query_params = []
        if 'marker' in local_var_params:
            query_params.append(('marker', local_var_params['marker']))
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
            resource_path='/v2/{project_id}/fgs/functions/{function_urn}/async-invoke-configs',
            method='GET',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ListFunctionAsyncInvokeConfigResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def list_function_statistics(self, request):
        """获取指定时间段的函数运行指标

        获取指定时间段的函数运行指标。

        :param ListFunctionStatisticsRequest request
        :return: ListFunctionStatisticsResponse
        """
        return self.list_function_statistics_with_http_info(request)

    def list_function_statistics_with_http_info(self, request):
        """获取指定时间段的函数运行指标

        获取指定时间段的函数运行指标。

        :param ListFunctionStatisticsRequest request
        :return: ListFunctionStatisticsResponse
        """

        all_params = ['func_urn', 'period']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'func_urn' in local_var_params:
            path_params['func_urn'] = local_var_params['func_urn']
        if 'period' in local_var_params:
            path_params['period'] = local_var_params['period']

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
            resource_path='/v2/{project_id}/fgs/functions/{func_urn}/statistics/{period}',
            method='GET',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ListFunctionStatisticsResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def list_function_versions(self, request):
        """获取指定函数的版本列表。

        获取指定函数的版本列表。

        :param ListFunctionVersionsRequest request
        :return: ListFunctionVersionsResponse
        """
        return self.list_function_versions_with_http_info(request)

    def list_function_versions_with_http_info(self, request):
        """获取指定函数的版本列表。

        获取指定函数的版本列表。

        :param ListFunctionVersionsRequest request
        :return: ListFunctionVersionsResponse
        """

        all_params = ['function_urn', 'marker', 'maxitems']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'function_urn' in local_var_params:
            path_params['function_urn'] = local_var_params['function_urn']

        query_params = []
        if 'marker' in local_var_params:
            query_params.append(('marker', local_var_params['marker']))
        if 'maxitems' in local_var_params:
            query_params.append(('maxitems', local_var_params['maxitems']))

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
            resource_path='/v2/{project_id}/fgs/functions/{function_urn}/versions',
            method='GET',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ListFunctionVersionsResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def list_functions(self, request):
        """获取函数列表

        获取函数列表

        :param ListFunctionsRequest request
        :return: ListFunctionsResponse
        """
        return self.list_functions_with_http_info(request)

    def list_functions_with_http_info(self, request):
        """获取函数列表

        获取函数列表

        :param ListFunctionsRequest request
        :return: ListFunctionsResponse
        """

        all_params = ['marker', 'maxitems', 'package_name']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'marker' in local_var_params:
            query_params.append(('marker', local_var_params['marker']))
        if 'maxitems' in local_var_params:
            query_params.append(('maxitems', local_var_params['maxitems']))
        if 'package_name' in local_var_params:
            query_params.append(('package_name', local_var_params['package_name']))

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
            resource_path='/v2/{project_id}/fgs/functions',
            method='GET',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ListFunctionsResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def list_quotas(self, request):
        """查询租户配额

        查询租户配额

        :param ListQuotasRequest request
        :return: ListQuotasResponse
        """
        return self.list_quotas_with_http_info(request)

    def list_quotas_with_http_info(self, request):
        """查询租户配额

        查询租户配额

        :param ListQuotasRequest request
        :return: ListQuotasResponse
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
            resource_path='/v2/{project_id}/fgs/quotas',
            method='GET',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ListQuotasResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def list_statistics(self, request):
        """租户函数统计信息

        租户函数统计信息。  返回三类的统计信息，函数格式和大小使用情况包括配额和使用量，流量报告。 通过查询参数filter可以进行过滤，查询参数period可以指定返回的时间段。

        :param ListStatisticsRequest request
        :return: ListStatisticsResponse
        """
        return self.list_statistics_with_http_info(request)

    def list_statistics_with_http_info(self, request):
        """租户函数统计信息

        租户函数统计信息。  返回三类的统计信息，函数格式和大小使用情况包括配额和使用量，流量报告。 通过查询参数filter可以进行过滤，查询参数period可以指定返回的时间段。

        :param ListStatisticsRequest request
        :return: ListStatisticsResponse
        """

        all_params = ['filter', 'period']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'filter' in local_var_params:
            query_params.append(('filter', local_var_params['filter']))
        if 'period' in local_var_params:
            query_params.append(('period', local_var_params['period']))

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
            resource_path='/v2/{project_id}/fgs/functions/statistics',
            method='GET',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ListStatisticsResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def list_version_aliases(self, request):
        """获取指定函数所有版本别名列表。

        获取函数版本别名列表。

        :param ListVersionAliasesRequest request
        :return: ListVersionAliasesResponse
        """
        return self.list_version_aliases_with_http_info(request)

    def list_version_aliases_with_http_info(self, request):
        """获取指定函数所有版本别名列表。

        获取函数版本别名列表。

        :param ListVersionAliasesRequest request
        :return: ListVersionAliasesResponse
        """

        all_params = ['function_urn']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'function_urn' in local_var_params:
            path_params['function_urn'] = local_var_params['function_urn']

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
            resource_path='/v2/{project_id}/fgs/functions/{function_urn}/aliases',
            method='GET',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ListVersionAliasesResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def show_dependency(self, request):
        """获取指定依赖包

        获取指定依赖包。

        :param ShowDependencyRequest request
        :return: ShowDependencyResponse
        """
        return self.show_dependency_with_http_info(request)

    def show_dependency_with_http_info(self, request):
        """获取指定依赖包

        获取指定依赖包。

        :param ShowDependencyRequest request
        :return: ShowDependencyResponse
        """

        all_params = ['depend_id']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'depend_id' in local_var_params:
            path_params['depend_id'] = local_var_params['depend_id']

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
            resource_path='/v2/{project_id}/fgs/dependencies/{depend_id}',
            method='GET',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ShowDependencyResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def show_event(self, request):
        """获取测试事件详细信息

        获取测试事件详细信息。

        :param ShowEventRequest request
        :return: ShowEventResponse
        """
        return self.show_event_with_http_info(request)

    def show_event_with_http_info(self, request):
        """获取测试事件详细信息

        获取测试事件详细信息。

        :param ShowEventRequest request
        :return: ShowEventResponse
        """

        all_params = ['event_id', 'function_urn']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'event_id' in local_var_params:
            path_params['event_id'] = local_var_params['event_id']
        if 'function_urn' in local_var_params:
            path_params['function_urn'] = local_var_params['function_urn']

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
            resource_path='/v2/{project_id}/fgs/functions/{function_urn}/events/{event_id}',
            method='GET',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ShowEventResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def show_function_async_invoke_config(self, request):
        """获取函数异步配置信息。

        获取函数异步配置信息。

        :param ShowFunctionAsyncInvokeConfigRequest request
        :return: ShowFunctionAsyncInvokeConfigResponse
        """
        return self.show_function_async_invoke_config_with_http_info(request)

    def show_function_async_invoke_config_with_http_info(self, request):
        """获取函数异步配置信息。

        获取函数异步配置信息。

        :param ShowFunctionAsyncInvokeConfigRequest request
        :return: ShowFunctionAsyncInvokeConfigResponse
        """

        all_params = ['function_urn']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'function_urn' in local_var_params:
            path_params['function_urn'] = local_var_params['function_urn']

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
            resource_path='/v2/{project_id}/fgs/functions/{function_urn}/async-invoke-config',
            method='GET',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ShowFunctionAsyncInvokeConfigResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def show_function_code(self, request):
        """获取指定函数代码。

        获取指定函数的代码。

        :param ShowFunctionCodeRequest request
        :return: ShowFunctionCodeResponse
        """
        return self.show_function_code_with_http_info(request)

    def show_function_code_with_http_info(self, request):
        """获取指定函数代码。

        获取指定函数的代码。

        :param ShowFunctionCodeRequest request
        :return: ShowFunctionCodeResponse
        """

        all_params = ['function_urn']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'function_urn' in local_var_params:
            path_params['function_urn'] = local_var_params['function_urn']

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
            resource_path='/v2/{project_id}/fgs/functions/{function_urn}/code',
            method='GET',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ShowFunctionCodeResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def show_function_config(self, request):
        """获取函数的metadata。

        获取指定函数的metadata。

        :param ShowFunctionConfigRequest request
        :return: ShowFunctionConfigResponse
        """
        return self.show_function_config_with_http_info(request)

    def show_function_config_with_http_info(self, request):
        """获取函数的metadata。

        获取指定函数的metadata。

        :param ShowFunctionConfigRequest request
        :return: ShowFunctionConfigResponse
        """

        all_params = ['function_urn']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'function_urn' in local_var_params:
            path_params['function_urn'] = local_var_params['function_urn']

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
            resource_path='/v2/{project_id}/fgs/functions/{function_urn}/config',
            method='GET',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ShowFunctionConfigResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def show_lts_log_details(self, request):
        """获取指定函数的lts日志组日志流配置。

        获取指定函数的lts日志组日志流配置。

        :param ShowLtsLogDetailsRequest request
        :return: ShowLtsLogDetailsResponse
        """
        return self.show_lts_log_details_with_http_info(request)

    def show_lts_log_details_with_http_info(self, request):
        """获取指定函数的lts日志组日志流配置。

        获取指定函数的lts日志组日志流配置。

        :param ShowLtsLogDetailsRequest request
        :return: ShowLtsLogDetailsResponse
        """

        all_params = ['function_urn']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'function_urn' in local_var_params:
            path_params['function_urn'] = local_var_params['function_urn']

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
            resource_path='/v2/{project_id}/fgs/functions/{function_urn}/lts-log-detail',
            method='GET',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ShowLtsLogDetailsResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def show_tracing(self, request):
        """获取函数调用链配置

        获取函数调用链配置

        :param ShowTracingRequest request
        :return: ShowTracingResponse
        """
        return self.show_tracing_with_http_info(request)

    def show_tracing_with_http_info(self, request):
        """获取函数调用链配置

        获取函数调用链配置

        :param ShowTracingRequest request
        :return: ShowTracingResponse
        """

        all_params = ['function_urn']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'function_urn' in local_var_params:
            path_params['function_urn'] = local_var_params['function_urn']

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
            resource_path='/v2/{project_id}/fgs/functions/{function_urn}/tracing',
            method='GET',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ShowTracingResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def show_version_alias(self, request):
        """获取函数版本的指定别名信息。

        获取函数指定的版本别名信息。

        :param ShowVersionAliasRequest request
        :return: ShowVersionAliasResponse
        """
        return self.show_version_alias_with_http_info(request)

    def show_version_alias_with_http_info(self, request):
        """获取函数版本的指定别名信息。

        获取函数指定的版本别名信息。

        :param ShowVersionAliasRequest request
        :return: ShowVersionAliasResponse
        """

        all_params = ['function_urn', 'alias_name']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'function_urn' in local_var_params:
            path_params['function_urn'] = local_var_params['function_urn']
        if 'alias_name' in local_var_params:
            path_params['alias_name'] = local_var_params['alias_name']

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
            resource_path='/v2/{project_id}/fgs/functions/{function_urn}/aliases/{alias_name}',
            method='GET',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ShowVersionAliasResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def update_dependency(self, request):
        """更新依赖包指定依赖包

        更新依赖包指定依赖包。

        :param UpdateDependencyRequest request
        :return: UpdateDependencyResponse
        """
        return self.update_dependency_with_http_info(request)

    def update_dependency_with_http_info(self, request):
        """更新依赖包指定依赖包

        更新依赖包指定依赖包。

        :param UpdateDependencyRequest request
        :return: UpdateDependencyResponse
        """

        all_params = ['depend_id', 'update_dependency_request_body']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'depend_id' in local_var_params:
            path_params['depend_id'] = local_var_params['depend_id']

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
            resource_path='/v2/{project_id}/fgs/dependencies/{depend_id}',
            method='PUT',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='UpdateDependencyResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def update_event(self, request):
        """更新测试事件

        更新测试事件。

        :param UpdateEventRequest request
        :return: UpdateEventResponse
        """
        return self.update_event_with_http_info(request)

    def update_event_with_http_info(self, request):
        """更新测试事件

        更新测试事件。

        :param UpdateEventRequest request
        :return: UpdateEventResponse
        """

        all_params = ['event_id', 'function_urn', 'update_event_request_body']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'event_id' in local_var_params:
            path_params['event_id'] = local_var_params['event_id']
        if 'function_urn' in local_var_params:
            path_params['function_urn'] = local_var_params['function_urn']

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
            resource_path='/v2/{project_id}/fgs/functions/{function_urn}/events/{event_id}',
            method='PUT',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='UpdateEventResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def update_function_async_invoke_config(self, request):
        """设置函数异步配置信息。

        设置函数异步配置信息。

        :param UpdateFunctionAsyncInvokeConfigRequest request
        :return: UpdateFunctionAsyncInvokeConfigResponse
        """
        return self.update_function_async_invoke_config_with_http_info(request)

    def update_function_async_invoke_config_with_http_info(self, request):
        """设置函数异步配置信息。

        设置函数异步配置信息。

        :param UpdateFunctionAsyncInvokeConfigRequest request
        :return: UpdateFunctionAsyncInvokeConfigResponse
        """

        all_params = ['function_urn', 'update_function_async_invoke_config_request_body']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'function_urn' in local_var_params:
            path_params['function_urn'] = local_var_params['function_urn']

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
            resource_path='/v2/{project_id}/fgs/functions/{function_urn}/async-invoke-config',
            method='PUT',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='UpdateFunctionAsyncInvokeConfigResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def update_function_code(self, request):
        """修改函数代码。

        修改指定的函数的代码。

        :param UpdateFunctionCodeRequest request
        :return: UpdateFunctionCodeResponse
        """
        return self.update_function_code_with_http_info(request)

    def update_function_code_with_http_info(self, request):
        """修改函数代码。

        修改指定的函数的代码。

        :param UpdateFunctionCodeRequest request
        :return: UpdateFunctionCodeResponse
        """

        all_params = ['function_urn', 'update_function_code_request_body']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'function_urn' in local_var_params:
            path_params['function_urn'] = local_var_params['function_urn']

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
            resource_path='/v2/{project_id}/fgs/functions/{function_urn}/code',
            method='PUT',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='UpdateFunctionCodeResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def update_function_config(self, request):
        """修改函数的metadata信息。

        修改指定的函数的metadata信息。

        :param UpdateFunctionConfigRequest request
        :return: UpdateFunctionConfigResponse
        """
        return self.update_function_config_with_http_info(request)

    def update_function_config_with_http_info(self, request):
        """修改函数的metadata信息。

        修改指定的函数的metadata信息。

        :param UpdateFunctionConfigRequest request
        :return: UpdateFunctionConfigResponse
        """

        all_params = ['function_urn', 'update_function_config_request_body']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'function_urn' in local_var_params:
            path_params['function_urn'] = local_var_params['function_urn']

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
            resource_path='/v2/{project_id}/fgs/functions/{function_urn}/config',
            method='PUT',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='UpdateFunctionConfigResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def update_function_reserved_instances(self, request):
        """更新函数预留实例个数

        为函数绑定预留实例

        :param UpdateFunctionReservedInstancesRequest request
        :return: UpdateFunctionReservedInstancesResponse
        """
        return self.update_function_reserved_instances_with_http_info(request)

    def update_function_reserved_instances_with_http_info(self, request):
        """更新函数预留实例个数

        为函数绑定预留实例

        :param UpdateFunctionReservedInstancesRequest request
        :return: UpdateFunctionReservedInstancesResponse
        """

        all_params = ['function_urn', 'update_function_reserved_instances_request_body']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'function_urn' in local_var_params:
            path_params['function_urn'] = local_var_params['function_urn']

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
            resource_path='/v2/{project_id}/fgs/functions/{function_urn}/reservedinstances',
            method='PUT',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='UpdateFunctionReservedInstancesResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def update_tracing(self, request):
        """修改函数调用链配置

        修改函数调用链配置,开通/修改传入aksk，关闭aksk传空

        :param UpdateTracingRequest request
        :return: UpdateTracingResponse
        """
        return self.update_tracing_with_http_info(request)

    def update_tracing_with_http_info(self, request):
        """修改函数调用链配置

        修改函数调用链配置,开通/修改传入aksk，关闭aksk传空

        :param UpdateTracingRequest request
        :return: UpdateTracingResponse
        """

        all_params = ['function_urn', 'update_tracing_request_body']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'function_urn' in local_var_params:
            path_params['function_urn'] = local_var_params['function_urn']

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
            resource_path='/v2/{project_id}/fgs/functions/{function_urn}/tracing',
            method='PUT',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='UpdateTracingResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def update_version_alias(self, request):
        """修改函数版本别名信息。

        修改函数版本别名信息。

        :param UpdateVersionAliasRequest request
        :return: UpdateVersionAliasResponse
        """
        return self.update_version_alias_with_http_info(request)

    def update_version_alias_with_http_info(self, request):
        """修改函数版本别名信息。

        修改函数版本别名信息。

        :param UpdateVersionAliasRequest request
        :return: UpdateVersionAliasResponse
        """

        all_params = ['function_urn', 'alias_name', 'update_version_alias_request_body']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'function_urn' in local_var_params:
            path_params['function_urn'] = local_var_params['function_urn']
        if 'alias_name' in local_var_params:
            path_params['alias_name'] = local_var_params['alias_name']

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
            resource_path='/v2/{project_id}/fgs/functions/{function_urn}/aliases/{alias_name}',
            method='PUT',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='UpdateVersionAliasResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def batch_delete_function_triggers(self, request):
        """删除指定函数的所有触发器。

        删除指定函数所有触发器设置。  在提供函数版本且非latest的情况下，删除对应函数版本的触发器。 在提供函数别名的情况下，删除对应函数别名的触发器。 在不提供函数版本（也不提供别名）或版本为latest的情况下，删除该函数所有的触发器（包括所有版本和别名）。

        :param BatchDeleteFunctionTriggersRequest request
        :return: BatchDeleteFunctionTriggersResponse
        """
        return self.batch_delete_function_triggers_with_http_info(request)

    def batch_delete_function_triggers_with_http_info(self, request):
        """删除指定函数的所有触发器。

        删除指定函数所有触发器设置。  在提供函数版本且非latest的情况下，删除对应函数版本的触发器。 在提供函数别名的情况下，删除对应函数别名的触发器。 在不提供函数版本（也不提供别名）或版本为latest的情况下，删除该函数所有的触发器（包括所有版本和别名）。

        :param BatchDeleteFunctionTriggersRequest request
        :return: BatchDeleteFunctionTriggersResponse
        """

        all_params = ['function_urn']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'function_urn' in local_var_params:
            path_params['function_urn'] = local_var_params['function_urn']

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
            resource_path='/v2/{project_id}/fgs/triggers/{function_urn}',
            method='DELETE',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='BatchDeleteFunctionTriggersResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def create_function_trigger(self, request):
        """创建触发器。

        创建触发器。  - 可以创建的触发器类型包括TIMER、APIG、CTS、DDS、DMS、DIS、LTS、OBS、SMN、KAFKA。 - DDS和KAFKA触发器创建时默认为DISABLED状态，其他触发器默认为ACTIVE状态。 - TIMER、DDS、DMS、KAFKA、LTS触发器支持禁用，其他触发器不支持。

        :param CreateFunctionTriggerRequest request
        :return: CreateFunctionTriggerResponse
        """
        return self.create_function_trigger_with_http_info(request)

    def create_function_trigger_with_http_info(self, request):
        """创建触发器。

        创建触发器。  - 可以创建的触发器类型包括TIMER、APIG、CTS、DDS、DMS、DIS、LTS、OBS、SMN、KAFKA。 - DDS和KAFKA触发器创建时默认为DISABLED状态，其他触发器默认为ACTIVE状态。 - TIMER、DDS、DMS、KAFKA、LTS触发器支持禁用，其他触发器不支持。

        :param CreateFunctionTriggerRequest request
        :return: CreateFunctionTriggerResponse
        """

        all_params = ['function_urn', 'create_function_trigger_request_body']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'function_urn' in local_var_params:
            path_params['function_urn'] = local_var_params['function_urn']

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
            resource_path='/v2/{project_id}/fgs/triggers/{function_urn}',
            method='POST',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='CreateFunctionTriggerResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def delete_function_trigger(self, request):
        """删除触发器。

        删除触发器。

        :param DeleteFunctionTriggerRequest request
        :return: DeleteFunctionTriggerResponse
        """
        return self.delete_function_trigger_with_http_info(request)

    def delete_function_trigger_with_http_info(self, request):
        """删除触发器。

        删除触发器。

        :param DeleteFunctionTriggerRequest request
        :return: DeleteFunctionTriggerResponse
        """

        all_params = ['function_urn', 'trigger_type_code', 'trigger_id']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'function_urn' in local_var_params:
            path_params['function_urn'] = local_var_params['function_urn']
        if 'trigger_type_code' in local_var_params:
            path_params['trigger_type_code'] = local_var_params['trigger_type_code']
        if 'trigger_id' in local_var_params:
            path_params['trigger_id'] = local_var_params['trigger_id']

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
            resource_path='/v2/{project_id}/fgs/triggers/{function_urn}/{trigger_type_code}/{trigger_id}',
            method='DELETE',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='DeleteFunctionTriggerResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def list_function_triggers(self, request):
        """获取指定函数的所有触发器。

        获取指定函数的所有触发器设置。

        :param ListFunctionTriggersRequest request
        :return: ListFunctionTriggersResponse
        """
        return self.list_function_triggers_with_http_info(request)

    def list_function_triggers_with_http_info(self, request):
        """获取指定函数的所有触发器。

        获取指定函数的所有触发器设置。

        :param ListFunctionTriggersRequest request
        :return: ListFunctionTriggersResponse
        """

        all_params = ['function_urn']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'function_urn' in local_var_params:
            path_params['function_urn'] = local_var_params['function_urn']

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
            resource_path='/v2/{project_id}/fgs/triggers/{function_urn}',
            method='GET',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ListFunctionTriggersResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def show_function_trigger(self, request):
        """获取指定触发器的信息。

        获取特定触发器的信息。

        :param ShowFunctionTriggerRequest request
        :return: ShowFunctionTriggerResponse
        """
        return self.show_function_trigger_with_http_info(request)

    def show_function_trigger_with_http_info(self, request):
        """获取指定触发器的信息。

        获取特定触发器的信息。

        :param ShowFunctionTriggerRequest request
        :return: ShowFunctionTriggerResponse
        """

        all_params = ['function_urn', 'trigger_type_code', 'trigger_id']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'function_urn' in local_var_params:
            path_params['function_urn'] = local_var_params['function_urn']
        if 'trigger_type_code' in local_var_params:
            path_params['trigger_type_code'] = local_var_params['trigger_type_code']
        if 'trigger_id' in local_var_params:
            path_params['trigger_id'] = local_var_params['trigger_id']

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
            resource_path='/v2/{project_id}/fgs/triggers/{function_urn}/{trigger_type_code}/{trigger_id}',
            method='GET',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ShowFunctionTriggerResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def update_trigger(self, request):
        """更新触发器

        更新触发器

        :param UpdateTriggerRequest request
        :return: UpdateTriggerResponse
        """
        return self.update_trigger_with_http_info(request)

    def update_trigger_with_http_info(self, request):
        """更新触发器

        更新触发器

        :param UpdateTriggerRequest request
        :return: UpdateTriggerResponse
        """

        all_params = ['function_urn', 'trigger_type_code', 'trigger_id', 'update_trigger_request_body']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'function_urn' in local_var_params:
            path_params['function_urn'] = local_var_params['function_urn']
        if 'trigger_type_code' in local_var_params:
            path_params['trigger_type_code'] = local_var_params['trigger_type_code']
        if 'trigger_id' in local_var_params:
            path_params['trigger_id'] = local_var_params['trigger_id']

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
            resource_path='/v2/{project_id}/fgs/triggers/{function_urn}/{trigger_type_code}/{trigger_id}',
            method='PUT',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='UpdateTriggerResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def batch_delete_workflows(self, request):
        """删除工作流列表

        删除工作流列表

        :param BatchDeleteWorkflowsRequest request
        :return: BatchDeleteWorkflowsResponse
        """
        return self.batch_delete_workflows_with_http_info(request)

    def batch_delete_workflows_with_http_info(self, request):
        """删除工作流列表

        删除工作流列表

        :param BatchDeleteWorkflowsRequest request
        :return: BatchDeleteWorkflowsResponse
        """

        all_params = ['batch_delete_workflows_request_body']
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
            resource_path='/v2/{project_id}/fgs/workflows',
            method='DELETE',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='BatchDeleteWorkflowsResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def create_workflow(self, request):
        """创建工作流列表

        创建工作流列表

        :param CreateWorkflowRequest request
        :return: CreateWorkflowResponse
        """
        return self.create_workflow_with_http_info(request)

    def create_workflow_with_http_info(self, request):
        """创建工作流列表

        创建工作流列表

        :param CreateWorkflowRequest request
        :return: CreateWorkflowResponse
        """

        all_params = ['create_workflow_request_body']
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
            resource_path='/v2/{project_id}/fgs/workflows',
            method='POST',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='CreateWorkflowResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def list_workflow_executions(self, request):
        """获取指定函数流执行实例列表

        获取指定函数流执行实例列表

        :param ListWorkflowExecutionsRequest request
        :return: ListWorkflowExecutionsResponse
        """
        return self.list_workflow_executions_with_http_info(request)

    def list_workflow_executions_with_http_info(self, request):
        """获取指定函数流执行实例列表

        获取指定函数流执行实例列表

        :param ListWorkflowExecutionsRequest request
        :return: ListWorkflowExecutionsResponse
        """

        all_params = ['workflow_id', 'limit', 'status', 'start_time', 'end_time']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'workflow_id' in local_var_params:
            path_params['workflow_id'] = local_var_params['workflow_id']

        query_params = []
        if 'limit' in local_var_params:
            query_params.append(('limit', local_var_params['limit']))
        if 'status' in local_var_params:
            query_params.append(('status', local_var_params['status']))
        if 'start_time' in local_var_params:
            query_params.append(('start_time', local_var_params['start_time']))
        if 'end_time' in local_var_params:
            query_params.append(('end_time', local_var_params['end_time']))

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
            resource_path='/v2/{project_id}/fgs/workflows/{workflow_id}/executions',
            method='GET',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ListWorkflowExecutionsResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def list_workflows(self, request):
        """查询工作流列表

        查询工作流列表

        :param ListWorkflowsRequest request
        :return: ListWorkflowsResponse
        """
        return self.list_workflows_with_http_info(request)

    def list_workflows_with_http_info(self, request):
        """查询工作流列表

        查询工作流列表

        :param ListWorkflowsRequest request
        :return: ListWorkflowsResponse
        """

        all_params = ['workflow_name', 'limit', 'offset']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'workflow_name' in local_var_params:
            query_params.append(('workflow_name', local_var_params['workflow_name']))
        if 'limit' in local_var_params:
            query_params.append(('limit', local_var_params['limit']))
        if 'offset' in local_var_params:
            query_params.append(('offset', local_var_params['offset']))

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
            resource_path='/v2/{project_id}/fgs/workflows',
            method='GET',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ListWorkflowsResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def retry_work_flow(self, request):
        """重试工作流

        重试工作流

        :param RetryWorkFlowRequest request
        :return: RetryWorkFlowResponse
        """
        return self.retry_work_flow_with_http_info(request)

    def retry_work_flow_with_http_info(self, request):
        """重试工作流

        重试工作流

        :param RetryWorkFlowRequest request
        :return: RetryWorkFlowResponse
        """

        all_params = ['workflow_id', 'execution_id']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'workflow_id' in local_var_params:
            path_params['workflow_id'] = local_var_params['workflow_id']
        if 'execution_id' in local_var_params:
            path_params['execution_id'] = local_var_params['execution_id']

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
            resource_path='/v2/{project_id}/fgs/workflows/{workflow_id}/executions/{execution_id}/retry',
            method='POST',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='RetryWorkFlowResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def show_tenant_metric(self, request):
        """获取函数流指标

        获取函数流指标

        :param ShowTenantMetricRequest request
        :return: ShowTenantMetricResponse
        """
        return self.show_tenant_metric_with_http_info(request)

    def show_tenant_metric_with_http_info(self, request):
        """获取函数流指标

        获取函数流指标

        :param ShowTenantMetricRequest request
        :return: ShowTenantMetricResponse
        """

        all_params = ['period']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'period' in local_var_params:
            query_params.append(('period', local_var_params['period']))

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
            resource_path='/v2/{project_id}/fgs/workflow-statistic',
            method='GET',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ShowTenantMetricResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def show_work_flow(self, request):
        """获取指定函数流实例

        获取指定函数流实例

        :param ShowWorkFlowRequest request
        :return: ShowWorkFlowResponse
        """
        return self.show_work_flow_with_http_info(request)

    def show_work_flow_with_http_info(self, request):
        """获取指定函数流实例

        获取指定函数流实例

        :param ShowWorkFlowRequest request
        :return: ShowWorkFlowResponse
        """

        all_params = ['workflow_id']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'workflow_id' in local_var_params:
            path_params['workflow_id'] = local_var_params['workflow_id']

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
            resource_path='/v2/{project_id}/fgs/workflows/{workflow_id}',
            method='GET',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ShowWorkFlowResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def show_work_flow_metric(self, request):
        """获取指定工作流指标

        获取指定工作流指标

        :param ShowWorkFlowMetricRequest request
        :return: ShowWorkFlowMetricResponse
        """
        return self.show_work_flow_metric_with_http_info(request)

    def show_work_flow_metric_with_http_info(self, request):
        """获取指定工作流指标

        获取指定工作流指标

        :param ShowWorkFlowMetricRequest request
        :return: ShowWorkFlowMetricResponse
        """

        all_params = ['workflow_urn', 'period']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'workflow_urn' in local_var_params:
            path_params['workflow_urn'] = local_var_params['workflow_urn']

        query_params = []
        if 'period' in local_var_params:
            query_params.append(('period', local_var_params['period']))

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
            resource_path='/v2/{project_id}/fgs/workflow-statistic/{workflow_urn}',
            method='GET',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ShowWorkFlowMetricResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def show_workflow_execution(self, request):
        """获取指定函数流执行实例

        获取指定函数流执行实例。

        :param ShowWorkflowExecutionRequest request
        :return: ShowWorkflowExecutionResponse
        """
        return self.show_workflow_execution_with_http_info(request)

    def show_workflow_execution_with_http_info(self, request):
        """获取指定函数流执行实例

        获取指定函数流执行实例。

        :param ShowWorkflowExecutionRequest request
        :return: ShowWorkflowExecutionResponse
        """

        all_params = ['workflow_id', 'execution_id']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'workflow_id' in local_var_params:
            path_params['workflow_id'] = local_var_params['workflow_id']
        if 'execution_id' in local_var_params:
            path_params['execution_id'] = local_var_params['execution_id']

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
            resource_path='/v2/{project_id}/fgs/workflows/{workflow_id}/executions/{execution_id}',
            method='GET',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ShowWorkflowExecutionResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def start_workflow_execution(self, request):
        """开始执行函数流

        开始执行函数流

        :param StartWorkflowExecutionRequest request
        :return: StartWorkflowExecutionResponse
        """
        return self.start_workflow_execution_with_http_info(request)

    def start_workflow_execution_with_http_info(self, request):
        """开始执行函数流

        开始执行函数流

        :param StartWorkflowExecutionRequest request
        :return: StartWorkflowExecutionResponse
        """

        all_params = ['workflow_id', 'start_workflow_execution_request_body', 'x_create_time', 'x_workflow_run_id']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'workflow_id' in local_var_params:
            path_params['workflow_id'] = local_var_params['workflow_id']

        query_params = []

        header_params = {}
        if 'x_create_time' in local_var_params:
            header_params['X-Create-Time'] = local_var_params['x_create_time']
        if 'x_workflow_run_id' in local_var_params:
            header_params['X-WorkflowRun-ID'] = local_var_params['x_workflow_run_id']

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
            resource_path='/v2/{project_id}/fgs/workflows/{workflow_id}/executions',
            method='POST',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='StartWorkflowExecutionResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def stop_work_flow(self, request):
        """停止工作流

        停止工作流

        :param StopWorkFlowRequest request
        :return: StopWorkFlowResponse
        """
        return self.stop_work_flow_with_http_info(request)

    def stop_work_flow_with_http_info(self, request):
        """停止工作流

        停止工作流

        :param StopWorkFlowRequest request
        :return: StopWorkFlowResponse
        """

        all_params = ['workflow_id', 'execution_id']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'workflow_id' in local_var_params:
            path_params['workflow_id'] = local_var_params['workflow_id']
        if 'execution_id' in local_var_params:
            path_params['execution_id'] = local_var_params['execution_id']

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
            resource_path='/v2/{project_id}/fgs/workflows/{workflow_id}/executions/{execution_id}/terminate',
            method='POST',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='StopWorkFlowResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def update_work_flow(self, request):
        """修改指定函数流实例

        修改指定函数流实例

        :param UpdateWorkFlowRequest request
        :return: UpdateWorkFlowResponse
        """
        return self.update_work_flow_with_http_info(request)

    def update_work_flow_with_http_info(self, request):
        """修改指定函数流实例

        修改指定函数流实例

        :param UpdateWorkFlowRequest request
        :return: UpdateWorkFlowResponse
        """

        all_params = ['workflow_id', 'update_workflow_request_body']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'workflow_id' in local_var_params:
            path_params['workflow_id'] = local_var_params['workflow_id']

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
            resource_path='/v2/{project_id}/fgs/workflows/{workflow_id}',
            method='PUT',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='UpdateWorkFlowResponse',
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
        :param header_params: Header parameters to be placed in the request header.
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
            request_type=request_type)
