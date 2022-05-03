import unittest

from tests.client import APIClientTestCase


class TmtAPITestCase(APIClientTestCase):
    def test_translate_text(self):
        translated_text = self.client.translate_text(source_text='高校学生和职场新人的第二课堂', source_language='zh', target_language='en')
        self.assertEqual(translated_text, "The second classroom for college students and workplace newcomers")


if __name__ == '__main__':
    unittest.main()
