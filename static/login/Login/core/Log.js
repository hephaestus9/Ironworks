/**
 * @class Bleext.core.Log
 * @extends Object
 * @autor Crysfel Villa
 * @date Sun Jul 10 22:12:39 CDT 2011
 *
 * Class for logging
 *
 **/

Ext.define("Login.core.Log",{
	extend 		: "Object",
	singleton	: true,

	log			: function(object){
		if(console){
			console.log(object);
		}
	}
});

Login.log = Login.core.Log.log;