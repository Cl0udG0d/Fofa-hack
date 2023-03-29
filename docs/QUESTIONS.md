# 问题集合

> 罗列可能使用过程中遇到的问题

### FOFA综合语法使用

> python fofa.py --keyword thinkphp && country="CN"

此时只会识别到 thinkphp,多个关键字的时候需要使用双引号包裹,内部的关键字用单引号包裹,示例如下
> python fofa.py --keyword "thinkphp && country='CN'"
### opencv-python错误

解决方法

[【Bug】ERROR: Could not build wheels for opencv-python, which is required to install pyproject.toml-ba](https://blog.csdn.net/AugustMe/article/details/126402049)


### ddddocr错误解决

> 因为有朋友说ddddocr这个库在不同版本的操作系统上会有各种运行的错误,为了避免完全用不了Fofa-hack
> 
> 现在将老版本的方式重新给出,如果账号密码登录不了,或者单纯不想用账号密码登录的时候,可以直接复制cookie登录
> 
将下图中的cookie直接复制到`fofa_cookie.txt`文件里,这样在启动的时候Fofa-hack就会识别到并且直接使用cookie爬取了

注意不是`Authorization`

`cookie`的位置如下
  ![](https://github.com/Cl0udG0d/Fofa-script/blob/master/images/2.png)


