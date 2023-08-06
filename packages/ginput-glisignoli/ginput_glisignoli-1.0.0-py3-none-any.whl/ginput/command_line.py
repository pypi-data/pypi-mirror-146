import sys
import logging
import pyperclip
import argparse
from ginput.ginput import ginput

def main():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    key_string = str

    if sys.stdin.isatty():
        parser = argparse.ArgumentParser(description='Type a string to virtual input device')
        parser.add_argument('-s', '--string', help='The string to send to the virtual input device', required=False)
        parser.add_argument('-c', '--clipboard', help='Use contents of the clipboard', action='store_true')
        args = parser.parse_args()
        
        if args.string is None and args.clipboard is False:
            parser.print_help()
            sys.exit(1)

        if args.clipboard:
            try:
                key_string = pyperclip.paste()
            except UnicodeDecodeError:
                logging.error('Clipboard contains non-ascii characters')
                sys.exit(1)

        else:
            try:
                key_string = args.string
            except UnicodeDecodeError:
                logging.error('String contains non-ascii characters')
                sys.exit(1)

    if not sys.stdin.isatty():
        key_string = ""
        for l in sys.stdin:
            key_string += str(l)

    while True:
        if len(key_string) < 1:
            logging.error("No string provided")
            sys.exit(1)
        if key_string[-1] == '\n':
            key_string = key_string[:-1]
        else:
            break

    g_main = ginput()
    if g_main._setup(key_string):
        g_main.send_string(key_string)

if __name__ == '__main__':
    main()
