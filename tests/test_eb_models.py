import unittest

from qcloud_sdk.config import settings
from qcloud_sdk.scf.models import QCloudScfResource, QCloudScfEvent


class TestDataMixin(object):
    def setUp(self):
        self.resource_raw = {
            'namespace': settings.SCF_DEFAULT_NAMESPACE,
            'function_name': settings.SCF_TEST_FUNCTION_NAME,
        }
        self.resource = QCloudScfResource(**self.resource_raw)
        self.event_raw = {
            'type': '',
            'subject': self.resource.to_string(),
            'data': {'task_id': '1'},
        }


class CloudEventTestCase(TestDataMixin, unittest.TestCase):
    def test_init(self):
        event = QCloudScfEvent(**self.event_raw)

    def test_to_dict(self):
        event = QCloudScfEvent(**self.event_raw)
        event_for_api = event.to_dict()


if __name__ == '__main__':
    unittest.main()
