.. |Build Status| image:: https://travis-ci.org/rkashapov/yandex-translator.svg?branch=master
   :target: https://travis-ci.org/rkashapov/yandex-translator
.. |Coverage Status| image:: https://coveralls.io/repos/rkashapov/yandex-translator/badge.png?branch=master
   :target: https://coveralls.io/r/rkashapov/yandex-translator?branch=master


Yandex translator |Build Status| |Coverage Status|
==================================================

Unofficial client to `Yandex translator API`_

.. _Yandex translator API: http://translate.yandex.com/

Installation
------------

* Note: it runs on python versions from 2.7 to 3.X:

  ``python setup.py install``  To use the default installation

  ``python2.7 setup.py install`` For a Python2.7 install

  ``python3 setup.py install``  For a Python3 install

Settings
--------
+ To use this package, you need access to the Yandex translation service via an API key.

  * You can get your key here: `GET API Key`_

  .. _GET API Key: http://api.yandex.com/key/form.xml?service=trnsl


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
