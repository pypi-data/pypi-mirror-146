"""
damei scp 配置好目标机器，同步文件
usage:
    dmscp siyuan ./xxx.zip  # 默认是上传 -u --upload, siyuan是配置好的服务器
    dmscp siyuan -d ./xxx.zip -d # 下载 -d --download

"""
import os, sys
import argparse

class RemoteServer(object):
    """远程服务器"""
    def __init__(self, host, port, user, password):
        self.host = host
        self.port = port
        self.user = user
        self.password = password


class DmSCP(object):
    def __init__(self):
        pass

    def upload(self, src, dst):
        pass

    def download(self, src, dst):
        pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='damei scp')
    parser.add_argument('server', help='server name')
    pass






