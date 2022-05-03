# -*- coding: utf-8 -*-

from qcloud_sdk.config import settings


class TmtAPIMixin(object):
    def request_tmt_api(self, action, params, region=None):
        region = region or settings.TMT_DEFAULT_REGION or settings.DEFAULT_REGION
        if not region:
            raise ValueError('地域不可为空')
        return self.request_api(service='tmt', action=action, params=params, api_version='2018-03-21',
                                region=region)

    def translate_text(self, source_text, source_language, target_language,
                       project_id=0, untranslated_text='', region=None) -> str:
        params = {
            'SourceText': source_text,
            'Source': source_language,
            'Target': target_language,
            'ProjectId': project_id,
            'UntranslatedText': untranslated_text,
        }
        return self.request_tmt_api(action='TextTranslate', params=params, region=region)['TargetText']
