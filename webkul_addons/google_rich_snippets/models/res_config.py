# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2017-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################


from odoo import api, fields, models


class RichSnippetsConfig(models.TransientModel):
    _name = 'rich.snippets.config'
    _inherit = 'res.config.settings'

    is_organization_enable = fields.Boolean(
        string='Organization info',
        help="Organization related features like contact, logo & social profile.")
    is_contact_enable = fields.Boolean(
        string='Corporate Contact',
        help="Your corporate contact information displayed in the Google Knowledge panel.")
    is_logo_enable = fields.Boolean(
        string='Logo',
        help="Your organization's logo in search results and Google Knowledge Graph.")
    is_social_enable = fields.Boolean(
        string='Social Profile',
        help="Your social profile information displayed on Google Knowledge panels.")

    is_website_enable = fields.Boolean(
        string='Website info',
        help="Website related features like Sitelinks Searchbox")
    is_searchbox_enable = fields.Boolean(
        string='Sitelinks Searchbox',
        help="A search box that is scoped to your website when it appears as a search result.")

    is_carousels_enable = fields.Boolean(
        string='Carousels',
        help="Display your rich results in a sequential list or gallery in search results.")
    is_breadcrumb_enable = fields.Boolean(
        string='Breadcrumb',
        help="Navigation that indicates the page's position in the site hierarchy.")
    is_rating_enable = fields.Boolean(
        string='Product Rating',
        help="The average rating based on multiple ratings or reviews of product.")
    is_stock_enable = fields.Boolean(
        string='Product Availibility',
        help="The average rating based on multiple ratings or reviews of product.")

    @api.model
    def get_values(self):
        res = {}
        IRSudo = self.env['ir.values'].sudo()
        res.update(
            is_organization_enable=IRSudo.get_default(
                'rich.snippets.config', 'is_organization_enable', False),
            is_contact_enable=IRSudo.get_default(
                'rich.snippets.config', 'is_contact_enable', False),
            is_logo_enable=IRSudo.get_default(
                'rich.snippets.config', 'is_logo_enable', False),
            is_social_enable=IRSudo.get_default(
                'rich.snippets.config', 'is_social_enable', False),
            is_website_enable=IRSudo.get_default(
                'rich.snippets.config', 'is_website_enable', False),
            is_searchbox_enable=IRSudo.get_default(
                'rich.snippets.config', 'is_searchbox_enable', False),
            is_carousels_enable=IRSudo.get_default(
                'rich.snippets.config', 'is_carousels_enable', False),
            is_breadcrumb_enable=IRSudo.get_default(
                'rich.snippets.config', 'is_breadcrumb_enable', False),
            is_rating_enable=IRSudo.get_default(
                'rich.snippets.config', 'is_rating_enable', False),
            is_stock_enable=IRSudo.get_default(
                'rich.snippets.config', 'is_stock_enable', False),
        )
        return res

    @api.multi
    def set_default_fields(self):
        IRSudo = self.env['ir.values'].sudo()
        IRSudo.set_default(
            'rich.snippets.config', 'is_organization_enable',
            self.is_organization_enable or False, False)
        IRSudo.set_default(
            'rich.snippets.config', 'is_contact_enable',
            self.is_contact_enable or False, False)
        IRSudo.set_default(
            'rich.snippets.config', 'is_logo_enable',
            self.is_logo_enable or False, False)
        IRSudo.set_default(
            'rich.snippets.config', 'is_social_enable',
            self.is_social_enable or False, False)
        IRSudo.set_default(
            'rich.snippets.config', 'is_website_enable',
            self.is_website_enable or False, False)
        IRSudo.set_default(
            'rich.snippets.config', 'is_searchbox_enable',
            self.is_searchbox_enable or False, False)
        IRSudo.set_default(
            'rich.snippets.config', 'is_carousels_enable',
            self.is_carousels_enable or False, False)
        IRSudo.set_default(
            'rich.snippets.config', 'is_breadcrumb_enable',
            self.is_breadcrumb_enable or False, False)
        IRSudo.set_default(
            'rich.snippets.config', 'is_rating_enable',
            self.is_rating_enable or False, False)
        IRSudo.set_default(
            'rich.snippets.config', 'is_stock_enable',
            self.is_stock_enable or False, False)
