from fofa_hack import fofa
def main():
    result_generator = fofa.api("thinkphp", endcount=100)
    for data in result_generator:
        print(data)

if __name__ == '__main__':
    main()