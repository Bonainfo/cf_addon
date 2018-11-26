# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ProductSupplierinfo(models.Model):
    _inherit = 'product.supplierinfo'

    standard_price = fields.Float('Cost', related='product_id.standard_price')
    qty_available = fields.Float('Quantity On Hand', related='product_tmpl_id.qty_available')