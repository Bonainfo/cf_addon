# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2017-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
# Developed By: Jahangir
#################################################################################


from odoo import api, models, fields

import logging
_logger = logging.getLogger(__name__)


class EmailVerificationConfig (models.TransientModel):
	_name = 'email.verification.config'
	_inherit = 'res.config.settings'


	# send_email_on_signup = fields.Boolean(
	# 	string="Send Email On Signup",
	# 	help="Email will be sent to the customers on signup"
	# 	)
	token_validity = fields.Integer(
		string='Token Validity In Days',
		help="Validity of the token in days sent in email. If validity is 0 it means infinite.",
		
	  )
	restrict_unverified_users = fields.Boolean(
		string='Restrict Unverified Users From Checkout',
		help="If enabled unverified users can not proceed to checkout untill they verify their emails")
	unverified_email_msg = fields.Char(
		string='Message for email verification',
		help="This msg is shown to user if email is unverified."

	)
	expired_email_link_msg =fields.Char(
		string='Message after email link expired',
		help="This msg is shown to user if verification link sent on email expires."

	)
	

	@api.multi
	def set_default_fields(self):
		ir_values = self.env['ir.values']
		# ir_values.sudo().set_default('email.verification.config', 'send_email_on_signup', self.send_email_on_signup)
		ir_values.sudo().set_default('email.verification.config', 'token_validity', self.token_validity)
		ir_values.sudo().set_default('email.verification.config', 'restrict_unverified_users', self.restrict_unverified_users)
		ir_values.sudo().set_default('email.verification.config', 'unverified_email_msg', self.unverified_email_msg)
		ir_values.sudo().set_default('email.verification.config', 'expired_email_link_msg', self.expired_email_link_msg)
		
		return True

	@api.multi
	def get_default_fields(self, fields):
		ir_values = self.env['ir.values']
		# send_email_on_signup = ir_values.sudo().get_default('email.verification.config', 'send_email_on_signup')
		token_validity = ir_values.sudo().get_default('email.verification.config', 'token_validity') 
		restrict_unverified_users = ir_values.sudo().get_default('email.verification.config', 'restrict_unverified_users') 
		unverified_email_msg = ir_values.sudo().get_default('email.verification.config', 'unverified_email_msg') 
		expired_email_link_msg = ir_values.sudo().get_default('email.verification.config', 'expired_email_link_msg') 
		
		return {
			# 'send_email_on_signup': send_email_on_signup,
			'token_validity': token_validity,
			'restrict_unverified_users': restrict_unverified_users,
			'unverified_email_msg':unverified_email_msg if unverified_email_msg!=None else "The account is not verified yet, you need to verify your account before proceeding further. If you want to re-send link",
			'expired_email_link_msg':expired_email_link_msg if expired_email_link_msg!=None else "The account is not verified yet, you need to verify your account before proceeding further. The link sent to your email has been expired, for sending a new link",
		}
