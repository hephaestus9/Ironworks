from flask import jsonify, render_template, session
from ironworks import serverTools
from ironworks.updater import checkGithub, Update
import ironworks

app = serverTools.getApp()
logger = serverTools.getLogger()
COMMITS_BEHIND = serverTools.getCommitsBehind()
COMMITS_COMPARE_URL = serverTools.getCommitsCompareURL()


@app.route('/xhr/update_bar')
def xhr_update_bar():
    if 'username' in session:
        if ironworks.COMMITS_BEHIND != 0:
            return render_template('includes/update_bar.html',
                commits=ironworks.COMMITS_BEHIND,
                compare_url=ironworks.COMMITS_COMPARE_URL,
            )
        else:
            return jsonify(up_to_date=True)
    else:
        return


@app.route('/xhr/updater/check')
def xhr_update_check():
    if 'username' in session:
        check = checkGithub()
        return jsonify(update=check)
    else:
        return


@app.route('/xhr/updater/update')
def xhr_update():
    if 'username' in session:
        updated = Update()
        if updated:
            logger.log('UPDATER :: Update complete', 'INFO')
        else:
            logger.log('UPDATER :: Update failed', 'ERROR')

        return jsonify(updated=updated)
    else:
        return
