# -*- coding: utf-8 -*-
from ironworks import serverTools
from modules_lib.freePBX.lib import ampuser.class
from modules_lib import bootstrap


class Settings():

    def __init__(self, extdisplay=None, restrictmods=None, skip_astman=None, handler=None):
        self.db = serverTools.getPrefsDb()
        self.ampDB = serverTools.getAmpDb()
        self.logger = serverTools.getLogger()

        self.bootstrap_settings = {}
        self.action = self.db.getPBXAction()
        self.confirm_email = self.db.getPBXConfirmEmail()
        self.confirm_password = self.db.getPBXConfirmPassword()
        self.display = self.db.getPBXDisplay()
        if self.db.getPBXExtdisplay() == "False":
            self.extdisplay = False
        else:
            self.extdisplay = self.db.getPBXExtdisplay()
        self.email_address = self.db.getPBXEmailAddress()
        self.fw_popover = self.db.getPBXFwPopover()
        self.fw_popover_process = self.db.getPBXFwPopoverProcess()
        self.logout = self.db.getPBXLogout()
        self.password = self.db.getPBXPassword()
        self.quietmode = self.db.getPBXQuietMode()
        if self.db.getPBXRestrcitmods() == "False":
            self.restrictmods = False
        else:
            self.restricmods = self.db.getPBXRestrcitmods()
        self.skip = self.db.getPBXSkip()
        if self.db.getPBXSkipAstman() == "False":
            self.skip_astman = False
        else:
            self.skip_astman = self.db.getPBXSkipAstman()
        self.type = self.db.getPBXType()
        self.username = self.db.getPBXUsername()

        if extdisplay != None and extdisplay != False:
            # htmlspecialchars($extdisplay, ENT_QUOTES) : false;
            self.extdisplay = extdisplay

        if restrictmods != None:
            self.restrictmods = restrictmods

        if skip_astman != None:
            self.skip_astman = skip_astman
            self.bootstrap_settings['skip_astman'] = skip_astman

        self.ampUser = ampuser.class.Ampuser_Class()

        if handler != None:
            if self.restrictmods == 'False':
                self.restrictmods = 'True'
            if 'api' in handler:
                pass
            if 'reload' in handler:
                pass

            # If we didn't provide skip_astman in the $_REQUEST[] array
            # it will be boolean false and for handlers, this should default
            # to true, if we did provide it, it will NOT be a boolean
            # (it could be 0) so we will honor the setting
            if self.bootstrap_settings['skip_astman'] == 'False':
                self.bootstrap_settings['skip_astman'] = 'True'

            self.bootstrap = bootstrap.Bootstrap(self.bootstrap_settings, self.restricmods)
