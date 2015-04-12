# -*- coding: utf-8 -*-
from ironworks import serverTools
import datetime


class RoleDAO:

    def __init__(self):
        self.db = serverTools.getSystemDb()

    def getAllRoles(self, limit=(0, 25)):
        result = self.db.query("select R.*,U.users from roles R left join (select R.role_k,count(R.role_k) as users from roles R join user_roles UR on UR.role_k=R.role_k group by R.role_k) U on U.role_k=R.role_k limit ?,?;", tuple=limit)
        return result

    def getUsersByRole(self, role_k):
        result = self.db.select("users U", what="U.*", join=[{"user_roles UR": "UR.user_k=U.user_k"}], where=[{"UR.role_k": role_k}])
        return result

    def getUserCount(self, role_k):
        result = self.db.query("select count(*) as total from roles R join user_roles UR on UR.role_k=R.role_k where R.role_k= ?", tuple=role_k)
        return result

    def getUserRole(self, data):
        result = self.db.select("user_roles", where=[{"role_k": data["role_k"]},
                                                     {"user_k": data["user_k"]}])
        return result

    def addUser(self, data):
        data["date_created"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.db.beginTransaction()
        self.db.insert("user_roles", data)
        self.db.commitTransaction()

    def saveRole(self, role):
        self.db.beginTransaction()
        self.db.insert("roles", role)
        self.db.commitTransaction()

    def updateRole(self, role):
        self.db.beginTransaction()
        self.db.update("roles", role, on=[{"role_k": role["role_k"]}])
        self.db.commitTransaction()

    def deleteRole(self, role):
        self.db.beginTransaction()
        self.db.delete("roles", where=[{"role_k": role["role_k"]}])
        self.db.commitTransaction()

    def getRoleByPermissions(self, permission_k):
        result = self.db.select("role_permissions RP", what="RP.*,R.name", join=[{"roles R": "R.role_k=RP.role_k"}], where=[{"RP.permission_k": permission_k}])
        return result
