#!/usr/bin/python3

# Author: Emmanuel Odeke <odeke@ualberta.ca>
# Number counter v1.0

AND_STR = "and"
INVALID_KEY ="invalid"
TEN       = 10
HUNDRED   = 100
THOUSAND  = 1000
MILLION   = 1000000
BILLION   = 1000000000
TRILLION  = 1000000000000

singleDigits={
    0:"zero", 1:"one", 2:"two", 3:"three", 4:"four",
	5:"five", 6:"six", 7:"seven", 8:"eight", 9:"nine"
}

teens={
    10:"ten", 11:"eleven",12:"twelve",13:"thirteen",14:"fourteen",
    15:"fifteen", 16:"sixteen", 17:"seventeen", 18:"eighteen", 19:"nineteen"
}

tenPowers  = {
    100:"hundred",1000:"thousand",1000000:"million",
    1000000000:"billion",1000000000000:"trillion"
}

tenMultiples = {
    20: "twenty", 30:"thirty", 40:"forty", 50:"fifty",
    60:"sixty", 70: "seventy", 80:"eighty", 90:"ninety"
}

def getWordDescription(number, wordString=""):
  if (number < 20):
    if (number < 10):
      wordString += singleDigits.get(number, INVALID_KEY)
    else:
      wordString += teens.get(number, INVALID_KEY)
    return wordString 

  if (number < 100):
    remainingDig = number % 10
    if not remainingDig:
      wordString += tenMultiples.get(number, INVALID_KEY)
      return wordString
    else:
      sigDig = number // 10
      wordString += tenMultiples.get(sigDig*10, INVALID_KEY)
      return getWordDescription(number % 10, wordString)

  if (number < MILLION):
    if (number < THOUSAND):
      powerofTen = HUNDRED
    else: 
      powerofTen = THOUSAND 

    remainingDigs = number % powerofTen
    sigDig = number // powerofTen

    if (sigDig >= 10): 
      wordString += getWordDescription(sigDig)+tenPowers[powerofTen]
    else:
      wordString += singleDigits.get(sigDig)+tenPowers[powerofTen]

    if not remainingDigs:
      return wordString

    else:
      if (powerofTen == HUNDRED): wordString+=AND_STR
      return getWordDescription(remainingDigs, wordString)

  if (number < TRILLION):
    if (number < BILLION):powerofTen = MILLION
    else: powerofTen = BILLION

    remainingDigs = number % powerofTen
    sigDig = number // powerofTen
    wordString += getWordDescription(sigDig)+tenPowers[powerofTen]

    if not remainingDigs:
      return wordString
    else:
	    return getWordDescription(remainingDigs, wordString)

class NumberTranslator:
    def __init__(self):
        self.__cache = {}

    def toWords(self, query):
        wordDesc = self.__cache.get(query, None)
        if not wordDesc:
            wordDesc = getWordDescription(query)
            self.__cache[query] = wordDesc

        return wordDesc
 
def main():
    nTrans = NumberTranslator()
    for i in range(1000):
        print(nTrans.toWords(i))
    # print(getWordDescription(999999999999, ''))

if __name__ == '__main__':
  main()
