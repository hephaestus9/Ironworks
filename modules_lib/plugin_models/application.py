# -*- coding: utf-8 -*-
import os
import sys

from ironworks import serverTools


def highest_position(model):
    highest_position = 0

    items = model.query.all()

    for item in items:
        if item.position > highest_position:
            highest_position = item.position

    return highest_position + 1


class Application():

    def __init__(self):
        """Table for one application in the applications module"""
        self.apps = serverTools.getPrefsDb()

        self.apps.beginTransaction()

        self.apps.checkTable("applications", [
            {"name": "id", "type": "integer primary key autoincrement"},
            {"name": "name", "type": "text"},
            {"name": "url", "type": "text"},
            {"name": "description", "type": "text"},
            {"name": "image", "type": "text"},
            {"name": "position", "type": "integer"}])

        self.apps.commitTransaction()

        """if position is None:
            self.position = highest_position(Application)
        else:
            self.position = position"""

    def getApplications(self, orderBy=False):
        cursor = self.apps.select("applications", orderBy)
        return cursor.fetchall()

    def getAppById(self, app):
        cursor = self.apps.select("applications", where={"id": app})
        return cursor.fetchone()

    def setApp(self, name, url, description, image, position):
        data = [
            {"name": name},
            {"url": url},
            {"description": description},
            {"image": image},
            {"position": position}]
        self.db.beginTransaction()
        self.db.insertOrUpdate("applications", data)
        self.db.commitTransaction()