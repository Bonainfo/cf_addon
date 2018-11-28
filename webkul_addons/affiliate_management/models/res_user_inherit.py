# -*- coding: utf-8 -*-
#################################################################################
# Author : Webkul Software Pvt. Ltd. (<https://webkul.com/>:wink:
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>;
#################################################################################
import logging
_logger = logging.getLogger(__name__)
from odoo.exceptions import UserError
from odoo import models, fields,api,_
import random, string
from ast import literal_eval

class ResUserInherit(models.Model):

	_inherit = 'res.users'
	_inherits = {'res.partner': 'partner_id'}

	res_affiliate_key = fields.Char(related='partner_id.res_affiliate_key',string='Partner Affiliate Key', inherited=True)


	@api.model
	def create(self,vals):
		result = super(ResUserInherit,self).create(vals)
		return result

	@api.multi
	def write(self,vals):
		_logger.info("========================= Res.users write operation  =======")
		return  super(ResUserInherit,self).write(vals)


	@api.multi
	def copy(self,default=None):
		_logger.info('-----copy values --%r------',default)
		_logger.info('-----copy values -partner_id-%r------',default.get('partner_id'))
		# _logger.info('-----copy values -partner_id-%r------',default.get('partner_id'))

		res= super(ResUserInherit,self).copy(default=default)

		# if default.get('partner_id'):
		# 	# assign the user group to new user
		# 	user_group_id = self.env['ir.model.data'].get_object_reference('affiliate_management', 'affiliate_security_user_group')[1]
		# 	groups_obj = self.env["res.groups"].browse(user_group_id)
		# 	if groups_obj:
		# 		for group_obj in groups_obj:
		# 			group_obj.write({"users": [(4, res.id, 0)]})
		return res
