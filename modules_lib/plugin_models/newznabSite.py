# -*- coding: utf-8 -*-
from ironworks import serverTools


def highest_position(model):
    highest_position = 0

    items = model.query.all()

    for item in items:
        if item.position > highest_position:
            highest_position = item.position

    return highest_position + 1


class NewznabSite():

    def __init__(self, name, url, apikey):

        configDb = serverTools.getPrefsDb()

        configDb.beginTransaction()

        configDb.checkTable("newznab", [
            {"name": "id", "type": "integer primary key autoincrement"},
            {"name": "name", "type": "text"},
            {"name": "url", "type": "text"},
            {"name": "apikey", "type": "string"}])

        configDb.commitTransaction()

        self.name = name
        self.url = url
        self.apikey = apikey

    def __repr__(self):
        return '<NewznabSite %r>' % (self.name)
