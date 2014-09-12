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
    for i in range(0, 1000):
        strRepr = ntrans.toWords(i)
        print("i: %d English: %s Ru: %s"%(
            i, strRepr, ytrans.translate(lang='ru', text=strRepr)
        ))

if __name__ == '__main__':
    main()
