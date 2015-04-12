# -*- coding: utf-8 -*-
from ironworks import serverTools
import datetime


class Bleex:

    def __init__(self):
        self.db = serverTools.getSystemDb()
        self.logger = serverTools.getLogger()
        self.date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        self.db.beginTransaction()

        self.db.query("SET SQL_MODE=\"NO_AUTO_VALUE_ON_ZERO\";")

        self.db.query("CREATE TABLE IF NOT EXISTS `applications` (`application_k` int(11) NOT NULL AUTO_INCREMENT,`application_parent_k` int(11) DEFAULT NULL,`name` varchar(200) NOT NULL,`description` text NOT NULL,`klass` varchar(255) NOT NULL,`configurations` text NOT NULL,`date_created` datetime NOT NULL,`date_updated` datetime NOT NULL,`active` tinyint(1) NOT NULL,PRIMARY KEY (`application_k`)) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=8 ;")

        self.db.query("CREATE TABLE IF NOT EXISTS `permissions` (`permission_k` int(11) NOT NULL AUTO_INCREMENT,`application_k` int(11) NOT NULL,`action` varchar(50) NOT NULL,`name` varchar(100) NOT NULL,`description` text NOT NULL,PRIMARY KEY (`permission_k`),KEY `application_k` (`application_k`)) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=42 ;")

        self.db.query("CREATE TABLE IF NOT EXISTS `roles` (`role_k` int(11) NOT NULL AUTO_INCREMENT,`name` varchar(50) NOT NULL,`description` text NOT NULL,PRIMARY KEY (`role_k`)) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=4 ;")

        self.db.query("CREATE TABLE IF NOT EXISTS `role_permissions` (`role_permission_k` int(11) NOT NULL AUTO_INCREMENT,`role_k` int(11) NOT NULL,`permission_k` int(11) NOT NULL,`value` tinyint(1) NOT NULL,`date_created` datetime NOT NULL,PRIMARY KEY (`role_permission_k`),KEY `role_k` (`role_k`),KEY `permission_k` (`permission_k`)) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=58 ;")

        self.db.query("CREATE TABLE IF NOT EXISTS `users` (`user_k` int(11) NOT NULL AUTO_INCREMENT,`username` varchar(20) NOT NULL,`password` char(128) NOT NULL,`email` varchar(100) NOT NULL,`name` varchar(50) NOT NULL,`lastname` varchar(50) NOT NULL,`avatar` varchar(255) DEFAULT NULL,`active` tinyint(1) NOT NULL,PRIMARY KEY (`user_k`),UNIQUE KEY `username` (`username`)) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=6 ;")

        self.db.query("CREATE TABLE IF NOT EXISTS `user_permissions` (`user_permission_k` int(11) NOT NULL AUTO_INCREMENT,`user_k` int(11) NOT NULL,`permission_k` int(11) NOT NULL,`value` int(11) NOT NULL,`date_created` datetime NOT NULL,PRIMARY KEY (`user_permission_k`),KEY `user_k` (`user_k`),KEY `permission_k` (`permission_k`)) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=3 ;")

        self.db.query("CREATE TABLE IF NOT EXISTS `user_roles` (`user_k` int(11) NOT NULL,`role_k` int(11) NOT NULL,`date_created` datetime NOT NULL,KEY `user_k` (`user_k`),KEY `role_k` (`role_k`)) ENGINE=InnoDB DEFAULT CHARSET=utf8;")

        # Check basic defaults
        #Applications
        self.checkDesktopDefaults("applications", data={
                                                        "application_k": "1",
                                                        "application_parent_k": "0",
                                                        "name": "Administration",
                                                        "description": "Administration Folder",
                                                        "klass": "",
                                                        "configurations": '{"iconCls":"","width":800,"height":480,"shorcutIconCls":""}',
                                                        "date_created": self.date,
                                                        "date_updated": self.date,
                                                        "active": "1"})
        self.checkDesktopDefaults("applications", data={
                                                        "application_k": "2",
                                                        "application_parent_k": '1',
                                                        "name": 'Applications',
                                                        "description": 'Applications Catalog',
                                                        "klass": 'Bleext.modules.catalogs.applications.controller.Application',
                                                        "configurations": '{"iconCls":"applications-icon"}',
                                                        "date_created": self.date,
                                                        "date_updated": self.date,
                                                        "active": "1"})
        self.checkDesktopDefaults("applications", data={
                                                        "application_k": "3",
                                                        "application_parent_k": '1',
                                                        "name": 'Roles',
                                                        "description": 'Roles Catalog',
                                                        "klass": 'Bleext.modules.catalogs.roles.controller.Roles',
                                                        "configurations": '{"iconCls":"roles-icon","width":800,"height":480,"shorcutIconCls":""}',
                                                        "date_created": self.date,
                                                        "date_updated": self.date,
                                                        "active": "1"})
        self.checkDesktopDefaults("applications", data={
                                                        "application_k": "4",
                                                        "application_parent_k": '1',
                                                        "name": 'Users',
                                                        "description": 'Users Module',
                                                        "klass": 'Bleext.modules.catalogs.users.controller.Users',
                                                        "configurations": '{"iconCls":"users-icon","shorcutIconCls":"roles-app-shorcut-icon","width":800,"height":480}',
                                                        "date_created": self.date,
                                                        "date_updated": self.date,
                                                        "active": "1"})
        self.checkDesktopDefaults("applications", data={
                                                        "application_k": "5",
                                                        "application_parent_k": '1',
                                                        "name": 'Privileges',
                                                        "description": 'This module allow you to set the privileges to the roles and applications',
                                                        "klass": 'Bleext.modules.security.permissions.controller.Permission',
                                                        "configurations": '{"iconCls":"permissions-icon-16","width":800,"height":480,"shorcutIconCls":""}',
                                                        "date_created": self.date,
                                                        "date_updated": self.date,
                                                        "active": "1"})
        self.checkDesktopDefaults("applications", data={
                                                        "application_k": "6",
                                                        "application_parent_k": '1',
                                                        "name": 'Groups',
                                                        "description": 'Groups Module',
                                                        "klass": 'Bleext.modules.security.groups.controller.Groups',
                                                        "configurations": '{"iconCls":"groups-icon-16","width":800,"height":480,"shorcutIconCls":""}',
                                                        "date_created": self.date,
                                                        "date_updated": self.date,
                                                        "active": "1"})

        #Permissions
        self.checkDesktopDefaults("permissions", data={
                                                        "permission_k": '1',
                                                        "application_k": '1',
                                                        "action": 'access',
                                                        "name": 'Access',
                                                        "description": 'Permission Access'})
        self.checkDesktopDefaults("permissions", data={
                                                        "permission_k": '2',
                                                        "application_k": '2',
                                                        "action": 'access',
                                                        "name": 'Access',
                                                        "description": 'Permission to read all the applications'})
        self.checkDesktopDefaults("permissions", data={
                                                        "permission_k": '3',
                                                        "application_k": '2',
                                                        "action": 'edit',
                                                        "name": 'Edit',
                                                        "description": 'Edit Access'})
        self.checkDesktopDefaults("permissions", data={
                                                        "permission_k": '4',
                                                        "application_k": '2',
                                                        "action": 'create',
                                                        "name": 'Create',
                                                        "description": 'Create'})
        self.checkDesktopDefaults("permissions", data={
                                                        "permission_k": '5',
                                                        "application_k": '2',
                                                        "action": 'update',
                                                        "name": 'Update',
                                                        "description": 'Update Access'})
        self.checkDesktopDefaults("permissions", data={
                                                        "permission_k": '6',
                                                        "application_k": '2',
                                                        "action": 'list',
                                                        "name": 'List',
                                                        "description": 'List'})
        self.checkDesktopDefaults("permissions", data={
                                                        "permission_k": '7',
                                                        "application_k": '2',
                                                        "action": 'delete',
                                                        "name": 'Delete',
                                                        "description": 'Delete Access'})
        self.checkDesktopDefaults("permissions", data={
                                                        "permission_k": '8',
                                                        "application_k": '2',
                                                        "action": 'print',
                                                        "name": 'Print',
                                                        "description": 'Print'})
        self.checkDesktopDefaults("permissions", data={
                                                        "permission_k": '9',
                                                        "application_k": '2',
                                                        "action": 'export',
                                                        "name": 'Export',
                                                        "description": 'Export Access'})
        self.checkDesktopDefaults("permissions", data={
                                                        "permission_k": '10',
                                                        "application_k": '3',
                                                        "action": 'access',
                                                        "name": 'Access',
                                                        "description": 'To Access the module'})
        self.checkDesktopDefaults("permissions", data={
                                                        "permission_k": '11',
                                                        "application_k": '3',
                                                        "action": 'edit',
                                                        "name": 'Edit',
                                                        "description": 'Edit Access'})
        self.checkDesktopDefaults("permissions", data={
                                                        "permission_k": '12',
                                                        "application_k": '3',
                                                        "action": 'create',
                                                        "name": 'Create',
                                                        "description": 'Create'})
        self.checkDesktopDefaults("permissions", data={
                                                        "permission_k": '13',
                                                        "application_k": '3',
                                                        "action": 'update',
                                                        "name": 'Update',
                                                        "description": 'Update Access'})
        self.checkDesktopDefaults("permissions", data={
                                                        "permission_k": '14',
                                                        "application_k": '3',
                                                        "action": 'list',
                                                        "name": 'List',
                                                        "description": 'List'})
        self.checkDesktopDefaults("permissions", data={
                                                        "permission_k": '15',
                                                        "application_k": '3',
                                                        "action": 'delete',
                                                        "name": 'Delete',
                                                        "description": 'Delete Access'})
        self.checkDesktopDefaults("permissions", data={
                                                        "permission_k": '16',
                                                        "application_k": '3',
                                                        "action": 'print',
                                                        "name": 'Print',
                                                        "description": 'Print'})
        self.checkDesktopDefaults("permissions", data={
                                                        "permission_k": '17',
                                                        "application_k": '3',
                                                        "action": 'export',
                                                        "name": 'Export',
                                                        "description": 'Export Access'})
        self.checkDesktopDefaults("permissions", data={
                                                        "permission_k": '18',
                                                        "application_k": '4',
                                                        "action": 'access',
                                                        "name": 'Access',
                                                        "description": 'To appear in the menu'})
        self.checkDesktopDefaults("permissions", data={
                                                        "permission_k": '19',
                                                        "application_k": '4',
                                                        "action": 'edit',
                                                        "name": 'Edit',
                                                        "description": 'Edit Access'})
        self.checkDesktopDefaults("permissions", data={
                                                        "permission_k": '20',
                                                        "application_k": '4',
                                                        "action": 'create',
                                                        "name": 'Create',
                                                        "description": 'Create'})
        self.checkDesktopDefaults("permissions", data={
                                                        "permission_k": '21',
                                                        "application_k": '4',
                                                        "action": 'update',
                                                        "name": 'Update',
                                                        "description": 'Update Access'})
        self.checkDesktopDefaults("permissions", data={
                                                        "permission_k": '22',
                                                        "application_k": '4',
                                                        "action": 'list',
                                                        "name": 'List',
                                                        "description": 'List'})
        self.checkDesktopDefaults("permissions", data={
                                                        "permission_k": '23',
                                                        "application_k": '4',
                                                        "action": 'delete',
                                                        "name": 'Delete',
                                                        "description": 'Delete Access'})
        self.checkDesktopDefaults("permissions", data={
                                                        "permission_k": '24',
                                                        "application_k": '4',
                                                        "action": 'print',
                                                        "name": 'Print',
                                                        "description": 'Print'})
        self.checkDesktopDefaults("permissions", data={
                                                        "permission_k": '25',
                                                        "application_k": '4',
                                                        "action": 'export',
                                                        "name": 'Export',
                                                        "description": 'Export Access'})
        self.checkDesktopDefaults("permissions", data={
                                                        "permission_k": '26',
                                                        "application_k": '5',
                                                        "action": 'access',
                                                        "name": 'Access',
                                                        "description": 'Allow users to access the permissions module, this module should be visible only for administrators'})
        self.checkDesktopDefaults("permissions", data={
                                                        "permission_k": '27',
                                                        "application_k": '5',
                                                        "action": 'edit',
                                                        "name": 'Edit',
                                                        "description": 'Edit Access'})
        self.checkDesktopDefaults("permissions", data={
                                                        "permission_k": '28',
                                                        "application_k": '5',
                                                        "action": 'create',
                                                        "name": 'Create',
                                                        "description": 'Create'})
        self.checkDesktopDefaults("permissions", data={
                                                        "permission_k": '29',
                                                        "application_k": '5',
                                                        "action": 'update',
                                                        "name": 'Update',
                                                        "description": 'Update Access'})
        self.checkDesktopDefaults("permissions", data={
                                                        "permission_k": '30',
                                                        "application_k": '5',
                                                        "action": 'list',
                                                        "name": 'List',
                                                        "description": 'List'})
        self.checkDesktopDefaults("permissions", data={
                                                        "permission_k": '31',
                                                        "application_k": '5',
                                                        "action": 'delete',
                                                        "name": 'Delete',
                                                        "description": 'Delete Access'})
        self.checkDesktopDefaults("permissions", data={
                                                        "permission_k": '32',
                                                        "application_k": '5',
                                                        "action": 'print',
                                                        "name": 'Print',
                                                        "description": 'Print'})
        self.checkDesktopDefaults("permissions", data={
                                                        "permission_k": '33',
                                                        "application_k": '5',
                                                        "action": 'export',
                                                        "name": 'Export',
                                                        "description": 'Export Access'})
        self.checkDesktopDefaults("permissions", data={
                                                        "permission_k": '34',
                                                        "application_k": '6',
                                                        "action": 'access',
                                                        "name": 'Access',
                                                        "description": 'Groups Access'})
        self.checkDesktopDefaults("permissions", data={
                                                        "permission_k": '35',
                                                        "application_k": '6',
                                                        "action": 'edit',
                                                        "name": 'Edit',
                                                        "description": 'Edit Access'})
        self.checkDesktopDefaults("permissions", data={
                                                        "permission_k": '36',
                                                        "application_k": '6',
                                                        "action": 'create',
                                                        "name": 'Create',
                                                        "description": 'Create'})
        self.checkDesktopDefaults("permissions", data={
                                                        "permission_k": '37',
                                                        "application_k": '6',
                                                        "action": 'list',
                                                        "name": 'List',
                                                        "description": 'List'})
        self.checkDesktopDefaults("permissions", data={
                                                        "permission_k": '38',
                                                        "application_k": '6',
                                                        "action": 'delete',
                                                        "name": 'Delete',
                                                        "description": 'Delete Access'})
        self.checkDesktopDefaults("permissions", data={
                                                        "permission_k": '39',
                                                        "application_k": '6',
                                                        "action": 'print',
                                                        "name": 'Print',
                                                        "description": 'Print'})
        self.checkDesktopDefaults("permissions", data={
                                                        "permission_k": '40',
                                                        "application_k": '6',
                                                        "action": 'export',
                                                        "name": 'Export',
                                                        "description": 'Export Access'})

        #Roles
        self.checkDesktopDefaults("roles", data={
                                                        "role_k": "1",
                                                        "name": 'Administrator',
                                                        "description": 'The Super User'})
        self.checkDesktopDefaults("roles", data={
                                                        "role_k": "2",
                                                        "name": 'Users',
                                                        "description": 'The Users Role'})
        self.checkDesktopDefaults("roles", data={
                                                        "role_k": "3",
                                                        "name": 'Visitors',
                                                        "description": 'Visitors'})

        #Role Permissions
        #Administrator
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '1',
                                                        "role_permission_k": '1',
                                                        "permission_k": '1',
                                                        "value": '1',
                                                        "date_created": self.date})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '1',
                                                        "role_permission_k": '2',
                                                        "permission_k": '2',
                                                        "value": '1',
                                                        "date_created": self.date})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '1',
                                                        "role_permission_k": '3',
                                                        "permission_k": '3',
                                                        "value": '1',
                                                        "date_created": self.date})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '1',
                                                        "role_permission_k": '4',
                                                        "permission_k": '4',
                                                        "value": '1',
                                                        "date_created": self.date})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '1',
                                                        "role_permission_k": '5',
                                                        "permission_k": '5',
                                                        "value": '1',
                                                        "date_created": self.date})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '1',
                                                        "role_permission_k": '6',
                                                        "permission_k": '6',
                                                        "value": '1',
                                                        "date_created": self.date})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '1',
                                                        "role_permission_k": '7',
                                                        "permission_k": '7',
                                                        "value": '1',
                                                        "date_created": self.date})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '1',
                                                        "role_permission_k": '8',
                                                        "permission_k": '8',
                                                        "value": '5',
                                                        "date_created": self.date})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '1',
                                                        "role_permission_k": '9',
                                                        "permission_k": '9',
                                                        "value": '1',
                                                        "date_created": self.date})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '1',
                                                        "role_permission_k": '10',
                                                        "permission_k": '10',
                                                        "value": '1',
                                                        "date_created": self.date})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '1',
                                                        "role_permission_k": '11',
                                                        "permission_k": '11',
                                                        "value": '1',
                                                        "date_created": self.date})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '1',
                                                        "role_permission_k": '12',
                                                        "permission_k": '12',
                                                        "value": '1',
                                                        "date_created": self.date})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '1',
                                                        "role_permission_k": '13',
                                                        "permission_k": '13',
                                                        "value": '1',
                                                        "date_created": self.date})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '1',
                                                        "role_permission_k": '14',
                                                        "permission_k": '14',
                                                        "value": '1',
                                                        "date_created": self.date})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '1',
                                                        "role_permission_k": '15',
                                                        "permission_k": '15',
                                                        "value": '1',
                                                        "date_created": self.date})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '1',
                                                        "role_permission_k": '16',
                                                        "permission_k": '16',
                                                        "value": '1',
                                                        "date_created": self.date})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '1',
                                                        "role_permission_k": '17',
                                                        "permission_k": '17',
                                                        "value": '1',
                                                        "date_created": self.date})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '1',
                                                        "role_permission_k": '18',
                                                        "permission_k": '18',
                                                        "value": '1',
                                                        "date_created": self.date})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '1',
                                                        "role_permission_k": '19',
                                                        "permission_k": '19',
                                                        "value": '1',
                                                        "date_created": self.date})

        #User
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '2',
                                                        "role_permission_k": '20',
                                                        "permission_k": '4',
                                                        "value": '0',
                                                        "date_created": self.date})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '2',
                                                        "role_permission_k": '21',
                                                        "permission_k": '5',
                                                        "value": '0',
                                                        "date_created": self.date})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '2',
                                                        "role_permission_k": '22',
                                                        "permission_k": '6',
                                                        "value": '0',
                                                        "date_created": self.date})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '2',
                                                        "role_permission_k": '23',
                                                        "permission_k": '7',
                                                        "value": '0',
                                                        "date_created": self.date})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '2',
                                                        "role_permission_k": '24',
                                                        "permission_k": '8',
                                                        "value": '0',
                                                        "date_created": self.date})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '2',
                                                        "role_permission_k": '25',
                                                        "permission_k": '9',
                                                        "value": '0',
                                                        "date_created": self.date})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '2',
                                                        "role_permission_k": '26',
                                                        "permission_k": '10',
                                                        "value": '0',
                                                        "date_created": self.date})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '2',
                                                        "role_permission_k": '27',
                                                        "permission_k": '11',
                                                        "value": '0',
                                                        "date_created": self.date})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '2',
                                                        "role_permission_k": '28',
                                                        "permission_k": '12',
                                                        "value": '0',
                                                        "date_created": self.date})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '2',
                                                        "role_permission_k": '29',
                                                        "permission_k": '13',
                                                        "value": '0',
                                                        "date_created": self.date})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '2',
                                                        "role_permission_k": '30',
                                                        "permission_k": '14',
                                                        "value": '0',
                                                        "date_created": self.date})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '2',
                                                        "role_permission_k": '31',
                                                        "permission_k": '15',
                                                        "value": '0',
                                                        "date_created": self.date})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '2',
                                                        "role_permission_k": '32',
                                                        "permission_k": '16',
                                                        "value": '0',
                                                        "date_created": self.date})

        #Visitor
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '3',
                                                        "role_permission_k": '33',
                                                        "permission_k": '4',
                                                        "value": '0',
                                                        "date_created": self.date})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '3',
                                                        "role_permission_k": '34',
                                                        "permission_k": '5',
                                                        "value": '0',
                                                        "date_created": self.date})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '3',
                                                        "role_permission_k": '35',
                                                        "permission_k": '6',
                                                        "value": '0',
                                                        "date_created": self.date})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '3',
                                                        "role_permission_k": '36',
                                                        "permission_k": '7',
                                                        "value": '0',
                                                        "date_created": self.date})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '3',
                                                        "role_permission_k": '37',
                                                        "permission_k": '8',
                                                        "value": '0',
                                                        "date_created": self.date})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '3',
                                                        "role_permission_k": '38',
                                                        "permission_k": '9',
                                                        "value": '0',
                                                        "date_created": self.date})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '3',
                                                        "role_permission_k": '39',
                                                        "permission_k": '10',
                                                        "value": '0',
                                                        "date_created": self.date})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '3',
                                                        "role_permission_k": '40',
                                                        "permission_k": '11',
                                                        "value": '0',
                                                        "date_created": self.date})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '3',
                                                        "role_permission_k": '41',
                                                        "permission_k": '12',
                                                        "value": '0',
                                                        "date_created": self.date})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '3',
                                                        "role_permission_k": '42',
                                                        "permission_k": '13',
                                                        "value": '0',
                                                        "date_created": self.date})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '3',
                                                        "role_permission_k": '43',
                                                        "permission_k": '14',
                                                        "value": '0',
                                                        "date_created": self.date})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '3',
                                                        "role_permission_k": '44',
                                                        "permission_k": '15',
                                                        "value": '0',
                                                        "date_created": self.date})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '3',
                                                        "role_permission_k": '45',
                                                        "permission_k": '16',
                                                        "value": '0',
                                                        "date_created": self.date})

        #User Permissions
        self.checkDesktopDefaults("user_permissions", data={
                                                        "user_permission_k": '1',
                                                        "user_k": '1',
                                                        "permission_k": '1',
                                                        "value": '1',
                                                        "date_created": self.date})

        #User Roles
        self.checkDesktopDefaults("user_roles", data={
                                                        "user_k": '1',
                                                        "role_k": '1',
                                                        "date_created": self.date})
        #Users password is "password"
        self.checkDesktopDefaults("users", data={
                                                        "user_k": '1',
                                                        "username": '',
                                                        "password": '',
                                                        "email": '',
                                                        "name": "Admin",
                                                        "lastname": "Super",
                                                        "avatar": "default.png",
                                                        "active": "1"})
        try:
            self.db.query("ALTER TABLE `permissions`ADD CONSTRAINT `permissions_ibfk_1` FOREIGN KEY (`application_k`) REFERENCES `applications` (`application_k`);")
            self.db.query("ALTER TABLE `role_permissions`ADD CONSTRAINT `role_permissions_ibfk_1` FOREIGN KEY (`role_k`) REFERENCES `roles` (`role_k`),ADD CONSTRAINT `role_permissions_ibfk_2` FOREIGN KEY (`permission_k`) REFERENCES `permissions` (`permission_k`);")
            self.db.query("ALTER TABLE `user_permissions`ADD CONSTRAINT `user_permissions_ibfk_1` FOREIGN KEY (`user_k`) REFERENCES `users` (`user_k`),ADD CONSTRAINT `user_permissions_ibfk_2` FOREIGN KEY (`permission_k`) REFERENCES `permissions` (`permission_k`);")
            self.db.query("ALTER TABLE `user_roles`ADD CONSTRAINT `user_roles_ibfk_1` FOREIGN KEY (`user_k`) REFERENCES `users` (`user_k`),ADD CONSTRAINT `user_roles_ibfk_2` FOREIGN KEY (`role_k`) REFERENCES `roles` (`role_k`);")
        except Exception as e:
            self.logger.log(e, "WARNING")

        self.db.commitTransaction()

    def checkDesktopDefaults(self, table, data):
        if table == "applications":
            lookup = {"application_k": data["application_k"]}
        elif table == "permissions":
            lookup = {"permission_k": data["permission_k"]}
        elif table == "role_permissions":
            lookup = {"role_permission_k": data["role_permission_k"]}
        elif table == "user_permissions":
            lookup = {"user_permission_k": data["user_permission_k"]}
        elif table == "user_roles":
            lookup = {"user_k": data["user_k"], "role_k": data["role_k"]}
        else:
            lookup = data

        cursor = self.db.select(table, where=lookup)
        if not cursor:
            try:
                self.db.beginTransaction()
                self.db.insert(table, data)
                self.db.commitTransaction()
            except Exception as e:
                self.logger.log(e, "WARNING")