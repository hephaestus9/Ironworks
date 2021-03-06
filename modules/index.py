from flask import render_template, request, session, redirect, url_for, jsonify
from datetime import timedelta
import hashlib
import time

from ironworks import serverTools, preferences

app = serverTools.getApp()
WEBROOT = serverTools.getWebroot()


def login(email, password, dbConn):
    # Using prepared Statements means that SQL injection is not possible.
    try:
        c = dbConn.cursor()
    except:
        prefs = preferences.Prefs()
        userName = prefs.getLoginUser()
        host = prefs.getLoginHost()
        dbName = prefs.getLoginDbName()
        severTools.resetLoginDb(host, userName, dbName)

        userName = prefs.getSystemUser()
        host = prefs.getSystemHost()
        dbName = prefs.getSystemDbName()
        serverTools.resetSystemDb(host, userName, dbName)

        userName = prefs.getPyEMONCMSUser()
        host = prefs.getPyEMONCMSHost()
        dbName = prefs.getPyEMONCMSDbName()
        serverTools.resetPyEMONCMSDb(host, userName, dbName)
        db = serverTools.getLoginDb()
        dbConn = db.getConn()
        c = dbConn.cursor()

    if c.execute("""SELECT id, username, password, salt FROM members WHERE email = %s LIMIT 1""", (email)) is not None:
        # (id, username, email, password, salt)
        result = c.fetchone()
        user_id = result[0]
        username = result[1]
        db_password = result[2]
        salt = result[3]
        #print result, user_id, username, db_password, salt
        password = hashlib.sha512(password + salt).hexdigest()  # hash the password with the unique salt.
        if checkbrute(user_id, dbConn) is True:
            # Account is locked
            # Send an email to user saying their account is locked
            return False
        elif db_password == password:  # Check if the password in the database matches the password the user submitted.
            # Password is correct!
            session['username'] = username
            #print 'Login successful.'
            return True
        else:
            # Password is not correct
            # We record this attempt in the database
            #print 'fail'
            now = int(time.time())
            c.execute("INSERT INTO login_attempts (user_id, time) VALUES (%s, %s)", (user_id, now))
            return False
    else:
        # No user exists.
        return False


def checkbrute(user_id, dbConn):
    c = dbConn.cursor()
    # Get timestamp of current time
    now = int(time.time())
    delta = 7200
    # All login attempts are counted from the past 2 hours.
    valid_attempts = now - delta
    # print valid_attempts
    if c.execute("SELECT time FROM login_attempts WHERE user_id = %s AND time > '%s'", (user_id, valid_attempts)) is not None:
        # Execute the prepared query.
        attempts = c.fetchall()
        # If there has been more than 5 failed logins
        if len(attempts) > 5:
            return True
        else:
            return False


@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=59)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500


@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('latestNews'))
    return render_template('index.html',
        webroot=WEBROOT)


@app.route('/process_login', methods=['GET', 'POST'])
def process_login():
    db = serverTools.getLoginDb()
    dbConn = db.getConn()
    if request.method == 'POST':
        user = request.form['email']
        password = hashlib.sha512(request.form['password']).hexdigest()

    if login(user, password, dbConn):
        return jsonify({"success": True})  # redirect(url_for('latestNews'))
    return jsonify({"success": False})  # render_template('index.html',
        #webroot=WEBROOT)
        #db_session.add(user)
        #flash('Thanks for registering')
        #return redirect(url_for('login'))
    #return render_template('register.html', form=form)
