/**
 * @class Bleext.desktop.Constants
 * @extends Object
 * requires
 * @autor Crysfel Villa
 * @date Mon Jul 25 23:04:37 CDT 2011
 *
 * Description
 *
 *
 **/

Ext.define("Bleext.desktop.Constants",{
	alternateClassName	: "Bleext.Constants" ,
	singleton	: true,

	/* login url*/
	DESKTOP_CONFIGURATION_URL          : "config_desktop",
	DESKTOP_LOGIN_URL                  : "settings_login",
	DESKTOP_CREATE_ACCOUNT_URL         : "settings_create_login",
	DESKTOP_LOGOUT_URL                 : "settings_logout",
	DESKTOP_HOME_URL                   : "settings",
	
	
	/*Applications*/
	GET_PERMISSION_BY_APPLICATION      :"permission_by_application",
	GET_ACTIVE_APPLICATIONS            :"get_active_applications",
	SAVE_APPLICATION                   :"save_application",
	REMOVE_APPLICATION                 :"remove_application",
	MOVE_APPLICATION                   :"move_application",
	
	/*Roles*/
	GET_ALL_ROLES                      :"get_all_roles",
	SAVE_ROLES                         :"save_roles",
	REMOVE_ROLE                        :"remove_role",
	
	/*Users*/
	GET_ALL_USERS                      :"get_all_users",
	SAVE_USER                          :"save_user",
	REMOVE_USER                        :"remove_user",
	ADD_USER                           :"add_user",
	
	/*Privliges*/
	SAVE_PERMISSIONS                   :"save_permissions",
	
	/* The directory where the avatars are */
	USERS_AVATAR_PATH                  : "static/bleextop/resources/avatars/",
	
	/* The directory where the JS's are*/
	JS_PATH                            : "static/bleextop/js/",
	
	/* Default width and height for windows */
	DEFAULT_WINDOW_WIDTH               : 800,
	DEFAULT_WINDOW_HEIGHT              : 480,
	
	LOGIN_IMAGE                        : "static/bleextop/resources/images/login-image.jpg"
	
});