# -*- coding: utf-8 -*-
from ironworks import serverTools


class DefaultSettings:

    def __init__(self, customDb=False):
        if customDb:
            self.db = customDb
            self.db.checkTable("prefs", [
                {"name": "name", "type": "text"},
                {"name": "value", "type": "text"}])
        else:
            self.db = serverTools.getPrefsDb()
            self.db.beginTransaction()

            self.db.checkTable("pyemoncms", [
                {"name": "name", "type": "text"},
                {"name": "value", "type": "text"}])

            self.checkDefaults("version", "8.3.6")
            self.checkDefaults("username", "ironworks_admin")
            self.checkDefaults("password", "")
            self.checkDefaults("server", "localhost")
            self.checkDefaults("database", "pyemoncms")
            self.checkDefaults("redis_enabled", "True")

            # Enable this to try out the experimental MQTT Features:
            # - updated to feeds are published to topic: emoncms/feed/feedid
            self.checkDefaults("mqtt_enabled", "False")
            self.checkDefaults("timestore", "{'adminkey': '_TS_ADMINKEY_'}")
            self.checkDefaults("graphite", "{'port': 0, 'host':0}")

            self.checkDefaults("smtp_email_settings", "{'host': '_SMTP_HOST_', 'username': '_SMTP_USER', 'password': '_SMTP_PASSWORD', 'from': {'_SMTP_EMAIL_ADDR_': '_SMTP_EMAIL_NAME_'}")

            self.checkDefaults("enalbe_password_reset", "False")

            # Checks for limiting garbage data?
            self.checkDefaults("max_node_id_limit", "32")

            # Default controller and action if none are specified and user is anonymous
            self.checkDefaults("default_controller", "user")
            self.checkDefaults("default_action", "login")

            # Default controller and action if none are specified and user is logged in
            self.checkDefaults("default_controller_auth", "user")
            self.checkDefaults("default_action_auth", "view")

            # Public profile functionality
            self.checkDefaults("public_profile_enabled", "True")
            self.checkDefaults("public_profile_controller", "dashboard")
            self.checkDefaults("public_profile_action", "view")

            # Misc
            self.checkDefaults("theme", "basic")
            self.checkDefaults("display_errors", "True")
            self.checkDefaults("allowusersregister", "True")
            self.checkDefaults("enable_rememberme", "True")

    def checkDefaults(self, name, value):
        cursor = self.db.select("pyemoncms", where={"name": name})
        if not cursor.fetchone():
            self.db.beginTransaction()
            self.db.insert("pyemoncms", {"name": name, "value": value})
            self.db.commitTransaction()
