# -*- coding: utf-8 -*-

from flask import jsonify, render_template, request, session, redirect, url_for
from ironworks.noneditable import *
from modules_lib.bleextop.libraries import applicationbi, permissionbi
from ironworks import serverTools

app = serverTools.getApp()
user = None


@app.route('/settings')
def settings():
    if 'username' in session:
        return render_template('bleex/settings.html')
    return render_template('index.html')


@app.route('/config_desktop', methods=['GET', 'POST'])
def configDesktop():
    if 'username' in session:
        global user
        user = serverTools.getUser()
        app = applicationbi.ApplicationBI()
        config = {"wallpaper": "static/bleextop/resources/wallpapers/background.png"}
        applications = app.getApplications(user["username"])
        #print applications
        configuration = {"dock": "bottom",
                         "user": user,
                         "config": config,
                         "applications": applications,
                         "success": True}
        return jsonify(configuration)
    return render_template('index.html')


@app.route('/permission_by_application', methods=['GET', 'POST'])
def getPermissionForCurrentUserApplication():
    if 'username' in session:
        permission = permissionbi.PermissionBI()
        application_k = request.values["application_k"]
        r = permission.getByUserApplication({"user_k": user["user_k"],
                                             "application_k": application_k})
        return jsonify(r)
    return render_template('index.html')


@app.route('/get_active_applications', methods=['GET', 'POST'])
def getActiveApplications():
    if 'username' in session:
        app = applicationbi.ApplicationBI()
        # print request.values
        dataList = False
        if "list" in request.values:
            dataList = request.values["list"]
        if dataList:
            result = {"data": dataList}

        else:
            result = {"text": "Applications",
                      "expanded": True,
                      "children": app.getTree(),
                      "success": True}
        return jsonify(result)
    return render_template('index.html')


@app.route('/save_application', methods=['GET', 'POST'])
def saveApplication():
    if 'username' in session:
        pass
    return render_template('index.html')


@app.route('/remove_application', methods=['GET', 'POST'])
def removeApplication():
    if 'username' in session:
        pass
    return render_template('index.html')


@app.route('/move_application', methods=['GET', 'POST'])
def moveApplication():
    if 'username' in session:
        pass
    return render_template('index.html')


@app.route('/get_all_roles', methods=['GET', 'POST'])
def getAllRoles():
    if 'username' in session:
        pass
    return render_template('index.html')


@app.route('/save_roles', methods=['GET', 'POST'])
def saveRoles():
    if 'username' in session:
        pass
    return render_template('index.html')


@app.route('/remove_role', methods=['GET', 'POST'])
def removeRole():
    if 'username' in session:
        pass
    return render_template('index.html')


@app.route('/settings_logout')
def settingsLogout():
    serverTools.setUser(None)
    return redirect(url_for('latestNews'))


@app.route('/add_rss', methods=['GET', 'POST'])
def add_rss():
    if 'username' in session:
        if request.method == 'POST':
            return render_template('feeds.html')
    return render_template('index.html')


@app.route('/add_news', methods=['GET', 'POST'])
def add_news():
    if 'username' in session:
        pass
    return render_template('index.html')


@app.route('/edit_rss', methods=['GET', 'POST'])
def edit_rss():
    if 'username' in session:
        pass
    return render_template('index.html')


@app.route('/edit_news', methods=['GET', 'POST'])
def edit_news():
    if 'username' in session:
        pass
    return render_template('index.html')
