# 代码运行

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