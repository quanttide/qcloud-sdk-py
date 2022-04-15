"""
腾讯云事件总线（EB）云API
"""

from typing import Optional, List

from qcloud_sdk.models.events import QCloudEvent, QCloudEventList
from qcloud_sdk.config import settings


class EbAPIMixin(object):
    def request_eb_api(self, action, params, region=None, api_region=None):
        region = region or settings.EB_DEFAULT_REGION or settings.DEFAULT_REGION
        return self.request_api(service='eb', action=action, params=params, region=region,
                                api_version='2021-04-16', api_region=api_region,
                                supported_regions=settings.EB_SUPPORTED_REGIONS,
                                supported_regions_doc=settings.EB_SUPPORTED_REGIONS_DOC)

    # ----- 事件集 -----
    def list_event_buses(self, region=None, order_by='AddTime', limit=20, order='ASC', filters=None, offset=0):
        """
        获取事件集列表，详见：https://cloud.tencent.com/document/product/1359/67683

        :param region:
        :param order_by:
        :param limit:
        :param order:
        :param filters:
        :param offset:
        :return:
        """
        # TODO: 增加对Filter的处理
        # TODO：把Python参数到云API参数转化写成通用工具函数。
        params = {
            'OrderBy': order_by,
            'Limit': limit,
            'Order': order,
            'Offset': offset,
        }
        return self.request_eb_api(action='ListEventBuses', params=params, region=None)

    def create_event_bus(self, name: str, description: Optional[str] = None, region=None, api_region: Optional[str] = None):
        """
        创建事件集，详见：https://cloud.tencent.com/document/product/1359/67686

        :param region:
        :param name: 事件集名称。只能包含字母、数字、下划线、连字符，以字母开头，以数字或字母结尾，2~60个字符。
        :param description: 事件集描述。不限字符类型，200字符描述以内。
        :param api_region:
        :return:
        """
        # 参数
        # TODO：验证参数格式，异常抛出ValueError。
        params = {
            'EventBusName': name,
            'Description': description,
        }
        return self.request_eb_api(action='CreateEventBus', params=params, region=region, api_region=api_region)

    def put_events(self, event_list: List[QCloudEvent], event_bus_id=None, region=None, api_region: Optional[str] = None):
        """
        投递事件，详见：https://cloud.tencent.com/document/product/1359/68465

        TODO: 支持直接传入原始dict格式的event。

        :param region:
        :param event_bus_id:
        :param event_list:
        :param api_region:
        :return:
        """
        if len(event_list) > 10:
            raise ValueError('投递事件API每次最多支持投递10条事件')
        params = {
            'EventBusId': event_bus_id or settings.EB_DEFAULT_EVENT_BUS_ID,
            'EventList': QCloudEventList(event_list).to_api_params(),
        }
        return self.request_eb_api(action='PutEvents', region=region, params=params, api_region=api_region)

    def put_all_events(self, event_list: List[QCloudEvent], event_bus_id=None, region=None, api_region: Optional[str] = None):
        if len(event_list) > 10:
            # 拆分成10个一组
            events_chunk = [event_list[i:i + 10] for i in range(0, len(event_list), 10)]
            # 分别运行
            return [self.put_events(events, event_bus_id, region, api_region) for events in events_chunk]
        # 正常调用
        return self.put_events(event_list, event_bus_id, region, api_region)

    def put_event(self, event: QCloudEvent, **kwargs):
        """
        （High-level API）投递单个事件。

        TODO: 支持直接传入原始dict格式的event。

        :param event:
        :param kwargs:
        :return:
        """
        return self.put_events(event_list=[event], **kwargs)

    # ----- 事件规则 -----
    def create_event_rule(self, rule_name: str, event_bus_id=None, enable=True, description=None, **kwargs):
        """

        :param rule_name:
        :param event_bus_id:
        :param enable:
        :param description: 事件集描述，不限字符类型，200字符描述以内
        :param kwargs:
        :return:
        """
        params = {
            'EventBusId': event_bus_id or settings.EB_DEFAULT_EVENT_BUS_ID,
            "RuleName": rule_name,
            "Enable": enable,
            "Description": description,
        }
        return self.request_eb_api(action='CreateRule', params=params, **kwargs)

    # ----- 事件目标 -----
    def create_event_target(self, region, event_bus_id, target_type, target_description, rule_id, api_region):
        params = {
            'EventBusId': event_bus_id,
            'Type': target_type,
            'TargetDescription': target_description,
            'RuleId': rule_id,
        }
        return self.request_eb_api(action='CreateTarget', region=region, params=params, api_region=api_region)

    # ----- 事件连接器 -----
    def create_event_connection(self):
        return self.request_eb_api(action='CreateConnection',)
