# -*- coding: utf-8 -*-
"""This file contains the descriptions and settings for all modules. Also it contains functions to add modules and so on"""

try:
    import json
except ImportError:
    import simplejson as json

from flask import jsonify, render_template, request
# from ironworks.database import db_session

import ironworks
import copy

from ironworks import serverTools
from ironworks.tools import *

from modules_lib.plugin_models.module import Module
from modules_lib.plugin_models.xbmcServer import XbmcServer
from modules_lib.plugin_models.recentlyAdded import RecentlyAdded
from modules_lib.plugin_models.newznabSite import NewznabSite

app = serverTools.getApp()
logger = serverTools.getLogger()

# name, label, description, and static are not user-editable and are taken from here
# poll and delay are user-editable and saved in the database - the values here are the defaults
# settings are also taken from the database - the values here are defaults
# if static = True then poll and delay are ignored


@app.route('/xhr/add_module_dialog')
def add_module_dialog():
    if 'username' in session:
        """Dialog to add a new module to Ironworks"""
        modules_on_page = Module.query.all()
        available_modules = copy.copy(AVAILABLE_MODULES)

        # filter all available modules that are not currently on the page
        for module_on_page in modules_on_page:
            for available_module in available_modules:
                if module_on_page.name == available_module['name']:
                    available_modules.remove(available_module)
                    break

        return render_template('dialogs/add_module_dialog.html',
            available_modules=available_modules,
        )
    else:
        return


@app.route('/xhr/add_module', methods=['POST'])
def add_module():
    if 'username' in session:
        """Add a new module to Ironworks"""
        try:
            module_id = request.form['module_id']
            column = request.form['column']
            position = request.form['position']

            # make sure that it's a valid module

            module_info = get_module_info(module_id)

            if not module_info:
                raise Exception

        except:
            return jsonify({'status': 'error'})

        module = Module(
            module_info['name'],
            column,
            position,
            module_info['poll'],
            module_info['delay'],
        )

        # db_session.add(module)

        # if module template has extra settings then create them in the database
        # with default values if they don't already exist

        if 'settings' in module_info:
            for s in module_info['settings']:
                setting = get_setting(s['key'])

                if not setting:
                    setting = Setting(s['key'], s['value'])
                    # db_session.add(setting)

        # db_session.commit()

        module_info['template'] = '%s.html' % (module_info['name'])

        # if the module is static and doesn't have any extra settings, return
        # the rendered module

        if module_info['static'] and not 'settings' in module_info:
            return render_template('placeholder_template.html',
                module=module_info
            )

        # otherwise return the rendered module settings dialog

        else:
            return module_settings_dialog(module_info['name'])
    else:
        return


@app.route('/xhr/rearrange_modules', methods=['POST'])
def rearrange_modules():
    if 'username' in session:
        """Rearrange a module on the page"""
        try:
            modules = json.JSONDecoder().decode(request.form['modules'])
        except:
            return jsonify({'status': 'error'})

        for module in modules:
            try:
                m = Module.query.filter(Module.name == module['name']).first()
                m.column = module['column']
                m.position = module['position']
                # db_session.add(m)
            except:
                pass

        # db_session.commit()

        return jsonify({'status': 'success'})
    else:
        return


@app.route('/xhr/remove_module/<name>', methods=['POST'])
def remove_module(name):
    if 'username' in session:
        """Remove module from the page"""
        module = Module.query.filter(Module.name == name).first()
        # db_session.delete(module)
        # db_session.commit()

        return jsonify({'status': 'success'})
    else:
        return


@app.route('/xhr/module_settings_dialog/<name>')
def module_settings_dialog(name):
    if 'username' in session:
        """show settings dialog for module"""
        module_info = get_module_info(name)
        module_db = get_module(name)

        if module_info and module_db:

            # look at the module template so we know what settings to look up

            module = copy.copy(module_info)

            # look up poll and delay from the database

            module['poll'] = module_db.poll
            module['delay'] = module_db.delay

            # iterate through possible settings and get values from database

            if 'settings' in module:
                for s in module['settings']:
                    setting = get_setting(s['key'])

                    if setting:
                        s['value'] = setting.value

                    if 'xbmc_servers' in s:
                        s['options'] = module_get_xbmc_servers()

            return render_template('dialogs/module_settings_dialog.html',
                                   module=module)

        return jsonify({'status': 'error'})
    else:
        return


