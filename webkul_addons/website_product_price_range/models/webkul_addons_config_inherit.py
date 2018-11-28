# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#	See LICENSE file for full copyright and licensing details.
#################################################################################

from odoo import api, fields, models, _
from odoo.exceptions import Warning

class WebkulWebsiteAddons(models.TransientModel):
    _inherit = 'webkul.website.addons'
    ##inherit the module for adding config option in webkul_website_addons
   