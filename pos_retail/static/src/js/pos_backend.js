odoo.define('pos_retail.pos_backend', function (require) {
    "use strict";

    var bus = require('bus.bus').bus;
    var WebClient = require('web.WebClient');

    var indexedDB = window.indexedDB || window.mozIndexedDB || window.webkitIndexedDB || window.msIndexedDB || window.shimIndexedDB;

    if (!indexedDB) {
        window.alert("Your browser doesn't support a stable version of IndexedDB.")
    }

    WebClient.include({
        remove_indexed_db: function (notifications) {
            var dbName = JSON.parse(notifications).db;
            indexedDB.deleteDatabase(dbName);
            console.log('deleted pos indexdb');
        },
        show_application: function () {
            bus.on('notification', this, function (notifications) {
                _.each(notifications, (function (notification) {
                    if (notification[0][1] === 'pos.indexed_db') {
                        this.remove_indexed_db(notification[1]);
                    }
                }).bind(this));
            });
            return this._super.apply(this, arguments);
        }
    });

});
