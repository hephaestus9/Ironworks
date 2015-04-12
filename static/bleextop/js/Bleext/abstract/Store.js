/**
 * @class Bleext.abstract.Store
 * @extends Ext.data.Store
 * requires
 * @autor Crysfel Villa
 * @date Thu Jul 21 19:16:11 CDT 2011
 *
 * Description
 *
 *
 **/

Ext.define("Bleext.abstract.Store",{
	extend	: "Ext.data.Store",
	
	autoLoad	: true,
	
	constructor	: function(options){
		var me = this;
		
		Ext.apply(me,options || {});
		me.proxy = {
	       type		: "ajax",
	       url		: "/settings",
	       reader	: {
	           	type			: "json",
	           	root			: "data",
	           	successProperty	: "success",
				totalProperty	: "total"
	       }
	   };
	
		me.callParent(arguments);
	}
});