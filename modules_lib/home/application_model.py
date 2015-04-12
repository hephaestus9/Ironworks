# -*- coding: utf-8 -*-
from flask import session
from ironworks import serverTools


class Application():

    def __init__(self):
        """Table for one application in the applications module"""
        self.bleex = serverTools.getSystemDb()

        self.bleex.beginTransaction()

        self.bleex.checkTable("home_applications", [
            {"name": "id", "type": "INT NOT NULL AUTO_INCREMENT PRIMARY KEY"},
            {"name": "name", "type": "text"},
            {"name": "url", "type": "text"},
            {"name": "description", "type": "text"},
            {"name": "image", "type": "text"},
            {"name": "position", "type": "integer"},
            {"name": "username", "type": "text"}])

        self.bleex.commitTransaction()

        """if position is None:
            self.position = highest_position(Application)
        else:
            self.position = position"""

    def getApplications(self, orderBy={"position": "DESC"}):
        applications = []
        application = {}
        cursor = self.bleex.select("home_applications", where={"username": session["username"]}, orderBy=orderBy)
        #((1L, 'Main Router', 'http://192.168.1.1', 'Main Home Router', '', 0L, 0L),)
        for app in cursor:
            application["id"] = app[0]
            application["name"] = app[1]
            application["url"] = app[2]
            application["description"] = app[3]
            application["img"] = app[4]
            application["position"] = app[5]
            applications.append(application)
            application = {}
        return applications

    def getAppById(self, app):
        application = {}
        app = self.bleex.select("home_applications", where={"id": app})[0]
        application["id"] = app[0]
        application["name"] = app[1]
        application["url"] = app[2]
        application["description"] = app[3]
        application["img"] = app[4]
        application["position"] = app[5]
        return application

    def setApp(self, name, url, description, image, position, username, app={}):
        if app != {}:
            self.bleex.beginTransaction()
            self.bleex.insertOrUpdate("home_applications", app, on={"url": url, "username": session["username"]})
            self.bleex.commitTransaction()
        else:
            data = {"name": name,
                    "url": url,
                    "description": description,
                    "image": image,
                    "position": position,
                    "username": username}

            self.bleex.beginTransaction()
            self.bleex.insertOrUpdate("home_applications", data, on={"url": url, "username": session["username"]})
            self.bleex.commitTransaction()
