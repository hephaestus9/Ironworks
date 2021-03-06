from flask import render_template
from ironworks import serverTools
from ironworks.noneditable import *
from lib.pastebin.pastebin import PastebinAPI

app = serverTools.getApp()
LOG_FILE = serverTools.getLogFile()
LOG_LIST = serverTools.getLogList()
logger = serverTools.getLogger()


@app.route('/xhr/log')
def xhr_log():
    if 'username' in session:
        global LOG_LIST
        return render_template('dialogs/log_dialog.html',
            log=LOG_LIST,
        )
    else:
        return


@app.route('/xhr/log/pastebin')
def xhr_log_pastebin():
    if 'username' in session:
        global LOG_FILE
        logFile = open(LOG_FILE)
        log = []
        log_str = ''

        for line in reversed(logFile.readlines()):
            log.append(line.rstrip())
            log_str += line.rstrip()
            log_str += '\n'

        logFile.close()
        x = PastebinAPI()
        try:
            url = x.paste('feed610f82c2c948f430b43cc0048258', log_str)
            logger.log('LOG :: Log successfully uploaded to %s' % url, 'INFO')
        except Exception as e:
            logger.log('LOG :: Log failed to upload - %s' % e, 'INFO')

        return render_template('dialogs/log_dialog.html',
            log=log,
            url=url,
        )
    else:
        return
