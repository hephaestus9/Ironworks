from flask import jsonify, render_template, session, redirect, url_for

from ironworks import serverTools, feedparser
from ironworks.tools import *
from modules_lib.home import application_model

app = serverTools.getApp()
RUNDIR = serverTools.getRunDir()
appModel = application_model.Application()


def parseFeeds():
    # Feeds

    google_url = 'https://news.google.com/news?pz=1&cf=all&ned=us&siidp=a3761a02c7bb42a6b2f9e47806ce78c4bb0d&ict=ln&output=rss'
    wallStreet_url = 'http://online.wsj.com/xml/rss/3_7014.xml'
    techNews_url = "http://www.technewsworld.com/perl/syndication/rssfull.pl"
    linuxNews_url = "http://www.linuxinsider.com/perl/syndication/rssfull.pl"

    google_feeds = feedparser.parse(google_url)
    wallStreet_feeds = feedparser.parse(wallStreet_url)
    techNews_feeds = feedparser.parse(techNews_url)
    linuxNews_feeds = feedparser.parse(linuxNews_url)
    return google_feeds, wallStreet_feeds, techNews_feeds, linuxNews_feeds


@app.route('/applications')
def applications():
    if 'username' in session:
        global appModel
        applications = appModel.getApplications()
        new_tab = '1'  # get_setting_value('app_new_tab') == '1'
        google, wallStreet, tech, linux = parseFeeds()

        return render_template('home/applications.html',
            applications=applications,
            new_tab=new_tab,
            googleFeed=google,
            wallStreetFeed=wallStreet,
            techNewsFeed=tech,
            linuxNewsFeed=linux)

    return render_template('index.html')


@app.route('/home_add_application_dialog')
def home_add_application_dialog():
    if 'username' in session:
        return add_edit_application_dialog()
    return render_template('index.html')


@app.route('/home_edit_application_dialog/<application_id>')
def home_edit_application_dialog(application_id):
    if 'username' in session:
        return add_edit_application_dialog(application_id)
    return render_template('index.html')


def add_edit_application_dialog(application_id=None):
    if 'username' in session:
        global appModel
        app = None

        rundir = RUNDIR + '/static/images/applications'

        icons = get_file_list(
            folder=rundir,
            extensions=['.png', '.jpg'],
            prepend_path=False)

        if application_id:
            app = appModel.getAppById(application_id)

        return render_template('home/dialogs/add_edit_application_dialog.html',
                                                                                application=app,
                                                                                icons=icons)
    return render_template('index.html')


@app.route('/home_add_edit_application', methods=['GET', 'POST'])
def home_add_edit_application():
    if 'username' in session:
        name = request.form['name']
        url = request.form['url']
        description = request.form['description']
        image = request.form['image']
        position = request.form['position']

        if name == '' or url == '':
            return jsonify({'status': 'error'})

        global appModel
        if 'application_id' in request.form:
            app = appModel.getAppById(request.form['application_id'])
            app.name = name
            app.url = url
            app.description = description
            app.image = image
            app.position = position
            appModel.setApp(app)
        else:
            app = appModel.setApp(name=name,
                                    url=url,
                                    description=description,
                                    image=image,
                                    position=position)

        return redirect(url_for('applications'))
    return render_template('index.html')


@app.route('/home_delete_application/<application_id>', methods=['POST'])
def home_delete_application(application_id):
    global appModel
    if 'username' in session:
        try:
            app = appModel.getAppById(application_id)
            db.delete(app)
            db.commit()

        except:
            return jsonify({'status': 'error'})

        return redirect(url_for('applications'))
    return render_template('index.html')


@app.route('/home_show_application/<application_id>')
def home_show_application(application_id):
    global appModel
    if 'username' in session:
        app = None
        message = None

        try:
            app = appModel.getAppById(application_id)

        except:
            message = 'Could not display application page'

        return render_template('application_window.html',
            message=message,
            application=app)
    return render_template('index.html')
