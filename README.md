# Fofa-hack

![Fofa-hack](./images/logo.png)

### 简介

PS: 感谢FOFA提供这么好的测绘工具

非付费会员,fofa数据采集工具

`-f` 参数开启关键字fuzz

使用示例
> python fofa.py --keyword thinkphp --endcount 100
### 安装

```shell
git clone https://github.com/Cl0udG0d/Fofa-hack
```

安装运行所需的库文件，国内请加源 https://pypi.tuna.tsinghua.edu.cn/simple

```shell
pip install -r requirements.txt
```

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
            |_| |_|/__/\__\\____)|__|\__\ v2.3.1
                                                
            公众号: 黑糖安全                    
                                                
usage: fofa.py [-h] (--keyword KEYWORD | --inputfile INPUTFILE) [--timesleep TIMESLEEP] 
      [--timeout TIMEOUT] [--endcount ENDCOUNT] [--level LEVEL] [--output OUTPUT] [--fuzz] 
      [--proxy PROXY] [--type {common,selenium}]
                             
                                                                      
Fofa-hack v2.3.1 使用说明

optional arguments:
  -h, --help            show this help message and exit
  --keyword KEYWORD, -k KEYWORD
                        fofa搜索关键字
  --inputfile INPUTFILE, -i INPUTFILE
                        指定文件,从文件中批量读取fofa语法
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
  --fuzz, -f            关键字fuzz参数,增加内容获取粒度
  --proxy PROXY         指定代理，代理格式 --proxy '127.0.0.1:7890'
  --type {common,selenium}
                        运行类型,默认为普通方式
```

爬取的去重结果会存储到`final_md5(搜索关键字)_运行时间戳.txt`文件中

### 测试

使用命令 

> python fofa.py --keyword thinkphp --endcount 100

爬取一百条数据轻轻松松

### 外部调用
这部分现在还比较复杂,等有空再封装吧

~~外部调用fofa-hack,返回扫描结果的集合~~

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

添加我微信备注`进群`

|               加我拉你入群               |                                                            黑糖安全公众号                                                             |                                                          知识星球                                                          |
|:----------------------------------------------------------: |:------------------------------------------------------------------------------------------------------------------------------:|:----------------------------------------------------------------------------------------------------------------------:|
| <img src="https://springbird3.oss-cn-chengdu.aliyuncs.com/lianxiang/1a1f7894a170bec207e61bf86a01592.jpg" width="300"/> | <img src="https://springbird3.oss-cn-chengdu.aliyuncs.com/lianxiang/qrcode_for_gh_cead8e1080d6_430.jpg" width="300"/> | <img src="https://springbird3.oss-cn-chengdu.aliyuncs.com/lianxiang/f15e36e768d83c799cc6bd0f3eff2a1.png" width="300"/> |