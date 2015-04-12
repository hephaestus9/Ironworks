#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This is the main executable of Ironworks. It parses the command line arguments, does init and calls the start function of Ironworks."""

import sys
import os
from flask import Flask
from ironworks import server
from ironworks import preferences

app = Flask(__name__)
app.secret_key = 'your secret key goes here'


def getApp():
    return app


class IronworksMain():
    def __init__(self):
        # Set the rundir
        dataDir = self.ironworksRootPath()
        if not os.path.isdir(self.ironworksRootPath()):
                        os.mkdir(self.ironworksRootPath())
        rundir = self.get_rundir()

        # Include paths
        sys.path.insert(0, rundir)
        sys.path.insert(0, os.path.join(rundir, 'lib'))

        self.app = getApp()
        self.iwServer = None

        # If frozen, we need define static and template paths
        if self.check_frozen():
            self.app.root_path = rundir
            self.app.static_path = '/static'
            self.app.add_url_rule(
                self.app.static_path + '/<path:filename>',
                endpoint='static',
                view_func=self.app.send_static_file
            )

            from jinja2 import FileSystemLoader
            self.app.jinja_loader = FileSystemLoader(os.path.join(self.app.root_path, 'templates'))

        """Main function that is called at the startup of Ironworks."""
        self.started = False
        self.prefs = preferences.Prefs()

        from optparse import OptionParser

        p = OptionParser()

        # define command line options
        p.add_option('-p', '--port',
                     dest='port',
                     default=None,
                     help="Force webinterface to listen on this port")
        p.add_option('-d', '--daemon',
                     dest='daemon',
                     action='store_true',
                     help='Run as a daemon')
        p.add_option('--pidfile',
                     dest='pidfile',
                     help='Create a pid file (only relevant when running as a daemon)')
        p.add_option('--log',
                     dest='log',
                     help='Create a log file at a desired location')
        p.add_option('-v', '--verbose',
                     dest='verbose',
                     action='store_true',
                     help='Silence the logger')
        p.add_option('--develop',
                     action="store_true",
                     dest='develop',
                     help="Start instance of development server")
        p.add_option('--database',
                     dest='database',
                     help='Custom database file location')
        p.add_option('--webroot',
                     dest='webroot',
                     help='Web root for Ironworks')
        p.add_option('--host',
                     dest='host',
                     help='Web host for Ironworks')
        p.add_option('--kiosk',
                     dest='kiosk',
                     action='store_true',
                     help='Disable settings in the UI')
        p.add_option('--datadir',
                     dest='datadir',
                     help='Write program data to custom location')
        p.add_option('--noupdate',
                     action="store_true",
                     dest='noupdate',
                     help='Disable the internal updater')

        # parse command line for defined options
        options, args = p.parse_args()

        if options.datadir:
            data_dir = options.datadir
        else:
            data_dir = dataDir

        if options.verbose:
            VERBOSE = True
        else:
            val = self.prefs.getVerbose()
            if val == "True":
                VERBOSE = True
            else:
                VERBOSE = False

        if options.daemon:
            DAEMON = True
            VERBOSE = False
        else:
            val = self.prefs.getDaemon()
            if val == "True":
                DAEMON = True
                VERBOSE = False
            else:
                DAEMON = False

        if options.pidfile:
            PIDFILE = options.pidfile
            VERBOSE = False
        else:
            val = self.prefs.getPidFile()
            if val == "True":
                PIDFILE = self.prefs.getPidFilName()
                VERBOSE = False
            else:
                PIDFILE = None

        if options.port:
            PORT = int(options.port)
        else:
            PORT = self.prefs.getPort()  # 7000

        if options.log:
            LOG_FILE = options.log
        else:
            LOG_FILE = None

        if options.develop:
            DEVELOPMENT = True
        else:
            val = self.prefs.getDevelopment()
            if val == "True":
                DEVELOPMENT = True
            else:
                DEVELOPMENT = False

        if options.database:
            DATABASE = options.database
        else:
            DATABASE = os.path.join(dataDir, 'ironworks.db')

        if options.webroot:
            WEBROOT = options.webroot
        else:
            WEBROOT = ''

        if options.host:
            HOST = options.host
        else:
            HOST = '0.0.0.0'

        if options.kiosk:
            KIOSK = True
        else:
            val = self.prefs.getKiosk()
            if val == "True":
                KIOSK = True
            else:
                KIOSK = False

        if options.noupdate:
            UPDATER = False
        else:
            val = self.prefs.getNoUpdate()
            if val == "True":
                UPDATER = False
            else:
                UPDATER = False

        self.iwServer = server.IronworksServer(DAEMON,
                                                    VERBOSE,
                                                    PIDFILE,
                                                    self.app.root_path,
                                                    data_dir,
                                                    os.path.join(self.app.root_path, 'ironworks.py'),
                                                    sys.argv[1:],
                                                    PORT,
                                                    LOG_FILE,
                                                    DEVELOPMENT,
                                                    DATABASE,
                                                    WEBROOT,
                                                    HOST,
                                                    KIOSK,
                                                    UPDATER,
                                                    self.app)

        self.iwServer.initialize()
        userName = self.prefs.getLoginUser()
        host = self.prefs.getLoginHost()
        dbName = self.prefs.getLoginDbName()
        self.iwServer.setLoginDb(host, userName, dbName)

        userName = self.prefs.getSystemUser()
        host = self.prefs.getSystemHost()
        dbName = self.prefs.getSystemDbName()
        self.iwServer.setSystemDb(host, userName, dbName)

        userName = self.prefs.getPyEMONCMSUser()
        host = self.prefs.getPyEMONCMSHost()
        dbName = self.prefs.getPyEMONCMSDbName()
        self.iwServer.setPyEMONCMSDb(host, userName, dbName)

        if PIDFILE or DAEMON:
            self.iwServer.daemonize()

        self.import_modules()
        self.iwServer.init_updater()

        self.iwServer.start()

    # Check if frozen by py2exe
    def check_frozen(self):
        return hasattr(sys, 'frozen')

    def get_rundir(self):
        if self.check_frozen():
            return os.path.abspath(unicode(sys.executable, sys.getfilesystemencoding()))

        return os.path.abspath(__file__)[:-13]

    def ironworksRootPath(self):
        if sys.platform == "darwin":
                return os.path.expanduser("~/Library/Application Support/ironworks")
        elif sys.platform.startswith("win"):
                return os.path.join(os.environ['APPDATA'], "ironworks")
        else:
                return os.path.expanduser("~/.ironworks")

    def import_modules(self):
        """All modules that are available in Ironworks are at this point imported."""
        import modules


if __name__ == '__main__':
    ironworksApp = IronworksMain()
