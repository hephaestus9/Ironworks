# -*- coding: utf-8 -*-
from flask import render_template, session, request, jsonify, redirect, url_for
from flask.ext.api import status
import json
import hashlib
import ast
from ironworks import serverTools
from ironworks.noneditable import *
from modules_lib.pyEMONCMS import cmsSettings
from modules_lib.pyEMONCMS.models.user import user_model
from modules_lib.pyEMONCMS.models.input import input_model
from modules_lib.pyEMONCMS.models.node import node_model

cms = serverTools.getCMSSettings()
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


@app.route('/house_login', methods=['GET', 'POST'])
def house_login():
    if 'username' in session:
        db = serverTools.getSystemDb()
        success = False
        if request.method == 'POST':
            user = request.form['username']
            password = request.form['password']
            success = validate(db, user, password)
        if success:
            serverTools.setUser(user)
            serverTools.setPyEmoncmsLogin(success, user)
            return jsonify(success=success)
        return render_template('house/houseLogin.html')
    return render_template('index.html')


@app.route('/pyemon_user')
def pyemon_user():
    if 'username' in session:
        status = serverTools.getPyEmoncmsLogin()
        if status["status"] is False:
            return redirect(url_for('houseLogin'))

        userModel = user_model.User()
        user = serverTools.getPyEmoncmsLogin()
        userId = userModel.get_id(user["user"])
        user = userModel.get_user(userId)
        username = user[1]
        email = user[2]
        writeKey = user[3]
        readKey = user[4]
        location = user[7]
        if int(user[8]) >= 0:
            timezone = "UTC +" + str(user[8])
        else:
            timezone = "UTC " + str(user[8])
        if user[9] == 'en_EN':
            language = 'American English'
        if user[10] is None:
            bio = ""
        else:
            bio = user[10]
        avatar = user[11]
        return render_template('house/pyemoncms/user.html',
                                                            username=username,
                                                            email=email,
                                                            writeKey=writeKey,
                                                            readKey=readKey,
                                                            location=location,
                                                            timezone=timezone,
                                                            language=language,
                                                            bio=bio,
                                                            avatar=avatar)
    return render_template('index.html')


@app.route('/houseLogin')
def houseLogin():
    if 'username' in session:
        global cms
        if cms is None:
            cms = cmsSettings.Settings()
            serverTools.setCMSSettings(cms)
        status = serverTools.getPyEmoncmsLogin()
        if status["status"] is False:
            return render_template('house/houseLogin.html')
        return redirect(url_for('pyemon_user'))
    return render_template('index.html')


@app.route('/pyemon_node')
def pyemon_node():
    if 'username' in session:
        status = serverTools.getPyEmoncmsLogin()
        if status["status"] is False:
            return redirect(url_for('houseLogin'))

        userModel = user_model.User()
        user = serverTools.getPyEmoncmsLogin()
        userId = userModel.get_id(user["user"])
        user = userModel.get_user(userId)
        username = user[1]
        email = user[2]
        writeKey = user[3]
        readKey = user[4]

        return render_template('house/pyemoncms/node.html',
                                                            username=username,
                                                            email=email,
                                                            writeKey=writeKey,
                                                            readKey=readKey)
    return render_template('index.html')


@app.route('/pyemon_node/create_node', methods=['GET', 'POST'])
def create_node():
    nodeModel = node_model.Node()
    if request.method == 'GET':
        if request.args['node']:
            node = ast.literal_eval(request.args['node'])
            success = nodeModel.createNode(node)
            return jsonify(success)
        else:
            return jsonify({'success': False})


@app.route('/pyemon_feeds')
def pyemon_feeds():
    if 'username' in session:
        status = serverTools.getPyEmoncmsLogin()
        if status["status"] is False:
            return redirect(url_for('houseLogin'))

        userModel = user_model.User()
        user = serverTools.getPyEmoncmsLogin()
        userId = userModel.get_id(user["user"])
        user = userModel.get_user(userId)
        username = user[1]
        email = user[2]
        writeKey = user[3]
        readKey = user[4]
        return render_template('house/pyemoncms/feeds.html',
                                                            username=username,
                                                            email=email,
                                                            writeKey=writeKey,
                                                            readKey=readKey)
    return render_template('index.html')


@app.route('/pyemon_input')
def pyemon_input():
    if 'username' in session:
        inputModel = input_model.Input()
        loginStatus = serverTools.getPyEmoncmsLogin()
        inputNames = []
        if loginStatus["status"] is False:
            return redirect(url_for('houseLogin'))

        userModel = user_model.User()
        user = serverTools.getPyEmoncmsLogin()
        userId = str(userModel.get_id(user["user"]))
        inputs = inputModel.getList(userId)
        for uniqueInput in inputs:
            for key in list(uniqueInput.keys()):
                inputNames.append(key)
        user = userModel.get_user(userId)
        username = user[1]
        email = user[2]
        writeKey = user[3]
        readKey = user[4]

        return render_template('house/pyemoncms/input.html',
                                                            inputs=inputs,
                                                            inputNames=inputNames,
                                                            username=username,
                                                            email=email,
                                                            writeKey=writeKey,
                                                            readKey=readKey)
    return render_template('index.html')


