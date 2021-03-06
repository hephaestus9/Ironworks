
from flask import jsonify, render_template, request, session
from ironworks.noneditable import *
from ironworks import serverTools
from modules_lib.bleextop import bleex

import hashlib

app = serverTools.getApp()
logger = serverTools.getLogger()
bleexSettings = serverTools.getBleexSettings()


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
            session['username'] = username
            return True
    else:
        # No user exists.
        return False


def validate(db, user, password):
    success = False
    password = hashlib.sha512(request.form['password']).hexdigest()
    # print password
    dbConn = db.getConn()
    if login(user, password, dbConn):
        success = True
        #tools.setUser(user)
    return success


def createLogin(db, user, password):
    success = False
    db.insertOrUpdate("users", {"username": user, "password": password})
    isValid = db.select("users", where={"username": user})
    if isValid:
        success = True
    return success


@app.route('/settingsLogin')
def settingsLogin():
    if 'username' in session:
        global bleexSettings
        if bleexSettings is None:
            bleexSettings = bleex.Bleex()
            serverTools.setBleexSettings(bleexSettings)
        return render_template('bleex/settingsLogin.html')
    return render_template('index.html')


@app.route('/settings_login', methods=['GET', 'POST'])
def settings_login():
    db = serverTools.getSystemDb()
    success = False

    if request.method == 'POST':
        user = request.form['username']
        password = request.form['password']
        #print password

        success = validate(db, user, password)

    if success:
        serverTools.setUser(user)
        return jsonify(success=success)
    return render_template('bleex/settingsLogin.html')


@app.route('/settings_create_login', methods=['GET', 'POST'])
def settings_create_login():
    db = serverTools.getSystemDb()
    success = False

    if request.method == 'POST':
        user = request.form['username']
        password = request.form['password']
        success = createLogin(db, user, password)

    if success:
        return jsonify(success=success)
    return render_template('bleex/settingsLogin.html')
