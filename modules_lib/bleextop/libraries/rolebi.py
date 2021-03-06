# -*- coding: utf-8 -*-
from modules_lib.bleextop.models import roledao, userdao


class RoleBI:

    def __init__(self):
        self.role = roledao.RoleDAO()
        self.user = userdao.UserDAO()

    def addUser(self, data):
        user = self.role.getUserRole(data)
        success = True
        if len(user) == 0:
            success = self.role.addUser(data)
        if success:
            obj = self.role.getUserCount(data["role_k"])
            return {"success": True, "total": obj["total"], "message": "User successfully added to the role"}
        else:
            return {"success": False, "message": "There was an error adding the user to the role, please try again"}

    def getAllUsers(self):
        return self.user.getAllUsers()

    def getUsersByRole(self, role_k):
        return self.role.getUserByRole(role_k)
