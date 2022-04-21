import unittest
import os

from qcloud_sdk.utils.hashlib import calculate_file_md5
from qcloud_sdk.config import settings


class FileMd5TestCase(unittest.TestCase):
    def test_calculate_file_md5(self):
        md5_str = calculate_file_md5(settings.COS_TEST_OBJECT_RAW_FILE_PATH)


if __name__ == '__main__':
    unittest.main()
