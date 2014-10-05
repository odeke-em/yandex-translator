yandex-translator [![Build Status](https://travis-ci.org/rkashapov/yandex-translator.svg?branch=master)](https://travis-ci.org/rkashapov/yandex-translator)
=================

Unofficial client to [Yandex translator API](http://translate.yandex.ru/)


Installation
------------
* Note: it runs on python versions from 2.7 to 3.X:
  
  ``python setup.py install`` # To use the default variable python

  OR

  ``python2.7 setup.py install`` # For a Python2.7 install

  OR

   ``python3 setup.py install`` # For a Python3 install

Settings
---------
+ To use this package, you need access to the Yandex translation service via an API key.

  * You can get your key here:

   ``http://api.yandex.ru/key/form.xml?service=trnsl``

+ With your API key, create a file and in it set your API key in this format:

  ``key=<API_KEY>``

+ To finish off, set the environment variable YANDEX_TRANSLATOR_KEY,

  that contains the path to this file. Do this in your shell, .bash_profile or .bash_rc file:

   ``export YANDEX_TRANSLATOR_KEY=path_to_key``

Usage
-----
This package provides a cli tool as well as an interactive translator.

* Cli tool usage:

  ``ytranslate.py -h``

* Interactive translator:

  ``ytrans-interactive.py``
