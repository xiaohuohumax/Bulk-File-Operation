'''
@Author: xiaohuohu
@Date: 2020-03-04 13:07:39
@LastEditTime: 2020-03-09 10:55:04
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: \CodeAll\code_Python\批量文件操作\批量操作5.0\Tools.py
'''
import os
import re
import shutil
import time
import json
import random
from pathlib import Path


class Tools:

    @staticmethod
    def fileRoot(path: str, userRe: str, boolson: bool = False, boolFOD: bool = True, boolShow: bool = False) -> list:
        res = {'boolOk': True, 'errorInf': [], 'findSum': 0, 'findList': []}
        try:
            for root, dirs, files in os.walk(path):  # 遍历所选路径
                for num, fileName in enumerate(files if boolFOD else dirs):
                    realyPath = os.path.join(root, fileName)
                    if re.findall(userRe, realyPath):  # 匹配筛选文件
                        if boolFOD:
                            nameSplit = os.path.splitext(fileName)  # 分离文件名与后缀名
                            res['findList'].append(
                                [root, nameSplit[0], nameSplit[1]])
                        else:
                            res['findList'].append([root, fileName])
                        res['findSum'] += 1
                        if boolShow:
                            print(res['findSum'], realyPath)
                if not boolson:  # 是否遍历子文件夹
                    break
        except Exception as e:
            res['boolOk'] = False
            res['errorInf'].append(str(e))
        return res

    @staticmethod
    def byFDiInfGetPa(fileOrDirInf: list):
        name = fileOrDirInf[1] if len(fileOrDirInf) < 3 else '{}{}'.format(
            fileOrDirInf[1], fileOrDirInf[2])
        return os.path.join(fileOrDirInf[0], name)

    @staticmethod
    def copyOrMoveFOD(oldPath: str, newPath: str, boolFOD: bool = True, copyOrMove: bool = True):
        errorInf = []  # 错误信息
        boolOk = True  # 是否有错误
        try:
            if boolFOD:  # 文件
                newPathRoot = Path(newPath).parents[0]
                if not os.path.exists(newPathRoot):  # 创建目录
                    os.makedirs(newPathRoot)
            else:  # 文件夹
                if not os.path.exists(newPath):  # 创建目录
                    os.makedirs(newPath)
            if copyOrMove:
                if boolFOD:  # 文件
                    shutil.copy(oldPath, newPath)
                else:  # 文件夹
                    shutil.copytree(oldPath, newPath)
            else:
                shutil.move(oldPath, newPath)  # 改名
        except Exception as e:
            errorInf.append(str(e))
            boolOk = False
        return {'boolOk': boolOk, 'errorInf': errorInf}

    @staticmethod
    def deleFileOrDir(oldPath: str, boolFOD: bool = True):
        errorInf = []  # 错误信息
        boolOk = True  # 是否有错误
        try:
            if boolFOD:  # 文件
                os.remove(oldPath)  # 尝试删除文件
            else:  # 文件夹
                shutil.rmtree(oldPath)  # 尝试删除文件夹
        except Exception as e:
            errorInf.append(str(e))
            boolOk = False
        return {'boolOk': boolOk, 'errorInf': errorInf}

    @staticmethod
    def creaFileOrDir(oldPath: str, boolFOD: bool = True):
        errorInf = []  # 错误信息
        boolOk = True  # 是否有错误
        try:
            if boolFOD:  # 文件
                file = open(oldPath, 'w')
                file.close()
            else:  # 文件夹
                if not os.path.exists(oldPath):  # 创建目录
                    os.makedirs(oldPath)
        except Exception as e:
            errorInf.append(str(e))
            boolOk = False
        return {'boolOk': boolOk, 'errorInf': errorInf}

    @staticmethod
    def shell(text: str) -> list:
        reRes = re.findall(r'(?:\".*?\")|(?:[^\s\"]*)', text)
        replaceRes = [value.replace('\"', '')
                      for value in reRes if value != '']
        replaceRes = [value for value in replaceRes if value != '']
        shellRealyRes = {'shellName': replaceRes[0], 'shellItem': {}}
        item = ''  # 子命令
        errorList = []  # 错误集合
        for value in replaceRes[1:]:
            if value[0] == '-':
                item = value
                shellRealyRes['shellItem'].update({item: ''})
            else:
                shellRealyRes['shellItem'][item] = value
                boolReach = False
                item = ''
        return shellRealyRes

    @staticmethod
    def shellCheck(shellRealyRes: dict, rule: dict) -> list:
        boolReach = True  # 是否有符合命令要求
        boolInRuleList = True  # 此命令是否在列表中
        errorList = []  # 错误集合
        if shellRealyRes['shellName'] in rule:
            rules = rule[shellRealyRes['shellName']]['rule']
            rulesList = [val['name'] for val in rules]
            for val in shellRealyRes['shellItem']:
                if val not in rulesList:
                    errorList.append('指令不存在:{}:{}'.format(
                        val, shellRealyRes['shellItem'].get(val)))
                    boolReach = False
            for key in rules:
                if key['must']:
                    if key['name'] not in shellRealyRes['shellItem']:
                        errorList.append('缺少指令{}'.format(key['name']))
                        boolReach = False
                if key['otherMust']:
                    if key['name'] in shellRealyRes['shellItem']:
                        if not shellRealyRes['shellItem'].get(key['name']):
                            errorList.append('缺少{}子项'.format(key['name']))
                            boolReach = False
        else:
            boolInRuleList = False
            boolReach = True
            errorList.append('无此项命令{}'.format(shellRealyRes['shellName']))
        return [boolInRuleList, boolReach, errorList]

    @staticmethod
    def getTime(rule: str = "%Y_%m_%d_%H_%M_%S") -> str:
        return time.strftime(rule, time.localtime(Tools.getTimeStamp()))

    @staticmethod
    def getTimeStamp() -> int:
        return int(time.time())

    @staticmethod
    def getOtherPath(oldPath: str, findPath: list, newPath: str, boolInRoot: bool = True):
        rootlist = []
        res = {'boolOk': False, 'newPath': ''}
        if not boolInRoot:
            for val in Path(Tools.byFDiInfGetPa(findPath)).parents:
                rootlist.insert(0, os.path.split(val)[1])
                if os.path.normcase(val) == os.path.normcase(oldPath):  # 判断路径是否相同
                    res['boolOk'] = True
                    res['newPath'] = Tools.byFDiInfGetPa(
                        [os.path.join(newPath, *rootlist[1:]), *findPath[1:]])
                    break
        else:
            res['boolOk'] = True
            res['newPath'] = Tools.byFDiInfGetPa([newPath, *findPath[1:]])
        return res

    @staticmethod
    def inputCheck(showText: str, regular: str, errorInf: str = '格式错误') -> str:
        while True:
            userChoose = input(showText)  # 用户输入
            if re.findall(regular, userChoose):  # 检验输入是否符合正则要求 符合就返回输入,不符合则重新输入
                return userChoose  # 返回输入结果
            print(errorInf)  # 提示输入错误

    @staticmethod
    def createDirs(path: str):
        try:
            os.makedirs(path)
            return True
        except Exception as e:
            print('路径创建失败:', path)
            return False

    @staticmethod
    def createLog(shellItem: dict, logRealyFile: str, logData: dict):
        if '-l' in shellItem:
            try:
                with open(logRealyFile, 'a', encoding='utf-8') as file:
                    file.write(json.dumps(logData))
                print('日志保存成功:', logRealyFile)
            except Exception as e:
                print('日志保存失败:', str(e))

    @staticmethod
    def checkBegin(checkText: str):
        return Tools.inputCheck(checkText, '[yYnN]', '错误选择') in ['n', 'N']

    @staticmethod
    def checkRule(text: str, boolAdd: bool = True) -> list:
        # 初始命令列表 匹配所有 <name:....> 格式的命令 如: <new:xioahuohu> <add:1:2> 其它自动丢掉 如: <> < name : asdas>
        nameList = re.findall(r'(<\w+:[^><"]*?>)', text)
        nameRuleList = []  # 解析命令列表
        nameRuleReaList = []
        deleteInf = text
        for value in range(len(nameList)-1, -1, -1):  # 倒叙遍历初始命令列表
            # 匹配 <add:?:?> 注意:第一个参数[可选] [0,+) 第二个参数[可选] (0,+)
            if re.findall(r'^<add:(?:(?:[1-9]\d+)|\d)?:(?:[1-9]\d*)?>$', nameList[value]):
                # 转换 缺省时 <add::> 默认两个参数都为 1
                nameRuleReaList.append(nameList[value])
                item = [1 if val == '' else int(
                    val) for val in nameList[value][nameList[value].find(':') + 1: -1].split(':')]
                nameRuleList.insert(
                    0, {'kind': 'add', 'item': item})  # 解析命令列表开头中添加新命令
                nameList.pop(value)  # 将此命令从初始命令列表中移除
            # 匹配 <old:?:?:?> 注意三个参数 为数组切分操作规则 start,end,step
            elif re.findall(r'^<old(?::(?:\d*|\-\d+)){3}>$', nameList[value]):
                nameRuleReaList.append(nameList[value])
                # 转换 不存在时为 None 例如: <old:::> 则表示 old[None:None:None]
                item = [None if val == '' else int(
                    val) for val in nameList[value][nameList[value].find(':')+1:-1].split(':')]
                nameRuleList.insert(0, {'kind': 'old', 'item': item})
                nameList.pop(value)
            # 匹配 <time:...> 注意: ... 表示 %, 字母, 数字, 下划线. 例如: %Y_%m_%d_%H_%M_%S 其它则不允许存在
            elif re.findall(r'^<time:[\%\w]*>$', nameList[value]):
                nameRuleReaList.append(nameList[value])
                item = nameList[value][nameList[value].find(
                    ':')+1:-1]  # 筛选出时间表达式
                nameRuleList.insert(0, {'kind': 'time', 'item': item})
                nameList.pop(value)
            # 匹配 <new:...> 注意: ... 表示 字母, 数字, 下划线. 其它则不允许存在
            elif re.findall(r'^<new:[^\s <>"]*>$', nameList[value]):
                nameRuleReaList.append(nameList[value])
                item = nameList[value][nameList[value].find(
                    ':')+1:-1]  # 筛选出新名字字符串
                nameRuleList.insert(0, {'kind': 'new', 'item': item})
                nameList.pop(value)
            elif re.findall(r'^<oldr(?::(?:(?:[1-9]\d+)|\d)?){2}:[^><]*?>$', nameList[value]):
                nameRuleReaList.append(nameList[value])
                item = nameList[value][nameList[value].find(':')+1:-1].split(':')  # 筛选出新名字字符串
                num=[0 if not val else int(val) for val in item[:2]]
                nameRuleList.insert(0, {'kind': 'oldr', 'num':num,'item': item[2]})
                nameList.pop(value)
        # 检验用户是否添加 <add::> 没写则自己在解析命令列表末尾添加 默认 <add:1:1>
        if len([1 for value in nameRuleList if value['kind'] == 'add']) == 0 and boolAdd:
            nameRuleList.append({'kind': 'add', 'item': [1, 1]})
        for value in nameList:
            deleteInf = deleteInf.replace(value, '.'*len(value))
        for value in nameRuleReaList:
            deleteInf = deleteInf.replace(value, '.'*len(value))
        return {'boolOk': len(nameList) == 0, 'noUseList': nameList, 'useList': nameRuleReaList, 'nameRuleRes': nameRuleList, 'oldList': deleteInf}

    @staticmethod
    def byRuleGetName(value: list, nameRule: dict, booLResListOrText: bool = True) -> str:
        newFile = ''  # 修改后的路径
        for rule in nameRule:
            if rule['kind'] == 'add':  # 累计计数
                newFile = '{}{}'.format(newFile, rule['item'][0])
                rule['item'][0] += rule['item'][1]  # 累计自增
            elif rule['kind'] == 'new':  # 新字母
                newFile = '{}{}'.format(newFile, rule['item'])
            elif rule['kind'] == 'time':  # 添加时间
                newFile = '{}{}'.format(newFile, Tools.getTime(rule['item']))
            elif rule['kind'] == 'old':  # 添加部分原名字字符
                newFile = '{}{}'.format(
                    newFile, value[1][rule['item'][0]:rule['item'][1]:rule['item'][2]])
            elif rule['kind'] == 'oldr':  # 添加部分原名字字符
                newText=''
                reRes=re.findall(rule['item'], value[1])
                if len(reRes)>rule['num'][0]:
                    if not isinstance(reRes[rule['num'][0]] , str):
                        if len(reRes[rule['num'][0]])>rule['num'][1]:
                            newText='{}{}'.format(newText,reRes[rule['num'][0]][rule['num'][1]])
                    else:
                        newText='{}{}'.format(newText,reRes[rule['num'][0]])
                if not newText:
                    newText=value[1]
                newFile = '{}{}'.format(newFile,newText)
                # newFile = '{}{}'.format(newFile, ''.join(
                #     [val.group()for val in re.finditer(rule['item'], value[1])]))
        if len(value) > 2:  # 组合出新名字真实路径
            newFile = [value[0], newFile, value[2]]
        else:
            newFile = [value[0], newFile]
        return newFile if booLResListOrText else Tools.byFDiInfGetPa(newFile)

    @staticmethod
    def getJson(address: str) -> list:
        dictRes = {}
        errorList = []
        boolRead = True
        try:
            with open(address, 'r', encoding='utf-8') as file:
                dictRes = json.load(file)
        except Exception as e:
            errorList.append('{}'.format(e))
            boolRead = False
        return {'boolOk': boolRead, 'errorInf': errorList, 'jsonRes': dictRes}

    @staticmethod
    def exchFile(oldPath: str, findPath: list, newPath: str):
        pathA = Tools.byFDiInfGetPa(findPath)  # 源文件
        pathB = Tools.getOtherPath(oldPath, findPath, newPath, boolInRoot=False)[
            'newPath']  # 目标替换文件
        res = {'errorInf': [], 'boolOk': True}

        randomText = Tools.randomText(start=5, end=10)  # 随机乱码
        findPath[1] = '{}{}'.format(randomText, findPath[1])

        pathC = Tools.getOtherPath(oldPath, findPath, newPath, boolInRoot=False)[
            'newPath']  # 目标替换文件

        if os.path.exists(pathB):  # 目标文件存在
            changeATC = Tools.copyOrMoveFOD(
                pathA, pathC, boolFOD=True, copyOrMove=False)
            if changeATC['boolOk']:
                changeBTA = Tools.copyOrMoveFOD(
                    pathB, pathA, boolFOD=True, copyOrMove=False)
                if changeBTA['boolOk']:
                    changeCTB = Tools.copyOrMoveFOD(
                        pathC, pathB, boolFOD=True, copyOrMove=False)
                    if changeCTB['boolOk']:
                        res['boolOk'] = True
                    else:
                        res['boolOk'] = False
                        res['errorInf'].extend(changeCTB['errorInf'])
                else:
                    Tools.copyOrMoveFOD(
                        pathA, pathC, boolFOD=True, copyOrMove=False)  # 错误移动回去
                    res['boolOk'] = False
                    res['errorInf'].extend(changeBTA['errorInf'])
            else:
                res['boolOk'] = False
                res['errorInf'].extend(changeATC['errorInf'])
        else:
            res['boolOk'] = False
            res['errorInf'].append('目标不存在对应的文件')
        return res

    @staticmethod
    def randomText(randomList: list = ['~', '$', '@', '[', ']'], start: int = 1, end: int = 5):
        text = ''
        for val in range(random.randint(start, end)):
            text = '{}{}'.format(text, random.choice(randomList))
        return text
