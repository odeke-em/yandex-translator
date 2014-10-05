# coding: utf-8
"""
Неофициальный клиент для translate.yandex.ru

Документация к API:
http://api.yandex.ru/translate/doc/dg/concepts/About.xml
"""
import os
import re
import json
import collections

from ytrans.exceptions import *
from ytrans import settings
from ytrans import utils


__all__ = ["YTranslator", "APIException"]


PLAIN = 'plain'
HTML = 'html'

OK = 200

reSpaceCompile = re.compile('\s', re.UNICODE)


class YTranslator(object):
    def __init__(self, key_path=None, api_key=None):
        self.__API_KEY = None
        if api_key:
            self.init_key(api_key)
        else:
            self.init_key_from_path(key_path)

        self.__invalid_langs_map = {}
        self.__valid_langs_map = collections.defaultdict(list)

    def is_valid_lang(self, lang_str):
        if not isinstance(lang_str, str):
            return False

        lang_str = lang_str.lower()

        if lang_str in self.__invalid_langs_map:
            return False

        if lang_str in self.__valid_langs_map:  # Cache hit
            return True

        # Refresh, since after all this could be a compulsory miss
        self.__valid_langs_map = self.__get_supported_langs_map()
        if lang_str not in self.__valid_langs_map: # Black list it
            self.__invalid_langs_map[lang_str] = True
            return False

        return True

    def get_supported_translations(self, lang_str):
        if not self.is_valid_lang(lang_str):
            return []

        lower_lang_str = lang_str
        return self.__valid_langs_map[lower_lang_str][:] # No tampering with internal data

    def get_supported_primaries(self):
        if not self.__valid_langs_map:
            self.__valid_langs_map = self.__get_supported_langs_map()

        return list(self.__valid_langs_map.keys())

    def __get_supported_langs_map(self, ui=None):
        lang_list = self.get_langs(ui=ui)
        lang_map = collections.defaultdict(list)

        for from_to_str in lang_list:
            primary, rest = from_to_str.split('-')
            lang_map[primary].append(rest)

        return lang_map

    def detect(self, text):
        """
        Text language detection

        :param str text: Текст для определения языка
        :return: text written language code
        """
        response = self.__call_api("detect", text=text)
        return response["lang"]

    def __call_api(self, method, text_collection=None, **kwargs):
        """
        Вызов метода ``method``

        :param str method: Название метода API
        :return: JSON ответ
        """
        assert self.__API_KEY, u"Не считан ключ API"

        kwargs['key'] = self.__API_KEY
        joined_per_line = ''

        text_collection = text_collection or []
        if text_collection:
            kwargs.pop('text', '')
            mapped_to_text = map(
                lambda e: 'text=%s' % (reSpaceCompile.sub('+', e)),
                text_collection)
            joined_per_line = '&'.join(mapped_to_text)

        data = utils.urlencode(kwargs).encode('utf-8')
        if joined_per_line:
            data += utils.bytes('&' + joined_per_line)

        response = utils.request(method, data=data)
        response = json.loads(response.read().decode("utf-8"))
        if response.get("code", OK) != OK:
            throw(response["code"])

        return response

    def translate(self, lang, text='', text_collection=None, format=PLAIN):
        """
        Перевод текста на заданный язык.

        :param str text: Текст, который необходимо перевести
        :param collections.Iterable text_collection:
         Примітка:text_collection итерируемый, що містять рядки тексту
        :param str lang: Направление перевода.
            Может задаваться одним из следующих способов:
            * В виде пары кодов языков («с какого»-«на какой»), разделенных дефисом.
            Например, en-ru обозначает перевод с английского на русский.
            *В виде кода конечного языка (например ru).
            В этом случае сервис пытается определить исходный язык автоматически.
        :param str format: Формат текста.
            Возможны два значения:
            * plain — текст без разметки (значение по умолчанию);
            * html — текст в формате HTML.
        ** Примітка:текст і text_collection є взаємовиключними
        :return: перевод текста

        """
        text_collection = text_collection or []
        response = self.__call_api("translate", text=text,
                                   text_collection=text_collection, lang=lang, format=format)

        return response["text"]

    def translate_file(self, lang, file_path):
        utils.check_existance_and_permissions(file_path)
        with open(file_path) as f:
            results = self.translate(lang=lang, text_collection=f.readlines())
        return results

    def get_langs(self, ui=None):
        """
        Получение списка направлений перевода, поддерживаемых сервисом.

        :param str ui: Если задан, ответ будет дополнен расшифровкой кодов языков.
        Названия языков будут выведены на языке, код которого соответствует этому параметру.
        :return: список направлений перевода
        """
        params = dict()
        if ui is not None:
            params['ui'] = ui
        response = self.__call_api('getLangs', **params)
        return response["dirs"]

    def init_key(self, API_KEY):
        self.__API_KEY = API_KEY

    def init_key_from_path(self, path_to_key):
        self.init_key(settings.read_key(path_to_key))
