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

import werkzeug
import odoo
from odoo import http
from odoo.http import request
import base64
from odoo.tools.translate import _
from odoo.addons.website_sale.controllers.main import WebsiteSale
from werkzeug import url_encode
import logging
_logger = logging.getLogger(__name__)

class WebsiteSale(WebsiteSale):

    @http.route(["/product/sellers/<int:product_template_id>"], type="http", auth="public", website=True)
    def product_all_seller(self, product_template_id, **post):
        res = super(WebsiteSale, self).product_all_seller(product_template_id, **post)
        res.qcontext.update({
            "mp_other_seller_products": res.qcontext.get("mp_other_seller_products").filtered(lambda p: p.marketplace_seller_id)
        })
        return res
