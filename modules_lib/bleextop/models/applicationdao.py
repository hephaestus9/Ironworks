# -*- coding: utf-8 -*-
from flask import json
from ironworks import serverTools
from collections import OrderedDict
import ast


class ApplicationDAO:

    def __init__(self):
        self.db = serverTools.getSystemDb()

    def getApplications(self, username):
        joinDict = OrderedDict([("permissions P", "P.application_k=A.application_k"),
                                ("role_permissions RP", "RP.permission_k=P.permission_k"),
                                ("roles R", "R.role_k=RP.role_k"),
                                ("user_roles UR", "UR.role_k=R.role_k"),
                                ("users U", "U.user_k=UR.user_k")])
        result = self.db.select("applications A", what="A.*",
                        join=joinDict,
                        where=
                        {"U.username": username,
                        "P.action": "access",
                        "RP.value": "1"},
                        groupBy="A.application_k",
                        orderBy={"A.application_parent_k": "ASC"})
        apps = []
        confs = []
        for res in result:
            apps.append({"application_k": str(res[0]),
                         "application_parent_k": res[1],
                         "name": res[2],
                         "description": res[3],
                         "klass": res[4],
                         "configurations": json.dumps(ast.literal_eval(res[5]), ensure_ascii=False),
                         "date_created": res[6].strftime("%Y-%m-%d %H:%M:%S"),
                         "date_updated": res[7].strftime("%Y-%m-%d %H:%M:%S"),
                         "active": res[8]})
            confs.append(ast.literal_eval(res[5]))

        return apps, confs

    def getAllApps(self):
        result = self.db.select("applications")
        apps = []
        confs = []
        for res in result:
            apps.append({"application_k": str(res[0]),
                         "application_parent_k": res[1],
                         "name": res[2],
                         "description": res[3],
                         "klass": res[4],
                         "configurations": json.dumps(ast.literal_eval(res[5]), ensure_ascii=False),
                         "date_created": res[6].strftime("%Y-%m-%d %H:%M:%S"),
                         "date_updated": res[7].strftime("%Y-%m-%d %H:%M:%S"),
                         "active": res[8]})
            confs.append(ast.literal_eval(res[5]))
        return apps, confs

    def saveApp(self, data):
        """data = "application_parent_k": application_parent_k,
                    "name": name,
                    "description": description,
                    "klass": klass,
                    "configurations": configurations,
                    "date_created": dateCreated,
                    "date_updated": dateUpdated,
                    "active": active}"""
        self.db.beginTransaction()
        self.db.insert("applications", data)
        self.db.commitTransaction()

    def updateApp(self, data):
        """data = "application_parent_k": application_parent_k,
                    "name": name,
                    "description": description,
                    "klass": klass,
                    "configurations": configurations,
                    "date_created": dateCreated,
                    "date_updated": dateUpdated,
                    "active": active}"""
        self.db.beginTransaction()
        success = self.db.update("applications", data, where={"application_k": data["application_k"]})
        self.db.commitTransaction()
        return success

    def removeApp(self, application):
        """application = {"application_k": application_k}"""
        self.db.delete("applications", application)

    def moveApp(self, application, parentApplication):
        self.db.beginTransaction()
        self.db.update("applications", data={"application_parent_k": parentApplication}, where={"application_k": application})
        self.db.commitTransaction()

    def addPermissions(self, application_k, permissions):
        """"permissions = {"access": "Access",
                            "view": "View",
                            "list": "List",
                            "edit": "Edit",
                            "delete": "Delete",
                            "export": "Export",
                            "print": "Print" """

        for permission in permissions.keys():
            self.db.beginTransaction()
            self.db.insertOrUpdate("permissions", data={"application_k": application_k,
                                                        "action": permission,
                                                        "name": permissions[permission]},
                                                 where={"application_k": application_k,
                                                        "action": permission,
                                                        "name": permissions[permission]})
            self.db.commitTransaction()

    def getInsertId(self):
        result = self.db.query("SELECT LAST_INSERT_ID()")
        return result
