# -*- coding: utf-8 -*-
###############################################################################
#
#  Copyright (c) 2017-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#
###############################################################################

from odoo import fields, models, api
from odoo.exceptions import Warning

import logging
_logger = logging.getLogger(__name__)


class HelpdeskConfigSettings(models.TransientModel):
    _name = "helpdesk.config.settings"
    _inherit = 'res.config.settings'

    enabled_recaptcha = fields.Boolean(
        string="Enabled reCAPTCHA")
    recaptcha_private_key = fields.Char(
        string="reCAPTCHA Private Key",
        help="Place Your reCAPTCHA Private Key",
        default='6LchkgATAAAAADbGqMvbRxHbTnTEkavjw1gSwCng'
    )
    recaptcha_site_key = fields.Char(
        string="reCAPTCHA Site Key",
        help="Place Your reCAPTCHA Site/Public Key",
        default='6LchkgATAAAAAAdTJ_RCvTRL7_TTcN3Zm_YXB39s'
    )
    review_template_id = fields.Many2one(
        "mail.template",string="Email Template",
        domain="[('model_id.model','=','helpdesk.review')]",
    )

    @api.multi
    def set_values(self):
        ir_values = self.env['ir.values'].sudo()
        review_template_id = self.env['ir.model.data'].get_object_reference(
            'website_helpdesk_system', 'email_template_review')[1]
        for config in self:
            ir_values.set_default(
                'helpdesk.config.settings', 'enabled_recaptcha',
                config.enabled_recaptcha or False)
            ir_values.set_default(
                'helpdesk.config.settings', 'recaptcha_private_key',
                config.recaptcha_private_key or '')
            ir_values.set_default(
                'helpdesk.config.settings', 'recaptcha_site_key',
                config.recaptcha_site_key or '')
            ir_values.set_default(
                'helpdesk.config.settings', 'review_template_id',
                config.review_template_id.id or review_template_id)

    @api.model
    def get_values(self):
        ir_values = self.env['ir.values'].sudo()
        review_template_id = self.env['ir.model.data'].get_object_reference('website_helpdesk_system', 'email_template_review')[1]
        return {
                'enabled_recaptcha': ir_values.get_default('helpdesk.config.settings', 'enabled_recaptcha') or False,
                'recaptcha_private_key': ir_values.get_default('helpdesk.config.settings', 'recaptcha_private_key'),
                'recaptcha_site_key': ir_values.get_default('helpdesk.config.settings', 'recaptcha_site_key'),
                'recaptcha_site_key': ir_values.get_default('helpdesk.config.settings', 'recaptcha_site_key') or review_template_id,
            }
