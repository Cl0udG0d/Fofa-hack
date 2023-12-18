import base64
import urllib
from urllib.parse import quote_plus

from fofa_hack import fofa
from fofa_hack.fofa import api


def main():
    print(f"quote_plus : {quote_plus('/')} , urllib.parse.quote : {urllib.parse.quote('/')}")

if __name__ == '__main__':
    main()