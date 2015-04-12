
Ext.Loader.setConfig({
	enabled : true,
	paths   : {
		Login : Login.Constants.JS_PATH
	}
});

Ext.require("Login.modules.LoginForm");
Ext.require("Login.modules.NewAccountForm");

Ext.onReady(function(){
	var win = Ext.create("Login.modules.LoginWindow");
	win.show();

	//Ext.get("loading").remove();
});