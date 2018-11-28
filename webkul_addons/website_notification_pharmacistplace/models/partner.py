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

class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def get_notification_domain(self):
        self.ensure_one()
        domain = [
            "|",
            ("is_website_notification", "!=", True),
            "&",
            ("subject", "!=", False),
            ("model", "=", self._name),
            ("res_id", "=",  self.id),
            # ("needaction", "=",  False),
            "|",
            "&",
            "&",
            ("email_from", "!=", self.email),
            ("message_type", "=", "email"),
            ("partner_ids", "=", self.id),
            '&',
            ("message_type", "=", "comment"),
            ("needaction_partner_ids", "=", self.id),
        ]
        return domain

    @api.multi
    def get_notifications(self):
        self.ensure_one()
        #partner message
        partner_messages = self.env["mail.message"].search(self.get_notification_domain())
        #partner message
        user_messages = self.env["mail.message"].search(self.env.user.with_context(partner_obj=self).get_notification_domain())
        
        all_message = partner_messages + user_messages
        current_month_msg = all_message.filtered(lambda msg: datetime.strptime(msg.create_date, '%Y-%m-%d %H:%M:%S').month == datetime.today().month)
        if self._context.get("unread"):
            return current_month_msg.filtered(lambda msg: msg.is_notification_read == False)
            # return current_month_msg.filtered(lambda msg: msg.message_type == "comment" and msg.notification_ids.filtered(lambda n: n.is_read == False))
        return current_month_msg

    @api.one
    def notify_via_mail_to_seller(self, mail_templ_id):
        email_values = {
            "needaction_partner_ids": [(4, self.id)],
            "notification": True,
        }
        if self._context.get("partner_ids"):
            email_values.update({"partner_ids": [(4, self._context.get("partner_ids"))]})
        if not mail_templ_id:
            return False
        template_obj = self.env['mail.template'].browse(mail_templ_id)
        template_obj.send_mail(self.id, True, email_values=email_values)


    # @api.multi
    # def notify_via_mail_to_seller(self, mail_templ_id):
    #     email_values = {

    #     }
    #     mail_id = super(ResPartner, self).notify_via_mail_to_seller(mail_templ_id)
    #     if mail_id:
    #         mail_obj = self.env["mail.mail"].browse(mail_id)
    #         mail_obj.mail_message_id.is_website_notification = True
    #     return mail_id