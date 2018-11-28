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

from odoo import api, fields, models, _  # alphabetically ordered

from odoo.exceptions import UserError, ValidationError

import logging
_logger = logging.getLogger(__name__)


class PPCity(models.Model):
    _name = "pp.city"

    @api.model
    def _default_country(self):
        egypt_country_id = self.env["res.country"].search(
            ["|", ("name", "ilike", "Egypt"), ("code", "ilike", "EG")], limit=1)
        return egypt_country_id

    name = fields.Char("Name", required=True)
    code = fields.Char("City Code",)
    state_id = fields.Many2one(
        "res.country.state", "Governorate", domain="[('country_id', '=', country_id)]")
    active = fields.Boolean("Active", default=True)
    country_id = fields.Many2one("res.country",  default=_default_country, string="Country")


class PharmacistIdDetails(models.Model):
    _inherit = "pharmacist.id.details"

    pp_city_id = fields.Many2one(
        "pp.city", string="City")
    #Should be related 
    # pp_city_id = fields.Many2one(
    #     "pp.city", related="pharmacist_customer_id.pp_city_id", string="City")
    city = fields.Char(related="pp_city_id.name", store=True)
