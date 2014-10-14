.. |Build Status| image:: https://travis-ci.org/rkashapov/yandex-translator.svg?branch=master
   :target: https://travis-ci.org/rkashapov/yandex-translator
.. |Coverage Status| image:: https://coveralls.io/repos/rkashapov/yandex-translator/badge.png?branch=master
   :target: https://coveralls.io/r/rkashapov/yandex-translator?branch=master


Yandex translator |Build Status| |Coverage Status|
==================================================

Unofficial python client to `Yandex translator API`_.

.. _Yandex translator API: http://translate.yandex.com/

Javascript client written by `Emmanuel Odeke`_ for node.js you can find `here`_.

.. _here: https://github.com/odeke-em/ytrans.js
.. _Emmanuel Odeke: https://github.com/odeke-em/

Installation
------------

* Note: it runs on python versions >= 2.7:

  ``pip install ytrans``

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
