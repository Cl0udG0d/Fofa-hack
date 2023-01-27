# Fofa-hack

### 简介

基于[fofa_spider-1.0.5](https://github.com/FightingForWhat/fofa_spider-1.0.5) - 非付费会员，fofa数据无限抓取版 的梅开二度，配置普通用户cookie即可使用

截止至 `2023-1-27` 日 ，亲测可用，如果项目不行了欢迎联系我



### 使用

```shell
git clone https://github.com/Cl0udG0d/Fofa-hack
```

安装运行所需的库文件，国内请加源 https://pypi.tuna.tsinghua.edu.cn/simple

```shell
pip install -r requirements.txt
```

配置`config.py`中的
+ fofa_username = ""
+ fofa_password = ""

也就是你的FOFA账号密码(老版本的直接复制cookie的方式弃用)

运行`fofa.py`

> python3 fofa.py

爬取的结果会存储到`spider_result.txt`文件中



### 测试

输入 搜索关键字 `app="ThinkPHP"`，等待秒数为5的情况下，下载1-50页数据经过测试无问题，经过自动去重之后剩余497条



### 更新日志

只记录比较重要的更新

+ 2023-1-27，合入[wanswu](https://github.com/wanswu)师傅提交的代码，通过账号密码进行登录

+ 2022-12-19，添加cookie的预判断

+ 2022-11-12，更新爬取规则

+ 2022-9-17，修改时间戳获取规则，项目整体趋于稳定

+ 2022-9-15，创建项目并修改适用于目前fofa的规则


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

建了一个微信的安全交流群，欢迎添加我微信备注`进群`，一起来聊天吹水哇，以及一个会发布安全相关内容的公众号，欢迎关注 :)

<div>
    <img  alt="GIF" src="https://springbird.oss-cn-beijing.aliyuncs.com/img/mmqrcode1632325540724.png"  width="280px" />
    <img  alt="GIF" src="https://springbird.oss-cn-beijing.aliyuncs.com/img/qrcode_for_gh_cead8e1080d6_344.jpg"  width="280px" />
</div>
