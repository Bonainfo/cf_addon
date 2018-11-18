# -*- coding: utf-8 -*-
from odoo import api, models, fields, registry
import json
import ast
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
import odoo
import base64

class pos_cache_database(models.Model):
    _name = "pos.cache.database"
    _description = "Management POS database"

    res_id = fields.Char('Id')
    res_model = fields.Char('Model')
    data = fields.Text('Data')
    deleted = fields.Boolean('Deleted', default=0)
    updated_date = fields.Datetime('Updated date')

    @api.model
    def create(self, vals):
        # when create new record, auto add updated date
        vals['updated_date'] = fields.Datetime.now()
        return super(pos_cache_database, self).create(vals)

    @api.multi
    def write(self, vals):
        # when write new record, auto add updated date
        vals['updated_date'] = fields.Datetime.now()
        return super(pos_cache_database, self).write(vals)

    @api.model
    def sync_orders(self, config_id, datas):
        config = self.env['pos.config'].sudo().browse(config_id)
        for data in datas:
            value = {
                'data': data,
                'action': 'new_order',
                'bus_id': config.bus_id.id,
                'order_uid': data['uid']
            }
            self.env['bus.bus'].sendmany(
                [[(self.env.cr.dbname, 'pos.bus', config.user_id.id), json.dumps({
                    'user_send_id': self.env.user.id,
                    'value': value
                })]])

    @api.model
    def load_master_data(self, models_cache = [], config_id=None):
        database = {}
        for model_cache in models_cache:
            database[model_cache] = []
        caches = self.search_read(
            [('res_model', 'in', models_cache), ('deleted', '!=', True)], ['res_id', 'res_model', 'data', 'updated_date'])
        if caches:
            for cache in caches:
                vals = json.loads(cache['data'])
                vals['write_date'] = cache['updated_date'] # when read record, auto replace write date viva updated date
                database[cache['res_model']].append(vals)
        if database == {} or len(caches) == 0:
            return False
        else:
            return database

    @api.model
    def get_stock_datas(self, location_id, product_need_update_onhand=[]):
        location = self.env['stock.location'].browse(location_id)
        if location.stocks and not product_need_update_onhand:
            return json.loads(base64.decodestring(location.stocks).decode('utf-8'))
        values = {}
        if not product_need_update_onhand:
            datas = self.env['product.template'].with_context(location=location_id).search_read(
                [('type', '=', 'product'), ('available_in_pos', '=', True)], ['name', 'qty_available', 'default_code'])
        else:
            datas = self.env['product.template'].with_context(location=location_id).search_read(
                [('id', 'in', product_need_update_onhand)],
                ['name', 'qty_available', 'default_code'])
        for data in datas:
            products = self.env['product.product'].search([('product_tmpl_id', '=', data['id'])])
            if products:
                values[products[0].id] = data['qty_available']
        if not product_need_update_onhand:
            location.refresh_stocks()
        if values:
            return values
        else:
            return False

    @api.multi
    def get_fields_by_model(self, model_name):
        params = self.env['ir.config_parameter'].sudo().get_param(model_name)
        if not params:
            list_fields = self.env[model_name].fields_get()
            fields_load = []
            for k, v in list_fields.items():
                if v['type'] not in ['one2many', 'binary']:
                    fields_load.append(k)
            return fields_load
        else:
            params = ast.literal_eval(params)
            return params.get('fields', [])

    @api.multi
    def get_domain_by_model(self, model_name):
        params = self.env['ir.config_parameter'].sudo().get_param(model_name)
        if not params:
            return []
        else:
            params = ast.literal_eval(params)
            return params.get('domain', [])

    @api.model
    def insert_data(self, datas, model, first_install=False):
        write_date = fields.Datetime.now()
        if type(model) == list:
            return False
        all_fields = self.env[model].fields_get()
        version_info = odoo.release.version_info[0]
        if version_info == 12:
            if all_fields:
                for data in datas:
                    for field, value in data.items():
                        if field == 'model':
                            continue
                        if all_fields[field] and all_fields[field]['type'] in ['date', 'datetime'] and value:
                            data[field] = value.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        if first_install:
            for data in datas:
                data['write_date'] = write_date
                self.create({
                    'res_id': str(data['id']),
                    'res_model': model,
                    'data': json.dumps(data),
                })
        else:
            for data in datas:
                data['write_date'] = write_date
                last_caches = self.search([('res_id', '=', str(data['id'])), ('res_model', '=', model)])
                if last_caches:
                    last_caches.write({
                        'data': json.dumps(data),
                    })
                else:
                    self.create({
                        'res_id': str(data['id']),
                        'res_model': model,
                        'data': json.dumps(data),
                    })
        return True

    def sync_to_pos(self, data):
        if data['model'] == 'product.product':
            data['price'] = data['list_price']
        sessions = self.env['pos.session'].sudo().search([
            ('state', '=', 'opened')
        ])
        self.insert_data([data], data['model'])
        for session in sessions:
            self.env['bus.bus'].sendmany(
                [[(self.env.cr.dbname, 'pos.sync.data', session.user_id.id), data]])
        return True

    @api.model
    def remove_record(self, data):
        self.search([('res_id', '=', str(data['id'])), ('res_model', '=', data['model'])]).write({
            'deleted': True
        })
        sessions = self.env['pos.session'].sudo().search([
            ('state', '=', 'opened')
        ])
        data['deleted'] = True
        for session in sessions:
            self.env['bus.bus'].sendmany(
                [[(self.env.cr.dbname, 'pos.sync.data', session.user_id.id), data]])
        return True

    @api.model
    def save_parameter_models_load(self, model_datas):
        for model_name, value in model_datas.items():
            self.env['ir.config_parameter'].sudo().set_param(model_name, value)
        return True
