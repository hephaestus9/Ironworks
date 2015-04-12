/**
 * @class Bleext.ui.ModalPanel
 * @extends Ext.Panel
 * @autor Crysfel Villa
 * @date Sun Jul 10 16:29:08 CDT 2011
 *
 * A modal panel that appears in top of everything
 *
 **/

Ext.define("Login.abstract.ModalWindow",{
	extend 			: "Ext.Window",
	
	layout			: "fit",
	cls				: "login-window",
	modal			: true,
	draggable 		: false,
	resizable		: false,
	bodyPadding		: 10
});