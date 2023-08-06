# -*- coding: UTF-8 -*-
import requests
import fabric
import ftplib
import traceback
import time
import cchardet
from requests.auth import HTTPBasicAuth


def sftp_farbic_connect(sftp_host, sftp_user, sftp_password, try_num=3, connect_timeout=10, debug=False):
    """
        建立sftp连接
        :param:str sftp_host:
        :param:str sftp_user:
        :param:str sftp_password:
        :param:int try_num: 重试次数
        :param:int connect_timeout: 连接请求超时设置
        :param:bool debug:
        :return: sftp_con: sftp_con连接对象
    """
    sftp_con = ''
    for i in range(try_num):
        try:
            sftp_con = fabric.Connection(host=sftp_host, user=sftp_user, connect_kwargs={'password': sftp_password},
                                         connect_timeout=connect_timeout)
            return sftp_con
        except Exception as e:
            if debug:
                traceback.print_exc()
            time.sleep(2)

    return sftp_con


def ftp_connect(ftp_ip, ftp_port, ftp_user_id, ftp_password, try_num=3, timeout=10, debug=False):
    """
        建立ftp连接
        :param:str ftp_ip:
        :param:str ftp_port:
        :param:str ftp_user_id:
        :param:str ftp_password:
        :param:int try_num: 重试次数
        :param:int timeout: 连接请求超时设置
        :param:bool debug:
        :return: ftp_con: ftp_con连接对象
    """
    ftp_con = ftplib.FTP()
    for i in range(try_num):
        try:
            ftp_con.connect(ftp_ip, ftp_port, timeout=timeout)
            ftp_con.login(ftp_user_id, ftp_password)
            return ftp_con
        except Exception as e:
            if debug:
                traceback.print_exc()
            time.sleep(5)
    return ftp_con


def get_request_content(url, headers={}, timeout=5, try_num=3, auth_user_name='', auth_password='', binary=False, proxies={}, debug=False):
    """
        get请求
        :param:str url:
        :param:dict headers:
        :param:int timeout: 连接请求超时设置
        :param:int try_num: 重试次数
        :param:str auth_user_name:
        :param:str auth_password:
        :param:bool binary: 是否需要返回二进制
        :param:dict proxies:
        :param:bool debug:
        :return: res_content
    """
    res_content = ''
    request_info = {"url": url, "timeout": timeout}
    if headers:
        request_info["headers"] = headers
    if auth_user_name and auth_password:
        auth = HTTPBasicAuth(auth_user_name, auth_password)
        request_info["auth"] = auth
    if proxies:
        request_info["proxies"] = proxies
    for i in range(try_num):
        try:
            res = requests.get(**request_info)
            if binary:
                res_content = res.content
            else:
                encoding_type = cchardet.detect(res.content)["encoding"]
                res_content = res.content.decode(encoding_type)
            return res_content
        except Exception as e:
            if debug:
                traceback.print_exc()
            time.sleep(5)
    return res_content
