# -*- coding: utf-8 -*-
##########################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2016-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# License URL :<https://store.webkul.com/license.html/>
##########################################################################
from odoo import api, fields, models, tools, _


class StageUpdateWizad(models.TransientModel):
    _name = "stage.update.wizard"

    @api.model
    def is_cancel(self):
        return self._context.get('cancelled', False)

    stage_id = fields.Many2one(
        'helpdesk.stage', string='Stage', index=True, required=True)
    reason = fields.Text(string="Reason", required=True)
    is_cancel = fields.Boolean(string="Cancel", default=is_cancel)

    @api.multi
    def get_resolved_reason(self):
        def create_token(active_obj):
            vals = {'ticket_id': active_obj.id,
                    'partner_id': active_obj.partner_id.id,
                    'email': active_obj.email}
            review = self.env['helpdesk.review'].create(vals)
            return review

        for wizard in self:
            active_obj = self.env['helpdesk.ticket'].browse(
                self._context.get('active_id', False))
            if active_obj:
                ctx = self._context.copy()
                active_obj.stage_id = wizard.stage_id.id
                active_obj.resolve = True
                default = self.env['helpdesk.config.settings'].sudo(
                ).get_values()
                template = default.get(
                    'review_template_id') if default.get(
                        'review_template_id') else self.env.ref(
                    'website_helpdesk_system.email_template_review',
                    raise_if_not_found=False)

                if template:
                    review = create_token(active_obj)
                    template.send_mail(review.id, True)
                active_obj.message_post(
                    body=wizard.reason,
                )
        return {'type': 'ir.actions.act_window_close'}

    @api.multi
    def get_cancel_reason(self):
        for wizard in self:
            active_obj = self.env['helpdesk.ticket'].browse(
                self._context.get('active_id', False))
            if active_obj:
                ctx = self._context.copy()
                active_obj.stage_id = wizard.stage_id.id
                active_obj.cancel = True
