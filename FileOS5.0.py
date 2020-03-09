'''
@Author: xiaohuohu
@Date: 2020-03-03 14:04:48
@LastEditTime: 2020-03-09 11:14:36
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: \CodeAll\code_Python\批量文件操作\批量操作5.0\FileOS5.0.py
'''
import os
import re
import shutil
import time
import json
from Tools import Tools
from pathlib import Path


class FileOS5:
    logSuffix = '.json'  # 日志后缀名
    shellRule = None  # 命令规则
    version = '5.0'  # 版本号
    rootPath = Path(__file__).parents[0]  # 文件路径
    ruleJson = 'rule.json'  # 日志后缀名
    tip = '提示:tip 退出:exit 指令列表:list 帮助信息:help 全部指令详细:helpall 详细指令信息:指令 -?'
    helps = '你可以通过此程序快速批量操作文件 附加:命令详细情况请使用 命令名 -? 来查看'
    canBreak = ['removefile', 'removedir', 'renamefile',
                'renamedir', 'exchangefile']  # 可回退操作

    @staticmethod
    def start():
        # 加载命令规则
        jsonRes = Tools.getJson(os.path.join(
            FileOS5.rootPath, FileOS5.ruleJson))
        if jsonRes['boolOk']:
            FileOS5.shellRule = jsonRes['jsonRes']
        else:
            print('加载错误,错误如下:', jsonRes['errorInf'])
            return
        # 程序本体 =========================================================================
        print(
            '>>>>>>>>>>>>>>>文件批量操作4.0 BY xiaohuohu TIME 2020-03-01 PS 区分大小写<<<<<<<<<<<<<<<')
        print(FileOS5.tip)
        while True:
            userInput = input('>>>').strip()
            if not userInput:
                continue
            # 字符串转指令字典
            shellRes = Tools.shell(userInput)
            # 检查是否符合规则
            shellCheckRes = Tools.shellCheck(shellRes, FileOS5.shellRule)
            shellName = shellRes['shellName']
            shellItem = shellRes['shellItem']
            # 日志数据
            logData = {'shellName': shellName, 'version': FileOS5.version,
                       'shellItem': shellItem, 'sum': [0, 0], 'data': []}
            # 展示帮助
            if '-?' in shellItem and shellCheckRes[0]:
                FileOS5.shellRuleShow(shellName)
                continue
            if shellCheckRes[0]:  # 是否是可用命令
                if not shellCheckRes[1]:  # 是否正确
                    print('名令出现错误,错误内容如下:{}'.format(shellCheckRes[2]))
                    continue
                # =====================================================================================
                if shellName == 'tip':  # 提示
                    print(FileOS5.tip)
                elif shellName == 'help':  # 提示
                    print(FileOS5.helps)
                elif shellName == 'version':  # 提示
                    print('版本号:', FileOS5.version)
                elif shellName == 'helpall':  # 全部命令帮助
                    for num, value in enumerate(FileOS5.shellRule):
                        FileOS5.shellRuleShow(value)
                        if len(FileOS5.shellRule)-1>num and Tools.inputCheck('继续{}/{}<Y/N>:'.format(num+1, len(FileOS5.shellRule)), '[YynN]', '错误选择:') in ['n', 'N']:
                            break
                elif shellName == 'list':  # 命令列表
                    print('指令列表{}'.format(
                        [value for value in FileOS5.shellRule]))
                elif shellName == 'exit':  # 退出
                    print('感谢使用')
                    break
                elif shellName == 'looklog':  # 查看日志
                    FileOS5.lookLogInf(shellName, shellItem)
                elif shellName == 'namerule':  # 改名规则测试
                    FileOS5.nameRuleShow(Tools.checkRule(
                        shellItem['-o'], boolAdd='-a' not in shellItem))
                elif shellName == 'findfile':  # 寻找文件
                    FileOS5.findfileOrDir(
                        shellName, shellItem, logData, boolFOD=True)
                elif shellName == 'finddir':  # 寻找文件夹
                    FileOS5.findfileOrDir(
                        shellName, shellItem, logData, boolFOD=False)
                elif shellName == 'copyfile':  # 复制文件
                    FileOS5.copyOrMoveFileOrDir(
                        shellName, shellItem, logData, boolFOD=True, copyOrMove=True)
                elif shellName == 'copydir':  # 复制文件夹
                    FileOS5.copyOrMoveFileOrDir(
                        shellName, shellItem, logData, boolFOD=False, copyOrMove=True)
                elif shellName == 'removefile':  # 转移文件
                    FileOS5.copyOrMoveFileOrDir(
                        shellName, shellItem, logData, boolFOD=True, copyOrMove=False)
                elif shellName == 'removedir':  # 转移文件夹
                    FileOS5.copyOrMoveFileOrDir(
                        shellName, shellItem, logData, boolFOD=False, copyOrMove=False)
                elif shellName == 'deletefile':  # 删除文件
                    FileOS5.deleteFileOrDir(
                        shellName, shellItem, logData, boolFOD=True)
                elif shellName == 'deletedir':  # 删除文件夹
                    FileOS5.deleteFileOrDir(
                        shellName, shellItem, logData, boolFOD=False)
                elif shellName == 'renamefile':  # 改名文件
                    FileOS5.renameFileOrDir(
                        shellName, shellItem, logData, boolFOD=True)
                elif shellName == 'renamedir':  # 改名文件夹
                    FileOS5.renameFileOrDir(
                        shellName, shellItem, logData, boolFOD=False)
                elif shellName == 'exchangefile':  # 交换文件
                    FileOS5.exchangeFile(shellName, shellItem, logData)
                elif shellName == 'breaklog':  # 文件回退
                    FileOS5.breakLog(shellName, shellItem)
            else:
                print('此命令不存在,解析结果如下: 命令名:{},子项:{}'.format(
                    shellName, shellItem))

    # 主要 ===================================================
    @staticmethod
    def findfileOrDir(shellName: str, shellItem: dict, logData: dict, boolFOD: bool = True):
        if not FileOS5.orderExists(shellItem, '-f'):  # 源文件
            return
        # 日志
        logRealyFile = FileOS5.logRealyPath(shellName, shellItem)
        print('开始搜索,请等待片刻')
        findFileRes = Tools.fileRoot(shellItem['-f'], shellItem['-r'], boolson=(
            '-s' in shellItem), boolFOD=boolFOD, boolShow=('-t' in shellItem))
        if not findFileRes['boolOk']:
            print('出现错误,错误如下:{}'.format(findFileRes['errorInf']))
            return
        logData['data'] = [{'find': Tools.byFDiInfGetPa(
            val)} for val in findFileRes['findList']]
        logData['sum'][0] = findFileRes['findSum']
        print('搜寻总数:', findFileRes['findSum'])
        # 写入日志
        Tools.createLog(shellItem, logRealyFile, logData)

    @staticmethod
    def copyOrMoveFileOrDir(shellName: str, shellItem: dict, logData: dict, boolFOD: bool = True, copyOrMove: bool = True):
        if not FileOS5.orderExists(shellItem, '-f'):  # 源文件
            return
        # 改名规则
        rule = []
        if '-o' in shellItem:
            rule = Tools.checkRule(
                shellItem['-o'], boolAdd='-a' not in shellItem)
            if not rule['boolOk']:
                print('改名规则错误', rule['noUseList'])
                return

        if not FileOS5.orderExists(shellItem, '-n'):  # 目标文件
            print('尝试创建路径')
            if not Tools.createDirs(shellItem['-n']):  # 尝试创建文件
                return
            print('创建路径成功')

        # 日志
        logRealyFile = FileOS5.logRealyPath(shellName, shellItem)
        # 搜索
        print('开始搜索,请等待片刻')
        findFileRes = Tools.fileRoot(shellItem['-f'], shellItem['-r'], boolson=(
            '-s' in shellItem), boolFOD=boolFOD, boolShow=('-t' in shellItem))
        if not findFileRes['boolOk']:
            print('出现错误,错误如下:{}'.format(findFileRes['errorInf']))
            return
        print('搜寻总数:', findFileRes['findSum'])
        # 确认操作
        if Tools.checkBegin('确认复制<Y/N>:'):
            return
        print('正在复制,请等待片刻')
        # 复制操作
        FileOS5.copyOrmoveFODItem(findFileRes['findList'], shellName, shellItem, logData, rule, boolInRoot=(
            '-p' not in shellItem), boolFOD=boolFOD, copyOrMove=copyOrMove)
        print('成功数:', logData['sum'][0], '失败数:', logData['sum'][1])
        # 写入日志
        Tools.createLog(shellItem, logRealyFile, logData)

    @staticmethod
    def copyOrmoveFODItem(fileList: list, shellName: str, shellItem: dict, logData: dict, rule: dict, boolInRoot: bool = True, boolFOD: bool = True, copyOrMove: bool = True):
        for num, val in enumerate(fileList):
            errorInf = []
            oldPath = Tools.byFDiInfGetPa(val)
            # 移动时改名
            if '-o' in shellItem:
                newName = Tools.byRuleGetName(
                    val, rule['nameRuleRes'], booLResListOrText=True)[1]
                val[1] = newName
            newPath = Tools.getOtherPath(
                shellItem['-f'], val, shellItem['-n'], boolInRoot=boolInRoot)['newPath']
            copyFODRes = Tools.copyOrMoveFOD(
                oldPath, newPath, boolFOD=boolFOD, copyOrMove=copyOrMove)
            if copyFODRes['boolOk']:
                print('{}成功'.format('复制' if copyOrMove else '转移'),
                      str(num), oldPath, newPath)
                logData['sum'][0] += 1
            else:
                print('{}失败'.format('复制' if copyOrMove else '转移'),
                      str(num), oldPath, newPath)
                logData['sum'][1] += 1
                errorInf = copyFODRes['errorInf']
            logData['data'].append(
                {'boolOk': copyFODRes['boolOk'], 'errorInf': errorInf, 'oldPath': oldPath, 'newPath': newPath})

    @staticmethod
    def deleteFileOrDir(shellName: str, shellItem: dict, logData: dict, boolFOD: bool = True):
        if not FileOS5.orderExists(shellItem, '-f'):  # 源文件
            return
        # 日志
        logRealyFile = FileOS5.logRealyPath(shellName, shellItem)
        # 搜索
        print('开始搜索,请等待片刻')
        findFileRes = Tools.fileRoot(shellItem['-f'], shellItem['-r'], boolson=(
            '-s' in shellItem), boolFOD=boolFOD, boolShow=('-t' in shellItem))
        if not findFileRes['boolOk']:
            print('出现错误,错误如下:{}'.format(findFileRes['errorInf']))
            return
        print('搜寻总数:', findFileRes['findSum'])
        # 确认操作
        if Tools.checkBegin('确认删除<Y/N>:'):
            return
        print('正在删除,请等待片刻')
        # 复制操作
        FileOS5.deleteFODItem(
            findFileRes['findList'], shellName, shellItem, logData, boolFOD=boolFOD)
        print('成功数:', logData['sum'][0], '失败数:', logData['sum'][1])
        # 写入日志
        Tools.createLog(shellItem, logRealyFile, logData)

    @staticmethod
    def deleteFODItem(fileList: list, shellName: str, shellItem: dict, logData: dict, boolFOD: bool = True):
        for num, val in enumerate(fileList):
            errorInf = []
            oldPath = Tools.byFDiInfGetPa(val)
            deleteFODRes = Tools.deleFileOrDir(oldPath, boolFOD=boolFOD)
            if deleteFODRes['boolOk']:
                print('删除成功', str(num), oldPath)
                logData['sum'][0] += 1
            else:
                print('删除失败', str(num), oldPath)
                logData['sum'][1] += 1
                errorInf = deleteFODRes['errorInf']
            logData['data'].append(
                {'boolOk': deleteFODRes['boolOk'], 'errorInf': errorInf, 'oldPath': oldPath})

    @staticmethod
    def renameFileOrDir(shellName: str, shellItem: dict, logData: dict, boolFOD: bool = True):
        if not FileOS5.orderExists(shellItem, '-f'):  # 源文件
            return
        # 改名规则
        rule = []
        if '-o' in shellItem:
            rule = Tools.checkRule(
                shellItem['-o'], boolAdd='-a' not in shellItem)
            if not rule['boolOk']:
                print('改名规则错误', rule['noUseList'])
                return
        # 日志
        logRealyFile = FileOS5.logRealyPath(shellName, shellItem)
        # 搜索
        print('开始搜索,请等待片刻')
        findFileRes = Tools.fileRoot(shellItem['-f'], shellItem['-r'], boolson=(
            '-s' in shellItem), boolFOD=boolFOD, boolShow=('-t' in shellItem))
        if not findFileRes['boolOk']:
            print('出现错误,错误如下:{}'.format(findFileRes['errorInf']))
            return
        print('搜寻总数:', findFileRes['findSum'])
        # 确认操作
        if Tools.checkBegin('确认改名<Y/N>:'):
            return
        print('正在修改,请等待片刻')
        # 复制操作
        FileOS5.renameFODItem(
            findFileRes['findList'], shellName, shellItem, logData, rule, boolFOD=boolFOD)
        print('成功数:', logData['sum'][0], '失败数:', logData['sum'][1])
        # 写入日志
        Tools.createLog(shellItem, logRealyFile, logData)

    @staticmethod
    def renameFODItem(fileList: list, shellName: str, shellItem: dict, logData: dict, rule: dict, boolFOD: bool = True):
        for num, val in enumerate(fileList):
            errorInf = []
            oldPath = Tools.byFDiInfGetPa(val)
            newPath = Tools.byRuleGetName(
                val, rule['nameRuleRes'], booLResListOrText=False)
            renameFODRes = Tools.copyOrMoveFOD(
                oldPath, newPath, boolFOD=boolFOD, copyOrMove=False)
            if renameFODRes['boolOk']:
                print('改名成功', str(num), oldPath, newPath)
                logData['sum'][0] += 1
            else:
                print('改名失败', str(num), oldPath, newPath)
                logData['sum'][1] += 1
                errorInf = renameFODRes['errorInf']
            logData['data'].append(
                {'boolOk': renameFODRes['boolOk'], 'errorInf': errorInf, 'oldPath': oldPath, 'newPath': newPath})

    @staticmethod
    def exchangeFile(shellName: str, shellItem: dict, logData: dict):
        if not FileOS5.orderExists(shellItem, '-f'):  # 源文件
            return
        # 日志
        logRealyFile = FileOS5.logRealyPath(shellName, shellItem)
        # 搜索
        print('开始搜索,请等待片刻')
        findFileRes = Tools.fileRoot(shellItem['-f'], shellItem['-r'], boolson=(
            '-s' in shellItem), boolFOD=True, boolShow=('-t' in shellItem))
        if not findFileRes['boolOk']:
            print('出现错误,错误如下:{}'.format(findFileRes['errorInf']))
            return
        print('搜寻总数:', findFileRes['findSum'])
        # 确认操作
        if Tools.checkBegin('确认交换<Y/N>:'):
            return
        print('正在修改,请等待片刻')
        # 复制操作
        FileOS5.exchangeFileItem(
            findFileRes['findList'], shellName, shellItem, logData)
        print('成功数:', logData['sum'][0], '失败数:', logData['sum'][1])
        # 写入日志
        Tools.createLog(shellItem, logRealyFile, logData)

    @staticmethod
    def exchangeFileItem(fileList: list, shellName: str, shellItem: dict, logData: dict):
        for num, val in enumerate(fileList):
            errorInf = []
            oldPath = Tools.byFDiInfGetPa(val)
            newPath = Tools.getOtherPath(
                shellItem['-f'], val, shellItem['-n'], boolInRoot=False)['newPath']
            exchangeRes = Tools.exchFile(shellItem['-f'], val, shellItem['-n'])
            if exchangeRes['boolOk']:
                logData['sum'][0] += 1
                print('交换成功', str(num), oldPath, newPath)
            else:
                logData['sum'][1] += 1
                print('交换失败', str(num), oldPath, newPath)
                errorInf = exchangeRes['errorInf']
            logData['data'].append(
                {'boolOk': exchangeRes['boolOk'], 'errorInf': errorInf, 'oldPath': oldPath, 'newPath': newPath})

    @staticmethod
    def nameRuleShow(rule: dict):
        print('是否符合:', rule['boolOk'], '\n未定义命令:', rule['noUseList'], '\n已定义命令:',
              rule['useList'], '\n剩余未使用字符:', rule['oldList'], '\n解析结果:', rule['nameRuleRes'])

    @staticmethod
    def lookLogInf(shellName: str, shellItem: dict):
        if not FileOS5.orderExists(shellItem, '-f'):  # 源文件
            return
        logJson = Tools.getJson(shellItem['-f'])
        if logJson['boolOk']:
            logInf = logJson['jsonRes']
            print('命令:', logInf['shellName'], '\n版本号:', logInf['version'],
                  '\n操作:', logInf['shellItem'], '\n成功/失败:', logInf['sum'])
        else:
            print('日志错误,错误如下:', logJson['errorInf'])

    @staticmethod
    def breakLog(shellName: str, shellItem: dict):
        if not FileOS5.orderExists(shellItem, '-f'):  # 源文件
            return
        logJson = Tools.getJson(shellItem['-f'])
        if logJson['boolOk']:
            logInf = logJson['jsonRes']
            if logInf['shellName'] in FileOS5.canBreak:
                ['removefile', 'removedir', 'renamefile',
                    'renamedir', 'exchangefile']
                for num, val in enumerate(logInf['data']):
                    if logInf['shellName'] in ['removefile', 'removedir', 'exchangefile']:  # 移动文件/文件夹,交换文件
                        oldPath = val['oldPath']
                        newPath = val['newPath']
                        copyFODRes = Tools.copyOrMoveFOD(newPath, oldPath, boolFOD=logInf['shellName'] in [
                                                         'removefile', 'exchangefile'], copyOrMove=False)
                        if copyFODRes['boolOk']:
                            print('回退成功', str(num), newPath, oldPath)
                        else:
                            print('回退失败', str(num), newPath, oldPath)
                    elif logInf['shellName'] in ['renamefile', 'renamedir']:  # 文件/文件夹改名回退
                        oldPath = val['oldPath']
                        newPath = val['newPath']
                        renameFODRes = Tools.copyOrMoveFOD(
                            newPath, oldPath, boolFOD=logInf['shellName'] == 'renamefile', copyOrMove=False)
                        if renameFODRes['boolOk']:
                            print('回退成功', str(num), newPath, oldPath)
                        else:
                            print('回退失败', str(num), newPath, oldPath)
            else:
                print('次命令不支持回退:', logInf['shellName'])
        else:
            print('日志错误,错误如下:', logInf['errorInf'])

    # 辅助 ===================================================
    @staticmethod
    def shellRuleShow(shellName: str) -> None:
        if shellName in FileOS5.shellRule:
            boolShell = FileOS5.shellRule[shellName]
            shell = boolShell['rule']
            print('命令名:{}\n说明:{}'.format(shellName, boolShell['help']))
            if len(shell) > 0:
                print('{}{}{}{}'.format('[命令]', '[命令]', '[子项]', '[说明]'))
                for value in shell:
                    print('{: <6}{}{}{}'.format(value['name'], ('[必填]' if value['must']
                                                                else '[选填]'), ('[必填]' if value['otherMust'] else '[选填]'), value['help']))
        else:
            print('无相关帮助信息')

    @staticmethod
    def logRealyPath(shellName: str, shellItem: dict):
        roots = ('' if '-f' not in shellItem else shellItem['-f']) if not (
            '-l' in shellItem and shellItem['-l'] != '') else shellItem['-l']
        return os.path.join(roots, '{}_{}{}'.format(shellName, Tools.getTime(), FileOS5.logSuffix))

    @staticmethod
    def orderExists(shellItem: dict, order: str):
        if order in shellItem and not os.path.exists(shellItem[order]):
            print('路径不存在:{}'.format(shellItem[order]))
            return False
        return True


FileOS5.start()
