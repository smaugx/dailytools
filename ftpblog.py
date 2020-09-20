#!/usr/bin/python
# -*- coding: UTF-8 -*-


from ftplib import FTP
import os
import sys
import time
import socket


class MyFTP:
    """
        ftp自动下载、自动上传脚本，可以递归目录操作
        作者：欧阳鹏
        博客地址：http://blog.csdn.net/ouyang_peng/article/details/79271113
    """

    def __init__(self, host, port=21):
        """ 初始化 FTP 客户端
        参数:
                 host:ip地址
                 port:端口号
        """
        self.host = host
        self.port = port
        self.ftp = FTP()
        # 重新设置下编码方式
        self.ftp.encoding = 'gbk'
        self.log_file = open("log.txt", "a")
        self.file_list = []

    def login(self, username, password):
        """ 初始化 FTP 客户端
            参数:
                 username: 用户名
                 password: 密码
            """
        try:
            timeout = 60
            socket.setdefaulttimeout(timeout)
            # 0主动模式 1 #被动模式
            self.ftp.set_pasv(True)
            # 打开调试级别2，显示详细信息
            # self.ftp.set_debuglevel(2)

            self.debug_print('开始尝试连接到 {0}'.format(self.host))
            self.ftp.connect(self.host, self.port)
            self.debug_print('成功连接到 {0}'.format(self.host))

            self.debug_print('开始尝试登录到 {0}'.format(self.host))
            self.ftp.login(username, password)
            self.debug_print('成功登录到 {0}'.format(self.host))

            self.debug_print(self.ftp.welcome)
        except Exception as err:
            self.deal_error("FTP 连接或登录失败, 错误描述为：{0}".format(err))
            pass

    def is_same_size(self, local_file, remote_file):
        """判断远程文件和本地文件大小是否一致
           参数:
             local_file: 本地文件
             remote_file: 远程文件
        """
        try:
            remote_file_size = self.ftp.size(remote_file)
        except Exception as err:
            remote_file_size = -1

        try:
            local_file_size = os.path.getsize(local_file)
        except Exception as err:
            local_file_size = -1

        self.debug_print('local_file_size:{0}, remote_file_size:{1}'.format(local_file_size, remote_file_size))
        if remote_file_size == local_file_size:
            return 1
        else:
            return 0

    def download_file(self, local_file, remote_file):
        """从ftp下载文件
            参数:
                local_file: 本地文件

                remote_file: 远程文件
        """
        self.debug_print("download_file()---> local_path = {0},remote_path = {1}".format(local_file, remote_file))

        if self.is_same_size(local_file, remote_file):
            self.debug_print('{0} 文件大小相同, 无需下载'.format(local_file))
            return
        else:
            try:
                self.debug_print('>>>>>>>>>>>>下载文件 {0} ... ...'.format(local_file))
                buf_size = 1024
                file_handler = open(local_file, 'wb')
                self.ftp.retrbinary('RETR {0}'.format(remote_file), file_handler.write, buf_size)
                file_handler.close()
            except Exception as err:
                self.debug_print('下载文件出错，出现异常：{0}'.format(err))
                return

    def download_file_tree(self, local_path, remote_path):
        """从远程目录下载多个文件到本地目录
                       参数:
                         local_path: 本地路径
                         remote_path: 远程路径
        """
        print("download_file_tree()--->  local_path = {0} ,remote_path = {1}".format(local_path, remote_path))
        try:
            self.ftp.cwd(remote_path)
        except Exception as err:
            self.debug_print('远程目录 {0} 不存在，继续... 具体错误: {1}'.format(remote_path, err))
            return

        if not os.path.isdir(local_path):
            self.debug_print('本地目录 {0} 不存在，先创建本地目录'.format(local_path))
            os.makedirs(local_path)

        self.debug_print('切换至目录: {0}'.format(self.ftp.pwd()))

        self.file_list = []
        # 方法回调
        self.ftp.dir(self.get_file_list)

        remote_names = self.file_list
        self.debug_print('远程目录 列表: {0}'.format(remote_names))
        for item in remote_names:
            file_type = item[0]
            file_name = item[1]
            local = os.path.join(local_path, file_name)
            file_name = os.path.join(remote_path, file_name)
            print(file_name)
            if file_type == 'd':
                print("download_file_tree()---> 下载目录： {0}".format(file_name))
                self.download_file_tree(local, file_name)
            elif file_type == '-':
                print("download_file()---> 下载文件：{0}".format(file_name))
                self.download_file(local, file_name)
            self.ftp.cwd("..")
            self.debug_print('返回上层目录 {0}'.format(self.ftp.pwd()))
        return True

    def upload_file(self, local_file, remote_file):
        """从本地上传文件到ftp
           参数:
             local_path: 本地文件
             remote_path: 远程文件
        """
        if not os.path.isfile(local_file):
            self.debug_print('{0} 不存在'.format(local_file))
            return

        if self.is_same_size(local_file, remote_file):
            self.debug_print('跳过相等的文件: {0}'.format(local_file))
            return

        buf_size = 1024
        file_handler = open(local_file, 'rb')
        self.ftp.storbinary('STOR {0}'.format(remote_file), file_handler, buf_size)
        file_handler.close()
        self.debug_print('###################上传: {0} 成功########################'.format(local_file))

    def upload_file_tree(self, local_path, remote_path):
        """从本地上传目录下多个文件到ftp
           参数:
             local_path: 本地目录
             remote_path: 对应远程目录
        """
        if not os.path.isdir(local_path):
            self.debug_print('本地目录 {0} 不存在'.format(local_path))
            return

        try:
            self.ftp.cwd(remote_path)
        except Exception as e:
            self.ftp.mkd(remote_path)
            self.ftp.cwd(remote_path)

        self.debug_print('切换至远程目录: {0}'.format(self.ftp.pwd()))

        local_name_list = os.listdir(local_path)
        for local_name in local_name_list:
            src = os.path.join(local_path, local_name)
            dest = os.path.join(remote_path, local_name)
            if os.path.isdir(src):
                try:
                    self.ftp.mkd(dest)
                    self.debug_print("创建目录: {0}", dest)
                except Exception as err:
                    None
                self.debug_print("upload_file_tree()---> 上传目录： {0}".format(dest))
                self.upload_file_tree(src, dest)
            else:
                self.debug_print("upload_file_tree()---> 上传文件：{0}".format(local_name))
                self.upload_file(src, dest)
        self.ftp.cwd("..")
        self.debug_print("upload local:{0} to remote:{1} success".format(local_path, remote_path))

    def close(self):
        """ 退出ftp
        """
        self.debug_print("close()---> FTP退出")
        self.ftp.quit()
        self.log_file.close()

    def debug_print(self, s):
        """ 打印日志
        """
        self.write_log(s)

    def deal_error(self, e):
        """ 处理错误异常
            参数：
                e：异常
        """
        log_str = '发生错误: {0}'.format(e)
        self.write_log(log_str)
        sys.exit()

    def write_log(self, log_str):
        """ 记录日志
            参数：
                log_str：日志
        """
        time_now = time.localtime()
        date_now = time.strftime('%Y-%m-%d', time_now)
        format_log_str = "{0} ---> {1} \n ".format(date_now, log_str)
        print(format_log_str)
        #self.log_file.write(format_log_str)

    def get_file_list(self, line):
        """ 获取文件列表
            参数：
                line：
        """
        file_arr = self.get_file_name(line)
        # 去除  . 和  ..
        if file_arr[1] not in ['.', '..']:
            self.file_list.append(file_arr)

    def get_file_name(self, line):
        """ 获取文件名
            参数：
                line：
        """
        pos = line.rfind(':')
        while (line[pos] != ' '):
            pos += 1
        while (line[pos] == ' '):
            pos += 1
        file_arr = [line[0], line[pos:]]
        return file_arr


if __name__ == "__main__":
    my_ftp = MyFTP("yourblog.com")
    my_ftp.login("yourname", "yourpassword")

    # 下载单个文件
    #my_ftp.download_file("./local-search.js", "/wwwroot/js/local-search.js")

    # 下载目录
    # my_ftp.download_file_tree("./js", "/wwwroot/js")

    # 上传单个文件
    #my_ftp.upload_file("./temp.html", "/wwwroot/temp.html")
    #my_ftp.upload_file("./bourne_legacy.mp4", "/wwwroot/bourne_legacy.mp4")

    # 上传目录
    my_ftp.upload_file_tree("./site", "/wwwroot")

    my_ftp.close()
