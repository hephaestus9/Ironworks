# -*- coding: utf-8 -*-
from ironworks import serverTools


def highest_position(model):
    highest_position = 0

    items = model.query.all()

    for item in items:
        if item.position > highest_position:
            highest_position = item.position

    return highest_position + 1


class RecentlyAdded():

    def __init__(self, name, data=[]):
        # Check for ~/.ironworks
        configDb = serverTools.getPrefsDb()

        configDb.beginTransaction()

        configDb.checkTable("recently_added", [
            {"name": "id", "type": "integer primary key autoincrement"},
            {"name": "name", "type": "text"},
            {"name": "data", "type": "text"}])

        configDb.commitTransaction()

        self.name = name
        self.data = data

    def __repr__(self):
        return '<RecentlyAdded %r>' % (self.name)
