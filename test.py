from fofa_hack import fofa
from fofa_hack.fofa import api


def main():
    result_generator = api("thinkphp", endcount=100)
    for data in result_generator:
        print(data)

if __name__ == '__main__':
    main()