@app.route('/xhr/module_settings_cancel/<name>')
def module_settings_cancel(name):
    if 'username' in session:
        """Cancel the settings dialog"""
        module = get_module_info(name)

        if module:
            module['template'] = '%s.html' % (module['name'])

            return render_template('placeholder_template.html',
                                    module=module)

        return jsonify({'status': 'error'})
    else:
        return


@app.route('/xhr/module_settings_save/<name>', methods=['POST'])
def module_settings_save(name):
    if 'username' in session:
        """Save options in settings dialog"""
        try:
            settings = json.JSONDecoder().decode(request.form['settings'])
        except:
            return jsonify({'status': 'error'})

        for s in settings:

            # poll and delay are stored in the modules tables

            if s['name'] == 'poll' or s['name'] == 'delay':
                module = get_module(name)

                if s['name'] == 'poll':
                    module.poll = int(s['value'])

                if s['name'] == 'delay':
                    module.delay = int(s['value'])

                # db_session.add(module)

            # other settings are stored in the settings table

            else:
                setting = get_setting(s['name'])

                if not setting:
                    setting = Setting(s['name'])

                setting.value = s['value']
                # db_session.add(setting)

                if s['name'] == 'ironworks_username':
                    ironworks.AUTH['username'] = s['value'] if s['value'] != '' else None

                if s['name'] == 'ironworks_password':
                    ironworks.AUTH['password'] = s['value'] if s['value'] != '' else None

        # db_session.commit()

        # you can't cancel server settings - instead, return an updated template
        # with 'Settings saved' text on the button

        if name == 'server_settings':
            return extra_settings_dialog(dialog_type='server_settings', updated=True)

        # for everything else, return the rendered module

        return module_settings_cancel(name)
    else:
        return


@app.route('/xhr/extra_settings_dialog/<dialog_type>')
def extra_settings_dialog(dialog_type, updated=False):
    if 'username' in session:
        """
        Extra settings dialog (search settings, misc settings, etc).
        """

        dialog_text = None
        dialog_extra = None

        if dialog_type == 'search_settings':
            settings = copy.copy(SEARCH_SETTINGS)
            dialog_title = 'Search settings'
            dialog_text = 'N.B. With search enabled, you can press \'ALT-s\' to display the search module.'
            dialog_extra = NewznabSite.query.order_by(NewznabSite.id)

        elif dialog_type == 'misc_settings':
            settings = copy.copy(MISC_SETTINGS)
            dialog_title = 'Misc. settings'

        elif dialog_type == 'server_settings':
            settings = copy.copy(SERVER_SETTINGS)
            dialog_title = 'Server settings'

        else:
            return jsonify({'status': 'error'})

        for s in settings:
            setting = get_setting(s['key'])

            if setting:
                s['value'] = setting.value

        return render_template('dialogs/extra_settings_dialog.html',
            dialog_title=dialog_title,
            dialog_text=dialog_text,
            dialog_type=dialog_type,
            dialog_extra=dialog_extra,
            settings=settings,
            updated=updated,
        )
    else:
        return


