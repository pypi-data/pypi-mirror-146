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


class VpcAsyncClient(Client):
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
        super(VpcAsyncClient, self).__init__()
        self.model_package = importlib.import_module("huaweicloudsdkvpc.v3.model")
        self.preset_headers = {'User-Agent': 'HuaweiCloud-SDK-Python'}

    @classmethod
    def new_builder(cls, clazz=None):
        if clazz is None:
            return ClientBuilder(cls)

        if clazz.__name__ != "VpcClient":
            raise TypeError("client type error, support client type is VpcClient")

        return ClientBuilder(clazz)

    def batch_create_sub_network_interface_async(self, request):
        """批量创建辅助弹性网卡

        批量创建辅助弹性网卡

        :param BatchCreateSubNetworkInterfaceRequest request
        :return: BatchCreateSubNetworkInterfaceResponse
        """
        return self.batch_create_sub_network_interface_with_http_info(request)

    def batch_create_sub_network_interface_with_http_info(self, request):
        """批量创建辅助弹性网卡

        批量创建辅助弹性网卡

        :param BatchCreateSubNetworkInterfaceRequest request
        :return: BatchCreateSubNetworkInterfaceResponse
        """

        all_params = ['batch_create_sub_network_interface_request_body']
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
            resource_path='/v3/{project_id}/vpc/sub-network-interfaces/batch-create',
            method='POST',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='BatchCreateSubNetworkInterfaceResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def create_security_group_async(self, request):
        """创建安全组

        创建安全组

        :param CreateSecurityGroupRequest request
        :return: CreateSecurityGroupResponse
        """
        return self.create_security_group_with_http_info(request)

    def create_security_group_with_http_info(self, request):
        """创建安全组

        创建安全组

        :param CreateSecurityGroupRequest request
        :return: CreateSecurityGroupResponse
        """

        all_params = ['create_security_group_request_body']
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
            resource_path='/v3/{project_id}/vpc/security-groups',
            method='POST',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='CreateSecurityGroupResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def create_security_group_rule_async(self, request):
        """创建安全组规则

        创建安全组规则

        :param CreateSecurityGroupRuleRequest request
        :return: CreateSecurityGroupRuleResponse
        """
        return self.create_security_group_rule_with_http_info(request)

    def create_security_group_rule_with_http_info(self, request):
        """创建安全组规则

        创建安全组规则

        :param CreateSecurityGroupRuleRequest request
        :return: CreateSecurityGroupRuleResponse
        """

        all_params = ['create_security_group_rule_request_body']
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
            resource_path='/v3/{project_id}/vpc/security-group-rules',
            method='POST',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='CreateSecurityGroupRuleResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def create_sub_network_interface_async(self, request):
        """创建辅助弹性网卡

        创建辅助弹性网卡

        :param CreateSubNetworkInterfaceRequest request
        :return: CreateSubNetworkInterfaceResponse
        """
        return self.create_sub_network_interface_with_http_info(request)

    def create_sub_network_interface_with_http_info(self, request):
        """创建辅助弹性网卡

        创建辅助弹性网卡

        :param CreateSubNetworkInterfaceRequest request
        :return: CreateSubNetworkInterfaceResponse
        """

        all_params = ['create_sub_network_interface_request_body']
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
            resource_path='/v3/{project_id}/vpc/sub-network-interfaces',
            method='POST',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='CreateSubNetworkInterfaceResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def delete_security_group_async(self, request):
        """删除安全组

        删除安全组

        :param DeleteSecurityGroupRequest request
        :return: DeleteSecurityGroupResponse
        """
        return self.delete_security_group_with_http_info(request)

    def delete_security_group_with_http_info(self, request):
        """删除安全组

        删除安全组

        :param DeleteSecurityGroupRequest request
        :return: DeleteSecurityGroupResponse
        """

        all_params = ['security_group_id']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'security_group_id' in local_var_params:
            path_params['security_group_id'] = local_var_params['security_group_id']

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
            resource_path='/v3/{project_id}/vpc/security-groups/{security_group_id}',
            method='DELETE',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='DeleteSecurityGroupResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def delete_security_group_rule_async(self, request):
        """删除安全组规则

        删除安全组规则

        :param DeleteSecurityGroupRuleRequest request
        :return: DeleteSecurityGroupRuleResponse
        """
        return self.delete_security_group_rule_with_http_info(request)

    def delete_security_group_rule_with_http_info(self, request):
        """删除安全组规则

        删除安全组规则

        :param DeleteSecurityGroupRuleRequest request
        :return: DeleteSecurityGroupRuleResponse
        """

        all_params = ['security_group_rule_id']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'security_group_rule_id' in local_var_params:
            path_params['security_group_rule_id'] = local_var_params['security_group_rule_id']

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
            resource_path='/v3/{project_id}/vpc/security-group-rules/{security_group_rule_id}',
            method='DELETE',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='DeleteSecurityGroupRuleResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def delete_sub_network_interface_async(self, request):
        """删除辅助弹性网卡

        删除辅助弹性网卡

        :param DeleteSubNetworkInterfaceRequest request
        :return: DeleteSubNetworkInterfaceResponse
        """
        return self.delete_sub_network_interface_with_http_info(request)

    def delete_sub_network_interface_with_http_info(self, request):
        """删除辅助弹性网卡

        删除辅助弹性网卡

        :param DeleteSubNetworkInterfaceRequest request
        :return: DeleteSubNetworkInterfaceResponse
        """

        all_params = ['sub_network_interface_id']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'sub_network_interface_id' in local_var_params:
            path_params['sub_network_interface_id'] = local_var_params['sub_network_interface_id']

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
            resource_path='/v3/{project_id}/vpc/sub-network-interfaces/{sub_network_interface_id}',
            method='DELETE',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='DeleteSubNetworkInterfaceResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def list_security_group_rules_async(self, request):
        """查询安全组规则列表

        查询安全组规则列表

        :param ListSecurityGroupRulesRequest request
        :return: ListSecurityGroupRulesResponse
        """
        return self.list_security_group_rules_with_http_info(request)

    def list_security_group_rules_with_http_info(self, request):
        """查询安全组规则列表

        查询安全组规则列表

        :param ListSecurityGroupRulesRequest request
        :return: ListSecurityGroupRulesResponse
        """

        all_params = ['limit', 'marker', 'id', 'security_group_id', 'protocol', 'description', 'remote_group_id', 'direction', 'action']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'limit' in local_var_params:
            query_params.append(('limit', local_var_params['limit']))
        if 'marker' in local_var_params:
            query_params.append(('marker', local_var_params['marker']))
        if 'id' in local_var_params:
            query_params.append(('id', local_var_params['id']))
            collection_formats['id'] = 'multi'
        if 'security_group_id' in local_var_params:
            query_params.append(('security_group_id', local_var_params['security_group_id']))
            collection_formats['security_group_id'] = 'multi'
        if 'protocol' in local_var_params:
            query_params.append(('protocol', local_var_params['protocol']))
            collection_formats['protocol'] = 'multi'
        if 'description' in local_var_params:
            query_params.append(('description', local_var_params['description']))
            collection_formats['description'] = 'multi'
        if 'remote_group_id' in local_var_params:
            query_params.append(('remote_group_id', local_var_params['remote_group_id']))
            collection_formats['remote_group_id'] = 'multi'
        if 'direction' in local_var_params:
            query_params.append(('direction', local_var_params['direction']))
        if 'action' in local_var_params:
            query_params.append(('action', local_var_params['action']))

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
            resource_path='/v3/{project_id}/vpc/security-group-rules',
            method='GET',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ListSecurityGroupRulesResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def list_security_groups_async(self, request):
        """查询安全组列表

        查询某租户下的安全组列表

        :param ListSecurityGroupsRequest request
        :return: ListSecurityGroupsResponse
        """
        return self.list_security_groups_with_http_info(request)

    def list_security_groups_with_http_info(self, request):
        """查询安全组列表

        查询某租户下的安全组列表

        :param ListSecurityGroupsRequest request
        :return: ListSecurityGroupsResponse
        """

        all_params = ['limit', 'marker', 'id', 'name', 'description', 'enterprise_project_id']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'limit' in local_var_params:
            query_params.append(('limit', local_var_params['limit']))
        if 'marker' in local_var_params:
            query_params.append(('marker', local_var_params['marker']))
        if 'id' in local_var_params:
            query_params.append(('id', local_var_params['id']))
            collection_formats['id'] = 'multi'
        if 'name' in local_var_params:
            query_params.append(('name', local_var_params['name']))
            collection_formats['name'] = 'multi'
        if 'description' in local_var_params:
            query_params.append(('description', local_var_params['description']))
            collection_formats['description'] = 'multi'
        if 'enterprise_project_id' in local_var_params:
            query_params.append(('enterprise_project_id', local_var_params['enterprise_project_id']))

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
            resource_path='/v3/{project_id}/vpc/security-groups',
            method='GET',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ListSecurityGroupsResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def list_sub_network_interfaces_async(self, request):
        """查询租户下辅助弹性网卡列表

        查询辅助弹性网卡列表，单次查询最多返回2000条数据

        :param ListSubNetworkInterfacesRequest request
        :return: ListSubNetworkInterfacesResponse
        """
        return self.list_sub_network_interfaces_with_http_info(request)

    def list_sub_network_interfaces_with_http_info(self, request):
        """查询租户下辅助弹性网卡列表

        查询辅助弹性网卡列表，单次查询最多返回2000条数据

        :param ListSubNetworkInterfacesRequest request
        :return: ListSubNetworkInterfacesResponse
        """

        all_params = ['limit', 'marker', 'id', 'virsubnet_id', 'private_ip_address', 'mac_address', 'vpc_id', 'description', 'parent_id']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'limit' in local_var_params:
            query_params.append(('limit', local_var_params['limit']))
        if 'marker' in local_var_params:
            query_params.append(('marker', local_var_params['marker']))
        if 'id' in local_var_params:
            query_params.append(('id', local_var_params['id']))
            collection_formats['id'] = 'multi'
        if 'virsubnet_id' in local_var_params:
            query_params.append(('virsubnet_id', local_var_params['virsubnet_id']))
            collection_formats['virsubnet_id'] = 'multi'
        if 'private_ip_address' in local_var_params:
            query_params.append(('private_ip_address', local_var_params['private_ip_address']))
            collection_formats['private_ip_address'] = 'multi'
        if 'mac_address' in local_var_params:
            query_params.append(('mac_address', local_var_params['mac_address']))
            collection_formats['mac_address'] = 'multi'
        if 'vpc_id' in local_var_params:
            query_params.append(('vpc_id', local_var_params['vpc_id']))
            collection_formats['vpc_id'] = 'multi'
        if 'description' in local_var_params:
            query_params.append(('description', local_var_params['description']))
            collection_formats['description'] = 'multi'
        if 'parent_id' in local_var_params:
            query_params.append(('parent_id', local_var_params['parent_id']))
            collection_formats['parent_id'] = 'multi'

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
            resource_path='/v3/{project_id}/vpc/sub-network-interfaces',
            method='GET',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ListSubNetworkInterfacesResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def migrate_sub_network_interface_async(self, request):
        """迁移辅助弹性网卡

        批量迁移辅助弹性网卡

        :param MigrateSubNetworkInterfaceRequest request
        :return: MigrateSubNetworkInterfaceResponse
        """
        return self.migrate_sub_network_interface_with_http_info(request)

    def migrate_sub_network_interface_with_http_info(self, request):
        """迁移辅助弹性网卡

        批量迁移辅助弹性网卡

        :param MigrateSubNetworkInterfaceRequest request
        :return: MigrateSubNetworkInterfaceResponse
        """

        all_params = ['migrate_sub_network_interface_request_body']
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
            resource_path='/v3/{project_id}/vpc/sub-network-interfaces/migrate',
            method='PUT',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='MigrateSubNetworkInterfaceResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def show_security_group_async(self, request):
        """查询安全组

        查询单个安全组详情

        :param ShowSecurityGroupRequest request
        :return: ShowSecurityGroupResponse
        """
        return self.show_security_group_with_http_info(request)

    def show_security_group_with_http_info(self, request):
        """查询安全组

        查询单个安全组详情

        :param ShowSecurityGroupRequest request
        :return: ShowSecurityGroupResponse
        """

        all_params = ['security_group_id']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'security_group_id' in local_var_params:
            path_params['security_group_id'] = local_var_params['security_group_id']

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
            resource_path='/v3/{project_id}/vpc/security-groups/{security_group_id}',
            method='GET',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ShowSecurityGroupResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def show_security_group_rule_async(self, request):
        """查询安全组规则

        查询单个安全组规则

        :param ShowSecurityGroupRuleRequest request
        :return: ShowSecurityGroupRuleResponse
        """
        return self.show_security_group_rule_with_http_info(request)

    def show_security_group_rule_with_http_info(self, request):
        """查询安全组规则

        查询单个安全组规则

        :param ShowSecurityGroupRuleRequest request
        :return: ShowSecurityGroupRuleResponse
        """

        all_params = ['security_group_rule_id']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'security_group_rule_id' in local_var_params:
            path_params['security_group_rule_id'] = local_var_params['security_group_rule_id']

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
            resource_path='/v3/{project_id}/vpc/security-group-rules/{security_group_rule_id}',
            method='GET',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ShowSecurityGroupRuleResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def show_sub_network_interface_async(self, request):
        """查询租户下辅助弹性网卡

        查询辅助弹性网卡详情

        :param ShowSubNetworkInterfaceRequest request
        :return: ShowSubNetworkInterfaceResponse
        """
        return self.show_sub_network_interface_with_http_info(request)

    def show_sub_network_interface_with_http_info(self, request):
        """查询租户下辅助弹性网卡

        查询辅助弹性网卡详情

        :param ShowSubNetworkInterfaceRequest request
        :return: ShowSubNetworkInterfaceResponse
        """

        all_params = ['sub_network_interface_id']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'sub_network_interface_id' in local_var_params:
            path_params['sub_network_interface_id'] = local_var_params['sub_network_interface_id']

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
            resource_path='/v3/{project_id}/vpc/sub-network-interfaces/{sub_network_interface_id}',
            method='GET',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ShowSubNetworkInterfaceResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def show_sub_network_interfaces_quantity_async(self, request):
        """查询租户下辅助弹性网卡数目

        查询辅助弹性网卡数目

        :param ShowSubNetworkInterfacesQuantityRequest request
        :return: ShowSubNetworkInterfacesQuantityResponse
        """
        return self.show_sub_network_interfaces_quantity_with_http_info(request)

    def show_sub_network_interfaces_quantity_with_http_info(self, request):
        """查询租户下辅助弹性网卡数目

        查询辅助弹性网卡数目

        :param ShowSubNetworkInterfacesQuantityRequest request
        :return: ShowSubNetworkInterfacesQuantityResponse
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
            resource_path='/v3/{project_id}/vpc/sub-network-interfaces/count',
            method='GET',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ShowSubNetworkInterfacesQuantityResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def update_security_group_async(self, request):
        """更新安全组

        更新安全组

        :param UpdateSecurityGroupRequest request
        :return: UpdateSecurityGroupResponse
        """
        return self.update_security_group_with_http_info(request)

    def update_security_group_with_http_info(self, request):
        """更新安全组

        更新安全组

        :param UpdateSecurityGroupRequest request
        :return: UpdateSecurityGroupResponse
        """

        all_params = ['security_group_id', 'update_security_group_request_body']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'security_group_id' in local_var_params:
            path_params['security_group_id'] = local_var_params['security_group_id']

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
            resource_path='/v3/{project_id}/vpc/security-groups/{security_group_id}',
            method='PUT',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='UpdateSecurityGroupResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def update_sub_network_interface_async(self, request):
        """更新辅助弹性网卡

        更新辅助弹性网卡

        :param UpdateSubNetworkInterfaceRequest request
        :return: UpdateSubNetworkInterfaceResponse
        """
        return self.update_sub_network_interface_with_http_info(request)

    def update_sub_network_interface_with_http_info(self, request):
        """更新辅助弹性网卡

        更新辅助弹性网卡

        :param UpdateSubNetworkInterfaceRequest request
        :return: UpdateSubNetworkInterfaceResponse
        """

        all_params = ['sub_network_interface_id', 'update_sub_network_interface_request_body']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'sub_network_interface_id' in local_var_params:
            path_params['sub_network_interface_id'] = local_var_params['sub_network_interface_id']

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
            resource_path='/v3/{project_id}/vpc/sub-network-interfaces/{sub_network_interface_id}',
            method='PUT',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='UpdateSubNetworkInterfaceResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def create_address_group_async(self, request):
        """创建地址组

        创建地址组

        :param CreateAddressGroupRequest request
        :return: CreateAddressGroupResponse
        """
        return self.create_address_group_with_http_info(request)

    def create_address_group_with_http_info(self, request):
        """创建地址组

        创建地址组

        :param CreateAddressGroupRequest request
        :return: CreateAddressGroupResponse
        """

        all_params = ['create_address_group_request_body']
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
            resource_path='/v3/{project_id}/vpc/address-groups',
            method='POST',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='CreateAddressGroupResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def delete_address_group_async(self, request):
        """删除地址组

        删除地址组，非强制删除，删除前请确保未被其他资源引用

        :param DeleteAddressGroupRequest request
        :return: DeleteAddressGroupResponse
        """
        return self.delete_address_group_with_http_info(request)

    def delete_address_group_with_http_info(self, request):
        """删除地址组

        删除地址组，非强制删除，删除前请确保未被其他资源引用

        :param DeleteAddressGroupRequest request
        :return: DeleteAddressGroupResponse
        """

        all_params = ['address_group_id']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'address_group_id' in local_var_params:
            path_params['address_group_id'] = local_var_params['address_group_id']

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
            resource_path='/v3/{project_id}/vpc/address-groups/{address_group_id}',
            method='DELETE',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='DeleteAddressGroupResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def delete_ip_address_group_force_async(self, request):
        """强制删除地址组

        强制删除地址组，删除的地址组与安全组规则关联时，会删除地址组与关联的安全组规则。

        :param DeleteIpAddressGroupForceRequest request
        :return: DeleteIpAddressGroupForceResponse
        """
        return self.delete_ip_address_group_force_with_http_info(request)

    def delete_ip_address_group_force_with_http_info(self, request):
        """强制删除地址组

        强制删除地址组，删除的地址组与安全组规则关联时，会删除地址组与关联的安全组规则。

        :param DeleteIpAddressGroupForceRequest request
        :return: DeleteIpAddressGroupForceResponse
        """

        all_params = ['address_group_id']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'address_group_id' in local_var_params:
            path_params['address_group_id'] = local_var_params['address_group_id']

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
            resource_path='/v3/{project_id}/vpc/address-groups/{address_group_id}/force',
            method='DELETE',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='DeleteIpAddressGroupForceResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def list_address_group_async(self, request):
        """查询地址组列表

        查询地址组列表，根据过滤条件进行过滤。

        :param ListAddressGroupRequest request
        :return: ListAddressGroupResponse
        """
        return self.list_address_group_with_http_info(request)

    def list_address_group_with_http_info(self, request):
        """查询地址组列表

        查询地址组列表，根据过滤条件进行过滤。

        :param ListAddressGroupRequest request
        :return: ListAddressGroupResponse
        """

        all_params = ['limit', 'marker', 'id', 'name', 'ip_version', 'description']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'limit' in local_var_params:
            query_params.append(('limit', local_var_params['limit']))
        if 'marker' in local_var_params:
            query_params.append(('marker', local_var_params['marker']))
        if 'id' in local_var_params:
            query_params.append(('id', local_var_params['id']))
            collection_formats['id'] = 'multi'
        if 'name' in local_var_params:
            query_params.append(('name', local_var_params['name']))
            collection_formats['name'] = 'multi'
        if 'ip_version' in local_var_params:
            query_params.append(('ip_version', local_var_params['ip_version']))
        if 'description' in local_var_params:
            query_params.append(('description', local_var_params['description']))
            collection_formats['description'] = 'multi'

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
            resource_path='/v3/{project_id}/vpc/address-groups',
            method='GET',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ListAddressGroupResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def show_address_group_async(self, request):
        """查询地址组

        查询地址组详情。

        :param ShowAddressGroupRequest request
        :return: ShowAddressGroupResponse
        """
        return self.show_address_group_with_http_info(request)

    def show_address_group_with_http_info(self, request):
        """查询地址组

        查询地址组详情。

        :param ShowAddressGroupRequest request
        :return: ShowAddressGroupResponse
        """

        all_params = ['address_group_id']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'address_group_id' in local_var_params:
            path_params['address_group_id'] = local_var_params['address_group_id']

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
            resource_path='/v3/{project_id}/vpc/address-groups/{address_group_id}',
            method='GET',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ShowAddressGroupResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def update_address_group_async(self, request):
        """更新地址组

        更新地址组。

        :param UpdateAddressGroupRequest request
        :return: UpdateAddressGroupResponse
        """
        return self.update_address_group_with_http_info(request)

    def update_address_group_with_http_info(self, request):
        """更新地址组

        更新地址组。

        :param UpdateAddressGroupRequest request
        :return: UpdateAddressGroupResponse
        """

        all_params = ['address_group_id', 'update_address_group_request_body']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'address_group_id' in local_var_params:
            path_params['address_group_id'] = local_var_params['address_group_id']

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
            resource_path='/v3/{project_id}/vpc/address-groups/{address_group_id}',
            method='PUT',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='UpdateAddressGroupResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def add_vpc_extend_cidr_async(self, request):
        """添加VPC扩展网段

        添加VPC的扩展网段

        :param AddVpcExtendCidrRequest request
        :return: AddVpcExtendCidrResponse
        """
        return self.add_vpc_extend_cidr_with_http_info(request)

    def add_vpc_extend_cidr_with_http_info(self, request):
        """添加VPC扩展网段

        添加VPC的扩展网段

        :param AddVpcExtendCidrRequest request
        :return: AddVpcExtendCidrResponse
        """

        all_params = ['vpc_id', 'add_vpc_extend_cidr_request_body']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'vpc_id' in local_var_params:
            path_params['vpc_id'] = local_var_params['vpc_id']

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
            resource_path='/v3/{project_id}/vpc/vpcs/{vpc_id}/add-extend-cidr',
            method='PUT',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='AddVpcExtendCidrResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def create_vpc_async(self, request):
        """创建VPC

        创建虚拟私有云

        :param CreateVpcRequest request
        :return: CreateVpcResponse
        """
        return self.create_vpc_with_http_info(request)

    def create_vpc_with_http_info(self, request):
        """创建VPC

        创建虚拟私有云

        :param CreateVpcRequest request
        :return: CreateVpcResponse
        """

        all_params = ['create_vpc_request_body']
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
            resource_path='/v3/{project_id}/vpc/vpcs',
            method='POST',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='CreateVpcResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def delete_vpc_async(self, request):
        """删除VPC

        删除VPC

        :param DeleteVpcRequest request
        :return: DeleteVpcResponse
        """
        return self.delete_vpc_with_http_info(request)

    def delete_vpc_with_http_info(self, request):
        """删除VPC

        删除VPC

        :param DeleteVpcRequest request
        :return: DeleteVpcResponse
        """

        all_params = ['vpc_id']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'vpc_id' in local_var_params:
            path_params['vpc_id'] = local_var_params['vpc_id']

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
            resource_path='/v3/{project_id}/vpc/vpcs/{vpc_id}',
            method='DELETE',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='DeleteVpcResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def list_vpcs_async(self, request):
        """查询VPC列表

        查询vpc列表

        :param ListVpcsRequest request
        :return: ListVpcsResponse
        """
        return self.list_vpcs_with_http_info(request)

    def list_vpcs_with_http_info(self, request):
        """查询VPC列表

        查询vpc列表

        :param ListVpcsRequest request
        :return: ListVpcsResponse
        """

        all_params = ['limit', 'marker', 'id', 'name', 'description', 'cidr']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'limit' in local_var_params:
            query_params.append(('limit', local_var_params['limit']))
        if 'marker' in local_var_params:
            query_params.append(('marker', local_var_params['marker']))
        if 'id' in local_var_params:
            query_params.append(('id', local_var_params['id']))
            collection_formats['id'] = 'multi'
        if 'name' in local_var_params:
            query_params.append(('name', local_var_params['name']))
            collection_formats['name'] = 'multi'
        if 'description' in local_var_params:
            query_params.append(('description', local_var_params['description']))
            collection_formats['description'] = 'multi'
        if 'cidr' in local_var_params:
            query_params.append(('cidr', local_var_params['cidr']))
            collection_formats['cidr'] = 'multi'

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
            resource_path='/v3/{project_id}/vpc/vpcs',
            method='GET',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ListVpcsResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def remove_vpc_extend_cidr_async(self, request):
        """移除VPC扩展网段

        移除VPC扩展网段

        :param RemoveVpcExtendCidrRequest request
        :return: RemoveVpcExtendCidrResponse
        """
        return self.remove_vpc_extend_cidr_with_http_info(request)

    def remove_vpc_extend_cidr_with_http_info(self, request):
        """移除VPC扩展网段

        移除VPC扩展网段

        :param RemoveVpcExtendCidrRequest request
        :return: RemoveVpcExtendCidrResponse
        """

        all_params = ['vpc_id', 'remove_vpc_extend_cidr_request_body']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'vpc_id' in local_var_params:
            path_params['vpc_id'] = local_var_params['vpc_id']

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
            resource_path='/v3/{project_id}/vpc/vpcs/{vpc_id}/remove-extend-cidr',
            method='PUT',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='RemoveVpcExtendCidrResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def show_vpc_async(self, request):
        """查询VPC详情

        查询vpc详情

        :param ShowVpcRequest request
        :return: ShowVpcResponse
        """
        return self.show_vpc_with_http_info(request)

    def show_vpc_with_http_info(self, request):
        """查询VPC详情

        查询vpc详情

        :param ShowVpcRequest request
        :return: ShowVpcResponse
        """

        all_params = ['vpc_id']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'vpc_id' in local_var_params:
            path_params['vpc_id'] = local_var_params['vpc_id']

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
            resource_path='/v3/{project_id}/vpc/vpcs/{vpc_id}',
            method='GET',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ShowVpcResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def update_vpc_async(self, request):
        """更新VPC

        更新vpc

        :param UpdateVpcRequest request
        :return: UpdateVpcResponse
        """
        return self.update_vpc_with_http_info(request)

    def update_vpc_with_http_info(self, request):
        """更新VPC

        更新vpc

        :param UpdateVpcRequest request
        :return: UpdateVpcResponse
        """

        all_params = ['vpc_id', 'update_vpc_request_body']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'vpc_id' in local_var_params:
            path_params['vpc_id'] = local_var_params['vpc_id']

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
            resource_path='/v3/{project_id}/vpc/vpcs/{vpc_id}',
            method='PUT',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='UpdateVpcResponse',
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
