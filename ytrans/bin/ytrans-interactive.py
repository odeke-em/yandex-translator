#!/usr/bin/env python
# coding: utf-8
# Simple interactive demo

import sys

from ytrans import YTranslator, read_key

token_trim = lambda token: token.rstrip(" ").lstrip(" ").strip("\n")


def do_show_menu(aux_message=''):
    sys.stdout.write("""
        %s
        c   -- Change the language
        d   -- Detect language
        m   -- Show this menu
        p   -- Get available primary languages
        r   -- Get available translations for a language code
        t   -- Translate content
        q   -- Exit the program
    \n"""%(aux_message))


def do_lang_listing(ytrans):
    sys.stdout.write("\n".join(ytrans.get_supported_primaries()))


def do_supported_translations_from_lang(ytrans, lang):
    text = prompt(
        pre_text="Primary language, leave blank to use '%s" % lang).strip('\n')

    if text:
        lang = text

    results = ytrans.get_supported_translations(lang)
    if not results:
        msg = "No translations supported for %s"%(lang)
    else:
        msg = "\n".join(results)
    sys.stdout.write(msg)


def do_detect_lang(ytrans):
    text = prompt(pre_text='Enter text to detect')
    sys.stdout.write(ytrans.detect(text.strip('\n')))


def set_lang(ytrans, current_lang):
    lang_in = prompt(
              "\n[Current: %s. Enter language code eg ru:$> " % current_lang)
    if lang_in:
        current_lang = token_trim(lang_in)

    if not ytrans.is_valid_lang(current_lang):
        sys.stdout.write("%s is an invalid language!"%(current_lang))
        return None

    return current_lang


def do_translate(ytrans, lang, lines):
    tokens = [token_trim(token) for token in lines if token]
    sys.stdout.write("Performing translation")
    translated = ytrans.translate(lang=lang, text_collection=tokens)
    if translated and tokens:
        sys.stdout.write("\n")
        for i, equiv in enumerate(translated):
            sys.stdout.write("%s <=> %s\n"%(tokens[i], equiv))
            sys.stdout.write("\n")


def do_translation(ytrans, dest_lang):
    sys.stdout.write("* Hit Ctrl-D to process *\nText separated by 'Enter'\n$> ")
    do_translate(ytrans, dest_lang, sys.stdin.read().split('\n'))


def do_report_invalid_opt(opt_str):
    sys.stderr.write("Invalid option: '%s'\n"%(opt_str))


def prompt(ps='$>', pre_text=''):
    sys.stdout.write('%s %s ' % (pre_text, ps)) and sys.stdout.flush()
    return sys.stdin.readline()


def main():
    api_key = read_key()
    ytrans = YTranslator(api_key)

    lang = 'ru'
    while True:
        try:
            do_show_menu("* Hit Ctrl-C to exit *. Target Language: '%s'"%(lang))
            opt_str = prompt(pre_text='Enter your option').strip('\n') or '^'
            l_opt_ch = opt_str.lower()[0]
            if l_opt_ch == 'c':
                tmp = set_lang(ytrans, lang)
                if tmp:
                    lang = tmp
                    sys.stdout.write("Language set to '%s'\n"%(lang))
            elif l_opt_ch == 'd':
                do_detect_lang(ytrans)
            elif l_opt_ch == 'p':
                do_lang_listing(ytrans)
            elif l_opt_ch == 'r':
                do_supported_translations_from_lang(ytrans, lang)
            elif l_opt_ch == 'm':
                continue
            elif l_opt_ch == 't':
                do_translation(ytrans, lang)
            elif l_opt_ch == 'q':
                break
            else:
                do_report_invalid_opt(opt_str)

        except KeyboardInterrupt:
            break
        except Exception as e:
            sys.stderr.write('%s\n'%(e))
            sys.stderr.flush()
        
    sys.stdout.write("\nBye\n")

if __name__ == "__main__":
    main()
