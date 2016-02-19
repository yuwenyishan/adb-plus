#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
from cmd import Cmd
import dircache
import sys
import os
import signal

__author__ = 'Jack_long'
adb_devices = []
adb_command = ''
default_str = u'戠'
default_win_coding = 'gbk'

adb_default_command = ['adb push ', 'adb pull ', 'adb sync ', 'adb shell',
                       'adb logcat', 'adb forward ', 'adb reverse ',
                       'adb jdwp', 'adb install', 'adb uninstall',
                       'adb bugreport', 'adb backup ', 'adb restore ',
                       'adb disable', 'adb enable', 'adb keygen ',
                       'adb wait-for-device', 'adb start-server',
                       'adb kill-server', 'adb get-state', 'adb get-serialno',
                       'adb get-devpath', 'adb remount', 'adb reboot',
                       'adb sideload ', 'adb root', 'adb unroot', 'adb usb',
                       'adb tcpip ', 'adb ppp ', 'adb sync notes']


# -------------取键盘指令，用在这里是为了控制ctrl+c不结束程序--------
def sigint_handler(signum, frame):  # 接受键盘信号
    pass


# 键盘信号捕获
# SIGINT is translated into a KeyboardInterrupt exception
signal.signal(signal.SIGINT, sigint_handler)


# -------------取键盘指令，用在这里是为了控制ctrl+c不结束程序--------

# 执行adb devices命令，获取设备列表在subprocess中处理可以取返回值
def deal_adb_devices(show=True):
    s = subprocess.Popen('adb devices', shell=False, stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    tips = s.communicate()
    outs = tips[0].split('\r\n')
    del adb_devices[:]
    for i, s in enumerate(outs):
        if s:
            adb_devices.append(s.split('\t')[0])
            if not i and show:
                print(s)
            if i and show:
                print i, '.', s


# 其他adb命令交与os处理
def deal_adb_command(command):
    os.system(command)


# 判断adb命令是否针对devices
def check_adb_command(input_s):
    for tmp_command in adb_default_command:
        if input_s.startswith(tmp_command):
            return True
    return False


# 等待交互输入
def wait_chose():
    while True:
        input_str = int(raw_input())
        try:
            if input_str >= len(adb_devices) or input_str == 0:
                print('please choose right device !')
            else:
                command = adb_command[0:3] + ' -s ' + \
                          adb_devices[input_str] + adb_command[3:len(adb_command)]
                command = re_fix_command(command)
                # print (command)
                deal_adb_command(command)
                break
        except Exception, e:
            print(e, '\n please input right number ! ')
            break


# 重新整合指令，替换掉|为空格，切对有空格的文件名加上“”
def re_fix_command(command):
    if sys.getfilesystemencoding() == 'mbcs':
        command = unicode(command, default_win_coding)
    if command[command.rfind(' ') + 1:].count(default_str) > 0:
        chg = '\"' + command.split(' ')[len(command.split(' ')) - 1] + '\"'
        return (command[:command.rfind(' ') + 1] + chg).replace(default_str, ' '). \
            encode(default_win_coding)
    else:
        return command


# adb_p:针对adb devices 结果操作
def adb_p(command):
    if command.startswith('adb devices'):
        deal_adb_devices()
    elif check_adb_command(command):
        global adb_command
        adb_command = command
        deal_adb_devices(show=False)
        if len(adb_devices) > 1:
            if len(adb_devices) == 2:
                command = adb_command[0:3] + ' -s ' + adb_devices[1] + adb_command[3:len(adb_command)]
                deal_adb_command(command)
                pass
            else:
                print 'chose devices to continue :'
                deal_adb_devices()
                wait_chose()
        else:
            print 'not connection device !'
    else:
        deal_adb_command(command)


class ADB_P(Cmd):
    def __init__(self):
        Cmd.__init__(self)
        self.adb_match = []
        self.tmp_match_count = 0

    @staticmethod
    def do_adb(line):
        adb_p('adb ' + line)

    def complete_adb(self, text, line, begidx, endidx):
        """ auto complete of file name.
        """
        # tmp_line = line.split(' ')
        if not check_input(line, self.adb_match):
            line = line.split(' ')
            # TODO 以后再考虑这块
            if len(line) < 3:
                filename = ''
                path = './'
            else:
                path = line[len(line) - 1]
                if (os.sep in path) and path:
                    i = path.rfind(os.sep)
                    filename = path[i + 1:]
                    path = path[:i]
                else:
                    filename = path
                    path = './'
            ls = dircache.listdir(path)
            ls = ls[:]  # for overwrite in annotate.
            dircache.annotate(path, ls)
            if filename == '':
                del self.adb_match[:]
                self.adb_match = map(deal_coding, ls)
            else:
                del self.adb_match[:]
                for f in ls:
                    try:
                        if f.startswith(filename):
                            self.adb_match.append(deal_coding(f))
                    except UnicodeDecodeError, e:
                        print(e)

            self.tmp_match_count = 0
        else:
            max_count = len(self.adb_match)
            now_count = self.tmp_match_count
            now_count += 1
            self.tmp_match_count = now_count % max_count

        return [self.adb_match[self.tmp_match_count]]

    @staticmethod
    def do_exit():
        sys.exit()


# 检测输入是否包含列表中的元素
def check_input(input_t, list_t):
    for li in list_t:
        try:
            c = len(input_t.split(' '))
            if input_t.split(' ')[c - 1].count(li) >= 1:
                return True
        except UnicodeDecodeError, e:
            print(e)
    return False


def deal_coding(f):
    if sys.getfilesystemencoding() == 'mbcs':
        return f.decode(default_win_coding).replace(' ', default_str)
    else:
        return f


def main():
    try:
        cmd = ADB_P()
        cmd.cmdloop()
    except BaseException, e:
        print e


if __name__ == '__main__':
    main()
