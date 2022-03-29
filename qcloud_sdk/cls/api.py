# -*- coding: utf-8 -*-

from typing import Union

from qcloud_sdk.config import settings


class ClsAPIMixin(object):
    def request_cls_api(self, action, params, region=None, api_region=None):
        region = region or settings.CLS_DEFAULT_REGION or settings.DEFAULT_REGION
        return self.request_api(service='cls', action=action, params=params, region=region,
                                api_version='2020-10-16', api_region=api_region)

    def search_log(self, topic_id: str, timestamp_from: Union[str, int], timestamp_to: Union[str, int], query: str,
                   limit=None, context=None, sort=None, use_new_analysis=None, **kwargs):
        """
        https://cloud.tencent.com/document/product/614/56447

        :return:
        """
        limit = limit or 1000
        params = {
            'TopicId': topic_id,
            'From': timestamp_from,
            'To': timestamp_to,
            'Query': query,
            'Limit': limit,
            'Context': context,
            'Sort': sort,
            'UseNewAnalysis': use_new_analysis,
        }
        return self.request_cls_api(action='SearchLog', params=params, **kwargs)

    def search_all_log(self, topic_id: str, timestamp_from: Union[str, int], timestamp_to: Union[str, int], query: str,
                       limit=None, context=None, sort=None, use_new_analysis=None, **kwargs):
        # TODO: 返回所有日志
        return self.search_log(topic_id, timestamp_from, timestamp_to, query, sort, use_new_analysis, **kwargs)
