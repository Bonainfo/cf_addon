# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#################################################################################

import pprint
import werkzeug
from odoo.http import request
from odoo import http
import logging
_logger = logging.getLogger(__name__)

class PayfortPayment(http.Controller):

    @http.route('/payment/payfort/return', type='http', auth="none",methods=['GET', 'POST'], csrf=False)
    def payfort_form_redirect(self, **post):
        """ Gets the URL from payfort and redirect to that URL for payment """
        _logger.info(
            'Beginning form_feedback with post data %s', pprint.pformat(post))
        # debug
        # return_url = self._get_return_url(**post)
        _logger.info('payfort: validated data')
        res = request.env['payment.transaction'].sudo().form_feedback(post, 'payfort')
        if res:
            return werkzeug.utils.redirect('/shop/payment/validate')
        else:
            values = {
                "error_msg": "Something went Wrong.."
            }
        return http.request.render("payment_payfort.payment_payfort_error", values)