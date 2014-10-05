# coding: utf-8
#!/usr/bin/env python
"""
Неофициальный клиент для translate.yandex.ru

Документация к API: 
http://api.yandex.ru/translate/doc/dg/concepts/About.xml
"""
import os
import re
import json

try:
    # Py3
    from urllib.parse import urlencode, urljoin
    from urllib.request import urlopen
except ImportError:
    # Py2
    from urlparse import urljoin
    from urllib2 import urlopen
    from urllib import urlencode


# Переменная окружения, указывающая на файл с ключем
KEY_ENVIRON_VARIABLE = "YANDEX_TRANSLATOR_KEY"

# URL переводчика
URL = "https://translate.yandex.net/api/v1.5/tr.json/"

PLAIN = 'plain'
HTML = 'html'

OK = 200

reSpaceCompile = re.compile('\s', re.UNICODE)


class APIException(Exception):
    """
    Base class for all API Exceptions
    """
    message = None

    def __init__(self):
        assert self.message is not None
        super(APIException, self).__init__(self.message)


class BadKeyError(APIException):
    message = u"Неправильные ключ API"


class KeyBlockedError(APIException):
    message = u"Ключ API заблокирован"


class TriesLimitError(APIException):
    message = u"Превышено суточное ограничение на количество запросов"


class TextLimitError(APIException):
    message = u"Превышено суточное ограничение на объем переведенного текста"


class TextLengthLimitError(APIException):
    message = u"Превышен максимально допустимый размер текста"


class CantTranslateError(APIException):
    message = u"Текст не может быть переведен"


class NotSupportedError(APIException):
    message = u"Заданное направление перевода не поддерживается"


# code -> exception mapping
exception_map = {
    401: BadKeyError,
    402: KeyBlockedError,
    403: TriesLimitError,
    404: TextLimitError,
    413: TextLengthLimitError,
    422: CantTranslateError,
    501: NotSupportedError
}


def throw(code):
    """
    Throws exception with code ``code``

    :param int code: Error code
    """
    assert code in exception_map
    raise exception_map[code]


def check_existance_and_permissions(path_to_check, permissions=os.R_OK):
    """
    проверяет нужные разрешения и бросает исключение,
     если нет доступа к файлу

    :param str path_to_check: путь в файловой системе
    :param int permissions: права доступа, например: os.R_OK|os.X_OK
    :return: нет
    """
    if not (path_to_check and os.path.isfile(path_to_check)):
        raise Exception(
            u"{0} должен быть допустимым обычным файлом!".format(path_to_check))

    elif not os.access(path_to_check, permissions):
        raise Exception(u"Нет доступа к файлу! {0}!".format(path_to_check))


def get_environ_key_path():
    assert KEY_ENVIRON_VARIABLE in os.environ, (
        u"Не установлена переменная окружения "
        u"{0}".format(KEY_ENVIRON_VARIABLE))

    return os.environ[KEY_ENVIRON_VARIABLE]


class YTranslator(object):
    def __init__(self, key_path=None, api_key=None):
        self.__API_KEY = None
        if api_key:
            self.init_key(api_key)
        else:
            self.init_key_from_path(key_path)
    
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

        data = urlencode(kwargs).encode('utf-8')
        if joined_per_line:
            data += bytes('&' + joined_per_line, encoding='utf-8')

        response = urlopen(urljoin(URL, method), data=data)
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
        response = self.__call_api(
            "translate", text=text, text_collection=text_collection, lang=lang, format=format
        )

        return response["text"]

    def translate_file(self, lang, file_path):
        check_existance_and_permissions(file_path)
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
        self.init_key(self.__read_key(path_to_key))

    def __read_key(self, path_to_key=None):
        """
        Считывает ключ из файла, на который указывает ``KEY_ENVIRON_VARIABLE``
        """
        if not path_to_key: 
            path_to_key = get_environ_key_path()

        check_existance_and_permissions(path_to_key, permissions=os.R_OK)

        value = None
        with open(path_to_key, "rt") as f:
            for line in f.readlines():
                line = line.strip().replace(" ", "").rsplit("=", 1)
                if len(line) == 2:
                    key, value = line
                    if key.lower() == "key":
                        break
            else:
                raise Exception(u"Ключ не найден!")
        return value


if __name__ == "__main__":
    def is_valid_file(parser, file_path):
        try:
            check_existance_and_permissions(file_path)
        except Exception as e:
            parser.error(str(e).encode('utf-8'))
        return file_path

    def get_args_parser():
        import argparse
        parser = argparse.ArgumentParser(description="Yandex translator")
        parser.add_argument("--lang", '-l', dest='lang', default='none', help='Translation direction')
        parser.add_argument("--available-languages", "-a", dest='available', action='store_true',
                            help="Show available languages")
        parser.add_argument("text", nargs='*', metavar='text', help='Text for translation')
        return parser

    ytrans = YTranslator()
    parser = get_args_parser()
    args = parser.parse_args()
    show_available_languages = args.available
    if show_available_languages:
        print("Languages available : {0}".format(", ".join(ytrans.get_langs())))
        exit()

    lang = args.lang
    text = " ".join(args.text)

    if not text:
        print("Text is required!")
        parser.print_help()
        exit()

    if lang == "none":
        text_lang = ytrans.detect(text=text[:100])
        if text_lang != "ru":
            lang = "ru"
        else:
            lang = "en"

    print(" ".join(ytrans.translate(lang=lang, text=text)))
