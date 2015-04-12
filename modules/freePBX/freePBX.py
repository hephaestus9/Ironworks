# -*- coding: utf-8 -*-
from flask import render_template, session, request, jsonify, redirect, url_for
from flask.ext.api import status
import json
import hashlib
import ast
from ironworks import serverTools

app = serverTools.getApp()
logger = serverTools.getLogger()


def login(username, password, dbConn):
    # Using prepared Statements means that SQL injection is not possible.
    c = dbConn.cursor()
    if c.execute("""SELECT user_k, username, password FROM users WHERE username = %s LIMIT 1""", (username)) is not None:
        result = c.fetchone()
        try:
            username = result[1]
            db_password = result[2]
        except:
            logger.log("Failed login for Admin. User does not exits", "WARNING")
        if db_password == password:  # Check if the password in the database matches the password the user submitted.
            # Password is correct!
            session['user'] = username
            return True
    else:
        # No user exists.
        return False


def validate(db, user, password):
    success = False
    password = hashlib.sha512(request.form['password']).hexdigest()
    dbConn = db.getConn()
    if login(user, password, dbConn):
        success = True
        #tools.setUser(user)
    return success


@app.route('/freePBX_login', methods=['GET', 'POST'])
def freePBX_login():
    db = serverTools.getSystemDb()
    success = False
    if request.method == 'POST':
        user = request.form['username']
        password = request.form['password']
        success = validate(db, user, password)
    if success:
        serverTools.setUser(user)
        return jsonify(success=success)
    return render_template('freepbx/freepbxLogin.html')


@app.route('/freepbxLogin')
def freepbxLogin():
    if 'username' in session:
        """global cms
        if cms is None:
            cms = cmsSettings.Settings()
            serverTools.setCMSSettings(cms)
        status = serverTools.getPyEmoncmsLogin()
        if status["status"] is False:
            return render_template('house/houseLogin.html')"""
        return redirect(url_for('freepbx/views/welcome'))
        return redirect(url_for('freepbx/views/welcome_nomanager'))
    return render_template('index.html')


@app.route('/freePBX_welcome')
def freePBX_welcome():
    if 'username' in session:
        """status = serverTools.getPyEmoncmsLogin()
        if status["status"] is False:
            return redirect(url_for('freepbxLogin'))"""

        return render_template('freepbx/views/welcome.html')
    return render_template('index.html')


@app.route('/freePBX_welcome_nomanager')
def freePBX_welcome_nomanager():
    if 'username' in session:
        loginstatus = serverTools.getPyEmoncmsLogin()
        if loginstatus["status"] is False:
            return redirect(url_for('freepbx/freepbxLogin'))

        return render_template('freepbx/views/welcome_nomanager.html')
    return render_template('index.html')


@app.route('/freePBX_custom_destination')
def freePBX_custom_destination():
    if 'username' in session:
        """status = serverTools.getPyEmoncmsLogin()
        if status["status"] is False:
            return redirect(url_for('freepbxLogin'))"""

        return render_template('freepbx/modules/customappsreg/custom_destinations.html')
    return render_template('index.html')


@app.route('/freePBX_custom_extension')
def freePBX_custom_extension():
    if 'username' in session:
        """status = serverTools.getPyEmoncmsLogin()
        if status["status"] is False:
            return redirect(url_for('freepbxLogin'))"""

        return render_template('freepbx/modules/customappsreg/custom_extensions.html')
    return render_template('index.html')


@app.route('/freePBX_modules')
def freePBX_modules():
    if 'username' in session:
        """status = serverTools.getPyEmoncmsLogin()
        if status["status"] is False:
            return redirect(url_for('freepbxLogin'))"""

        return render_template('freepbx/modules.html')
    return render_template('index.html')


@app.route('/original_freePBX')
def original_freePBX():
    if 'username' in session:
        return render_template('freepbx/index.php')
    return render_template('index.html')
