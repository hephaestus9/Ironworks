# -*- coding: utf-8 -*-
from ironworks import serverTools
from collections import OrderedDict
import ast


class PermissionDAO:

    def __init__(self):
        self.db = serverTools.getSystemDb()

    def getPermission(self, perId):
        result = self.db.select("permissions", where={"permission_k": perId})
        permissions = []
        for res in result:
            permissions.append({"application_k": str(res[0]),
                         "application_parent_k": res[1],
                         "name": res[2],
                         "description": res[3],
                         "klass": res[4],
                         "configurations": ast.literal_eval(res[5]),
                         "date_created": res[6].strftime("%Y-%m-%d %H:%M:%S"),
                         "date_updated": res[7].strftime("%Y-%m-%d %H:%M:%S"),
                         "active": res[8]})
        return permissions

    def getAllPermissions(self):
        result = self.db.select("permissions")
        permissions = []
        for res in result:
            permissions.append({"application_k": str(res[0]),
                         "application_parent_k": res[1],
                         "name": res[2],
                         "description": res[3],
                         "klass": res[4],
                         "configurations": ast.literal_eval(res[5]),
                         "date_created": res[6].strftime("%Y-%m-%d %H:%M:%S"),
                         "date_updated": res[7].strftime("%Y-%m-%d %H:%M:%S"),
                         "active": res[8]})
        return permissions

    def savePermission(self, data):
        self.db.beginTransaction()
        self.db.insertOrUpdate("permissions", data)
        self.db.commitTransaction()

    def updatePermission(self, data):
        self.db.beginTransaction()
        self.db.update("permissions", data, on={"permission_k": data["permission_k"]})
        self.db.commitTransaction()

    def deletePermission(self, data):
        self.db.beginTransaction()
        self.db.delete("permissions", where={"permission_k": data["permission_k"]})
        self.db.commitTransaction()

    def getPermissionByApp(self, application_k):
        result = self.db.select("permissions", where={"application_k": application_k}, orderBy={"name ASC": "none"})
        permissions = []
        for res in result:
            permissions.append({"application_k": str(res[0]),
                         "application_parent_k": res[1],
                         "name": res[2],
                         "description": res[3],
                         "klass": res[4],
                         "configurations": ast.literal_eval(res[5]),
                         "date_created": res[6].strftime("%Y-%m-%d %H:%M:%S"),
                         "date_updated": res[7].strftime("%Y-%m-%d %H:%M:%S"),
                         "active": res[8]})
        return permissions

    def deleteRolePermissions(self, data):
        self.db.beginTransaction()
        self.db.delete("role_permissions", data, where={"role_permission_k": data["role_permission_k"]})
        self.db.commitTransaction()

    def updateRolePermissions(self, data):
        self.db.beginTransaction()
        self.db.update("role_permissions", data, on={"permission_k": data["permission_k"], "role_k": data["role_k"]})
        self.db.commitTransaction()

    def addRolePermissions(self, data):
        self.db.beginTransaction()
        self.db.insert("role_permissions", data)
        self.db.commitTransaction()

    def getRolePermissions(self, application_k):
        joinDict = OrderedDict([("roles R", "R.role_k=RP.role_k"),
                                ("permissions P", "P.permission_k=RP.permission_k")])

        result = self.db.select("role_permissions RP", what="RP.*",
                                join=joinDict,
                                where={"P.application_k": application_k})
        permissions = []
        for res in result:
            permissions.append({"application_k": str(res[0]),
                         "application_parent_k": res[1],
                         "name": res[2],
                         "description": res[3],
                         "klass": res[4],
                         "configurations": ast.literal_eval(res[5]),
                         "date_created": res[6].strftime("%Y-%m-%d %H:%M:%S"),
                         "date_updated": res[7].strftime("%Y-%m-%d %H:%M:%S"),
                         "active": res[8]})
        return permissions

    def getUserRoleAppPermission(self, data):
        joinDict = OrderedDict([("role_permissions RP", "RP.permission_k = P.permission_k"),
                                ("roles R", "R.role_k = RP.role_k"),
                                ("user_roles UR", "UR.role_k = R.role_k"),
                                ("users U", "U.user_k = UR.user_k")])

        result = self.db.select("permissions P", what="P.*, RP.value",
                                join=joinDict,
                                where={"P.application_k": data["application_k"],
                                       "U.user_k": data["user_k"]})
        permissions = []
        for res in result:
            permissions.append({"permission_k": str(res[0]),
                         "application_k": str(res[1]),
                         "action": res[2],
                         "name": res[3],
                         "description": res[4],
                         "value": res[5]})
        #print permissions

        return permissions
