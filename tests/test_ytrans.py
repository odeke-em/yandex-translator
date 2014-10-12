# coding: utf-8
import os
import stat
import unittest
from ytrans.utils import to_unicode

import ytrans

key = "trnsl.1.1.20140731T144606Z.639639bc480e82b7.7cb97a33d3b2e88fa363e789fe03e2426478c53a"

test_dir = os.path.dirname(__file__)


class YtransTest(unittest.TestCase):
    def setUp(self):
        self.translator = ytrans.YTranslator(api_key=key)

    def test_load_api_key(self):
        os.environ['YANDEX_TRANSLATOR_KEY'] = os.path.join(test_dir, 'key')
        api_key = ytrans.read_key()
        translator = ytrans.YTranslator(api_key)
        translator.translate("en", "Загружен ключ API")
        del os.environ['YANDEX_TRANSLATOR_KEY']

    def test_key_file_not_exists(self):
        self.assertRaises(IOError, ytrans.read_key, 'not exists')

    def test_key_not_found(self):
        import tempfile
        from ytrans.exceptions import KeyNotFound
        with tempfile.NamedTemporaryFile() as f:
            self.assertRaises(KeyNotFound, ytrans.read_key, f.name)

        with tempfile.NamedTemporaryFile(mode='w') as f:
            os.chmod(f.name, 000)
            self.assertRaises(IOError, ytrans.read_key, f.name)

    def test_ytrans_get_langs_direction(self):
        langs = self.translator.get_translation_directions()
        self.assertIn('en-ru', langs)
        self.assertIn('ru-en', langs)

    def test_ytrans_get_langs(self):
        self.assertEqual(self.translator.get_langs(ui='ru')['ru'], to_unicode("Русский"))

    def test_ytrans_detect(self):
        self.assertEqual('en', self.translator.detect("Hello, Word!"))
        self.assertEqual('ru', self.translator.detect("Привет, Мир!"))

    def test_is_valid_lang(self):
        self.assertFalse(self.translator.is_valid_lang('none'))
        self.assertTrue(self.translator.is_valid_lang('en'))
        self.assertFalse(self.translator.is_valid_lang(None))
        self.assertFalse(self.translator.is_valid_lang('none'))

    def test_get_supported_translations(self):
        self.assertIn('ru', self.translator.get_supported_translations('en'))
        self.assertIn('en', self.translator.get_supported_translations('ru'))
        self.assertEqual(self.translator.get_supported_translations('none'), [])

    def test_get_supported_primaries(self):
        self.assertIn('en', self.translator.get_supported_primaries())

    def test_translate_plain_str(self):
        self.assertEqual("Hello World", self.translator.translate("en", "Привет Мир"))
        self.assertEqual(["Hi", "World"], self.translator.translate("en", text_collection=["Привет", "Мир"]))
        self.assertRaises(AssertionError, self.translator.translate, "ru", text="One", text_collection=["Two"])

    def test_translate_plain_unicode(self):
        self.assertEqual("Hello World", self.translator.translate("en", to_unicode("Привет Мир")))
        self.assertEqual(["Hi", "World"], self.translator.translate("en", text_collection=[
            to_unicode("Привет"), to_unicode("Мир")]))
        self.assertRaises(AssertionError, self.translator.translate, "ru", text="One", text_collection=["Two"])

    def test_translate_html(self):
        en_html = to_unicode("<html><head><title>My Site</title></head></html>")
        ru_html = to_unicode("<html><head><title>Мой Сайт</title></head></html>")
        self.assertEqual(ru_html, self.translator.translate("ru", text=en_html, format=ytrans.HTML))

    def test_translate_from_file(self):
        file_path = os.path.join(test_dir, 'text.txt')
        translated = self.translator.translate_file('ru', file_path)
        with open(file_path) as f:
            lines_count = len(f.readlines())
        self.assertIn(to_unicode("Красивое лучше, чем уродливое. "), translated)
        self.assertEqual(len(translated), lines_count)


if __name__ == '__main__':
    unittest.main()
