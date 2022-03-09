"""
腾讯云事件总线（EB）云API
"""

from typing import Optional

# 服务可选地域
EB_SERVICE_REGIONS = ['ap-beijing', 'ap-chengdu', 'ap-chongqing', 'ap-guangzhou', 'ap-hongkong',
                      'ap-shanghai', 'ap-singapore', 'eu-moscow', 'na-siliconvalley']
EB_SERVICE_REGIONS_DOC = 'https://cloud.tencent.com/document/product/1359/67707#.E5.9C.B0.E5.9F.9F.E5.88.97.E8.A1.A8'


class EbAPIMixin(object):
    def request_eb_api(self, action, region, params, api_region=None):
        # TODO: 允许环境变量或Django声明式配置传入默认地域。
        return self.request_api(service='sms', action=action, params=params, api_version='2021-04-16',
                                api_region=api_region, service_region=region,
                                supported_service_regions=EB_SERVICE_REGIONS,
                                supported_service_regions_doc=EB_SERVICE_REGIONS_DOC)

    # ----- 事件集 -----
    def create_event_bus(self, region: str, name: str, description: Optional[str] = None, api_region: Optional[str] = None):
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

    def put_events(self, region, event_bus_id, event_list, api_region: Optional[str] = None):
        params = {
            'EventBusId': event_bus_id,
            'EventList': event_list,
        }
        return self.request_eb_api(action='PutEvents', region=region, params=params, api_region=api_region)

    # ----- 事件目标 -----
    def create_target(self, region, event_bus_id, target_type, target_description, rule_id, api_region):
        params = {
            'EventBusId': event_bus_id,
            'Type': target_type,
            'TargetDescription': target_description,
            'RuleId': rule_id,
        }
        return self.request_eb_api(action='CreateTarget', region=region, params=params, api_region=api_region)