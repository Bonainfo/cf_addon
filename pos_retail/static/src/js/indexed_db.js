odoo.define('pos_retail.indexedDB', function (require) {
    "use strict";

    var indexedDB = window.indexedDB || window.mozIndexedDB || window.webkitIndexedDB || window.msIndexedDB || window.shimIndexedDB;

    if (!indexedDB) {
        window.alert("Your browser doesn't support a stable version of IndexedDB.")
    }

    var exports = {
        init: function (table_name) {
            var status = new $.Deferred();
            this.server_version = self.posmodel.server_version;
            var request = indexedDB.open(self.posmodel.session.db, 1);
            request.onerror = function (ev) {
                status.reject(ev);
            };
            request.onupgradeneeded = function (ev) {
                var db = ev.target.result;
                db.createObjectStore('product.pricelist', {keyPath: "id"});
                db.createObjectStore('product.pricelist.item', {keyPath: "id"});
                db.createObjectStore('product.product', {keyPath: "id"});
                db.createObjectStore('res.partner', {keyPath: "id"});
                db.createObjectStore('account.invoice', {keyPath: "id"});
                db.createObjectStore('account.invoice.line', {keyPath: "id"});
                db.createObjectStore('pos.category', {keyPath: "id"});
                db.createObjectStore('pos.order', {keyPath: "id"});
                db.createObjectStore('pos.order.line', {keyPath: "id"});
                db.createObjectStore('sale.order', {keyPath: "id"});
                db.createObjectStore('sale.order.line', {keyPath: "id"});
            };
            request.onsuccess = function (ev) {
                var db = ev.target.result;
                var transaction = db.transaction([table_name], "readwrite");
                transaction.oncomplete = function () {
                    db.close();
                };
                if (!transaction) {
                    status.reject(new Error('Cannot create transaction with ' + table_name));
                }
                var store = transaction.objectStore(table_name);
                if (!store) {
                    status.reject(new Error('Cannot get object store with ' + table_name));
                }
                status.resolve(store);
            };
            return status.promise();
        },
        write: function (table_name, items) {
            var self = this;
            $.when(this.init(table_name)).done(function (store) {
                _.each(items, function (item) {
                    store.put(item).onerror = function (e) {
                        console.warn(e)

                    }
                });
            }).fail(function (error) {
                console.log(error);
            });
        },
        unlink: function (table_name, item) {
            $.when(this.init(table_name)).done(function (store) {
                store.delete(item.id).onerror = function (e) {
                    console.warn(e);
                };
            }).fail(function (error) {
                console.warn(error);
            });
        },
        search_read: function (table_name) {
            var status = new $.Deferred();
            $.when(this.init(table_name)).done(function (store) {
                var request = store.getAll();
                request.onsuccess = function (ev) {
                    var items = ev.target.result || [];
                    status.resolve(items);
                };
                request.onerror = function (error) {
                    status.reject(error);
                };
            }).fail(function (error) {
                status.reject(error);
            });
            return status.promise();
        }
    };

    return exports;
});
