# -*- coding: utf-8 -*-
from modules_lib.bleextop.models import roledao, permissiondao
import datetime
import re


class PermissionBI:

    def __init__(self):
        self.permission = permissiondao.PermissionDAO()
        self.role = roledao.RoleDAO()

    def getAllPermissions(self):
        return self.permission.getAllPermissions()

    #/**
    #* Return the application permissions for the given user
    #* @params data An array containing the user model and the application_id
    #* @return Array containing the permissions and success property
    #**/

    def getByUserApplication(self, data):
        permissions = {}
        # //get permissions generic permissions by role
        result = self.permission.getUserRoleAppPermission({"application_k": data["application_k"],
                                                           "user_k": data["user_k"]})

        #//@TODO query the database here to get especific permissions on this user

        for r in result:
            #//Collaboration by @joel-e
            if r["action"] in permissions or r["value"] == 1:
                permissions[r["action"]] = r["value"]
        #print permissions
        return {"success": True,
                "data": permissions}

    #/**
    #* Return the permissions for the given application
    #* @params application_k The id application
    #* @return Array containing the application permissions and a success property
    #**/

    def getByApplication(self, application_k):
        rows = []
        permissions = self.permissions.getByApplication(application_k)
        actives = self.permissions.getRolePermissions(application_k)

        for permission in permissions:
            rows.append({"permission_k": permission["permission_k"],
                         "permission": permission["name"]})
        result = []
        for row in rows:
            for role in actives:
                if role["permission_k"] == row["permission_k"]:
                    row["role_" + role["role_k"]] = role["value"]
            result.append(row)

        return {"success": True,
                "data": result}

    def updatePermissions(self, permissions):
        for p in permissions:
            obj = {}
            obj["permission_k"] = p["permission_k"]
            obj["date_created"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # //remove this permission from all roles
            roles = self.role.getByPermissions(p["permission_k"])
            for role in roles:
                self.permission.deleteRolePermissions(role)

            #//add this permission to each role
            for key in p.keys():
                match = re.find("/^role_/", key)
                if match:
                    obj["role_k"] = key[5:]
                    obj["value"] = p[key]
                    self.permissions.addRolePermissions(obj)

        return {"success": True,
                "message": "Permissions successfully saved"}
