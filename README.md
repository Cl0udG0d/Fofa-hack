# Fofa-hack

![Fofa-hack](./images/logo.png)

### 简介

非付费会员,fofa数据无限抓取版,一整个返璞归真

`-f` 参数开启关键字fuzz

使用示例
> python fofa.py --keyword thinkphp --endcount 100 -f
### 安装

```shell
git clone https://github.com/Cl0udG0d/Fofa-hack
```

安装运行所需的库文件，国内请加源 https://pypi.tuna.tsinghua.edu.cn/simple

```shell
pip install -r requirements.txt
```

### 配置

无需账号直接使用

### 运行

运行`fofa.py` , `-k`或`--keyword` 参数传入搜索关键字

更多参数查看 `--help`

> python3 fofa.py --help

```shell
Fofa-hack>python fofa.py -h

         ____  ____  ____  ____      
        | ===|/ () \| ===|/ () \     
        |__|  \____/|__| /__/\__\    
             _   _   ____   ____  __  __ 
            | |_| | / () \ / (__`|  |/  /
            |_| |_|/__/\__\\____)|__|\__\ V2.1.7
        
usage: fofa.py [-h] [--timesleep TIMESLEEP] [--timeout TIMEOUT] --keyword KEYWORD [--endcount ENDCOUNT] [--level LEVEL] [--output OUTPUT] [--fuzz]

Fofa-hack v2.1.9 使用说明

optional arguments:
  -h, --help            show this help message and exit
  --timesleep TIMESLEEP, -t TIMESLEEP
                        爬取每一页等待秒数,防止IP被Ban,默认为3
  --timeout TIMEOUT, -to TIMEOUT
                        爬取每一页的超时时间
  --keyword KEYWORD, -k KEYWORD
                        fofa搜索关键字,默认为test
  --endcount ENDCOUNT, -e ENDCOUNT
                        爬取结束数量
  --level LEVEL, -l LEVEL
                        爬取等级: 1-3 ,数字越大内容越详细,默认为 1
  --output OUTPUT, -o OUTPUT
                        输出格式:txt、json,默认为txt
  --fuzz, -f            关键字fuzz参数,增加内容获取粒度
```

爬取的去重结果会存储到`final_md5(搜索关键字)_运行时间戳.txt`文件中

### 测试

使用命令 

> python fofa.py --keyword thinkphp --endcount 100

爬取一百条数据轻轻松松

### 赞赏列表

详情请见[SPONSOR](docs/SPONSOR.md)

### 使用问题集合

详情请见[QUESTIONS](docs/QUESTIONS.md)

+ [ERROR: Could not build wheels for opencv-python-headless, which is required to install pyproject.toml-based projects](docs/QUESTIONS.md#opencv-python错误)
+ [ddddocr错误解决](docs/QUESTIONS.md#ddddocr错误解决)
+ [FOFA综合语法使用](docs/QUESTIONS.md#FOFA综合语法使用)

### 更新日志

详情请见[CHANGELOG](docs/CHANGELOG.md)

### TODO List

详情请见[CHANGELOG](docs/TODO.md)

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
</tr>
</table>

### END 

网络乞丐在线乞讨
<div>
    <img  alt="PNG" src="./images/sponsor.png"  width="280px" />
</div>

建了一个微信的安全交流群，欢迎添加我微信备注`进群`，一起来聊天吹水哇，以及一个会发布安全相关内容的公众号，欢迎关注 :)

<div>
    <img  alt="JPG" src="https://springbird3.oss-cn-chengdu.aliyuncs.com/lianxiang/1a1f7894a170bec207e61bf86a01592.jpg"  width="280px" />
    <img  alt="JPG" src="https://springbird3.oss-cn-chengdu.aliyuncs.com/lianxiang/qrcode_for_gh_cead8e1080d6_430.jpg"  width="280px" />
</div>
