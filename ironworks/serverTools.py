# -*- coding: utf-8 -*-
import keyring
from ironworks.database import mDb, db

app = None
rundir = None
datadir = None
logger = None
webroot = ""
log_list = []
log_file = ""
commits_behind = 0
latest_commit = None
current_commit = None
commits_compare_url = ""
use_git = False
first_run = 0
threads = []
host = '0.0.0.0'
port = 7000
database = None
loginDatabase = None
systemDatabase = None
pyemoncmsDatabase = None
user = None
cmsSettings = None
bleexSettings = None
adminLogin = False
pyemoncmsLogin = False
pyemoncmsUser = None


def setApp(APP):
    global app
    app = APP


def getApp():
    global app
    return app


def setRunDir(RUNDIR):
    global rundir
    rundir = RUNDIR


def getRunDir():
    global rundir
    return rundir


def setDataDir(DATA_DIR):
    global datadir
    datadir = DATA_DIR


def getDataDir():
    global datadir
    return datadir


def setLogger(LOGGER):
    global logger
    logger = LOGGER


def getLogger():
    global logger
    return logger


def setWebroot(WEBROOT):
    global webroot
    webroot = WEBROOT


def getWebroot():
    global webroot
    return webroot


def setLogList(LOG_LIST):
    global log_list
    log_list = LOG_LIST


def getLogList():
    global log_list
    return log_list


def setLogFile(LOG_FILE):
    global log_file
    log_file = LOG_FILE


def getLogFile():
    global log_file
    return log_file


def setCommitsBehind(COMMITS_BEHIND):
    global commits_behind
    commits_behind = COMMITS_BEHIND


def getCommitsBehind():
    global commits_behind
    return commits_behind


def setCommitsCompareURL(COMMITS_COMPARE_URL):
    global commits_compare_url
    commits_compare_url = COMMITS_COMPARE_URL


def getCommitsCompareURL():
    global commits_compare_url
    return commits_compare_url


def setUseGit(USE_GIT):
    global use_git
    use_git = USE_GIT


def getUseGit():
    global use_git
    return use_git


def setLatestCommit(LATEST_COMMIT):
    global latest_commit
    latest_commit = LATEST_COMMIT


def getLatestCommit():
    global latest_commit
    return latest_commit


def setCurrentCommit(CURRENT_COMMIT):
    global current_commit
    current_commit = CURRENT_COMMIT


def getCurrentCommit():
    global current_commit
    return current_commit


def setFirstRun(FIRST_RUN):
    global first_run
    first_run = FIRST_RUN


def getFirstRun():
    global first_run
    return first_run


def setThreads(THREADS):
    global threads
    threads = THREADS


def getThreads():
    global threads
    return threads


def setHost(HOST):
    global host
    host = HOST


def getHost():
    global host
    return host


def setPort(PORT):
    global port
    port = PORT


def getPort():
    global port
    return port


def setAdminLogin(val):
    global adminLogin
    adminLogin = val


def getAdminLogin():
    global adminLogin
    return adminLogin


def setPyEmoncmsLogin(val, user):
    global pyemoncmsLogin, pyemoncmsUser
    pyemoncmsLogin = val
    pyemoncmsUser = user


def getPyEmoncmsLogin():
    global pyemoncmsLogin, pyemoncmsUser
    status = {"user": pyemoncmsUser, "status": pyemoncmsLogin}
    return status


#sqlite database-------------------------------------------------------------------------
def setPrefsDb(DATABASE):
    global database
    database = db.Db(DATABASE)


def getPrefsDb():
    global database
    return database


#mysql database----------------------------------------------------------------------------
def setLoginDb(host, userName, dbPassword, dbName):
    global loginDatabase, logger
    loginDatabase = mDb.Db(host, userName, dbPassword, dbName, logger)


def getLoginDb():
    global loginDatabase
    return loginDatabase


def setSystemDb(host, userName, dbPassword, dbName):
    global systemDatabase, logger
    systemDatabase = mDb.Db(host, userName, dbPassword, dbName, logger)


def getSystemDb():
    global systemDatabase
    return systemDatabase


def setPyEMONCMSDb(host, userName, dbPassword, dbName):
    global pyemoncmsDatabase, logger
    pyemoncmsDatabase = mDb.Db(host, userName, dbPassword, dbName, logger)


def getPyEMONCMSDb():
    global pyemoncmsDatabase
    return pyemoncmsDatabase


#Settings - Bleextop----------------------------------------------------------------------
def setUser(username):
    global user
    if username is not None:
        result = systemDatabase.select("users", where={"username": username})
        user = result[0]
        userDict = {}
        userDict["user_k"] = str(user[0])
        userDict["username"] = user[1]
        userDict["email"] = user[3]
        userDict["name"] = user[4]
        userDict["lastname"] = user[5]
        userDict["avatar"] = user[6]
        userDict["active"] = user[7]
        user = userDict
    else:
        user = username
    return user


def getUser():
    return user


def setCMSSettings(cms):
    global cmsSettings
    cmsSettings = cms


def getCMSSettings():
    global cmsSettings
    return cmsSettings


def setBleexSettings(bleex):
    global bleexSettings
    bleexSettings = bleex


def getBleexSettings():
    global bleexSettings
    return bleexSettings


#Try to fix the "Oerationalrror: (2006 MySQL server has gone away.)"
def checkDbKey(prefix, userName):
    userName = userName
    try:
        dbPassword = keyring.get_password(prefix + userName, userName)
        if dbPassword is None:
            password = 'your db password'
            keyring.set_password(prefix + userName, userName, password)
            logger.log('Initial database password added to keyring.', "INFO")
        elif str(dbPassword) == 'your db password':
            logger.log('Initial database password in keyring.', "WARNING")
            logger.log('Please change your password.', "WARNING")
        else:
            logger.log('Userdefined database password set.', "INFO")
        return dbPassword
    except:
        logger.log('Either could not access keyring or an entry could not be made.', "ERROR")
        return ""


def resetLoginDb(host, userName, dbName):
    userPassword = checkDbKey("Ironworks-Login-", userName)
    setLoginDb(host, userName, userPassword, dbName)


def resetSystemDb(host, userName, dbName):
    userPassword = checkDbKey("Ironworks-MySQL-", userName)
    setSystemDb(host, userName, userPassword, dbName)


def resetPyEMONCMSDb(host, userName, dbName):
    userPassword = checkDbKey("Ironworks-PyEMONCMS-", userName)
    setPyEMONCMSDb(host, userName, userPassword, dbName)
