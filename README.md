# Fofa-hack

### 简介

非付费会员，fofa数据无限抓取版 , 配置FoFa普通用户账号密码即可使用

在当前的Fofa机制下,普通用户本月最多只能获取3000条数据,等待`Fofa-hack`的`1.4.0`版本更新吧

使用示例
> python fofa.py --username fofa_hack_test --password Test123456 -k app="ThinkPHP" -t 5
### 安装

```shell
git clone https://github.com/Cl0udG0d/Fofa-hack
```

安装运行所需的库文件，国内请加源 https://pypi.tuna.tsinghua.edu.cn/simple

```shell
pip install -r requirements.txt
```

### 配置
有三种方式配置登录账号

#### 1.运行传值
传入`--username` 和 `--password` 参数
> Fofa-hack>python fofa.py --username fofa_hack_test --password Test123

#### 2.配置config.py
配置`config.py`中的`fofa_account`，支持多账号
```json
fofa_account=[
    {
        "fofa_username" : "test@email.com",
        "fofa_password" : "12345678"
    },
  {
        "fofa_username" : "test1@email.com",
        "fofa_password" : "12345678"
    }
]
```

也就是你的FOFA账号密码

#### 3.配置fofa_cookie.txt文件
将下图中的cookie直接复制到`fofa_cookie.txt`文件里,这样在启动的时候Fofa-hack就会识别到并且直接使用cookie爬取了

注意不是`Authorization`

`cookie`的位置如下
  ![](https://github.com/Cl0udG0d/Fofa-script/blob/master/images/2.png)

### 运行

运行`fofa.py` , `-k`或`--keyword` 参数传入搜索关键字

更多参数查看 `--help`

> python3 fofa.py --help

```shell
Fofa-hack>python fofa.py --help                                         

         ____  ____  ____  ____                 
        | ===|/ () \| ===|/ () \                
        |__|  \____/|__| /__/\__\               
             _   _   ____   ____  __  __        
            | |_| | / () \ / (__`|  |/  /       
            |_| |_|/__/\__\\____)|__|\__\ V1.3.0
                                                
usage: fofa.py [-h] [--timesleep TIMESLEEP] --keyword KEYWORD                 
               [--username USERNAME] [--password PASSWORD] [--endpage ENDPAGE]
               [--level LEVEL]                                                

Fofa-hack v1.3.0 使用说明

optional arguments:
  -h, --help            show this help message and exit
  --timesleep TIMESLEEP, -t TIMESLEEP
                        爬取每一页等待秒数,防止IP被Ban,默认为3
  --keyword KEYWORD, -k KEYWORD
                        fofa搜索关键字,默认为test
  --username USERNAME, -u USERNAME
                        fofa用户名
  --password PASSWORD, -p PASSWORD
                        fofa密码
  --endpage ENDPAGE, -e ENDPAGE
                        爬取结束页码
  --level LEVEL, -l LEVEL
                        爬取等级: 1-3 ,数字越大内容越详细,默认为 1
```

爬取的结果会存储到`md5(搜索关键字)_运行时间戳.txt`文件中

### 测试

输入 搜索关键字 `app="ThinkPHP"`，等待秒数为5的情况下，下载1-50页数据经过测试无问题，经过自动去重之后剩余497条

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
<details>
<summary>TODO</summary>
<table >
  <tr>
    <td>名称</td>
    <td>简介</td>
  </tr>
<tr>
    <td>支持代理池</td>
    <td>使用代理池的方式防止FOFA断开连接</td>
  </tr>
<tr>
    <td>支持多种导出格式</td>
    <td>支持json、txt、excel等方式导出结果</td>
  </tr>
<tr>
    <td>编写图形化界面</td>
    <td>生成可执行文件运行</td>
  </tr>
<tr>
    <td>增加程序稳定性</td>
    <td>防止程序因为各种情况运行失败或者被ban的情况</td>
  </tr>
<tr>
    <td>内容去重</td>
    <td>去除重复的url信息</td>
  </tr>
</table>
</details>

### 贡献者

<!-- readme: collaborators,contributors -start -->
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
    </td></tr>
</table>
<!-- readme: collaborators,contributors -end -->

### END 

网络乞丐在线乞讨
<div>
    <img  alt="PNG" src="./images/sponsor.png"  width="280px" />
</div>

建了一个微信的安全交流群，欢迎添加我微信备注`进群`，一起来聊天吹水哇，以及一个会发布安全相关内容的公众号，欢迎关注 :)

<div>
    <img  alt="GIF" src="https://springbird.oss-cn-beijing.aliyuncs.com/img/mmqrcode1632325540724.png"  width="280px" />
    <img  alt="GIF" src="https://springbird.oss-cn-beijing.aliyuncs.com/img/qrcode_for_gh_cead8e1080d6_344.jpg"  width="280px" />
</div>
