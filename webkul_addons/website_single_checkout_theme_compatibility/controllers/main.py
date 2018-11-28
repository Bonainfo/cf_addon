# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
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
# If not, see <https://store.webkul.com/license.html/>
#################################################################################
from odoo import http, tools, api, _, SUPERUSER_ID
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.report import report_sxw

import logging
_logger = logging.getLogger(__name__)


# class WebsiteSale(WebsiteSale):

#     @http.route(['/shop/payment/transaction/<int:acquirer_id>'], type='json', auth="public", website=True)
#     def payment_transaction(self, acquirer_id, tx_type='form', token=None, **kwargs):
#         res = super(WebsiteSale, self).payment_transaction(
#             acquirer_id=acquirer_id, tx_type=tx_type, token=token, **kwargs)
#         if type(res) is str and '<form' in res:
#             res = res.replace('<form', '<form class="hide"')
#         return res
