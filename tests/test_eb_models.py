import unittest

from qcloud_sdk.config import settings
from qcloud_sdk.scf.models import ScfResource
from qcloud_sdk.eb.models import CloudEvent


class TestDataMixin(object):
    def setUp(self):
        self.resource_raw = {
            'region': 'ap-shanghai',
            'account': f'uin/{settings.UIN}',
            'namespace': settings.SCF_DEFAULT_NAMESPACE,
            'function_name': settings.SCF_TEST_FUNCTION_NAME,
        }
        self.resource = ScfResource(**self.resource_raw)
        self.event_raw = {
            'source': 'scf.cloud.tencent',
            'type': '',
            'subject': self.resource.to_string(),
            'data': {'task_id': '1'},
        }


class CloudEventTestCase(TestDataMixin, unittest.TestCase):
    def test_init(self):
        event = CloudEvent(**self.event_raw)

    def test_to_dict(self):
        event = CloudEvent(**self.event_raw)
        event_for_api = event.to_dict()
        print(event_for_api)


if __name__ == '__main__':
    unittest.main()
