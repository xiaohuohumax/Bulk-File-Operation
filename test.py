'''
@Author: your name
@Date: 2020-03-09 09:16:41
@LastEditTime: 2020-03-09 10:56:09
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: \CodeAll\code_Python\批量操作\批量操作6.0\test.py
'''
import os
import re
import shutil
import time
import json
from Tools import Tools
from pathlib import Path

text='<oldr:10::\d(\d+)><add:1:0>'
checkRuleRes=Tools.checkRule(text,boolAdd=False)
print(checkRuleRes)
value =['c:/xiaohuohu/image/show/','im12ag123sss1','.jpg']
byRuleGetNameRes=Tools.byRuleGetName(value,checkRuleRes['nameRuleRes'],booLResListOrText=False)
print(byRuleGetNameRes)


# size="xiaohui123dahuo"
# print(re.findall(r'\w+((\d)(\d(\d)))\w+',size))
# print(re.findall(r'(?:(?:[1-9]\d+)|\d)',size))
# print(re.search(r'(\w\w(\w))',size).group(1))