@app.route('/pyemon_input/post_json', methods=['GET', 'PUT', 'POST'])
def post_json():
    if request.method == 'GET' or request.method == 'PUT' or request.method == 'POST':
        try:
            # Post and Put
            data = ast.literal_eval(request.get_json())
            data = data['datastream'][0]

            cms = cmsSettings.Settings()
            writeKey = request.headers['I-ApiKey']
            userID = cms.getIDByWriteKey(writeKey)
            dataString = str(data['data'])
            inputString = ""
            for i in dataString:
                if i == "'":
                    inputString += "\\" + i
                else:
                    inputString += i
            inputID = cms.setInput(userID, data['name'], data['time'], inputString, data['description'], 'Null', 'Null')
            return jsonify({'Status Code': status.HTTP_200_OK, 'success': True, 'format': 'PUT||POST, json', 'Input ID': inputID})
        except:
            # Get
            try:
                if request.args['json']:
                    return jsonify({'Status Code': status.HTTP_200_OK, 'success': True, 'format': 'GET, json'})
            except:
                try:
                    if request.args['csv']:
                        try:
                            if request.args['node']:
                                print request.args['node']
                        except:
                            pass
                        try:
                            if request.args['time']:
                                print request.args['time']
                        except:
                            pass
                    return jsonify({'Status Code': status.HTTP_200_OK, 'success': True, 'format': 'GET, csv'})
                except:
                    pass
    return jsonify({'Status Code': status.HTTP_400_BAD_REQUEST, "body": {'success': False}})


@app.route('/pyemon_input/post_csv', methods=['GET', 'POST'])
def post_csv():
    pass


@app.route('/pyemon_input/bulk_json', methods=['GET', 'POST'])
def bulk_json():
    pass


@app.route('/pyemon_input/list_inputs', methods=['GET', 'POST'])
def list_inputs():
    pass


@app.route('/pyemon_input/delete_input', methods=['GET', 'POST'])
def delete_input():
    pass


@app.route('/pyemon_input/add_input', methods=['GET', 'POST'])
def add_input():
    pass


@app.route('/pyemon_input/move_input', methods=['GET', 'POST'])
def move_input():
    pass


@app.route('/pyemon_input/reset_input', methods=['GET', 'POST'])
def reset_input():
    pass


@app.route('/pyemon_vis')
def pyemon_vis():
    if 'username' in session:
        status = serverTools.getPyEmoncmsLogin()
        if status["status"] is False:
            return redirect(url_for('houseLogin'))

        userModel = user_model.User()
        user = serverTools.getPyEmoncmsLogin()
        userId = userModel.get_id(user["user"])
        user = userModel.get_user(userId)
        username = user[1]
        email = user[2]
        writeKey = user[3]
        readKey = user[4]
        return render_template('house/pyemoncms/vis.html',
                                                            username=username,
                                                            email=email,
                                                            writeKey=writeKey,
                                                            readKey=readKey)
    return render_template('index.html')


@app.route('/pyemon_dashboard')
def pyemon_dashboard():
    if 'username' in session:
        status = serverTools.getPyEmoncmsLogin()
        if status["status"] is False:
            return redirect(url_for('houseLogin'))

        userModel = user_model.User()
        user = serverTools.getPyEmoncmsLogin()
        userId = userModel.get_id(user["user"])
        user = userModel.get_user(userId)
        username = user[1]
        email = user[2]
        writeKey = user[3]
        readKey = user[4]
        return render_template('house/pyemoncms/dashboard.html',
                                                            username=username,
                                                            email=email,
                                                            writeKey=writeKey,
                                                            readKey=readKey)
    return render_template('index.html')


@app.route('/pyemon_myelectric')
def pyemon_myelectric():
    if 'username' in session:
        status = serverTools.getPyEmoncmsLogin()
        if status["status"] is False:
            return redirect(url_for('houseLogin'))

        userModel = user_model.User()
        user = serverTools.getPyEmoncmsLogin()
        userId = userModel.get_id(user["user"])
        user = userModel.get_user(userId)
        username = user[1]
        email = user[2]
        writeKey = user[3]
        readKey = user[4]
        return render_template('house/pyemoncms/myelectric.html',
                                                            username=username,
                                                            email=email,
                                                            writeKey=writeKey,
                                                            readKey=readKey)
    return render_template('index.html')


@app.route('/pyemon_api')
def pyemon_api():
    if 'username' in session:
        status = serverTools.getPyEmoncmsLogin()
        if status["status"] is False:
            return redirect(url_for('houseLogin'))

        userModel = user_model.User()
        user = serverTools.getPyEmoncmsLogin()
        userId = userModel.get_id(user["user"])
        user = userModel.get_user(userId)
        username = user[1]
        email = user[2]
        writeKey = user[3]
        readKey = user[4]
        return render_template('house/pyemoncms/api.html',
                                                            username=username,
                                                            email=email,
                                                            writeKey=writeKey,
                                                            readKey=readKey)
    return render_template('index.html')


@app.route('/pyemon_docs')
def pyemon_docs():
    if 'username' in session:
        status = serverTools.getPyEmoncmsLogin()
        if status["status"] is False:
            return redirect(url_for('houseLogin'))

        userModel = user_model.User()
        user = serverTools.getPyEmoncmsLogin()
        userId = userModel.get_id(user["user"])
        user = userModel.get_user(userId)
        username = user[1]
        email = user[2]
        writeKey = user[3]
        readKey = user[4]
        return render_template('house/pyemoncms/docs.html',
                                                            username=username,
                                                            email=email,
                                                            writeKey=writeKey,
                                                            readKey=readKey)
    return render_template('index.html')