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
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import time
import logging
_logger = logging.getLogger(__name__)


class MarketplaceConfigSettings(models.TransientModel):

    _inherit = 'marketplace.config.settings'

    pharmacies_count = fields.Integer(string="Pharmacies Count")
    distributor_count = fields.Integer(string="Distributor Count")

    @api.one
    def set_default_values(self):
        res = super(MarketplaceConfigSettings, self).set_default_values()
        self.env['ir.values'].sudo().set_default('marketplace.config.settings', 'pharmacies_count', self.pharmacies_count)
        self.env['ir.values'].sudo().set_default('marketplace.config.settings', 'distributor_count', self.distributor_count)
        return res

    @api.model
    def get_default_values(self, fields=None):
        res = super(MarketplaceConfigSettings, self).get_default_values()
        pharmacies_count = self.env['ir.values'].sudo().get_default('marketplace.config.settings', 'pharmacies_count')
        distributor_count = self.env['ir.values'].sudo().get_default('marketplace.config.settings', 'distributor_count')
        res.update(
            {
                'pharmacies_count'     :   pharmacies_count,
                'distributor_count' :   distributor_count,
            }
        )
        return res

