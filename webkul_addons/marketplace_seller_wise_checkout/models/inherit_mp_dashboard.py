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

from odoo import models, fields, api, _
import logging
_logger = logging.getLogger(__name__)

class marketplace_dashboard(models.Model):
    _inherit = "marketplace.dashboard"

    @api.one
    def _get_approved_count(self):
        res = super(marketplace_dashboard, self)._get_approved_count()
        if self.state == 'order':
            if self.is_seller:
                user_obj = self.env['res.users'].browse(self._uid)
                obj = self.env['sale.order'].search(
                    [('marketplace_seller_id', '=',user_obj.partner_id.id), ('mp_order_state', '=', 'approved')])
            else:
                obj = self.env['sale.order'].search(
                    [('marketplace_seller_id', '!=', False), ('mp_order_state', '=', 'approved')])
            self.count_product_approved = len(obj)
        return res

    @api.one
    def _get_pending_count(self):
        res = super(marketplace_dashboard, self)._get_pending_count()
        if self.state == 'order':
            user_obj = self.env['res.users'].browse(self._uid)
            if self.is_seller:
                obj = self.env['sale.order'].search(
                    [('marketplace_seller_id', '=',user_obj.partner_id.id), ('mp_order_state', '=', 'new')])
            else:
                obj = self.env['sale.order'].search(
                    [('marketplace_seller_id', '!=', False), ('mp_order_state', '=', 'new')])
            self.count_product_pending = len(obj)
        return res
