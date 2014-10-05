# coding: utf-8
import os

# Переменная окружения, указывающая на файл с ключем
KEY_ENVIRON_VARIABLE = "YANDEX_TRANSLATOR_KEY"

# URL переводчика
URL = "https://translate.yandex.net/api/v1.5/tr.json/"


def _get_environ_key_path():
    assert KEY_ENVIRON_VARIABLE in os.environ, (
        u"Не установлена переменная окружения "
        u"{0}".format(KEY_ENVIRON_VARIABLE))

    return os.environ[KEY_ENVIRON_VARIABLE]


def read_key(path_to_key):
    """
    Считывает ключ из файла, на который указывает ``KEY_ENVIRON_VARIABLE``
    """
    from ytrans.utils import check_existance_and_permissions
    if not path_to_key:
        path_to_key = _get_environ_key_path()

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
