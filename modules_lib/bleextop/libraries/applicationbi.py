# -*- coding: utf-8 -*-
import tree
from modules_lib.bleextop.models import applicationdao
import datetime


class ApplicationBI:

    def __init__(self):
        self.appdao = applicationdao.ApplicationDAO()

    def getApplications(self, username):
        apps, confs = self.appdao.getApplications(username)
        #print apps
        thisTree = self.buildTree(apps, confs, "menu")
        return thisTree.getRoot()

    def getTree(self):
        apps, confs = self.appdao.getAllApps()
        #print apps, confs
        thisTree = self.buildTree(apps, confs, "children")
        return thisTree.getRoot()

    def saveApp(self, data):
        data["date_updated"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data["date_created"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.appdao.saveApp(data)
        appId = self.appdao.getInsertId()
        self.appdao.addPermissions(appId)

        return [{"success": True},
                {"application_k": id},
                {"message": "Application successfully saved"}]

    def updateApp(self, data):
        data["date_updated"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        success = self.appdao.updateApp(data)
        if success:
            return [{"success": True}, {"application_k": data["application_k"]}, {"message": "Application successfully updated"}]
        else:
            return [{"success": False}, {"message": "There was an error updating this application."}]

    def removeApp(self, application_k):
        self.appdao.removeApp(application_k)

    def moveApp(self, data):
        success = self.moveApp(data)
        if success:
            return [{"success": True}, {"message": "Application successfully moved"}]
        else:
            return [{"success": False}, {"message": "There was an error moving this application."}]

    def buildTree(self, apps, confs, text):
        temp = []
        count = 0
        #print apps
        for app in apps:
            iconCls = ""
            if app["configurations"]:
                conf = confs[count]
                if conf["iconCls"]:
                    iconCls = conf["iconCls"]
            temp.append({"text": app["name"],
                    "name": app["name"],
                    "application_k": app["application_k"],
                    "application_parent_k": app["application_parent_k"],
                    "klass": app["klass"],
                    "description": app["description"],
                    "configurations": app["configurations"],
                    "active": app["active"],
                    "iconCls": iconCls})
            count += 1

        # Creating the Tree
        thisTree = tree.Tree()
        thisTree.setChildProperty(text)
        thisTree.setIdProperty("application_k")
        for app in temp:
            #print app
            thisTree.addChild(app, app["application_parent_k"])

        return thisTree
