# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#	See LICENSE file for full copyright and licensing details.
#################################################################################
from odoo import api, fields , models
from odoo.http import request
import logging
_logger = logging.getLogger(__name__)

class Website(models.Model):
	_inherit = "website"

	def get_current_price_range(self):
		if request.session.get("new_domain") and request.session.get("new_domain")[2]:
		 	return [request.session.get("new_domain")[2][0],request.session.get("new_domain")[2][-1]]
		else:  return self.get_price_range_limits()

	def get_price_range_limits(self):
		start = self.env['ir.values'].get_default('website.product.price.range.setting', 'product_range_start')
		end =  self.env['ir.values'].get_default('website.product.price.range.setting', 'product_range_end')
		return [start or 1,end or 1]
