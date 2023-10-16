import gettext
import pathlib

# # 创建 gettext 对象，用于加载翻译文件
# language = gettext.translation('fofa_hack', localedir='./locale', languages=['en'])
# language.install()
# _ = language.gettext
#
# print(_('Fofa-hack v{} 使用说明').format(2))
import os

# 获取当前脚本文件的绝对路径
current_path = os.path.abspath(__file__)
# 获取当前脚本文件所在的目录
script_directory = os.path.dirname(os.path.abspath(__file__))
# 获取当前项目的根目录
project_directory = os.path.dirname(script_directory)

print(current_path)
