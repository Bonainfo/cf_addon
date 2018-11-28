
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
class AffiliateProgram(models.Model):
    _name = "affiliate.program"

    name = fields.Char(string = "Name",required=True)
    ppc_type = fields.Selection([("s","Simple"),("a","Advance")], string="Type",required=True,default="s")
    amount_ppc_fixed = fields.Float(string="Amount Fixed",default=0,required=True)
    pps_type = fields.Selection([("s","Simple"),("a","Advanced")], string="Type",required=True,default="s")
    matrix_type = fields.Selection([("f","Fixed"),("p","Percentage")],required=True,default='f',string="Matrix Type")
    amount = fields.Float(string="Amount",default=0, required=True)
    currency_id = fields.Many2one('res.currency', 'Currency',
        default=lambda self: self.env.user.company_id.currency_id.id)
    advance_commision_id = fields.Many2one('advance.commision',string="Pricelist",domain="[('active_adv_comsn', '=', True)]")
     
    # product_id = fields.Many2one('product.product', string='Product')
    # product_price = fields.Float(string="product price")


    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        cxt = dict(self._context)
        cxt['hide_ppc'] = not self.env['ir.values'].get_default('affiliate.config.setting', 'enable_ppc')
        res = super(AffiliateProgram, self.with_context(cxt)).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        return res

    @api.onchange('matrix_type')
    def check_amount(self):
        m_type = self.matrix_type
        amount = self.amount
        if m_type == 'p' and amount > 100:
            self.amount = 0

    # def compute_price(self):
    #     _logger.info("-----compute price-=-%r-----------",1)
    #     pl,rule_id = self.product_pricelist_id.get_product_price_rule(self.product_id, 1.0, self.env.user)
    #     _logger.info("-----pl pl-=-%r-----------",pl)

    #     self. product_price = pl

       