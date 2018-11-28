# -*- coding: utf-8 -*-
##########################################################################
#
#    Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#
##########################################################################
import logging
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = "sale.order"


    @api.multi
    @api.depends('order_line.product_uom_qty', 'order_line.product_id')
    def _compute_cart_count(self):
        is_wesiteSaleDelivery = self.env['mobikul'].sudo().check_mobikul_addons().get('website_sale_delivery')
        isSellerCheckout = self.env['mobikul'].sudo().check_mobikul_addons().get('marketplace_seller_wise_checkout')
        for order in self:
            if is_wesiteSaleDelivery:
                if isSellerCheckout:
                    order.cart_count = self.getCartCount(order)
                else:
                    order.cart_count = int(sum([line.product_uom_qty for line in order.order_line if not line.is_delivery]))
            else:
                order.cart_count = int(sum(order.mapped('order_line.product_uom_qty')))


    def getCartCount(self,order):
        so_ids = self.env["sale.order"].sudo().search([("partner_id","=",order.partner_id.id),("state","=","draft")])
        cart_value= 0
        for order in so_ids:
            cart_value += int(sum([line.product_uom_qty for line in order.order_line if not line.is_delivery]))
        return cart_value