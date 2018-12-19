# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ProductSupplierinfo(models.Model):
    _inherit = 'product.supplierinfo'

    barcode = fields.Char('Barcode', related='product_tmpl_id.barcode')
    standard_price = fields.Float('Cost', related='product_tmpl_id.standard_price')
    qty_available = fields.Float('Quantity On Hand', related='product_tmpl_id.qty_available')
    total = fields.Float(compute='_value_pc', string='Total')

    @api.multi
    @api.depends('standard_price', 'qty_available')
    def _value_pc(self):
        for line in self:
            line.total = line.standard_price * line.qty_available


class ProducProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    product_ref = fields.Integer(related='product_id.default_code', store=True, translate=True)
    product_barcode = fields.Char('Barcode', related='product_id.barcode', store=True, translate=True)


class QuantsRports(models.Model):
    _inherit = 'stock.quant'

    lot_life_date = fields.Datetime(related='lot_id.life_date', store=True)
    product_ref = fields.Integer(related='product_id.default_code', store=True)
    product_barcode = fields.Char(related='product_id.barcode', store=True)
    qty_available = fields.Float(related='product_id.qty_available', store=True)


class ProductTempalteLot(models.Model):
    _inherit = 'product.template'

    lot_no = fields.One2many('stock.production.lot', 'product_id', string='Batch No.')
    default_code = fields.Integer(store=True)
    
class ProductProductIndex(models.Model):
    _inherit = 'product.product'
    
    display_name = fields.Char(index=True)
    name = fields.Char(index=True, store=True)
    default_code = fields.Integer(store=True)
