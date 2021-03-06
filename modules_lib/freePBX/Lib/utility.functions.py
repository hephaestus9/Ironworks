# -*- coding: utf-8 -*-# License for all code of this FreePBX module can be found in the license file inside the module directory
# Copyright 2013 Schmooze Com Inc.
#
from ironworks import serverTools


class Utility_Functions():

    def __init__(self):
        self.errorCodes = {"FPBX_LOG_FATAL": "FATAL",
                           "FPBX_LOG_CRITICAL": "CRITICAL",
                           "FPBX_LOG_SECURITY": "SECURITY",
                           "FPBX_LOG_UPDATE":  "UPDATE",
                           "FPBX_LOG_ERROR": "ERROR",
                           "FPBX_LOG_WARNING": "WARNING",
                           "FPBX_LOG_NOTICE": "NOTICE",
                           "FPBX_LOG_INFO": "INFO",
                           "FPBX_LOG_PHP": "PHP"}

    #** FreePBX Logging facility to FILE or syslog
    #* @param  string   The level/severity of the error. Valid levels use constants:
    #*                  FPBX_LOG_FATAL, FPBX_LOG_CRITICAL, FPBX_LOG_SECURITY, FPBX_LOG_UPDATE,
    #*                  FPBX_LOG_ERROR, FPBX_LOG_WARNING, FPBX_LOG_NOTICE, FPBX_LOG_INFO.
    #* @param  string   The error message
    #*
    def freepbx_log(self, level, message):
