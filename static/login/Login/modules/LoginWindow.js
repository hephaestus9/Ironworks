/**
 * @class Bleext.modules.login.LoginPanel
 * @extends Bleext.ui.ModalPanel
 * @autor Crysfel Villa
 * @date Sun Jul 10 16:27:45 CDT 2011
 *
 * The login Panel.
 *
 **/


Ext.define("Login.modules.LoginWindow",{
	extend 			: "Login.abstract.ModalWindow",
	requires		: ["Login.modules.LoginForm"],
	
	layout			: "auto",
	modal			: false,
	width			: 400,
	height			: 240,
	closable		: false,
	
	forward			: true,
	
	initComponent: function() {
		
        this.items = this.buildItems();

		this.callParent();
	},
	
	buildItems	: function(){
		return [{
			xtype	: "component",
			html 	: '<img src="'+Login.Constants.LOGIN_IMAGE+'" />'
		},
			Ext.create("Login.modules.LoginForm",{forward:this.forward})
		];
	}
});