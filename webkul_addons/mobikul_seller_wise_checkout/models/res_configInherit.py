# -*- coding: utf-8 -*-
##########################################################################
#
#    Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#
##########################################################################
from odoo import api, fields, models
from odoo.tools.safe_eval import safe_eval

class MobikulConfigSettings(models.TransientModel):
	_inherit = 'mobikul.config.settings'


	module_marketplace_seller_wise_checkout = fields.Boolean(string='Allow Marketplace Seller Wise Checkout on App.', help="Use external Addon to add Marketplace Seller Wise Checkout")
