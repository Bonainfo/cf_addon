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
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = 'res.partner'

    pharmacy_account_detail_ids = fields.One2many("pharmacist.id.details",
        "pharmacist_customer_id",
        string= "Pharmacy Account Details",
        auto_join=True,)

    comm_registration_file = fields.Binary( string="Commercial Registration")
    comm_registration_filename = fields.Char( string='file name')
    tax_card_filename = fields.Char( string='file name')
    tax_card = fields.Binary( string="Tax Card")

    # comm_registration_file = fields.Binary(compute="_compute_files", string="Commercial Registration")
    # comm_registration_filename = fields.Char(compute="_compute_files", string='file name')
    # tax_card_filename = fields.Char(compute="_compute_files", string='file name')
    # tax_card = fields.Binary(compute="_compute_files", string="Tax Card")
    #
    # @api.depends("pharmacy_account_detail_ids")
    # def _compute_files(self):
    #     for obj in self:
    #         if obj.pharmacy_account_detail_ids:
    #             obj.comm_registration_file = obj.comm_registration_file.comm_registration_file
    #             obj.comm_registration_filename = obj.comm_registration_filename.comm_registration_filename
    #             obj.tax_card_filename = obj.tax_card_filename.tax_card_filename
    #             obj.tax_card = obj.tax_card.tax_card
