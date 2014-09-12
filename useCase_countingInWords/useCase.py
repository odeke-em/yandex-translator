#!/usr/bin/env python3

import sys
sys.path.append('..')

from numberRecon import NumberTranslator
from translate import YTranslator

def main():
    ytrans = YTranslator()
    ntrans = NumberTranslator()

    # Dirty hack to try out counting from 0 to 1000 in ru.
    # TODO: Send content in one request
    engL = []
    for i in range(0, 10):
        strRepr = ntrans.toWords(i)
        engL.append(strRepr)

    # Translate multiple words in one fetch
    print(ytrans.translate(lang='ru', text_collection=engL))

    # Translate this file to German
    print(ytrans.translate_file(lang='de', file_path=__file__))

    # What does it look like in Spanish?
    print(ytrans.translate_file(lang='es', file_path=__file__))

if __name__ == '__main__':
    main()
