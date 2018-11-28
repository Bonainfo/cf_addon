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

from odoo import api, fields, models, _ # alphabetically ordered

from odoo.exceptions import UserError, ValidationError

import logging
_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = "product.template"

    pharmacy_tag_ids = fields.Many2many("pharmacy.product.tag", string="Pharmacy Tags")

class PharmacyProductTag(models.Model):
    _name = "pharmacy.product.tag"

    name = fields.Char("Name", required=True, translate=True)
