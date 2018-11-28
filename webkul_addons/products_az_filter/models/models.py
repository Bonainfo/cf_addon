# -*- coding: utf-8 -*-
##########################################################################
#
#    Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#
##########################################################################
from odoo import models, fields, api, _
import string
class Website(models.Model):
	_inherit = 'website'
	@api.model
	def get_alphabets(self):
		return list(string.ascii_uppercase)
