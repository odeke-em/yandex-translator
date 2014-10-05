# coding: utf-8
import os
import unittest

import ytrans

key = "trnsl.1.1.20140731T144606Z.639639bc480e82b7.7cb97a33d3b2e88fa363e789fe03e2426478c53a"

test_dir = os.path.dirname(__file__)


class YtransTest(unittest.TestCase):
    def setUp(self):
        self.translator = ytrans.YTranslator(api_key=key)

    def test_ytrans_get_langs(self):
        langs = self.translator.get_langs()
        self.assertIn('en-ru', langs)
        self.assertIn('ru-en', langs)

    def test_ytrans_detect(self):
        self.assertEqual('en', self.translator.detect("Hello, Word!"))
        self.assertEqual('ru', self.translator.detect("Привет, Мир!"))

    def test_is_valid_lang(self):
        self.assertFalse(self.translator.is_valid_lang('none'))
        self.assertTrue(self.translator.is_valid_lang('en'))

    def test_get_supported_translations(self):
        self.assertIn('ru', self.translator.get_supported_translations('en'))
        self.assertIn('en', self.translator.get_supported_translations('ru'))

    def test_translate_plain(self):
        self.assertEqual("Hello World", self.translator.translate("en", "Привет Мир"))
        self.assertEqual(["Hi", "World"], self.translator.translate("en", text_collection=["Привет", "Мир"]))

        self.assertRaises(AssertionError, self.translator.translate, "ru", text=u"One", text_collection=["Two"])

    def test_translate_html(self):
        en_html = "<html><head><title>My Site</title></head></html>"
        ru_html = u"<html><head><title>Мой Сайт</title></head></html>"
        self.assertEqual(ru_html, self.translator.translate("ru", text=en_html, format=ytrans.HTML))

    def test_translate_from_file(self):
        file_path = os.path.join(test_dir, 'text.txt')
        translated = self.translator.translate_file('ru', file_path)
        with open(file_path) as f:
            lines_count = len(f.readlines())
        self.assertIn(u"Красивое лучше, чем уродливое. ", translated)
        self.assertEqual(len(translated), lines_count)


if __name__ == '__main__':
    unittest.main()
