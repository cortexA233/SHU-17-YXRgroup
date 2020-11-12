import requests
import hashlib
import json
import time
import client_config as cfg
import os
from User import User
from FileInfo import FileInfo
from urllib import parse
from matplotlib import pyplot as plt
import ast
import sys


class Client:

    def __init__(self):
        self.sess = requests.Session()
        self.user = User()

    def get_cmd_map(self):
        cmd_map = {
            'login': self.login,
            'list': self.query,
            'exit': self.exit,
            'exit_account': self.exit_account,
            'download': self.download,
            'upload': self.upload,
            'draw': self.draw_pic,
            # 中英文分界
            '登录': self.login,
            '查询': self.query,
            '退出': self.exit,
            '注销': self.exit_account,
            '下载': self.download,
            '上传': self.upload,
            '画图': self.draw_pic,
        }
        return cmd_map

    def register(self, username=None, password=None):
        pass

    def login(self, username=None, password=None):
        """
        登录网盘账号，具体操作为
        """
        def judge(txt):
            txt = json.loads(txt)
            if txt['status'] == 0:
                return True
            return False

        t1 = time.time()
        # 测试账号
        if username is None and password is None:
            username = 'test'
            password = 'testCyDrive'

        self.user = User()
        password = password.encode()
        psw_hashed = hashlib.sha256(hashlib.md5(password).digest()).digest()
        psw_str = ''
        for item in psw_hashed:
            psw_str = psw_str + str(int(item))
        # 处理响应
        login_response = self.sess.post(cfg.URLS['login'], data={'username': username, 'password': psw_str})
        print(login_response.headers, '!')
        login_dict = json.loads(login_response.text)
        print('login time: ', time.time() - t1)
        if judge(login_response.text):
            if username == 'test':
                self.user.username = username
                self.user.password = password
                return True, '测试账号登陆成功！' + login_dict['message']
            self.user.username = username
            self.user.password = password
            return True, '登陆成功！' + login_dict['message']
        return False, '登陆失败！' + login_dict['message']

    def query(self, path=''):
        lists_response = self.sess.get(cfg.URLS['list'] + path)
        print(lists_response.url)
        # 处理响应
        list_res = json.loads(lists_response.text)
        msg = '查询成功！'
        # print(list_res['data'])
        # list_res_dict = json.loads(list_res)
        # print(type(list_res['data']))
        que_dict = json.loads(list_res['data'])
        if list_res['status'] != 0:
            msg = '查询失败！' + list_res['message']
        if list_res['status'] == 0:
            for item in que_dict:
                print(item)
        return list_res['status'] == 0, msg

    def exit(self):
        print('886')
        exit(0)

    def exit_account(self):
        try:
            self.sess = requests.Session()
        except Exception as err:
            return False, '注销失败，错误信息：\n' + str(err)
        return True, '注销成功！'

    def download(self, path='123.txt'):
        t1 = time.time()
        if path.strip() == '':
            return False, '请输入下载文件路径！'
        download_response = self.sess.get(cfg.URLS['download'] + path, stream=True)
        print(download_response.text)
        status = 1
        try:
            response_dict = json.loads(download_response.text)
        except Exception as err:
            status = 0
            response_dict = {}
        print('download time: ', time.time() - t1)
        if status != 0:
            status = response_dict['status']
        else:
            file_content = download_response.content
            print(file_content)
            with open(os.path.join('download', path), 'wb') as dld_file:
                dld_file.write(file_content)

        if status != 0:
            msg = '下载失败！' + response_dict['message']
        else:
            msg = '下载成功！'
        return status == 0, msg

    def upload(self, path='123.txt'):
        with open(path, 'rb') as upload_file:
            upload_data = upload_file.read()
            file_info = os.stat(path)
        cur_file_info = FileInfo(file_info.st_mode, file_info.st_mtime, path, os.path.getsize(path)).json_dump()
        print(cur_file_info)
        cur_file_info = parse.quote(cur_file_info, safe='')
        # print((cur_file_info))
        upload_response = self.sess.put(cfg.URLS['upload'] + '123.txt', data=upload_data)
        print(upload_data)
        upload_res = upload_response.text
        upload_res_dict = json.loads(upload_res)
        if upload_res_dict['status'] == 0:
            return True, '上传成功！'
        return False, '上传失败！'

    def draw_pic(self, path='123.txt'):
        with open(path, 'r') as data_file:
            pic_data = data_file.read()
            pic_data = '[' + pic_data.replace('0', '').strip().replace(' ', ',') + ']'
        pic_data = ast.literal_eval(pic_data)
        print(pic_data)
        x_line = []
        for i in range(len(pic_data)):
            x_line.append(i)
        print(x_line)

        pic_data_r = []
        pic_data_g = []
        pic_data_b = []
        x_line_r = []
        x_line_g = []
        x_line_b = []
        cur_id = 0
        for item in pic_data:
            if item == 1:
                x_line_r.append(cur_id)
                pic_data_r.append(1)
            if item == 2:
                x_line_g.append(cur_id)
                pic_data_g.append(2)
            if item == 3:
                x_line_b.append(cur_id)
                pic_data_b.append(3)
            cur_id += 1

        if 'download/' in path:
            plt.title('DATA BASE')
        else:
            plt.title('HISTORY')
        plt.close('all')
        plt.bar(x_line_r, pic_data_r, color='r', align='center')
        plt.bar(x_line_g, pic_data_g, color='g', align='center')
        plt.bar(x_line_b, pic_data_b, color='b', align='center')

        plt.show()


if __name__ == '__main__':
    user = User()
    c = Client()
    # print(c.user.username, c.user.password)
    c.login()
    # print(c.user.username, c.user.password)
    c.upload()
    c.download()
    c.draw_pic_1()
