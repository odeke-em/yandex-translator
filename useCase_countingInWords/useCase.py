#!/usr/bin/env python3

import sys
sys.path.append('..')

from numberRecon import NumberTranslator
from translate import YTranslator

def main():
    ytrans = YTranslator()
    ntrans = NumberTranslator()

    # Let's learn to count in Russian till 100
    engL = []
    for i in range(100):
        strRepr = ntrans.toWords(i)
        engL.append(strRepr)

    # Translate multiple words in one fetch
    print(ytrans.translate(lang='ru', text_collection=engL))

    # Translate this file to German
    print('\n'.join(ytrans.translate_file(lang='de', file_path=__file__)))

    # What does it look like in Spanish?
    print('\n'.join(ytrans.translate_file(lang='es', file_path=__file__)))

if __name__ == '__main__':
    main()
