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


class Disk():

    def __init__(self, path, position=None):

        """Old diskspace module table. No longer in use."""
        # Check for ~/.ironworks
        if not os.path.isdir(configRootPath()):
            os.mkdir(configRootPath())

        configDb = ironworks.db.Db(os.path.join(configRootPath(), "config.db"))

        configDb.beginTransaction()

        configDb.checkTable("disks", [
            {"name": "id", "type": "integer primary key autoincrement"},
            {"name": "path", "type": "text"},
            {"name": "position", "type": "integer"}])

        configDb.commitTransaction()

        self.path = path

        if position is None:
            self.position = highest_position(Disk)
        else:
            self.position = position

    def __repr__(self):
        return '<Disk %r>' % (self.path)
