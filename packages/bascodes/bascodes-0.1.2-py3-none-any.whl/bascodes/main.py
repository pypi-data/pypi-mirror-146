#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = "0.1.2"


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


def open_webbrowser():
    try:
        import webbrowser
        webbrowser.open(BROWSER_URL)
    except:
        pass


def main(show_card=True, open_browser=True):
    if show_card:
        print(get_card())
    if open_browser:
        open_webbrowser()


if __name__ == '__main__':
    main()