@app.route('/xhr/server_settings_dialog/', methods=['GET', 'POST'])
@app.route('/xhr/server_settings_dialog/<server_id>', methods=['GET', 'POST'])
def server_settings_dialog(server_id=None):
    if 'username' in session:
        """
        Server settings dialog.
        If server_id exists then we're editing a server, otherwise we're adding one.
        """

        server = None

        if server_id:
            try:
                server = XbmcServer.query.get(server_id)

            except:
                logger.log('Error retrieving server details for server ID %s' % server_id, 'WARNING')

        # GET

        if request.method == 'GET':
            return render_template('dialogs/server_settings_dialog.html',
                                    server=server)

        # POST

        else:
            if not server:
                server = XbmcServer('', 1, '')

            label = request.form['label']
            if not label:
                label = 'XBMC server'

            try:
                server.label = label
                server.position = request.form['position']
                server.hostname = request.form['hostname']
                server.port = request.form['port']
                server.username = request.form['username']
                server.password = request.form['password']
                server.mac_address = request.form['mac_address']

                # db_session.add(server)
                # db_session.commit()

                active_server = get_setting('active_server')

                if not active_server:
                    active_server = Setting('active_server', server.id)
                    # db_session.add(active_server)
                    # db_session.commit()

                return render_template('includes/servers.html',
                                        servers=XbmcServer.query.order_by(XbmcServer.position))

            except:
                logger.log('Error saving XBMC server to database', 'WARNING')
                return jsonify({'status': 'error'})

        return jsonify({'status': 'error'})
    else:
        return


@app.route('/xhr/delete_server/<server_id>', methods=['POST'])
def delete_server(server_id=None):
    if 'username' in session:
        """
        Deletes a server.
        """

        try:
            xbmc_server = XbmcServer.query.get(server_id)
            # db_session.delete(xbmc_server)
            # db_session.commit()

            # Remove the server's cache
            label = xbmc_server.label
            recent_cache = [label + '_episodes', label + '_movies', label + '_albums']

            try:
                for entry in recent_cache:
                    recent_db = RecentlyAdded.query.filter(RecentlyAdded.name == entry).first()

                    if recent_db:
                            # db_session.delete(recent_db)
                            # db_session.commit()
                            pass
            except:
                logger.log('Failed to remove servers database cache', 'WARNING')

            image_dir = os.path.join(ironworks.DATA_DIR, 'cache', 'xbmc', xbmc_server.label)
            if os.path.isdir(image_dir):
                import shutil

                try:
                    shutil.rmtree(image_dir)
                except:
                    logger.log('Failed to remove servers image cache', 'WARNING')

            return render_template('includes/servers.html',
                                    servers=XbmcServer.query.order_by(XbmcServer.position))

        except:
            logger.log('Error deleting server ID %s' % server_id, 'WARNING')
            return jsonify({'status': 'error'})
    else:
        return


@app.route('/xhr/switch_server/<server_id>')
def switch_server(server_id=None):
    if 'username' in session:
        """
        Switches XBMC servers.
        """

        xbmc_server = XbmcServer.query.get(server_id)

        try:
            active_server = get_setting('active_server')
            active_server.value = server_id
            db_session.add(active_server)
            db_session.commit()
            logger.log('Switched active server to ID %s' % server_id, 'INFO')

        except:
            logger.log('Error setting active server to ID %s' % server_id, 'WARNING')
            return jsonify({'status': 'error'})

        return jsonify({'status': 'success'})
    else:
        return


def get_module(name):
    """helper method which returns a module record from the database"""
    try:
        return Module.query.filter(Module.name == name).first()

    except:
        return None


def get_module_info(name):
    """helper method which returns a module template"""
    for available_module in AVAILABLE_MODULES:
        if name == available_module['name']:
            return available_module

    return None


def module_get_xbmc_servers():
    servers = XbmcServer.query.order_by(XbmcServer.position)
    options = [{'value': '', 'label': 'Default'}]

    for server in servers:
        server = {
            'label': server.label,
            'hostname': server.hostname,
            'port': server.port,
            'username': server.username,
            'password': server.password,
            'mac_address': server.mac_address,
        }
        if server['hostname'] and server['port']:
            url = 'http://'

            if server['username'] and server['password']:
                url += '%s:%s@' % (server['username'], server['password'])

            url += '%s:%s/jsonrpc' % (server['hostname'], server['port'])
            server['api'] = url

        else:
            server['api'] = ''

        options.append({'value': str(server), 'label': server['label']})

    return options
