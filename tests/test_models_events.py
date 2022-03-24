import unittest

from qcloud_sdk.config import settings
from qcloud_sdk.models.events import QCloudEvent, QCloudEventList
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


class QCloudEventTestCase(TestDataMixin, unittest.TestCase):
    def test_init(self):
        event = QCloudScfEvent(**self.event_raw)

    def test_to_api_params(self):
        event = QCloudScfEvent(**self.event_raw)
        event_api_params_format = event.to_api_params()


class QCloudEventListTestCase(TestDataMixin, unittest.TestCase):
    def test_init(self):
        event = QCloudScfEvent(**self.event_raw)
        event_list = QCloudEventList([event])

    def test_to_api_params(self):
        event = QCloudScfEvent(**self.event_raw)
        event_list = QCloudEventList([event])
        event_list.to_api_params()


if __name__ == '__main__':
    unittest.main()
