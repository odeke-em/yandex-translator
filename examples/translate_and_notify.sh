#!/usr/bin/env bash
# Translates selected text and shows translation in system notifications area
# xsel package is required. On Ubuntu it can be installed with
#   sudo apt-get install xsel
# command.

notify-send -u critical "Translation:" "$(ytranslate.py "$(xsel -o)")"
