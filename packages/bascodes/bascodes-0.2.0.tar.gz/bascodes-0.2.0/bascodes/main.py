#!/usr/bin/env python
# -*- coding: utf-8 -*-


import argparse

__version__ = "0.2.0"


CARD_URL    = 'https://bas.surf/terminalcard'
BROWSER_URL = 'https://bas.surf/terminalcard-open'



def online():
    import urllib.request
    f = urllib.request.urlopen(CARD_URL)
    return f.read().decode('utf-8')


def offline():
    from pathlib import Path
    dir = Path(__file__).parent
    fname = dir / "output.bas"
    with open(fname) as f:
        return f.read()


def get_card():
    try:
        return online()
    except:
        pass
    try:
        return offline()
    except:
        pass


def open_webbrowser(url):
    try:
        import webbrowser
        webbrowser.open(url)
    except:
        pass


def main(show_card=True, open_browser=True):
    parser = argparse.ArgumentParser(description='Display card and Short URL')
    parser.add_argument('shurl', metavar='short-url', type=str, nargs='?',
                        help='A bas.surf short url')
    args = parser.parse_args()
    try:
        shurl = args.shurl
        assert shurl
        shurl = f"https://bas.surf/{shurl}"
    except:
        shurl = BROWSER_URL
    if show_card:
        print(get_card())
    if open_browser:
        open_webbrowser(shurl)


if __name__ == '__main__':
    main()
