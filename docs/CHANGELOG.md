# CHANGELOG 代码变更记录

### 2.4.8
+ 修复setup.py问题
+ 合并[新增可设置保存文件名代码](https://github.com/Cl0udG0d/Fofa-hack/pull/58)
+ 新增贡献者[10cks](https://github.com/10cks)

### 2.4.7
+ 去除没有获取到语言情况下为空的问题
+ 生成fofa-hack pip包

### 2.4.6
+ 修复 [issues 54](https://github.com/Cl0udG0d/Fofa-hack/issues/54)
+ 终端颜色输出问题解决

### 2.4.5
+ 修复 [issues 51](https://github.com/Cl0udG0d/Fofa-hack/issues/51)
+ 修复 [issues 53](https://github.com/Cl0udG0d/Fofa-hack/issues/53)

### 2.4.4
+ unit.py 修剪关键字功能扩展

### 2.4.3

+ 修复打包问题

### 2.4.2

+ 修复打包问题
### 2.4.1

+ 根据环境切换语言

### 2.4.0

+ 删除多余逻辑文件
+ 更新获取数据逻辑,页面爬虫 -> api接口获取
+ 默认步长设置为 50,防止等待过久
### 2.3.9

+ 修复exit(0)退出报错问题
+ 无时间戳的情况下退出并保存final文件

### 2.3.8

+ 输出内容为json的情况下 ,level=2、3时报错问题修复

### 2.3.7

+ 添加地区访问fofa判断
+ linux环境下不支持运行selenium模式

### 2.3.6

+ 修复[ISSUE](https://github.com/Cl0udG0d/Fofa-hack/issues/34)

### 2.3.5

+ 修复[ISSUE](https://github.com/Cl0udG0d/Fofa-hack/issues/22)
+ 高亮界面输出
+ 新增exe输出

### 2.3.4

+ 新增英文readme
### 2.3.3

+ 修复部分已知BUG 
  + 修复搜索结果为0时出现的列表索引越界问题
  + 修复搜索结果时间戳列表为空时的报错问题
### 2.3.2

+ 修改运行方式readme

### 2.3.1

+ 新增selenium部分
+ 新增type字段 虽然它不太稳定

### 2.3.0

+ 分离参数输入和爬取部分

### 2.2.6

+ 新增fofa公安版登录代码,该部分未完善

### 2.2.5

+ 从文件批量读取语法 -i --inputfile

### 2.2.4

+ 修复变量名BUG

### 2.2.3

+ 除特殊变量外,变量统一命名规范为 小写字母+下划线
+ 除特殊方法外,方法一律使用小驼峰命名 camelCase
+ 方法名见名知意 复杂方法添加注释
+ 代码格式化

### 2.2.2

+ 增加外部调用接口
+ 递归结束使用全局变量判定

### 2.2.1

+ 合并tastypear程序兼容性功能

### 2.2.0

+ 合并wanswu代理功能

### 2.1.12

+ 支持JSON文件输出 -o json

### 2.1.11

+ 修订 python maximum recursion depth exceeded错误
+ json文件输出BUG修改

### 2.1.10

+ 修改logo

### 2.1.9

+ 修改readme对于保存文件的描述
+ 实现fofa的两种URL获取逻辑，增加获取内容

### 2.1.8

+ 增加了fuzz之后的去重 免得获取到一堆重复数据

### 2.1.7

+ 新增fuzz参数 -f 开启
+ 修复header问题

### 2.1.6

+ 删除测试 print
+ 新增 != fuzz 逻辑

### 2.1.5

+ 删除config.py文件,合并内容到fofa.py
+ 每次递归的时候的关键字列表应当与下标对应，而不是统一SET
+ 运行测试 python fofa.py -k index --endcount 1000
+ 合并FUZZ关键字并进行递归

### 2.1.4

+ 修复 https://github.com/Cl0udG0d/Fofa-hack/issues/13 ISSUE BUG

### 2.1.3

+ 添加 port 自动化fuzz
+ 新增 搜索关键字 port判断

### 2.1.2

+ 修复 host="edu.cn" 搜索错误

### 2.1.1

+ 提升程序稳定性
+ 添加org 、asn 自动化fuzz
+ 修改递归逻辑
+ 新增项目头图
+ 新增TODO文件

### 2.1.0

+ 删除多余images
+ 修改readme图片
+ 添加country 自动化fuzz

### 2.0.6

+ 修改README等文件
+ 合并代码 - 优化时间戳逻辑

### 2.0.5
+ 新增贡献者 tastypear
+ 尝试优化时间戳逻辑

### 2.0.4
+ 删除.github文件夹
+ 新增TODO List
+ 删除csv导出

### 2.0.3
+ 修复fofa单关键字下第二页错误情况

### 2.0.2
+ 修复fofa多个查询条件下出现的错误

### 2.0.1
+ 修改filename,timeSleep等为类内部变量
+ 新增logoutInitMsg方法输出初始化信息
+ 新增fofa_fuzz_spider方法

### 2.0.0

+ 返璞归真,去除账号登录,直接使用时间戳来在第一页进行爬取

### 1.3.1

+ 支持多种导出方式 txt,json,csv
+ 因FOFA对普通用户的限制停止该项目的更新
### 1.3.0

+ `README`添加示例运行参考
+ 新增工具文件夹`tookit`,创建`levelData`等级模板文件
+ 新增 `--level`参数,内容明细如下
  + level=1 [ url ]
  + level=2 [ url , port , title , ip ]
  + level=3 [ url , port , title , ip , city , asn , organization , server , rep ]

### 1.2.8

+ 修改keyword为必须参数

### 1.2.7

+ 添加运行参数模式 --help
+ 修改README.md等文件
+ 支持三种方式登录账号

### 1.2.6

+ 设置开始页码为1,不支持自定义开始页码,防止普通用户无法查看页面问题
+ 添加赞赏账户文档与二维码
+ 修改README

### 1.2.5

+ 修改`ddddocr`版本号

### 1.2.4

+ 修改切换账号逻辑,首先重试当前账号

### 1.2.3

+ 显示运行过程中的报错详情
+ 优化项目结构
+ 支持复制cookie和账号密码两种方式登录,防止ddddocr等库环境问题
+ 新增工具文件`unit.py`

### 1.2.2

+ BUG修复
> 存储结果到`md5(搜索关键字)_运行时间戳.txt`文件中


### 1.2.1

+ 添加`QUESTIONS.md`问题集合文件
+ 增加断点重连机制，重连最大次数为3,提高系统运行稳定性
+ 增加多账户
+ 部分文件的微小更新(fofa_useragent.py、README.md....)

### 1.2.0

+ 添加CHANGELOG文件
+ 优化代码结构，分离useragent文件
+ 提取版本号在项目启动时加载
+ FOFA登录重试机制，最大重试值默认为3
+ 添加部分代码注释
+ 自动生成文件名 搜索关键字_运行时间戳.txt


### 此前的一些提交

+ 2023-1-27，合入[wanswu](https://github.com/wanswu)师傅提交的代码，通过账号密码进行登录

+ 2022-12-19，添加cookie的预判断

+ 2022-11-12，更新爬取规则

+ 2022-9-17，修改时间戳获取规则，项目整体趋于稳定

+ 2022-9-15，创建项目并修改适用于目前fofa的规则