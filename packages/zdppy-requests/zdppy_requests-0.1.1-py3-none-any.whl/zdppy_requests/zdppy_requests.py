#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/2/22 15:17
# @Author  : 张大鹏
# @Site    : 
# @File    : zdppy_requests.py
# @Software: PyCharm
from typing import Dict, List, Union
from .libs import requests
from zdppy_log import Log
from .exceptions import StatusCodeError, ParamError, EmptyError


class Requests:
    def __init__(self,
                 *,
                 host: str = "127.0.0.1",
                 port: int = 8888,
                 root_path: str = "",
                 username: str = None,  # 用户名
                 password: str = None,  # 密码
                 prefix: str = "http",
                 log_file_path: str = "logs/zdppy/zdppy_requests.log",
                 debug: bool = False):
        self.host = host
        self.port = port
        self.root_path = root_path
        self.prefix = prefix

        # 权限
        self.username = username
        self.password = password
        self.auth = None
        if self.username is not None and self.password is not None:
            self.auth = (username, password)

        # 基础路径
        self.url = f"{prefix}://{host}:{port}/{root_path}"
        if self.url.endswith("/"):  # 去除尾部空格
            self.url = self.url[:-1]

        # 初始化日志
        self.__log_file_path = log_file_path
        self.debug = debug
        self.log = Log(log_file_path=log_file_path, debug=debug)

    def get(self, path: str, query: Dict = None,
            headers: Dict = None,
            basic_auth: Dict = None,
            cookies=None):
        """
        发送GET请求
        :param path:
        :param query: 查询参数
        :param headers: 请求头
        :param cookies: cookie
        :return:
        """
        url = self.__get_url(path)
        self.log.info(f"正在发送GET请求：{url}")

        # 处理cookie
        if cookies is not None:
            cookies = requests.utils.dict_from_cookiejar(cookies)

        # 处理auth
        if basic_auth is not None:
            self.auth = (basic_auth.get("username"), basic_auth.get("password"))

        # 发送请求
        response = requests.get(url, auth=self.auth, params=query, headers=headers, cookies=cookies)
        return response

    def post(self, path: str, query: Dict = None, form: Dict = None, json: Dict = None, headers: Dict = None,
             cookies=None):
        """
        发送post请求
        :param path 请求路径
        :param query query查询参数
        :param form form表单参数
        :param json json请求体参数
        :param headers 请求头
        :param cookies cookies数据
        :return:
        """
        url = self.__get_url(path)
        self.log.info(f"正在发送POST请求：{url}")

        # 处理cookie
        if cookies is not None:
            cookies = requests.utils.dict_from_cookiejar(cookies)

        # 发送请求，获取响应
        response = requests.post(url, auth=self.auth, params=query, data=form,
                                 json=json, headers=headers, cookies=cookies)
        return response

    def put(self, path: str, query: Dict = None, form: Dict = None,
            json: Dict = None, headers: Dict = None, cookies=None):
        """
        发送put请求
        :return:
        """
        url = self.__get_url(path)
        self.log.info(f"正在发送PUT请求：{url}")

        # 处理cookie
        if cookies is not None:
            cookies = requests.utils.dict_from_cookiejar(cookies)

        # 发送请求，获取响应
        response = requests.put(url, auth=self.auth, params=query, data=form,
                                json=json, headers=headers, cookies=cookies)
        return response

    def delete(self, path: str, query: Dict = None, form: Dict = None,
               json: Dict = None, headers: Dict = None, cookies=None):
        """
        发送DELETE请求
        :return:
        """
        url = self.__get_url(path)
        self.log.info(f"正在发送DELETE请求：{url}")

        # 处理cookie
        if cookies is not None:
            cookies = requests.utils.dict_from_cookiejar(cookies)

        # 发送请求，获取响应
        response = requests.delete(url, auth=self.auth, params=query, data=form,
                                   json=json, headers=headers, cookies=cookies)
        return response

    def patch(self, path: str, query: Dict = None, form: Dict = None,
              json: Dict = None, headers: Dict = None, cookies=None):
        """
        发送PATCH请求
        :return:
        """
        url = self.__get_url(path)
        self.log.info(f"正在发送PATCH请求：{url}")

        # 处理cookie
        if cookies is not None:
            cookies = requests.utils.dict_from_cookiejar(cookies)

        # 发送请求，获取响应
        response = requests.patch(url, auth=self.auth, params=query, data=form,
                                  json=json, headers=headers, cookies=cookies)
        return response

    def __get_url(self, path):
        """
        根据path获取请求的URL路径
        :param path: 路径
        :return: url字符串
        """
        if path.startswith("/"):
            path = path[1:]
        if path.endswith("/"):
            path = path[:-1]
        url = f"{self.url}/{path}"
        return url

    def add(self, table: str, data: Dict, status_code: int = 200):
        """
        添加数据
        :return:
        """
        url = f"{self.url}/{table}"
        response = requests.post(url, json=data)

        # 校验状态码
        if response.status_code != status_code:
            raise StatusCodeError(f"期望状态码={status_code} 实际状态码={response.status_code}")

        # 返回数据
        return response.json()

    def find_by_page(self, table: str, offset: int = 0, size: int = 100, status_code: int = 200):
        """
        根据分页查询数据
        :return:
        """
        url = f"{self.url}/{table}"
        response = requests.get(url, data={"offset": offset, "size": size})

        # 校验状态码
        if response.status_code != status_code:
            raise StatusCodeError(f"期望状态码={status_code} 实际状态码={response.status_code}")

        # 返回数据
        return response.json()

    def find_by_id(self, table: str, id: int = 1, status_code: int = 200):
        """
        根据ID查询数据
        :return:
        """
        url = f"{self.url}/{table}/{id}"
        response = requests.get(url)

        # 校验状态码
        if response.status_code != status_code:
            raise StatusCodeError(f"期望状态码={status_code} 实际状态码={response.status_code}")

        # 返回数据
        return response.json()

    def delete_by_id(self, table: str, id: int = 1, status_code: int = 200):
        """
        根据ID查询数据
        :return:
        """
        url = f"{self.url}/{table}/{id}"
        response = requests.delete(url)

        # 校验状态码
        if response.status_code != status_code:
            raise StatusCodeError(f"期望状态码={status_code} 实际状态码={response.status_code}")

        # 返回数据
        return response.json()

    def update_by_id(self, table: str, id: int = 1, data: Dict = None, status_code: int = 200):
        """
        根据ID更新数据
        :return:
        """
        # 校验参数
        if data is None:
            raise ParamError(f"要更新的数据不能为空：data = {data}")

        # 准备url
        url = f"{self.url}/{table}/{id}"
        response = requests.patch(url, json=data)

        # 校验状态码
        if response.status_code != status_code:
            raise StatusCodeError(f"期望状态码={status_code} 实际状态码={response.status_code}")

        # 返回数据
        return response.json()

    def upload(self, path: str, upload_name: str, file_name: Union[str, List] = None):
        """
        上传文件
        :param path 上传的路径
        :param upload_name 上传的名字
        :param file_name 文件的名字，可以是一个字符串，也可以是一个列表
        """
        # 准备url
        url = self.__get_url(path)
        self.log.info(f"正在发送POST请求：{url}")

        # 准备文件
        files = {}

        # 单文件上传
        if isinstance(file_name, str):
            files[upload_name] = open(file_name, "rb")

        # 多文件上传
        elif isinstance(file_name, list):
            files = []
            for file in file_name:
                files.append((upload_name, (file, open(file, "rb"))))
            self.log.info(f"要上传的文件：{files}")
        else:
            raise EmptyError("要上传的文件不能为空")

        # 上传文件
        response = requests.post(url, files=files, verify=False)

        # 返回结果
        return response
