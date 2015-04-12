# -*- coding: utf-8 -*-
from flask import session
import netifaces as nif
from ironworks import serverTools


class XBMCServer():

    def __init__(self):

        """Table for the XBMC server config"""

        self.bleex = serverTools.getSystemDb()

        self.bleex.beginTransaction()

        self.bleex.checkTable("xbmc_servers", [
            {"name": "id", "type": "INT NOT NULL AUTO_INCREMENT PRIMARY KEY"},
            {"name": "label", "type": "text"},
            {"name": "position", "type": "text"},
            {"name": "hostname", "type": "text"},
            {"name": "port", "type": "text"},
            {"name": "xbmc_username", "type": "text"},
            {"name": "xbmc_password", "type": "text"},
            {"name": "mac_address", "type": "text"},
            {"name": "active_server", "type": "text"},
            {"name": "username", "type": "text"}])

        self.bleex.commitTransaction()

    def getNumXbmcServers(self):
        serverList = self.bleex.select("xbmc_servers")
        servers = len(serverList)
        return servers

    def getXBMCServers(self, orderBy={"position": "DESC"}):
        servers = []
        serverDict = {}
        serverList = self.bleex.select("xbmc_servers", where={"username": session["username"]}, orderBy=orderBy)
        for server in serverList:
            serverDict["id"] = server[0]
            serverDict["label"] = server[1]
            serverDict["position"] = server[2]
            serverDict["hostname"] = server[3]
            serverDict["port"] = server[4]
            serverDict["xbmc_username"] = server[5]
            serverDict["xbmc_password"] = server[6]
            serverDict["mac_address"] = server[7]
            serverDict["active_server"] = server[8]
            servers.append(serverDict)
            serverDict = {}
        return servers

    def getServerById(self, server_id):
        serverDict = {}
        server = self.bleex.select("xbmc_servers", where={"username": session["username"], "id": server_id})[0]
        serverDict["id"] = server[0]
        serverDict["label"] = server[1]
        serverDict["position"] = server[2]
        serverDict["hostname"] = server[3]
        serverDict["port"] = server[4]
        serverDict["xbmc_username"] = server[5]
        serverDict["xbmc_password"] = server[6]
        serverDict["mac_address"] = server[7]
        serverDict["active_server"] = server[8]
        return serverDict

    def deleteServer(self, server_id):
        self.bleex.delete("xbmc_servers", where={"username": session["username"], "id": server_id})
        return

    def setXBMCServer(self, label, hostname, port='8080', xbmc_username="", xbmc_password="", mac_address="", position="0", active_server="False", server={}):
        if server != {}:
            self.bleex.beginTransaction()
            self.bleex.insertOrUpdate("xbmc_servers", server, on={"mac_address": mac_address, "hostname": hostname, "username": session["username"]})
            self.bleex.commitTransaction()
        else:
            if mac_address == "":
                mac_address = self.mac_for_ip(hostname)

            data = {"label": label,
                    "position": position,
                    "hostname": hostname,
                    "port": port,
                    "xbmc_username": xbmc_username,
                    "xbmc_password": xbmc_password,
                    "mac_address": mac_address,
                    "active_server": active_server,
                    "username": session["username"]}

            self.bleex.beginTransaction()
            self.bleex.insertOrUpdate("xbmc_servers", data, on={"mac_address": mac_address, "hostname": hostname, "username": session["username"]})
            self.bleex.commitTransaction()

    def mac_for_ip(self, ip):
        'Returns a list of MACs for interfaces that have given IP, returns None if not found'
        for i in nif.interfaces():
            addrs = nif.ifaddresses(i)
            try:
                if_mac = addrs[nif.AF_LINK][0]['addr']
                if_ip = addrs[nif.AF_INET][0]['addr']
            except IndexError, KeyError: #ignore ifaces that dont have MAC or IP
                if_mac = if_ip = None
            if if_ip == ip:
                return if_mac
        return ""
