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

from odoo import models, fields, api

class marketplace_dashboard(models.Model):
    _inherit = "marketplace.dashboard"

    @api.one
    def _get_approved_count(self):
        res = super(marketplace_dashboard, self)._get_approved_count()
        if self.state == 'pharmacy_account':
            if self.is_user_seller():
                user_id = self.env['res.users'].search([('id', '=', self._uid)])
                seller_id = user_id.partner_id.id
                obj = self.env['pharmacist.id.details'].search([('marketplace_seller_id', '=', seller_id), ('pharmacist_id', '!=', False)])
            else:
                obj = self.env['pharmacist.id.details'].search([('marketplace_seller_id', '!=', False), ('pharmacist_id', '!=', False)])
            self.count_product_approved = len(obj)
        return res

    @api.one
    def _get_pending_count(self):
        res = super(marketplace_dashboard, self)._get_pending_count()
        if self.state == 'pharmacy_account':
            if self.is_user_seller():
                user_id = self.env['res.users'].search([('id', '=', self._uid)])
                seller_id = user_id.partner_id.id
                obj = self.env['pharmacist.id.details'].search([('marketplace_seller_id', '=', seller_id), ('pharmacist_id', '=', False)])
            else:
                obj = self.env['pharmacist.id.details'].search([('marketplace_seller_id', '!=', False), ('pharmacist_id', '=', False)])
            self.count_product_pending = len(obj)
        return res

    state = fields.Selection(selection_add=[('pharmacy_account', 'Pharmacy Accounts')])
