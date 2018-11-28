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

from odoo import http, tools, _

from odoo.http import request
from odoo.addons.website_single_page_checkout.controllers.main import WebsiteSale

import logging
_logger = logging.getLogger(__name__)


class WebsiteSale(WebsiteSale):

    @http.route(['/shop/pricelist'], type='http', auth="public", website=True)
    def pricelist(self, promo, **post):
        res = super(WebsiteSale, self).pricelist(promo, **post)
        sale_order_id = request.session.get('sale_order_id')
        sale_order = request.env['sale.order'].sudo().browse(
            sale_order_id).exists() if sale_order_id else None
        if post.get("checkout_page"):
            pricelist = request.env['product.pricelist'].sudo().search(
                [('code', '=', promo)], limit=1)
            if not pricelist:
                if sale_order and sale_order.applied_sale_offer_id:
                    return request.redirect("/shop/checkout?code_applied=1")
                else:
                    return request.redirect("/shop/checkout?code_not_available=1")
            if pricelist and not request.website.is_pricelist_available(
                    pricelist.id):
                return request.redirect("/shop/checkout?code_not_available=1")

            request.website.sale_get_order(code=promo)
            return request.redirect("/shop/checkout")
        return res