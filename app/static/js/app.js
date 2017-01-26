
Ext.onReady(function () {

    //Creating base data model to work with
    Ext.define('Parcel', {
        extend: 'Ext.data.Model',
        fields: [
            'id',
            'first_name',
            'last_name',
            'sender_name',
            'city',
            'delivery_status',
        ]
    });

    //Creating store to hold data with dynamic loading via rest
    var store = Ext.create('Ext.data.Store', {
        model: 'Parcel',
        autoLoad: {start: 0, limit: 25},
        proxy: {
            noCache: false,
            type: 'rest',
            url: 'parcels',
            format: 'json',
            reader: {
                type: 'json',
                rootProperty: 'data',
                totalProperty: 'total'
            },
            writer: 'json',
        },
    });

    //Plugin to edit rows
    var rowEditing = Ext.create('Ext.grid.plugin.RowEditing', {
        clicksToEdit: 2,
        autoCancel: false,
    });

    //creating editor for rows data
    var textField = {
        xtype: 'textfield',
        getSubmitValue: function(){
            var value = this.getValue();
            if(Ext.isEmpty(value)) {
                return null;
            }
            return value;
    }
    };
    //initializing columns for the table
    var columns = [
        {
            header: 'ID',
            dataIndex: 'id',
            sortable: true,
            width: 50,
        },
        {
            header: 'First Name',
            dataIndex: 'first_name',
            sortable: true,
            flex: 1,
            editor: textField
        },
        {
             header: 'Last Name',
             dataIndex: 'last_name',
             sortable: true,
             flex: 1,
             editor: textField
        },
        {
            header: 'Sender Name',
            dataIndex: 'sender_name',
            sortable: true,
            editor: textField,
        },
        {
            header: 'City',
            dataIndex: 'city',
            sortable: true,
            editor: textField
        },
        {
            header: 'Parcel status',
            dataIndex: 'delivery_status',
            sortable: true,
            editor: textField
        },
    ];

    //setting pagination toolbar
    var pagingToolbar = {
        xtype: 'pagingtoolbar',
        store: store,
        displayInfo: true,
        items: [
            '-',
            {
                text: 'Save Changes',
                handler: function () {
                    store.sync();
                }
            },
            '-',
            {
                text: 'Reject Changes',
                handler: function () {
                    store.rejectChanges();
                }
            },
            '-'
        ]
    };

    //setting delete method
    var onDelete = function () {
        var selected = grid.selModel.getSelection();
        Ext.MessageBox.confirm(
                'Confirm delete',
                'Are you sure?',
                function (btn) {
                    if (btn == 'yes') {
                        var nn = selected[0].get('id')
                        var emp = store.getProxy();
                        emp.setExtraParam("id", nn)
                        grid.store.remove(selected);
                        grid.store.sync();
                    }
                }
        );
    };

    //setting create method
    var onInsertRecord = function () {
        var selected = grid.selModel.getSelection();
        rowEditing.cancelEdit();
        var newParcel= Ext.create("Parcel");
        store.insert(selected[0].index, newParcel);
        rowEditing.startEdit(selected[0].index, 0);
    };

    //setting context menu to edit data
    var doRowCtxMenu = function (view, record, item, index, e) {
        e.stopEvent();
        if (!grid.rowCtxMenu) {
            grid.rowCtxMenu = new Ext.menu.Menu({
                items: [
                    {
                        text: 'Insert Record',
                        handler: onInsertRecord

                    },
                    {
                        text: 'Delete Record',
                        handler: onDelete
                    }
                ]
            });
        }
        grid.selModel.select(record);
        grid.rowCtxMenu.showAt(e.getXY());
    };

    //setting panel for the table
    var grid = Ext.create('Ext.grid.Panel', {
        columns: columns,
        store: store,
        loadMask: true,
        bbar: pagingToolbar,
        plugins: [rowEditing],
        stripeRows: true,
        selType: 'rowmodel',
        viewConfig: {
            forceFit: true
        },
        listeners: {
            itemcontextmenu: doRowCtxMenu,
            destroy: function (thisGrid) {
                if (thisGrid.rowCtxMenu) {
                    thisGrid.rowCtxMenu.destroy();
                }
            }
        }
    });

    //setting window to hold table
    Ext.create('Ext.Window', {
        title: 'Parcels for BookCrossing',
        height: 600,
        width: 800,
        border: false,
        layout: 'fit',
        items: grid,
        closable: true,
        maximizable: true,
    }).show();
    store.load();
});

//set session token
Ext.Ajax.on('beforerequest', function (conn, options) {
   if (!(/^http:.*/.test(options.url) || /^https:.*/.test(options.url))) {
     if (typeof(options.headers) == "undefined") {
       options.headers = {'X-CSRFToken': Ext.util.Cookies.get('csrftoken')};
     } else {
       options.headers.extend({'X-CSRFToken': Ext.util.Cookies.get('csrftoken')});
     }
   }
}, this);