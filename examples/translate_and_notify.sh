#!/usr/bin/env bash
notify-send -u critical "Translation:" "$(ytranslate.py "$(xsel -o)")"
