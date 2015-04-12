# -*- coding: utf-8 -*-
from ironworks import serverTools


def highest_position(model):
    highest_position = 0

    items = model.query.all()

    for item in items:
        if item.position > highest_position:
            highest_position = item.position

    return highest_position + 1


class Setting():

    def __init__(self):
        """Table for one setting value"""
        self.configDb = serverTools.getPrefsDb()

        self.configDb.beginTransaction()

        self.configDb.checkTable("settings", [
            {"name": "id", "type": "integer primary key autoincrement"},
            {"name": "key", "type": "text"},
            {"name": "value", "type": "text"}])

        self.configDb.commitTransaction()

    def __repr__(self):
        return '<Setting %r>' % (self.key)

    def get_setting(self, key):
        """Get setting 'key' from db"""
        try:
            data = self.configDb.select("settings", where={"key": key})
            setting = data.fetchone()
            return setting
        except:
            return None

    def get_setting_value(self, key, default=None):
        """Get value for setting 'key' from db"""
        try:
            data = self.configDb.select("settings", where={"key": key}, what="value")
            value = data.fetchone()

            if value == '':
                return None

            #Strip http/https from hostnames
            if key.endswith('_host') or key.endswith('_ip'):
                if value.startswith('http://'):
                    return value[7:]
                elif value.startswith('https://'):
                    return value[8:]
            return value

        except:
            return default