import gettext

# 创建 gettext 对象，用于加载翻译文件
language = gettext.translation('fofa_hack', localedir='./locale', languages=['en'])
language.install()
_ = language.gettext

print(_('Fofa-hack v{} 使用说明').format(2))
