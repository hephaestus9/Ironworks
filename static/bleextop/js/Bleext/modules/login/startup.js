
Ext.Loader.setConfig({
	enabled : true,
	paths   : {
		Bleext : Bleext.desktop.Constants.JS_PATH+"Bleext"
	}
});

Ext.require("Bleext.modules.login.LoginForm");

Ext.onReady(function(){
	var win = Ext.create("Bleext.modules.login.LoginWindow");
	win.show();

	Ext.get("loading").remove();
});