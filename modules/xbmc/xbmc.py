# -*- coding: utf-8 -*-
from flask import render_template, session, request, jsonify, redirect, url_for
from flask.ext.api import status
from ironworks import serverTools

from modules_lib.xbmc import xbmc_server

xbmc = xbmc_server.XBMCServer()
app = serverTools.getApp()
logger = serverTools.getLogger()


@app.route('/xbmc_home')
def xbmc_home():
    if 'username' in session:
        xbmc = xbmc_server.XBMCServer()
        servers = xbmc.getXBMCServers()
        selected = False
        selected_server = None
        for server in servers:
            if server["active_server"] == 'True':
                selected = True
                selected_server = server
        return render_template('xbmc/xbmc/xbmc.html',
                                servers=servers,
                                selected=selected,
                                selected_server=selected_server)
    return render_template('index.html')


@app.route('/xbmc_add_server_dialog')
def xbmc_add_server_dialog():
    if 'username' in session:
        return add_edit_server_dialog()
    return render_template('index.html')


@app.route('/xbmc_edit_server_dialog/<server_id>')
def xbmc_edit_server_dialog(server_id):
    if 'username' in session:
        return add_edit_server_dialog(server_id)
    return render_template('index.html')


def add_edit_server_dialog(server_id=None):
    if 'username' in session:
        global xbmc
        server = None

        if server_id:
            server = xbmc.getServerById(server_id)

        return render_template('xbmc/dialogs/server_settings_dialog.html',
                                server=server)
    return render_template('index.html')


@app.route('/xbmc_add_edit_server', methods=['GET', 'POST'])
def xbmc_add_edit_server():
    if 'username' in session:
        label = request.form['label']
        position = request.form['position']
        hostname = request.form['hostname']
        port = request.form['port']
        xbmc_username = request.form['username']
        xbmc_password = request.form['password']
        mac_address = request.form['mac_address']

        if label == '' or hostname == '' or port == '':
            return jsonify({'status': 'error'})

        global xbmc
        if 'server_id' in request.form:
            server = xbmc.getServerById(request.form['server_id'])
            server.label = label
            server.position = position
            server.hostname = hostname
            server.port = port
            server.xbmc_username = xbmc_username
            server.xbmc_password = xbmc_password
            server.mac_address = mac_address
            xbmc.setXBMCServer(server)
        else:
            server = xbmc.setXBMCServer(label=label,
                                        position=position,
                                        hostname=hostname,
                                        port=port,
                                        xbmc_username=xbmc_username,
                                        xbmc_password=xbmc_password,
                                        mac_address=mac_address)

        return redirect(url_for('xbmc_home'))
    return render_template('index.html')


@app.route('/xbmc_delete_server/<server_id>', methods=['POST'])
def xbmc_delete_server(server_id):
    global xbmc
    if 'username' in session:
        try:
            server = xbmc.getServerById(server_id)
            xbmc.deleteServer(server)
        except:
            return jsonify({'status': 'error'})

        return redirect(url_for('xbmc_home'))
    return render_template('index.html')


@app.route('/xbmc_select_server/<server_id>')
def xbmc_select_server(server_id):
    global xbmc
    if 'username' in session:
        servers = xbmc.getXBMCServers()
        for server in servers:
            server["active_server"] = "False"
            xbmc.setXBMCServer(server["label"], server["hostname"], server=server)

        server = xbmc.getServerById(server_id)
        server["active_server"] = "True"
        xbmc.setXBMCServer(server["label"], server["hostname"], server=server)

        return redirect(url_for('xbmc_home'))
    return render_template('index.html')


