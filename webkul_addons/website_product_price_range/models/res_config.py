# -*- coding: utf-8 -*-
##########################################################################
#
#   Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#
##########################################################################
from odoo import api, fields, models, _
from odoo.exceptions import Warning
from odoo import SUPERUSER_ID

class WebsiteProductRangeSetting(models.TransientModel):
    _name = 'website.product.price.range.setting'
    _inherit = 'website.config.settings'
    product_range_start = fields.Integer(
        string="Price Range Start",
        default=1,
        required=1
    )
    product_range_end = fields.Integer(
        string="Price Range End",
        default=1000,
        required=1
    )
    @api.model
    def wk_activate_website_view(self):
        products_attributes = self.env.ref('website_sale.products_attributes')
        products_attributes.write(dict(active=1))
        return True


    @api.multi
    def set_product_price_range_limit_fields(self):
        ir_values = self.env['ir.values']
        for config in self:
            if self.product_range_start <=0 or self.product_range_end<=0:
                raise Warning(_("Range Start and Range End must be positive Integer."))
            elif (self.product_range_start >= config.product_range_end):
                raise Warning(_("Range Start must be smaller than Range End."))

            ir_values.set_default(
                'website.product.price.range.setting',
                'product_range_start',
                config.product_range_start or 1)
            ir_values.set_default(
                'website.product.price.range.setting',
                'product_range_end',
                config.product_range_end or 1000)
        return True
    @api.model
    def get_product_price_range_limit(self):
        ir_values = self.env['ir.values']
        rang_config_values_list_tuples = ir_values.get_defaults('website.product.price.range.setting')
        rang_config_values = {}
        for item in rang_config_values_list_tuples:
            rang_config_values.update({item[1]:item[2]})
        return rang_config_values
