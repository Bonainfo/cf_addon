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


class Website(models.Model):

    _inherit = "website"

    @api.multi
    def get_saas_portal_client(self):
        partner = self.env.user.partner_id
        SaasPortalClient = self.env['saas_portal.client']

        instances = SaasPortalClient.sudo().search(
            [('partner_id', '=', partner.id)])
        return_dict = {
            "instances": instances,
            "pending_approval": instances.filtered(lambda o: o.state in ['pending', 'draft']),
            "all_done": len(instances) == len(instances.filtered(lambda o: o.state in ['cancelled', 'deleted'])),
        }
        return return_dict
