# -*- coding: utf-8 -*-
import os
import sys

import ironworks.db


def configRootPath():
    if sys.platform == "darwin":
            return os.path.expanduser("~/Library/Application Support/ironworks")
    elif sys.platform.startswith("win"):
            return os.path.join(os.environ['APPDATA'], "ironworks")
    else:
            return os.path.expanduser("~/.ironworks")


def highest_position(model):
    highest_position = 0

    items = model.query.all()

    for item in items:
        if item.position > highest_position:
            highest_position = item.position

    return highest_position + 1


class HardDisk():

    def __init__(self, data={}, position=None):
        """Table for one disk in the diskspace module"""
        # Check for ~/.ironworks
        if not os.path.isdir(configRootPath()):
            os.mkdir(configRootPath())

        configDb = ironworks.db.Db(os.path.join(configRootPath(), "config.db"))

        configDb.beginTransaction()

        configDb.checkTable("disks2", [
            {"name": "id", "type": "integer primary key autoincrement"},
            {"name": "data", "type": "text"},
            {"name": "position", "type": "integer"}])

        configDb.commitTransaction()

        self.data = data

        if position is None:
            self.position = highest_position(HardDisk)
        else:
            self.position = position

    def __repr__(self):
        return '<HardDisk %r>' % (self.position)
