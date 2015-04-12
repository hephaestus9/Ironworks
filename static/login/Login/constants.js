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

Ext.define("Login.Constants",{
	alternateClassName	: "Login.Constants" ,
	singleton	: true,

	/* login url*/
	CONFIGURATION_URL          : "config_desktop",
	LOGIN_URL                  : "process_login",
	CREATE_ACCOUNT_URL         : "create_login",
	LOGOUT_URL                 : "logout",
	HOME_URL                   : "latestNews",
	
	/* The directory where the JS's are*/
	JS_PATH                            : "static/login/Login/",
	
	/* Default width and height for windows */
	DEFAULT_WINDOW_WIDTH               : 800,
	DEFAULT_WINDOW_HEIGHT              : 480,
	
	LOGIN_IMAGE                        : "static/bleextop/resources/images/login-image.jpg"
	
});