import sys

# funcName = sys._getframe().f_back.f_code.co_name #获取调用函数名
lineNumber = sys._getframe().f_back.f_lineno     #获取行号

print(sys._getframe().f_code.co_name) # 获取当前函数名