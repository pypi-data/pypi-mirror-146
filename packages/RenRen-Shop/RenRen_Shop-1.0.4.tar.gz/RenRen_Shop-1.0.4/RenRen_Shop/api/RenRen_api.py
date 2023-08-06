# -*- coding: utf-8 -*-
"""
@Time : 2022/3/30 14:27 
@Author : YarnBlue 
@description : 
@File : RenRen_api.py
"""
import requests

from RenRen_Shop.api.url.url import URL


class RenRenApi:
    """
    __init__复用

    """
    def __init__(self, session: requests.Session, **kwargs):
        self.session = session
        self.URL = URL()
        self.kwargs = kwargs
