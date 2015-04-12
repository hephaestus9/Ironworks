Ext.define("Login.modules.NewAccountForm",{
    extend             : "Login.abstract.Form",
    alias              : "newaccountform",
    forward            : true,
    initComponent      : function() {
        this.items = this.createNewAccountFields();
        this.fbar = this.createButton();
        this.callParent();
    },

    createButton: function(){
        return [{
            text       : "New Account",
            scope      : this,
            handler    : this.createAccount
        }];
    },

    createNewAccountFields: function(){
        return [{
            xtype    : "fieldcontainer",
            layout    : "hbox",
            defaultType : "textfield",
            width    : 360,
            items    : [{
                labelAlign    : "top",
                msgTarget     : 'side',
                fieldLabel    : "EMail",
                name          : "email",
                allowBlank    : false,
                flex          : 1,
                margins       : {right:3}
            },{
                labelAlign    : "top",
                msgTarget     : 'side',
                inputType     : 'password',
                fieldLabel    : 'Password',
                name          : 'password',
                allowBlank    : false,
                flex          : 1,
                margins       : {left:3},
                listeners     : {
                    scope         : this,
                    specialkey    : function(f,e){
                        if (e.getKey() == e.ENTER) {
                            this.createAccount();
                        }
                    }
                }
            }]
        }];
    },

    createAccount: function(){
        if(this.getForm().isValid()){
            var values = this.getForm().getValues();
            Login.Ajax.request({
                url        : Login.Constants.LOGIN_URL,
                params     : values,
                el         : this.up("window").el,
                scope      : this,
                success    : this.onSuccess,
                failure    : this.onFailure
            });
        }
    },

    onSuccess: function(data){
        if(data.success){
            if(this.forward){
                document.location = Login.Constants.HOME_URL;
            }else{
                var win = this.up("window");
                if(win){
                    win.close();
                }
            }

        }
    },

    onFailure: function(data,response){
        var passwrd = this.down("textfield[name=password]");

        Ext.create("Ext.tip.ToolTip",{
            anchor        : "left",
            target        : passwrd.bodyEl,
            trackMouse    : false,
            html          : data.message,
            autoShow      : true
        });
        passwrd.markInvalid(data.message);
    }
});