import unittest


from qcloud_sdk.utils.crcmod import calculate_file_crc64
from qcloud_sdk.config import settings


class FileCrc64TestCase(unittest.TestCase):
    def test_calculate_file_crc64(self):
        crc64 = calculate_file_crc64(settings.COS_TEST_OBJECT_RAW_FILE_PATH)
        print(crc64)


if __name__ == '__main__':
    unittest.main()
