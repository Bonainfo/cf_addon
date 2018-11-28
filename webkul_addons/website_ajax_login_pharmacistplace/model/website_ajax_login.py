# -*- coding: utf-8 -*-
#################################################################################
#
#    Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#
#################################################################################
from odoo import fields,models,api,http
from odoo.tools.safe_eval import safe_eval

import logging
_logger = logging.getLogger(__name__)


class website(models.Model):
	""" this model make these fields avilable on front end template """
	_inherit='website'
	wk_allow_signup=fields.Boolean(string="Allow Sign-UP")
	website_odoo_login=fields.Boolean("Odoo Login")
	website_facebook_login=fields.Boolean("Facebook Login")
	website_gmail_login=fields.Boolean("Gmail Login")


	@api.one 
	def wk_get_social_enabled(self):
		if  self.website_gmail_login or self.website_facebook_login or self.website_odoo_login:
			return True
		else:
			return False
		
	@api.model
	def get_db_list(self):
		return http.db_list()

	@api.model
	def get_wk_block_ui_info(self):
		web_config_obj = self.env["website.config.settings"].sudo().get_default_ajax_values()
		return web_config_obj.get("wk_block_ui")
	
	@api.model
	def get_enable_reset_password(self):
		return safe_eval(self.env['ir.config_parameter'].get_param('auth_signup.reset_password', 'False'))

