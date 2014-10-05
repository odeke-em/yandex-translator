# coding: utf-8


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
