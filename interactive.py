#!/usr/bin/env python
# Simple interactive demo

import sys

from translate import YTranslator

token_trim = lambda token: token.rstrip(" ").lstrip(" ").strip("\n")

def do_show_menu(aux_message=''):
    sys.stdout.write("""
        %s
        c   -- Change the language
        l   -- Get available languages
        m   -- Show this menu
        t   -- Translate content
    \n"""%(aux_message))

def do_lang_listing(ytrans):
    sys.stdout.write("\n".join(ytrans.get_langs()))

def get_lang(default_lang="ru"):
    sys.stdout.write("\n[Default: %s. Enter language code eg ru:$> "%(default_lang))

    lang_in = sys.stdin.readline()
    if lang_in:
        trimmed = token_trim(lang_in)
        return token_trim(lang_in)
    return default_lang

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
    sys.stdout.write('%s %s '%(pre_text, ps)) and sys.stdout.flush()
    return sys.stdin.readline()

def main():
    ytrans = YTranslator()

    lang = 'ru'
    while True:
        try:
            do_show_menu("* Hit Ctrl-C to exit *. Target Language: '%s'"%(lang))
            opt_str = prompt(pre_text='Enter your option').strip('\n') or '^'
            l_opt_ch = opt_str.lower()[0]
            if l_opt_ch == 'l':
                do_lang_listing(ytrans)
            elif l_opt_ch == 'c':
                lang = get_lang()
                sys.stdout.write("Language set to '%s'\n"%(lang))
            elif l_opt_ch == 't':
                do_translation(ytrans, lang)
            else:
                do_report_invalid_opt(opt_str)

        except KeyboardInterrupt:
            sys.stdout.write("\nBye\n")
            break
        except Exception as e:
            sys.stderr.write('%s\n'%(e))
            sys.stderr.flush()
       
if __name__ == "__main__":
    main()
