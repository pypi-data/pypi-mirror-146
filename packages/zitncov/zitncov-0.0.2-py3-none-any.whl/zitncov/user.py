#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import requests
import json
from fuckzk import fuckzk 
from zitncov import endpoints


class zitUser:
    """ zit user object"""
    def __init__(self,username: str,password: str):
        self.session = requests.Session()
        self.username = username
        self.password = password

        self.verify = "{}_zit".format(username)
        

        # login the account
        try:
            self.post = self.__post()
        except:
            pass



        
    def __login(self):

        self.cook = fuckzk.getid(self.username,self.password)
        self.info = fuckzk.getme(self.username,self.cook)
        
    
    def __post(self):
        self.login = self.__login()
      
        self.__head = {
                'Content-Type': 'application/json',
                'Cookie': self.cook,
        }
        ## post
        try:
      
            respose = self.session.post(url=endpoints["sign"],
            json=self.info,
            headers=self.__head,
            ).json()
          
            if respose.get("errcode") == 0:
                print("Successfully")
            else:
                print("Already Clocked")

        except:
            return "Unknown"

        



        