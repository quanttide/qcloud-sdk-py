import unittest


from qcloud_sdk.cos.utils import calculate_file_crc64, calculate_file_md5
from qcloud_sdk.config import settings


class FileMd5TestCase(unittest.TestCase):
    def test_calculate_file_md5(self):
        md5_str = calculate_file_md5(settings.COS_TEST_OBJECT_RAW_FILE_PATH)


class FileCrc64TestCase(unittest.TestCase):
    def test_calculate_file_crc64(self):
        crc64_value = calculate_file_crc64(settings.COS_TEST_OBJECT_RAW_FILE_PATH)
        self.assertEqual(crc64_value, settings.TEST_CRC64_VALUE)


if __name__ == '__main__':
    unittest.main()
