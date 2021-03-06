# -*- coding: utf-8 -*-
# Copyright (c) 2006-2010, Jesse Liesch
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the author nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE IMPLIED
# DISCLAIMED. IN NO EVENT SHALL JESSE LIESCH BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import sys
import os

from ironworks import serverTools
from ironworks.database import db


class Prefs:
    @staticmethod
    def prefsRootPath():
        if sys.platform == "darwin":
            return os.path.expanduser("~/Library/Application Support/ironworks/")
        elif sys.platform.startswith("win"):
            # not tested
            return os.path.join(os.environ['APPDATA'], "ironworks")
        else:
            return os.path.expanduser("~/.ironworks/")

    def __init__(self, customDb=False):
        if customDb:
            self.db = customDb
            self.db.checkTable("prefs", [
                {"name": "name", "type": "text"},
                {"name": "value", "type": "text"}])
        else:
            # Check for ~/.ironworks
            if not os.path.isdir(self.prefsRootPath()):
                os.mkdir(self.prefsRootPath())

            if serverTools.getPrefsDb() is not None:
                self.db = serverTools.getPrefsDb()
            else:
                self.db = db.Db(os.path.join(self.prefsRootPath(), 'ironworks.db'))

            self.db.beginTransaction()

            self.db.checkTable("prefs", [
                {"name": "name", "type": "text"},
                {"name": "value", "type": "text"}])

            # Check basic defaults
            self.checkDefaults("timesRun", "0")
            self.checkDefaults("daemon", "False")
            self.checkDefaults("pidfile", "False")
            self.checkDefaults("pidFileName", "")
            self.checkDefaults("port", 7000)
            self.checkDefaults("verbose", "True")
            self.checkDefaults("development", "True")
            self.checkDefaults("kiosk", "False")
            self.checkDefaults("noupdate", "True")

            self.db.commitTransaction()

            self.db.checkTable("rss", [
                {"name": "name", "type": "text"},
                {"name": "value", "type": "text"}])

            self.db.checkTable("news", [
                {"name": "name", "type": "text"},
                {"name": "value", "type": "text"}])

            self.db.checkTable("xbmc_server", [
                {"name": "name", "type": "text"},
                {"name": "value", "type": "text"}])

            self.db.checkTable("login", [
                {"name": "name", "type": "text"},
                {"name": "value", "type": "text"}])

            self.db.checkTable("desktop", [
                {"name": "name", "type": "text"},
                {"name": "value", "type": "text"}])

            self.db.checkTable("pyemoncms", [
                {"name": "name", "type": "text"},
                {"name": "value", "type": "text"}])

            self.db.checkTable("freePBX", [
                {"name": "name", "type": "text"},
                {"name": "value", "type": "text"}])

            self.checkLoginDefaults("dbName", "ironworks_login")
            self.checkLoginDefaults("host", "localhost")
            self.checkLoginDefaults("user", "'db username'")
            self.checkLoginDefaults("password", "")

            self.checkDesktopDefaults("dbName", "desktop")
            self.checkDesktopDefaults("host", "localhost")
            self.checkDesktopDefaults("user", "db username")
            self.checkDesktopDefaults("password", "")

            self.checkPyEMONCMSDefaults("dbName", "pyemoncms")
            self.checkPyEMONCMSDefaults("host", "localhost")
            self.checkPyEMONCMSDefaults("user", "db username")
            self.checkPyEMONCMSDefaults("password", "")

            self.checkFreePBXDefaults("AMPDBNAME", "asterisk")
            self.checkFreePBXDefaults("AMPDBHOST", "localhost")
            self.checkFreePBXDefaults("AMPDBUSER", "asterisk username")
            self.checkFreePBXDefaults("AMPDBPASS", "asterisk db password")
            self.checkFreePBXDefaults("AMPDBENGINE", "mysql")
            self.checkFreePBXDefaults("datasource", "")  # for sqlite3
            self.checkFreePBXDefaults("action", "null")
            self.checkFreePBXDefaults("confirm_email", "")
            self.checkFreePBXDefaults("confirm_password", "")
            self.checkFreePBXDefaults("display", "")
            self.checkFreePBXDefaults("extdisplay", "False")
            self.checkFreePBXDefaults("email_address", "")
            self.checkFreePBXDefaults("fw_popover", "")
            self.checkFreePBXDefaults("fw_popover_process", "")
            self.checkFreePBXDefaults("logout", "False")
            self.checkFreePBXDefaults("password", "")
            self.checkFreePBXDefaults("quitemode", "")
            self.checkFreePBXDefaults("restrictmods", "False")
            self.checkFreePBXDefaults("skip", "0")
            self.checkFreePBXDefaults("skip_astman", "False")
            self.checkFreePBXDefaults("type", "")
            self.checkFreePBXDefaults("username", "")

    def checkDefaults(self, name, value):
        cursor = self.db.select("prefs", where={"name": name})
        if not cursor.fetchone():
            self.db.beginTransaction()
            self.db.insert("prefs", {"name": name, "value": value})
            self.db.commitTransaction()

    def checkLoginDefaults(self, name, value):
        cursor = self.db.select("login", where={"name": name})
        if not cursor.fetchone():
            self.db.beginTransaction()
            self.db.insert("login", {"name": name, "value": value})
            self.db.commitTransaction()

    def checkDesktopDefaults(self, name, value):
        cursor = self.db.select("desktop", where={"name": name})
        if not cursor.fetchone():
            self.db.beginTransaction()
            self.db.insert("desktop", {"name": name, "value": value})
            self.db.commitTransaction()

    def checkPyEMONCMSDefaults(self, name, value):
        cursor = self.db.select("pyemoncms", where={"name": name})
        if not cursor.fetchone():
            self.db.beginTransaction()
            self.db.insert("pyemoncms", {"name": name, "value": value})
            self.db.commitTransaction()

    def checkFreePBXDefaults(self, name, value):
        cursor = self.db.select("freePBX", where={"name": name})
        if not cursor.fetchone():
            self.db.beginTransaction()
            self.db.insert("freePBX", {"name": name, "value": value})
            self.db.commitTransaction()


    def checkXbmcDefaults(self, name, value):
        cursor = self.db.select("xbmc_server", where={"name": name})
        if not cursor.fetchone():
            self.db.beginTransaction()
            self.db.insert("xbmc_server", {"name": name, "value": value})
            self.db.commitTransaction()

    def getAllPrefs(self):
        res = self.db.select("prefs")
        return res.fetchall()

    def getAllRss(self):
        res = self.db.select("rss")
        return res.fetchall()

    def getAllNews(self):
        res = self.db.select("news")
        return res.fetchall()

    def getPreference(self, name):
        cursor = self.db.select("prefs", where={"name": name})
        row = cursor.fetchone()
        if not row:
            raise Exception("No preference " + name)
        return row["value"]

    def getRss(self, name):
        cursor = self.db.select("rss", where={"name": name})
        row = cursor.fetchone()
        if not row:
            raise Exception("No Rss feed named: " + name)
        return row["value"]

    def getNews(self, name):
        cursor = self.db.select("news", where={"name": name})
        row = cursor.fetchone()
        if not row:
            raise Exception("No news feed named: " + name)
        return row["value"]

    def getLogin(self, name):
        cursor = self.db.select("login", where={"name": name})
        row = cursor.fetchone()
        if not row:
            raise Exception("No Login property named: " + name)
        return row["value"]

    def getDesktop(self, name):
        cursor = self.db.select("desktop", where={"name": name})
        row = cursor.fetchone()
        if not row:
            raise Exception("No Bleextop property named: " + name)
        return row["value"]

    def getPyEMONCMS(self, name):
        cursor = self.db.select("pyemoncms", where={"name": name})
        row = cursor.fetchone()
        if not row:
            raise Exception("No PyEMONCMS property named: " + name)
        return row["value"]

    def getXbmc(self, name):
        cursor = self.db.select("xbmc_server", where={"name": name})
        row = cursor.fetchone()
        if not row:
            raise Exception("XBMC Server property named: " + name)
        if name == "position":
            return int(row["value"])
        return row["value"]

    def getLastXbmcServer(self):
        cursor = self.db.select("xbmc_server")
        row = cursor.fetchall()
        data = {}
        for e in row:
            data.update({str(e["name"]): str(e["value"])})
        position = data["position"]
        data["position"] = int(position)
        return data

    def getTimesRun(self):
        return int(self.getPreference("timesRun"))

    def getDaemon(self):
        return self.getPreference("daemon")

    def getPidFile(self):
        return self.getPreference("pidfile")

    def getPidFileName(self):
        return self.getPreference("pidFileName")

    def getPort(self):
        return int(self.getPreference("port"))

    def getVerbose(self):
        return self.getPreference("verbose")

    def getDevelopment(self):
        return self.getPreference("development")

    def getKiosk(self):
        return self.getPreference("kiosk")

    def getNoUpdate(self):
        return self.getPreference("noupdate")

    def getLoginDbName(self):
        return self.getLogin("dbName")

    def getLoginHost(self):
        return self.getLogin("host")

    def getLoginUser(self):
        return self.getLogin("user")

    def getLoginPassword(self):
        return self.getLogin("password")

    def getSystemDbName(self):
        return self.getDesktop("dbName")

    def getSystemHost(self):
        return self.getDesktop("host")

    def getSystemUser(self):
        return self.getDesktop("user")

    def getSystemPassword(self):
        return self.getDesktop("password")

    def getPyEMONCMSDbName(self):
        return self.getPyEMONCMS("dbName")

    def getPyEMONCMSHost(self):
        return self.getPyEMONCMS("host")

    def getPyEMONCMSUser(self):
        return self.getPyEMONCMS("user")

    def getPyEMONCMSPassword(self):
        return self.getPyEMONCMS("password")

    def getXbmcLabel(self):
        return self.getXbmc("label")

    def getXbmcPosition(self):
        return self.getXbmc("position")

    def getXbmcHostname(self):
        return self.getXbmc("hostname")

    def getXbmcPort(self):
        return self.getXbmc("port")

    def getXbmcUsername(self):
        return self.getXbmc("username")

    def getXbmcPassword(self):
        return self.getXbmc("password")

    def getXbmcMac(self):
        return self.getXbmc("mac_address")

    def incTimesRun(self):
        r = int(self.getPreference("timesRun"))
        self.db.beginTransaction()
        self.db.update("prefs", {"value": r + 1}, {"name": "timesRun"})
        self.db.commitTransaction()

    def setDaemon(self, value):
        self.db.beginTransaction()
        self.db.update("prefs", {"value": value}, {"name": "daemon"})
        self.db.commitTransaction()

    def setPidFile(self, value):
        self.db.beginTransaction()
        self.db.insertOrUpdate("prefs", {"value": value}, {"name": "pidfile"})
        self.db.commitTransaction()

    def setPidFileName(self, value):
        self.db.beginTransaction()
        self.db.insertOrUpdate("prefs", {"value": value}, {"name": "pidFileName"})
        self.db.commitTransaction()

    def setPort(self, port):
        self.db.beginTransaction()
        self.db.insertOrUpdate("prefs", {"value": port}, {"name": "port"})
        self.db.commitTransaction()

    def setVerbose(self, value):
        self.db.beginTransaction()
        self.db.insertOrUpdate("prefs", {"value": value}, {"name": "verbose"})
        self.db.commitTransaction()

    def setDevelopment(self, value):
        self.db.beginTransaction()
        self.db.update("prefs", {"value": value}, {"name": "development"})
        self.db.commitTransaction()

    def setKiosk(self, value):
        self.db.beginTransaction()
        self.db.update("prefs", {"value": value}, {"name": "kiosk"})
        self.db.commitTransaction()

    def setNoUpdate(self, value):
        self.db.beginTransaction()
        self.db.update("prefs", {"value": value}, {"name": "noupdate"})
        self.db.commitTransaction()

    def setLoginDbName(self, value):
        self.db.beginTransaction()
        self.db.update("login", {"value": value}, {"name": "dbName"})
        self.db.commitTransaction()

    def setLoginHost(self, value):
        self.db.beginTransaction()
        self.db.update("login", {"value": value}, {"name": "host"})
        self.db.commitTransaction()

    def setLoginUser(self, value):
        self.db.beginTransaction()
        self.db.update("login", {"value": value}, {"name": "user"})
        self.db.commitTransaction()

    def setLoginPassword(self, value):
        self.db.beginTransaction()
        self.db.update("login", {"value": value}, {"name": "password"})
        self.db.commitTransaction()

    def setSystemDbName(self, value):
        self.db.beginTransaction()
        self.db.update("desktop", {"value": value}, {"name": "dbName"})
        self.db.commitTransaction()

    def setSystemHost(self, value):
        self.db.beginTransaction()
        self.db.update("desktop", {"value": value}, {"name": "host"})
        self.db.commitTransaction()

    def setSystemUser(self, value):
        self.db.beginTransaction()
        self.db.update("desktop", {"value": value}, {"name": "user"})
        self.db.commitTransaction()

    def setSystemPassword(self, value):
        self.db.beginTransaction()
        self.db.update("desktop", {"value": value}, {"name": "password"})
        self.db.commitTransaction()

    def setPyEMONCMSDbName(self, value):
        self.db.beginTransaction()
        self.db.update("pyemoncms", {"value": value}, {"name": "dbName"})
        self.db.commitTransaction()

    def setPyEMONCMSHost(self, value):
        self.db.beginTransaction()
        self.db.update("pyemoncms", {"value": value}, {"name": "host"})
        self.db.commitTransaction()

    def setPyEMONCMSUser(self, value):
        self.db.beginTransaction()
        self.db.update("pyemoncms", {"value": value}, {"name": "user"})
        self.db.commitTransaction()

    def setPyEMONCMSPassword(self, value):
        self.db.beginTransaction()
        self.db.update("pyemoncms", {"value": value}, {"name": "password"})
        self.db.commitTransaction()

    def setXbmc(self, name, value):
        self.db.beginTransaction()
        self.db.update("xbmc_server", {"value": value}, {"name": name})
        self.db.commitTransaction()

    def setXbmcLabel(self, value):
        self.db.beginTransaction()
        self.db.update("xbmc_server", {"value": value}, {"name": "label"})
        self.db.commitTransaction()

    def setXbmcPosition(self, value):
        self.db.beginTransaction()
        self.db.update("xbmc_server", {"value": value}, {"name": "position"})
        self.db.commitTransaction()

    def setXbmcHostname(self, value):
        self.db.beginTransaction()
        self.db.update("xbmc_server", {"value": value}, {"name": "hostname"})
        self.db.commitTransaction()

    def setXbmcPort(self, value):
        self.db.beginTransaction()
        self.db.update("xbmc_server", {"value": value}, {"name": "port"})
        self.db.commitTransaction()

    def setXbmcUsername(self, value):
        self.db.beginTransaction()
        self.db.update("xbmc_server", {"value": value}, {"name": "username"})
        self.db.commitTransaction()

    def setXbmcPassword(self, value):
        self.db.beginTransaction()
        self.db.update("xbmc_server", {"value": value}, {"name": "password"})
        self.db.commitTransaction()

    def setXbmcMac(self, value):
        self.db.beginTransaction()
        self.db.update("xbmc_server", {"value": value}, {"name": "mac_address"})
        self.db.commitTransaction()

preferences = False
