# Fofa-hack

![Fofa-hack](../images/logo.png)

[简体中文](../README.md) | English
### summary

PS: Thanks to [FOFA](https://fofa.info/) for such a great cyberspace mapping tool!

Non-paying members,fofa data collection tool

`-f` this parameter turns on the keyword fuzz

getting Started
> fofa-hack.exe --keyword thinkphp --endcount 500
### mounting

download the latest version of fofa-hack [releases](https://github.com/Cl0udG0d/Fofa-hack/releases)

### movement

run `fofa-hack.exe` , `-k` or `--keyword` parameter pass in search keywords

more parameters to view `--help`

> fofa-hack.exe --help

```shell
Fofa-hack>fofa_hack-hack.exe --help

             ____  ____  ____  ____
            | ===|/ () \| ===|/ () \
            |__|  \____/|__| /__/\__\
                 _   _   ____   ____  __  __
                | |_| | / () \ / (__`|  |/  /
                |_| |_|/__/\__\\____)|__|\__\ V2.4.3

                公众号: 2.4.3

usage: fofa_hack-hack.exe [-h] (--keyword KEYWORD | --inputfile INPUTFILE) [--timesleep TIMESLEEP] [--timeout TIMEOUT]
                     [--endcount ENDCOUNT] [--level LEVEL] [--output OUTPUT] [--fuzz] [--proxy PROXY] [--type {common,selenium}]

Fofa-hack v2.4.3 Usage Notes

optional arguments:
  -h, --help            show this help message and exit
  --keyword KEYWORD, -k KEYWORD
                        fofa搜索关键字
  --inputfile INPUTFILE, -i INPUTFILE
                        指定文件,从文件中批量读取fofa语法
  --base BASE, -b BASE Input keyword as base64 -b InRoaW5rcGhwIg==
  --timesleep TIMESLEEP, -t TIMESLEEP
                        爬取每一页等待秒数,防止IP被Ban,默认为3
  --timeout TIMEOUT, -to TIMEOUT
                        爬取每一页的超时时间
  --endcount ENDCOUNT, -e ENDCOUNT
                        爬取结束数量
  --level LEVEL, -l LEVEL
                        爬取等级: 1-3 ,数字越大内容越详细,默认为 1
  --output OUTPUT, -o OUTPUT
                        输出格式:txt、json,默认为txt
  --outputname OUTPUT, -on OUTPUTNAME
                        指定输出文件名，默认为fofaHack
  --fuzz, -f            关键字fuzz参数,增加内容获取粒度
  --proxy PROXY         指定代理，代理格式 --proxy '127.0.0.1:7890'
```

crawled de-duplication results are stored in the `final_md5(search_keyword)_runtimestamp.txt` file

### Search syntax
Some search examples
+ Search for Thinkphp 1000 pieces of data
> fofa.exe -k thinkphp -e 1000
+ Search for keywords with connectors (note single and double quotes)
> fofa.exe -k "index && country='CN'"
+ Advanced grammar search (I thought advanced grammar wouldn't work, but it seems to have been lifted recently)
> fofa.exe -k icon_hash="1165838194"
+ Welcome to add

### test

using commands

> fofa-hack.exe --keyword thinkphp --endcount 500

capturing 500 pieces of data is easy

### appreciation List

for more information, please see [SPONSOR](docs/SPONSOR.md)

### using the problem set

for more information, please see [QUESTIONS](docs/QUESTIONS.md)

+ [ERROR: Could not build wheels for opencv-python-headless, which is required to install pyproject.toml-based projects](docs/QUESTIONS.md#opencv-python错误)
+ [ddddocr错误解决](docs/QUESTIONS.md#ddddocr错误解决)
+ [FOFA综合语法使用](docs/QUESTIONS.md#FOFA综合语法使用)

### update Log

for more information, please see [CHANGELOG](docs/CHANGELOG.md)

### TODO List

for more information, please see [CHANGELOG](docs/TODO.md)

### benefactor

<table>
<tr>
    <td align="center">
        <a href="https://github.com/Cl0udG0d">
            <img src="https://avatars.githubusercontent.com/u/45556496?v=4" width="100;" alt="Cl0udG0d"/>
            <br />
            <sub><b>潘一二三</b></sub>
        </a>
    </td>
    <td align="center">
        <a href="https://github.com/wanswu">
            <img src="https://avatars.githubusercontent.com/u/49047734?v=4" width="100;" alt="wanswu"/>
            <br />
            <sub><b>Wans</b></sub>
        </a>
    </td>
    <td align="center">
        <a href="https://github.com/tastypear">
            <img src="https://avatars.githubusercontent.com/u/1382667?v=4" width="100;" alt="wanswu"/>
            <br />
            <sub><b>tastypear</b></sub>
        </a>
    </td>
    <td align="center">
        <a href="https://github.com/KawaiiSh1zuku">
            <img src="https://avatars.githubusercontent.com/u/51824296?v=4" width="100;" alt="wanswu"/>
            <br />
            <sub><b>KawaiiSh1zuku</b></sub>
        </a>
    </td>
    <td align="center">
        <a href="https://github.com/Valdo-Caeserius">
            <img src="https://avatars.githubusercontent.com/u/148833225?v=4" width="100;" alt="wanswu"/>
            <br />
            <sub><b>Valdo-Caeserius</b></sub>
        </a>
    </td>
    <td align="center">
        <a href="https://github.com/10cks">
            <img src="https://avatars.githubusercontent.com/u/47177550?v=4" width="100;" alt="wanswu"/>
            <br />
            <sub><b>10cks</b></sub>
        </a>
    </td>
</tr>
</table>

### END 

add me on Wechat and say `Join the group`.

|               加我拉你入群               |                                                            黑糖安全公众号                                                             |
|:----------------------------------------------------------: |:------------------------------------------------------------------------------------------------------------------------------:|
| <img src="https://springbird3.oss-cn-chengdu.aliyuncs.com/lianxiang/1a1f7894a170bec207e61bf86a01592.jpg" width="300"/> | <img src="https://springbird3.oss-cn-chengdu.aliyuncs.com/lianxiang/qrcode_for_gh_cead8e1080d6_430.jpg" width="300"/> |