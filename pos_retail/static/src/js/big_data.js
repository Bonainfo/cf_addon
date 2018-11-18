odoo.define('pos_retail.big_data', function (require) {
    var models = require('point_of_sale.models');
    var core = require('web.core');
    var _t = core._t;
    var rpc = require('pos.rpc');
    var ParameterDB = require('pos_retail.parameter');
    var pos_chanel = require('pos_retail.pos_chanel');
    var session = require('web.session');
    var indexed_db = require('pos_retail.indexedDB');

    models.load_models([
        {
            label: 'stock datas',
            condition: function (self) {
                return self.config.display_onhand;
            },
            loaded: function (self) {
                var stock_datas_loaded = new $.Deferred();
                rpc.query({
                    model: 'pos.cache.database',
                    method: 'get_stock_datas',
                    args: [self.config.stock_location_id[0], []]
                }).then(function (stock_datas) {
                    console.log('loaded stock done');
                    self['stock_datas'] = stock_datas;
                    stock_datas_loaded.resolve();
                }, function (type, err) {
                    stock_datas_loaded.reject();
                });
                return stock_datas_loaded;
            }
        }, {
            label: 'loading database',
            loaded: function (self) {
                /**
                 * We restore database for pos
                 * @type {{}}
                 */
                self.database = {};
                console.log('load browse cache');
                var status = new $.Deferred();
                $.when(indexed_db.search_read('product.pricelist')).then(function (results) {
                    self.database['product.pricelist'] = results;
                    return $.when(indexed_db.search_read('product.pricelist.item')).then(function (results) {
                        self.database['product.pricelist.item'] = results;
                        return $.when(indexed_db.search_read('product.product')).then(function (results) {
                            self.database['product.product'] = results;
                            return $.when(indexed_db.search_read('res.partner')).then(function (results) {
                                self.database['res.partner'] = results;
                                return $.when(indexed_db.search_read('account.invoice')).then(function (results) {
                                    self.database['account.invoice'] = results;
                                    return $.when(indexed_db.search_read('account.invoice.line')).then(function (results) {
                                        self.database['account.invoice.line'] = results;
                                        return $.when(indexed_db.search_read('pos.order')).then(function (results) {
                                            self.database['pos.order'] = results;
                                            return $.when(indexed_db.search_read('pos.order.line')).then(function (results) {
                                                self.database['pos.order.line'] = results;
                                                return $.when(indexed_db.search_read('sale.order')).then(function (results) {
                                                    self.database['sale.order'] = results;
                                                    return $.when(indexed_db.search_read('sale.order.line')).then(function (results) {
                                                        self.database['sale.order.line'] = results;
                                                        if (self.database['product.product'].length == 0 && self.database['res.partner'].length == 0) {
                                                            self.cached = false;
                                                        } else {
                                                            self.load_datas(self.database);
                                                            self.cached = true;
                                                        }
                                                        return status.resolve();
                                                    }).fail(function (error) {
                                                        self.database = false;
                                                        status.reject(error);
                                                    });
                                                }).fail(function (error) {
                                                    self.database = false;
                                                    status.reject(error);
                                                });
                                            }).fail(function (error) {
                                                self.database = false;
                                                status.reject(error);
                                            });
                                        }).fail(function (error) {
                                            self.database = false;
                                            status.reject(error);
                                        });
                                    }).fail(function (error) {
                                        self.database = false;
                                        status.reject(error);
                                    });
                                }).fail(function (error) {
                                    self.database = false;
                                    status.reject(error);
                                });
                            }).fail(function (error) {
                                self.database = false;
                                status.reject(error);
                            });
                        }).fail(function (error) {
                            self.database = false;
                            status.reject(error);
                        });
                    }).fail(function (error) {
                        self.database = false;
                        status.reject(error);
                    });
                }).fail(function (error) {
                    self.database = false;
                    status.reject(error);
                });
                return status.promise();
            }
        }, {
            label: 'store databases',
            condition: function (self) {
                return !self.cached
            },
            loaded: function (self) {
                console.log('load databases cache');
                self.models_cache = [];
                for (var index_number in self.model_lock) {
                    self.models_cache.push(self.model_lock[index_number]['model']);
                }
                var databases_loaded = new $.Deferred();
                rpc.query({
                    model: 'pos.cache.database',
                    method: 'load_master_data',
                    args: [self.models_cache, self.config.id]
                }).then(function (database) {
                    if (database) {
                        console.log('loading database done');
                        self.database = database;
                        self.load_datas(self.database);
                        for (var model in self.database) {
                            indexed_db.write(model, self.database[model]);
                        }
                    } else {
                        self.database = false
                    }
                    databases_loaded.resolve();
                }, function (type, err) {
                    databases_loaded.reject();
                });
                return databases_loaded;
            }
        }
    ]);
    var _super_PosModel = models.PosModel.prototype;
    models.PosModel = models.PosModel.extend({
        initialize: function (session, attributes) {
            this.stock_datas = {};
            this.write_date = '';
            this.next_load = 2000;
            this.model_lock = [];
            this.model_unlock = [];
            this.model_ids = session['model_ids'];
            for (var i = 0; i < this.models.length; i++) {
                var current_model = this.models[i];
                if (current_model.model && this.model_ids[current_model.model]) {
                    current_model['max_id'] = this.model_ids[current_model.model]['max_id'];
                    current_model['min_id'] = this.model_ids[current_model.model]['min_id'];
                    this.model_lock = _.filter(this.model_lock, function (model_check) {
                        return model_check['model'] != current_model.model;
                    });
                    this.model_lock.push(current_model);

                } else {
                    this.model_unlock.push(current_model)
                }
            }
            this.ParameterDB = new ParameterDB({});
            var config_id = this.ParameterDB.load(session.db + '_config_id');
            if (config_id) {
                var config_model = _.find(this.models, function (model) {
                    return model.model && model.model == "pos.config"
                });
                config_model.domain = [['id', '=', config_id]];
                this.config_id = config_id;
            }
            this.session = session;
            if (this.server_version == 10) {
                var currency_model = _.find(this.models, function (model) {
                    return model.model && model.model == "res.currency"
                });
                currency_model.ids = function (self) {
                    return [session.currency_id]
                }
            }
            return _super_PosModel.initialize.apply(this, arguments);
        },
        save_parameter_models_load: function () {
            console.log('save_parameter_models_load()');
            var models = {};
            var models_cache = [];
            for (var number in this.model_lock) {
                var model = this.model_lock[number];
                models[model['model']] = {
                    fields: model['fields'] || [],
                    domain: model['domain'] || [],
                    context: model['context'] || [],
                };
                if (model['model'] == 'res.partner' || model['model'] == 'product.pricelist.item' || model['model'] == 'product.pricelist') {
                    models[model['model']]['domain'] = []
                }
                if (model['model'] == 'product.pricelist.item') {
                    models[model['model']]['domain'] = []
                }
                models_cache.push(model['model'])
            }
            models['models_cache'] = models_cache;
            return rpc.query({
                model: 'pos.cache.database',
                method: 'save_parameter_models_load',
                args:
                    [models]
            })
        },
        first_install: function (model_name) {
            var self = this;
            var loaded = new $.Deferred();
            var model = _.find(this.model_lock, function (model) {
                return model.model == model_name;
            });
            if (!model) {
                return loaded.resolve();
            }
            var tmp = {};
            var fields = model.fields;

            function load_data(min_id, max_id) {
                var domain = [['id', '>=', min_id], ['id', '<', max_id]];
                var context = {}
                context['retail'] = true;
                if (model['model'] == 'product.product') {
                    domain.push(['available_in_pos', '=', true]);
                    var price_id = null;
                    if (self.pricelist) {
                        price_id = self.pricelist.id;
                    }
                    var stock_location_id = null;
                    if (self.config.stock_location_id) {
                        stock_location_id = self.config.stock_location_id[0]
                    }
                    context['location'] = stock_location_id;
                    context['pricelist'] = price_id;
                    context['display_default_code'] = false;
                }
                var params = {
                    model: model.model,
                    domain: domain,
                    fields: fields,
                    context: context,
                };
                var url = '/pos/api_first_install';
                return session.rpc(url, params, {}).then(function (results) {
                    if (!self.database) {
                        self.database = {};
                    }
                    if (!self.database[model['model']]) {
                        self.database[model['model']] = [];
                    }
                    self.database[model['model']] = self.database[model['model']].concat(results);
                    min_id += self.next_load;
                    if (results.length <= 0) {
                        console.warn('model ' + model['model'] + ' have results is 0')
                    }
                    if (results.length > 0) {
                        var process = min_id / model['max_id'];
                        if (process > 1) {
                            process = 1
                        }
                        self.chrome.loading_message(_t('Only one time installing ') + model['model'] + ': ' + (process * 100).toFixed(2) + ' %', process);
                        if (!self.database[model.model]) {
                            self.database[model.model] = results;
                        } else {
                            self.database[model.model] = self.database[model.model].concat(results);
                        }
                        max_id += self.next_load;
                        load_data(min_id, max_id);
                        indexed_db.write(model['model'], results);
                        return $.when(model.loaded(self, results, tmp)).then(function () {
                        }, function (err) {
                            loaded.reject(err);
                        })
                    } else {
                        if (max_id < model['max_id']) {
                            max_id += self.next_load;
                            load_data(min_id, max_id);
                        } else {
                            loaded.resolve();
                        }
                    }
                }).fail(function (type, error) {
                    self.chrome.loading_message(_t('Install fail, please try-again'));
                });
            }

            load_data(model['min_id'], model['min_id'] + this.next_load);
            return loaded;
        },
        load_datas: function (database) {
            this.chrome.loading_message(_t('Restore pos databases'), 0.90);
            var self = this;
            this.database = database;
            var pricelist_model = _.find(this.model_lock, function (model) {
                return model.model == 'product.pricelist';
            });
            if (pricelist_model) {
                var results = database[pricelist_model.model];
                pricelist_model.loaded(this, results, {});
            }
            for (var model_name in database) {
                var values = database[model_name];
                var model_loaded = _.find(this.model_lock, function (model) {
                    return model.model == model_name;
                });
                if (model_loaded) {
                    var results = database[model_name];
                    if (model_loaded.model == 'product.product') {
                        for (var i = 0; i < results.length; i++) {
                            var product = results[i];
                            if (this.stock_datas[product['id']]) {
                                product['qty_available'] = this.stock_datas[product['id']]
                            }
                        }
                    }
                    if (model_loaded.model != 'product.pricelist') {
                        model_loaded.loaded(this, results, {});
                    }
                }
                for (var i = 0; i < values.length; i++) {
                    var line = values[i];
                    if (!this.write_date) {
                        this.write_date = line.write_date;
                        continue;
                    }
                    if (this.write_date != line.write_date && new Date(this.write_date).getTime() < new Date(line.write_date).getTime()) {
                        this.write_date = line.write_date;
                    }
                }
            }
            console.log(this.write_date);
        },
        load_server_data: function () {
            var self = this;
            this.models = this.model_unlock;
            return _super_PosModel.load_server_data.apply(this, arguments).then(function () {
                for (var index_number in self.model_lock) {
                    self.models.push(self.model_lock[index_number]);
                }
                if (self.database) {
                    return true;
                } else {
                    return $.when(self.first_install('product.pricelist')).then(function () {
                        return $.when(self.first_install('product.pricelist.item')).then(function () {
                            return $.when(self.first_install('product.product')).then(function () {
                                return $.when(self.first_install('res.partner')).then(function () {
                                    return $.when(self.first_install('account.invoice')).then(function () {
                                        return $.when(self.first_install('account.invoice.line')).then(function () {
                                            return $.when(self.first_install('pos.order')).then(function () {
                                                return $.when(self.first_install('pos.order.line')).then(function () {
                                                    return $.when(self.first_install('sale.order')).then(function () {
                                                        return $.when(self.first_install('sale.order.line')).then(function () {
                                                            return true;
                                                        })
                                                    })
                                                })
                                            })
                                        })
                                    })
                                })
                            })
                        })
                    })
                }
            }).then(function () {
                if (self.write_date) {
                    rpc.query({
                        model: 'pos.cache.database',
                        method: 'search_read',
                        domain: [['updated_date', '>', self.write_date]],
                    }).then(function (results) {
                        console.log('total record need update: ' + results.length)
                        for (var i = 0; i < results.length; i++) {
                            result = results[i];
                            result_data = JSON.parse(result['data']);
                            result_data['model'] = result['res_model'];
                            result_data['deleted'] = result['deleted'];
                            if (self.server_version != 12) {
                                self.sync_backend.sync_with_backend(result_data);
                            }
                        }
                    });
                }
                return rpc.query({
                    model: 'res.currency',
                    method: 'search_read',
                    domain: [['active', '=', true]],
                    fields: ['name', 'symbol', 'position', 'rounding', 'rate']
                }).then(function (currencies) {
                    self.multi_currency = currencies;
                    self.save_parameter_models_load();
                });
            })
        }
    });
});
