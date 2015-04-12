# -*- coding: utf-8 -*-

"""Ironworks module"""

import sys
import os
import subprocess
import threading
import keyring
from cherrypy import wsgiserver
from logger import IronworksLogger
from lib.apscheduler.scheduler import Scheduler
import serverTools


class IronworksServer:

    def __init__(self, DAEMON, VERBOSE, PIDFILE, RUNDIR, DATA_DIR, FULL_PATH, ARGS, PORT, LOG_FILE, DEVELOPMENT, DATABASE, WEBROOT, HOST, KIOSK, UPDATER, APP):
        self.FULL_PATH = FULL_PATH
        self.RUNDIR = RUNDIR
        self.ARGS = ARGS
        self.DAEMON = DAEMON
        self.PIDFILE = PIDFILE
        self.VERBOSE = VERBOSE
        self.LOG_FILE = LOG_FILE
        self.LOG_LIST = []
        self.PORT = PORT
        self.INIT_LOCK = threading.Lock()
        self.__INITIALIZED__ = False
        self.DEVELOPMENT = DEVELOPMENT
        self.SCHEDULE = Scheduler()
        self.DATABASE = DATABASE
        self.WEBROOT = WEBROOT
        self.logger = None
        self.SERVER = None
        self.HOST = HOST
        self.KIOSK = KIOSK
        self.DATA_DIR = DATA_DIR
        self.SCRIPT_DIR = None
        self.THREADS = []
        self.APP = APP

        self.AUTH = {
            'username': None,
            'password': None,
        }

        self.UPDATER = UPDATER
        self.USE_GIT = False
        self.version_file = None
        self.CURRENT_COMMIT = None
        self.LATEST_COMMIT = None
        self.COMMITS_BEHIND = 0
        self.COMMITS_COMPARE_URL = ''
        self.FIRST_RUN = 0

        serverTools.setApp(self.APP)
        serverTools.setWebroot(self.WEBROOT)
        serverTools.setRunDir(self.RUNDIR)
        serverTools.setDataDir(self.DATA_DIR)
        serverTools.setThreads(self.THREADS)
        serverTools.setHost(self.HOST)
        serverTools.setPort(self.PORT)
        serverTools.setPrefsDb(self.DATABASE)

    def initialize(self):
        """Init function for this module"""
        with self.INIT_LOCK:

            if self.__INITIALIZED__:
                return False

            # Set up logger
            if not self.LOG_FILE:
                self.LOG_FILE = os.path.join(self.DATA_DIR, 'logs', 'ironworks.log')

            FILENAME = os.path.basename(self.LOG_FILE)
            LOG_DIR = self.LOG_FILE[:-len(FILENAME)]

            if not os.path.exists(LOG_DIR):
                try:
                    os.makedirs(LOG_DIR)
                except OSError:
                    if self.VERBOSE:
                        print(('Unable to create the log directory.'))

            serverTools.setLogList(self.LOG_LIST)
            serverTools.setLogFile(self.LOG_FILE)
            self.logger = IronworksLogger(self.LOG_FILE, self.VERBOSE, self.DEVELOPMENT)
            serverTools.setLogger(self.logger)

            #set up script dir
            if not self.SCRIPT_DIR:
                self.SCRIPT_DIR = os.path.join(self.RUNDIR, 'scripts')

            if self.KIOSK:
                self.logger.log('Running in KIOSK Mode, settings disabled.', 'INFO')

            #Check if a version file exists. If not assume latest revision.
            self.version_file = os.path.join(self.DATA_DIR, 'Version.txt')
            if not os.path.exists(self.version_file):
                self.FIRST_RUN = 1
                serverTools.setFirstRun(self.FIRST_RUN)

            # check if database exists or create it
            try:
                self.logger.log('Checking if PATH exists: %s' % (self.DATABASE), 'WARNING')
                dbpath = os.path.dirname(self.DATABASE)
                if not os.path.exists(dbpath):
                    try:
                        self.logger.log('It does not exist, creating it...', 'WARNING')
                        os.makedirs(dbpath)
                    except:
                        self.logger.log('Could not create %s.' % (self.DATABASE), 'CRITICAL')
                        print(('Could not create %s.' % (self.DATABASE)))
                        quit()

            except:
                self.logger.log('Could not create %s.' % (self.DATABASE), 'CRITICAL')
                quit()

            self.logger.log('Database successfully initialised', 'INFO')

            if self.WEBROOT:
                if self.WEBROOT[0] != '/':
                    self.WEBROOT = '/' + self.WEBROOT
                d = wsgiserver.WSGIPathInfoDispatcher({self.WEBROOT: self.APP})
            else:
                d = wsgiserver.WSGIPathInfoDispatcher({'/': self.APP})
            self.SERVER = wsgiserver.CherryPyWSGIServer((self.HOST, self.PORT), d)

            self.__INITIALIZED__ = True
            return True

    def init_updater(self):
        from ironworks.updater import checkGithub, gitCurrentVersion

        if self.UPDATER:
            if os.name == 'nt':
                self.USE_GIT = False
            else:
                self.USE_GIT = os.path.isdir(os.path.join(self.RUNDIR, '.git'))
                if self.USE_GIT:
                    gitCurrentVersion()

            self.version_file = os.path.join(self.DATA_DIR, 'Version.txt')
            if os.path.isfile(self.version_file):
                f = open(self.version_file, 'r')
                self.CURRENT_COMMIT = f.read()
                f.close()
            else:
                self.COMMITS_BEHIND = -1

            threading.Thread(target=checkGithub).start()

            serverTools.setCommitsBehind(self.COMMITS_BEHIND)
            serverTools.setCommitsCompareURL(self.COMMITS_COMPARE_URL)
            serverTools.setUseGit(self.USE_GIT)
            serverTools.setCurrentCommit(self.CURRENT_COMMIT)

    def start_schedules(self):
        """Add all periodic jobs to the scheduler"""
        if self.UPDATER:
            # check every 6 hours for a new version
            from ironworks.updater import checkGithub
            self.SCHEDULE.add_interval_job(checkGithub, hours=6)
        self.SCHEDULE.start()

    def start(self):
        """Start the actual server"""
        if self.__INITIALIZED__:

            self.start_schedules()

            if not self.DEVELOPMENT:
                try:
                    self.logger.log('Starting IRONWORKS on %s:%i%s' % (self.HOST, self.PORT, self.WEBROOT), 'INFO')
                    self.SERVER.start()
                    while not True:
                        pass
                except KeyboardInterrupt:
                    self.stop()
            else:
                self.logger.log('Starting IRONWORKS development server on port: %i' % (self.PORT), 'INFO')
                self.logger.log(' ##### IMPORTANT : WEBROOT DOES NOT WORK UNDER THE DEV SERVER #######', 'INFO')
                self.APP.run(debug=True, port=self.PORT, host=self.HOST)

    def stop(self):
        """Shutdown Ironworks"""
        self.logger.log('Shutting down IRONWORKS...', 'INFO')

        if not self.DEVELOPMENT:
            self.SERVER.stop()
        else:
            from flask import request
            func = request.environ.get('werkzeug.server.shutdown')
            if func is None:
                raise RuntimeError('Not running with the Werkzeug Server')
            func()

        self.SCHEDULE.shutdown(wait=False)

        if self.PIDFILE:
            self.logger.log('Removing pidfile: %s' % str(self.PIDFILE), 'INFO')
            os.remove(self.PIDFILE)

    def restart(self):
        """Restart Ironworks"""
        self.SERVER.stop()
        popen_list = [sys.executable, self.FULL_PATH]
        popen_list += self.ARGS
        self.logger.log('Restarting IRONWORKS with: %s' % popen_list, 'INFO')
        self.SCHEDULE.shutdown(wait=False)
        subprocess.Popen(popen_list, cwd=self.RUNDIR)

    def daemonize(self):
        """Start Ironworks as a daemon"""
        if threading.activeCount() != 1:
            self.logger.log('There are %s active threads. Daemonizing may cause strange behavior.' % threading.activeCount(), 'WARNING')

        sys.stdout.flush()
        sys.stderr.flush()

        try:
            pid = os.fork()
            if pid == 0:
                pass
            else:
                self.logger.log('Forking once...', 'DEBUG')
                os._exit(0)
        except OSError as e:
            sys.exit('1st fork failed: %s [%d]' % (e.strerror, e.errno))

        os.chdir('/')
        os.umask(0)
        os.setsid()

        try:
            pid = os.fork()
            if pid > 0:
                self.logger.log('Forking twice...', 'DEBUG')
                os._exit(0)
        except OSError as e:
            sys.exit('2nd fork failed: %s [%d]' % (e.strerror, e.errno))

        pid = os.getpid()

        self.logger.log('Daemonized to PID: %s' % pid, 'INFO')
        if self.PIDFILE:
            self.logger.log('Writing PID %s to %s' % (pid, self.PIDFILE), 'INFO')
            file(self.PIDFILE, 'w').write("%s\n" % pid)

    def setLoginDb(self, host, userName, dbName):
        #userPassword = self.checkDbKey("Ironworks-Login-", userName)
        userPassword = 'your db key goes here'
        db = serverTools.getLoginDb()
        if db is None:
            serverTools.setLoginDb(host, userName, userPassword, dbName)

    def setSystemDb(self, host, userName, dbName):
        #userPassword = self.checkDbKey("Ironworks-MySQL-", userName)
        userPassword = 'your db key goes here'
        db = serverTools.getSystemDb()
        if db is None:
            serverTools.setSystemDb(host, userName, userPassword, dbName)

    def setPyEMONCMSDb(self, host, userName, dbName):
        #userPassword = self.checkDbKey("Ironworks-PyEMONCMS-", userName)
        userPassword = 'your db key goes here'
        db = serverTools.getPyEMONCMSDb()
        if db is None:
            serverTools.setPyEMONCMSDb(host, userName, userPassword, dbName)

    def checkDbKey(self, prefix, userName):
        userName = userName
        try:
            try:
                dbPassword = keyring.get_password(prefix + userName, userName)
            except:
                dbPassword = None

            if dbPassword is None:
                password = 'your db key goes here'
                keyring.set_password(prefix + userName, userName, password)
                self.logger.log('Initial database password added to keyring.', "INFO")
            elif str(dbPassword) == 'your db key goes here':
                self.logger.log('Initial database password in keyring.', "WARNING")
                self.logger.log('Please change your password.', "WARNING")
            else:
                self.logger.log('Userdefined database password set.', "INFO")
            return dbPassword
        except:
            self.logger.log('Either could not access keyring or an entry could not be made.', "ERROR")
            return ""
