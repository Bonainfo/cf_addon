# -*- coding: utf-8 -*-
#################################################################################
# Author : Webkul Software Pvt. Ltd. (<https://webkul.com/>:wink:
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>;
#################################################################################
import logging
_logger = logging.getLogger(__name__)
from odoo.exceptions import UserError
from odoo import models, fields,api,_

class AffiliateProductPricelistItem(models.Model):
    _name = "affiliate.product.pricelist.item"
    _order = 'sequence'

    name = fields.Char(string="Name")
    advance_commision_id = fields.Many2one('advance.commision')
    applied_on = fields.Selection([
        ('3_global', 'Global'),
        ('2_product_category', ' Product Category'),
        ('1_product', 'Product')], "Apply On",
        default='3_global', required=True,
        help='Pricelist Item applicable on selected option')   
    categ_id = fields.Many2one(
        'product.public.category', 'Product Category', ondelete='cascade',
        help="Specify a product category if this rule only applies to products belonging to this eccmmerce website category or its children categories. Keep empty otherwise.")
    product_tmpl_id = fields.Many2one(
        'product.template', 'Product Template', ondelete='cascade',
        help="Specify a template if this rule only applies to one product template. Keep empty otherwise.")
    compute_price = fields.Selection([
        ('fixed', 'Fix Price'),
        ('percentage', 'Percentage (discount)')], index=True, default='fixed')
    fixed_price = fields.Float('Fixed Price')
    percent_price = fields.Float('Percentage Price')
    
    currency_id = fields.Many2one('res.currency', 'Currency', required=True,
        default=lambda self: self.env.user.company_id.currency_id.id,readonly='True')
    sequence = fields.Integer(required=True, default=1,
        help="The sequence field is used to define order in which the pricelist item are applied.")