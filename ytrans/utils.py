# coding: utf-8
import os
import sys

try:
    # Py3
    from urllib.parse import urlencode, urljoin
    from urllib.request import urlopen
except ImportError:
    # Py2
    from urlparse import urljoin
    from urllib2 import urlopen
    from urllib import urlencode

if sys.version_info.major >= 3:
    bytefy_kwargs = {'encoding': 'utf-8'}
else:
    bytefy_kwargs = {}


_bytes = bytes


def bytes(value):
    return _bytes(value, **bytefy_kwargs)


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


def is_valid_file(parser, file_path):
    try:
        check_existance_and_permissions(file_path)
    except Exception as e:
        parser.error(str(e).encode('utf-8'))
    return file_path


def request(method, data=None):
    from ytrans.settings import URL
    return urlopen(urljoin(URL, method), data=data)
