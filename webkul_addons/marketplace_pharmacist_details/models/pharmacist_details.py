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


class PharmacistIdDetails(models.Model):
    _name = "pharmacist.id.details"
    _rec_name = "pharmacist_id"
    _order = "write_date desc"

    @api.model
    def _default_country(self):
        egypt_country_id = self.env["res.country"].sudo().search(
            ["|", ("name", "ilike", "Egypt"), ("code", "ilike", "EG")], limit=1)
        return egypt_country_id

    name = fields.Char("Name", required=True)

    comm_registration_file = fields.Binary("Commercial Registration")
    comm_registration_filename = fields.Char('file name')
    tax_card_filename = fields.Char('file name')
    tax_card = fields.Binary("Tax Card")

    pharmacist_id = fields.Char("Pharmacy Id")
    pharmacist_name = fields.Char("Pharmacy Name")
    marketplace_seller_id = fields.Many2one("res.partner", "Seller",
        required= True,
        domain="[('seller','=', True),('state','=','approved')]")
    pharmacist_customer_id = fields.Many2one("res.partner", string="Pharmacy Customer", required= True)

    email = fields.Char(related="pharmacist_customer_id.email", string="Email")
    phone = fields.Char(related="pharmacist_customer_id.phone", string="Phone")
    # mobile = fields.Char(related="pharmacist_customer_id.mobile", "Mobile")
    street1 = fields.Char(related="pharmacist_customer_id.street", string="Street")
    street2 = fields.Char(related="pharmacist_customer_id.street2", string="Street2")
    city = fields.Char(related="pharmacist_customer_id.city", string="City")
    zipcode = fields.Char(related="pharmacist_customer_id.zip", string="Postal Code")
    state_id = fields.Many2one(
        'res.country.state', related="pharmacist_customer_id.state_id", string="State")
    country_id = fields.Many2one(
        'res.country', related="pharmacist_customer_id.country_id", default=_default_country, string="Country")

    _sql_constraints = [
        ('unique_pharmacist_id', 'unique(pharmacist_id)', _('There is already a record with this Pharmacy Id.')),
        ('pharmacist_customer_seller_uniq', 'unique (pharmacist_customer_id, marketplace_seller_id)',
        _('There is already a record for this customer with this seller.'))
    ]

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            if record.pharmacist_id:
                result.append((record.id, record.pharmacist_customer_id.name + "("+ record.pharmacist_id +")"))
                # result.append((record.id, record.pharmacist_id))
            else:
                result.append((record.id, record.pharmacist_customer_id.name))
        return result

    @api.multi
    def write(self, vals):
        res = super(PharmacistIdDetails, self).write(vals)
        for rec in self:
            pharmacist_customer_id = vals.get("pharmacist_customer_id") if vals.get("pharmacist_customer_id") else rec.pharmacist_customer_id
            if vals.get("comm_registration_file"):
                pharmacist_customer_id.comm_registration_file = rec.comm_registration_file
                pharmacist_customer_id.comm_registration_filename = rec.comm_registration_filename
            if vals.get("tax_card"):
                pharmacist_customer_id.tax_card = rec.tax_card
                pharmacist_customer_id.tax_card_filename = rec.tax_card_filename
        return res
