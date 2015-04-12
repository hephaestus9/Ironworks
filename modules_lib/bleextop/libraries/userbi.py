# -*- coding: utf-8 -*-
from modules_lib.bleextop.models import userdao


class UserBI:

    def __init__(self):
        self.userdao = userdao.UserDAO()

    def getAllUsers(self):
        return self.userdao.getAllUsers()

    def getUser(self, username):
        return self.userdao.getUser({"username": username})

    def saveUser(self, data):
        pass
