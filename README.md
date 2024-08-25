# Fofa-hack

![Fofa-hack](./images/logo.png)

简体中文 | [English](./docs/EN_README.md)


### 简介

PS: 感谢[FOFA](https://fofa.info/)提供这么好的测绘工具

非付费会员,fofa数据采集工具

使用示例
> fofa-hack.exe --keyword thinkphp --endcount 500


### 安装

下载 fofa-hack [releases](https://github.com/Cl0udG0d/Fofa-hack/releases) 最新版本

### 运行

运行`fofa-hack.exe` , `-k`或`--keyword` 参数传入搜索关键字

更多参数查看 `--help`

> fofa-hack.exe --help

```shell
Fofa-hack>python fofa.py -h

             ____  ____  ____  ____      
            | ===|/ () \| ===|/ () \     
            |__|  \____/|__| /__/\__\    
                 _   _   ____   ____  __  __ 
                | |_| | / () \ / (__`|  |/  /
                |_| |_|/__/\__\\____)|__|\__\ V2.5.1

                公众号: 黑糖安全
            
usage: fofa.py [-h] (--keyword KEYWORD | --inputfile INPUTFILE | --base BASE | --iconurl ICONURL | --iconfile ICONFILE) [--timesleep TIMESLEEP] [--timeout TIMEOUT] [--endcount ENDCOUNT] [--level LEVEL]
               [--output OUTPUT] [--outputname OUTPUTNAME] [--fuzz] [--proxy-type {socks4,socks5,http}] [--authorization AUTHORIZATION] [--authorization-file AUTHORIZATION_FILE] [--fofa-key FOFA_KEY]
               [--proxy PROXY | --proxy-url PROXY_URL | --proxy-file PROXY_FILE]

Fofa-hack v2.5.1 使用说明

optional arguments:
  -h, --help            show this help message and exit
  --keyword KEYWORD, -k KEYWORD
                        fofa搜索关键字
  --inputfile INPUTFILE, -i INPUTFILE
                        指定文件,从文件中批量读取fofa语法
  --base BASE, -b BASE  以base64的形式输入关键字 -b InRoaW5rcGhwIg==
  --iconurl ICONURL     指定url的icon作为icon_hash关键字
  --iconfile ICONFILE   指定icon_file作为icon_hash关键字
  --timesleep TIMESLEEP, -t TIMESLEEP
                        爬取每一页等待秒数,防止IP被Ban,默认为3
  --timeout TIMEOUT, -to TIMEOUT
                        爬取每一页的超时时间,默认为180秒
  --endcount ENDCOUNT, -e ENDCOUNT
                        爬取结束数量
  --level LEVEL, -l LEVEL
                        爬取等级: 1-3 ,数字越大内容越详细,默认为 1
  --output OUTPUT, -o OUTPUT
                        输出格式:txt、json,默认为txt
  --outputname OUTPUTNAME, -on OUTPUTNAME
                        指定输出文件名，默认文件名为 fofaHack
  --fuzz, -f            关键字fuzz参数,增加内容获取粒度
  --proxy-type {socks4,socks5,http}
                        代理类型,默认为http
  --authorization AUTHORIZATION
                        指定Authorization值
  --authorization-file AUTHORIZATION_FILE
                        从文件中读取authorization列表 --authorization-file authorization.txt
  --fofa-key FOFA_KEY   fofa api key值(配合fofa终身会员使用)
  --proxy PROXY         指定代理,代理格式 --proxy '127.0.0.1:7890'
  --proxy-url PROXY_URL
                        指定代理url，即访问URL响应为proxy,代理格式 --proxy-url http://127.0.0.1/proxy_pool/get
  --proxy-file PROXY_FILE
                        指定txt格式的代理文件,按行分割,代理格式 --proxy-file proxy.txt

```

爬取的去重结果会存储到`final_fofaHack.txt`文件中

### API

也可以使用api调用

`pip install fofa-hack`

```python
from fofa_hack import fofa
def main():
    result_generator = fofa.api("thinkphp", endcount=100)
    for data in result_generator:
        print(data)

if __name__ == '__main__':
    main()
```

### 搜索语法
一些搜索的示例

+ 搜索 thinkphp 1000条数据
> fofa.exe -k thinkphp -e 1000

+ 搜索有连接符的关键字(注意单双引号)
> fofa.exe -k "index && country='CN'"

+ 高级语法搜索(本来我以为高级语法用不了,但是最近好像又解禁了)
> fofa.exe -k icon_hash="1165838194"

+ 欢迎补充....

### 测试

使用命令 

> fofa-hack.exe --keyword thinkphp --endcount 500

爬取五百条数据轻轻松松

### 赞赏列表

详情请见[SPONSOR](docs/SPONSOR.md)

### 使用问题集合

详情请见[ISSUES](https://github.com/Cl0udG0d/Fofa-hack/issues)

### 更新日志

详情请见[CHANGELOG](docs/CHANGELOG.md)

### TODO List

详情请见[TODO](docs/TODO.md)

### 贡献者

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
<td align="center">
        <a href="https://github.com/fireinrain">
            <img src="https://avatars.githubusercontent.com/u/14249262?v=4" width="100;" alt="fireinrain"/>
            <br />
            <sub><b>10cks</b></sub>
        </a>
    </td>
</tr>
</table>
