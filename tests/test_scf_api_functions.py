import unittest

from qcloud_sdk.config import settings
from tests.client import APIClientTestCase


class ScfFunctionAPITestCase(APIClientTestCase):
    @unittest.skip('参数未完成')
    def test_invoke_function(self):
        data = self.client.invoke_function(settings.TEST_SCF_FUNCTION_NAME)
        self.assertTrue(int(data['BillDuration']))


if __name__ == '__main__':
    unittest.main()
