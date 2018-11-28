# -*- coding: utf-8 -*-
##########################################################################
#
#    Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#
##########################################################################
from odoo import fields, models
from odoo import api
import logging
from odoo.tools.safe_eval import safe_eval

_logger = logging.getLogger(__name__)


class website_config_settings(models.TransientModel):

    _inherit = 'website.config.settings'

    auth_signup_uninvited = fields.Boolean(
        "Allow Sign-UP",
        related="website_id.wk_allow_signup"
    )
    website_odoo_login = fields.Boolean(
        "Odoo Login",
        related="website_id.website_odoo_login"
    )
    website_facebook_login = fields.Boolean(
        "Facebook Login",
        related="website_id.website_facebook_login"
    )
    website_gmail_login = fields.Boolean(
        "Google Login",
        related="website_id.website_gmail_login"
    )
    facebook_client_id = fields.Char(
        "Facebook App ID"
    )
    google_client_id = fields.Char(
        "Google Client ID"
    )
    show_ajax_form_always = fields.Boolean(
        "Pop Up Ajax form if user not logged in, on every web page.")
    wk_block_ui = fields.Boolean(
        "Don't allow user to close the Ajax Pop Up form without login.")

    @api.model
    def get_default_ajax_values(self, fields=None):
        google_id = self.env.ref('auth_oauth.provider_google')
        facebook_id = self.env.ref('auth_oauth.provider_facebook')

        # rg = google_idread(['enabled','client_id'])
        # rf = facebook_id.read(['enabled','client_id'])
        ir_values = self.env['ir.values']
        auth_signup_uninvited = ir_values.get_default(
            'website.config.settings',
            'auth_signup_uninvited'
        )
        show_ajax_form_always = ir_values.get_default(
            'website.config.settings',
            'show_ajax_form_always'
        )
        wk_block_ui = ir_values.get_default(
            'website.config.settings',
            'wk_block_ui'
        )
        return {
            'auth_signup_uninvited': auth_signup_uninvited,
            'website_gmail_login': google_id.enabled,
            'google_client_id': google_id.client_id,
            'website_facebook_login': facebook_id.enabled,
            'facebook_client_id': facebook_id.client_id,
            'show_ajax_form_always': show_ajax_form_always,
            'wk_block_ui': wk_block_ui
        }

    @api.multi
    def set_ajax_values(self):
        icp = self.env['ir.config_parameter']
        ir = self.env['ir.values']
        for record in self:
            google_id = self.env.ref('auth_oauth.provider_google')
            facebook_id = self.env.ref('auth_oauth.provider_facebook')
            config = record
            google_vals = {
                'enabled': config.website_gmail_login,
                'client_id': config.google_client_id,
            }
            fb_vals = {
                'enabled': config.website_facebook_login,
                'client_id': config.facebook_client_id,
            }
            google_id.write(google_vals)
            facebook_id.write(fb_vals)
            icp.set_param(
                'auth_signup.allow_uninvited',
                repr(config.auth_signup_uninvited))
            self.env["ir.values"].set_default(
                'website.config.settings',
                'auth_signup_uninvited',
                config.auth_signup_uninvited
            )
            self.env["ir.values"].set_default(
                'website.config.settings',
                'show_ajax_form_always',
                config.show_ajax_form_always
            )
            self.env["ir.values"].set_default(
                'website.config.settings',
                'wk_block_ui',
                config.wk_block_ui
            )

        return True
