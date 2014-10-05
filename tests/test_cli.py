# coding: utf-8
import os
import sys
import unittest


test_dir = os.path.dirname(__file__)


class TestCli(unittest.TestCase):
    def setUp(self):
        project_dir = os.path.dirname(os.path.dirname(__file__))
        bin_dir = os.path.join(os.path.join(project_dir, 'ytrans'), 'bin')
        sys.path.insert(0, bin_dir)
        os.environ['PATH'] = "{0}:{1}".format(os.environ['PATH'], bin_dir)
        os.environ['YANDEX_TRANSLATOR_KEY'] = os.path.join(test_dir, 'key')

    def test_get_languages(self):
        with os.popen('ytranslate.py -a') as resut:
            result = resut.read()

        self.assertIn("Languages available", result)
        self.assertIn("ru-en", result)

    def test_translate_without_lang(self):
        with os.popen('ytranslate.py Hello') as result:
            result = result.read()

        self.assertEqual("Привет", result.strip())
        with os.popen(u'ytranslate.py Привет') as result:
            result = result.read()
        self.assertEqual("Hi", result.strip())

    def test_translate_with_lang(self):
        with os.popen('ytranslate.py -l de Good morning') as result:
            result = result.read()
        self.assertEqual("Guten morgen", result.strip())


if __name__ == '__main__':
    unittest.main()