# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
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

from odoo import fields, models, api
from odoo import SUPERUSER_ID
from odoo.exceptions import UserError
from odoo.tools.translate import _
import logging
_logger = logging.getLogger(__name__)


class Users(models.Model):
    _inherit = 'res.users'

    @api.multi
    def get_notification_domain(self):
        self.ensure_one()
        if self._context.get("partner_obj"):
            self = self._context.get("partner_obj").user_ids[0]
        domain = [
            "|",
            ("is_website_notification", "!=", True),
            "&",
            ("subject", "!=", False),
            ("model", "=", self._name),
            ("res_id", "=",  self.id),
            "|",
            "&",
            "&",
            ("email_from", "!=", self.email),
            ("message_type", "=", "email"),
            ("partner_ids", "=", self.partner_id.id),
            '&',
            ("message_type", "=", "comment"),
            ("needaction_partner_ids", "=", self.partner_id.id),
        ]
        return domain

    @api.model
    def create(self, values):
        user_obj = super(Users, self).create(values)
        # Send signup mail
        if user_obj:
            email_template_obj = self.env.ref("website_notification_pharmacistplace.pp_website_signup_email_template")
            if email_template_obj:
                mail_confirmed = email_template_obj.send_mail(
                    user_obj.id, 
                    True, 
                    email_values={
                        "needaction_partner_ids": [(4, user_obj.partner_id.id)],
                        "notification": True,
                        "partner_ids": [(4, user_obj.partner_id.id)],
                    }
                )
                if mail_confirmed:
                    _logger.info(
                        "*****************Signup Mail Send to New User with User id :- %r", user_obj)
            else:
                _logger.info(
                    "*****************Signup Mail not Send email template not found")
        return user_obj
