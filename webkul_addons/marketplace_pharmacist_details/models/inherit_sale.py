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
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = "sale.order"

    pharmacy_id = fields.Many2one("pharmacist.id.details", string="Pharmacy Id")
    # pharmacy_id = fields.Many2one("pharmacist.id.details", compute="_compute_so_pharmacy_id", search="_make_pharmacy_id_searchable", string="Pharmacy Id")

    # @api.multi
    # def _compute_so_pharmacy_id(self):
    #     obj = self.search([])
    #     for rec in obj:
    #         if rec.marketplace_seller_id:
    #            pharmacy_account = self.env['pharmacist.id.details'].sudo().search([
    #                    ('pharmacist_customer_id','=', rec.partner_id.id),
    #                    ('marketplace_seller_id','=', rec.marketplace_seller_id.id)]
    #                )
    #                rec.pharmacy_id = pharmacy_account.id if pharmacy_account else False
    #
    # @api.multi
    # def _make_pharmacy_id_searchable(self, operator, value):
    #     so_ids = []
    #     for obj in self.sudo().search([]):
    #         if obj.pharmacy_id.id == value:
    #             so_ids.append(obj.id)
    #     return [('id', 'in', so_ids)]

    @api.multi
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        if self._context.get("check_pharmacy_id"):
            for rec in self:
                if rec.marketplace_seller_id and rec.pharmacy_id and not rec.pharmacy_id.pharmacist_id:
                    raise UserError(_("Please provide a Pharmacy Id to Approve this Order."))
        return res

class account_invoice(models.Model):
    _inherit = 'account.invoice'

    pharmacy_id = fields.Many2one("pharmacist.id.details", compute="_compute_inv_pharmacy_id", string="Pharmacy Id")

    @api.multi
    def _compute_inv_pharmacy_id(self):
        obj = self.search([])
        for rec in obj:
            if rec.origin:
                so_obj = self.env["sale.order"].sudo().search([('name', '=', rec.origin)], limit=1)
                if so_obj and so_obj.marketplace_seller_id:
                    rec.pharmacy_id = so_obj.pharmacy_id if so_obj.pharmacy_id else False
