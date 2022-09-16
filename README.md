# Fofa-hack

### 简介

基于[fofa_spider-1.0.5](https://github.com/FightingForWhat/fofa_spider-1.0.5) - 非付费会员，fofa数据无限抓取版 的梅开二度

配置普通用户cookie即可使用

因为目前只是把原来的规则重新修改了一下，还不是很稳定，可以适当把等待时间拉长，后续会进行优化



### 使用

```shell
git clone https://github.com/Cl0udG0d/Fofa-hack
```

配置`config.py`中的`cookie`

`cookie`的位置如下
  ![](https://github.com/Cl0udG0d/Fofa-script/blob/master/images/2.png)

运行`fofa.py`

> python3 fofa.py

爬取的结果会存储到`spider_result.txt`文件中



### 原理

群友说[ [fofa_spider-1.0.5](https://github.com/FightingForWhat/fofa_spider-1.0.5) - 非付费会员，fofa数据无限抓取版 ] 这个项目的爬取规则早早失效了，原理就是通过修改搜索关键字来获取更多的数据（众所周知非会员只能查看前五页）



目前大多数Fofa爬虫都是直接调用Fofa官方给出的API接口来获取数据，非会员是用不了接口的，所以问题回归到直接在`fofa.info`上获取数据



另外一个问题就是不断修改关键字的时间戳即可



### END 

建了一个微信的安全交流群，欢迎添加我微信备注`进群`，一起来聊天吹水哇，以及一个会发布安全相关内容的公众号，欢迎关注 :)

<div>
    <img  alt="GIF" src="https://springbird.oss-cn-beijing.aliyuncs.com/img/mmqrcode1632325540724.png"  width="280px" />
    <img  alt="GIF" src="https://springbird.oss-cn-beijing.aliyuncs.com/img/qrcode_for_gh_cead8e1080d6_344.jpg"  width="280px" />
</div>
