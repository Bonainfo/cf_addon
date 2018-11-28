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
from odoo.tools.translate import _

from odoo.exceptions import except_orm, Warning, RedirectWarning

import logging
_logger = logging.getLogger(__name__)


class MarketplaceConfigSettings(models.TransientModel):
    _inherit = "marketplace.config.settings"

    mp_membership_product = fields.Integer(string="# of Products")

    @api.one
    def set_default_values(self):
        super(MarketplaceConfigSettings, self).set_default_values()
        self.env['ir.values'].sudo().set_default(
            'marketplace.config.settings', 'mp_membership_product', self.mp_membership_product)
        return True


    @api.model
    def get_default_values(self, fields=None):
        res = super(MarketplaceConfigSettings, self).get_default_values(fields)
        mp_membership_product = self.env['ir.values'].get_default(
            'marketplace.config.settings', 'mp_membership_product')
        res.update({"mp_membership_product" : mp_membership_product})
        return res

    @api.model
    def mp_config_translatable(self):
        res = super(MarketplaceConfigSettings, self).mp_config_translatable()
        try:
            trans_mp_config_setting_obj = self.env["translate.marketplace.config.settings"].browse([int(self.env['ir.values'].get_default(
                'marketplace.config.settings', 'trans_mp_config_setting_id'))])
            res.update({'mp_membership_plan_link_label': trans_mp_config_setting_obj.mp_membership_plan_link_label if trans_mp_config_setting_obj else False,})
        except Exception, e:
            _logger.info(
                "---Marketplace Miscellaneous setting is not configure -----------------------------")
        return res


    @api.multi
    def execute(self):
        for rec in self:
            if rec.mp_membership_product < 0 :
                raise Warning(_("Amount Limit can't be negative."))
        return super(MarketplaceConfigSettings, self).execute()

class TranslateMarketplaceConfigSettings(models.Model):
    _inherit = 'translate.marketplace.config.settings'

    mp_membership_plan_link_label = fields.Char(string="Seller Membership Plan Link Label", translate=True, default="Seller Membership Plans")
