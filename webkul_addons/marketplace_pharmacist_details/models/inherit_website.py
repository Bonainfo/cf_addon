# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# License URL : https://store.webkul.com/license.html/
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################

from odoo import api, models, fields, _
import logging
_logger = logging.getLogger(__name__)
from odoo.http import request

class Website(models.Model):
    _inherit = 'website'

    def _hide_distributor_activator_step(self):
        url = request.httprequest.full_path
        order = request.website.sale_get_order()
        if "shop/cart" in url:
            admin_so = request.session.get('admin_so') or order
            seller_so = request.website._get_all_seller_sale_order_ids()
            admin_qty = order and order.cart_quantity or 0
            seller_qty = seller_so and sum(seller_so.mapped('cart_quantity')) or 0
            if admin_qty and not seller_qty:
                return False
        if "shop/checkout" in url and order and not order.marketplace_seller_id:
            return False
        if "/shop/payment" in url and order and not order.marketplace_seller_id:
            return False
        if "/shop/confirmation" in url:
            sale_last_order_id = self.env['sale.order'].sudo().browse(int(request.session.get("sale_last_order_id")))
            if sale_last_order_id and not sale_last_order_id.marketplace_seller_id:
                return False
        return True

    # @api.multi
    # def _check_pharmacy_account_exist(self):
    #     sale_order_id = request.website.sale_get_order()
    #     if sale_order_id and sale_order_id.marketplace_seller_id:
    #         so_ids = request.env['sale.order'].search([('pharmacy_id','=',sale_order_id.pharmacy_id.id)])
    #         if so_ids and len(so_ids) == 1:
    #             return True
    #     return False
