# -*- coding: utf-8 -*-
#################################################################################
#
#    Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#
#################################################################################
from odoo.http import route,request
import logging
from odoo import http,SUPERUSER_ID
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo.tools.translate import _
import re
import werkzeug
import json
from odoo.addons.auth_oauth.controllers.main import OAuthLogin
from odoo.addons.auth_signup.models.res_users import SignupError

_logger = logging.getLogger(__name__)

class wk_ajax_signin(http.Controller):
	""" custom login and sign up methods on controllers"""
	""" called from js using  json Rpc"""

	@http.route('/web/session/wk_check', type='json', auth="none")
	def get_session_info(self):
		values = {}
		if request.env.user:
			values["wk_login"] = True
		else:
			values["wk_login"] = False
		web_config_obj = request.env["website.config.settings"].sudo().get_default_ajax_values()
		values["show_ajax_form_always"] = web_config_obj.get("show_ajax_form_always")
		values["wk_block_ui"] = web_config_obj.get("wk_block_ui")
		return values

	@http.route('/shop/login/', type='json', auth='public', website=True)
	def wk_login(self, *args, **kwargs):
		values = request.params.copy()
		values.update({'message':'','status':True})
		if not request.session.db:
			values['message'] = "No Database Selected"
			values['status'] = False
		if not request.uid:
			request.uid = SUPERUSER_ID

		if ((not kwargs.has_key('redirect')) or (kwargs.has_key('redirect') and not kwargs['redirect'])):
			kwargs['redirect'] = "/web"
		values['redirect'] = kwargs['redirect']
		old_uid = request.uid
		uid = request.session.authenticate(request.session.db, values['login'], values['password'])
		values['uid'] = uid
		if uid is not False:
			values['message'] = "sucessfully login"
			return values

		values['message'] = "Wrong login/password"
		return values


	@http.route('/website_ajax_login/signup', type='json', auth="public", website=True)
	def wk_signup(self, *args, **kw):
		res = {}
		qcontext = request.params.copy()
		try :
			res = self.custom_validate(qcontext)
			values = dict((key, qcontext.get(key)) for key in ('login', 'name', 'password'))
			if res['error'] == "":
				token = ""
				db, login, password = request.env['res.users'].sudo().signup(values, token)
				request.env.cr.commit()	 # as authenticate will use its own cursor we need to commit the current transaction
				uid = request.session.authenticate(db, login, password)
				com = request.cr.commit()
				res['com'] = com
				res['uid'] = uid
				res["redirect"] = '/page/selectyourplan'

				# new code added for pharmacistplace
				if uid:
					uid_obj = request.env['res.users'].sudo().browse(uid)
					if uid_obj:
						uid_obj.partner_id.function = kw.get("job_title") if kw.get("job_title") else None
						uid_obj.partner_id.mobile = kw.get("phone") if kw.get("phone") else None
						if kw.get("pharmacy_name"):
							vals = {
								'name' : kw.get("pharmacy_name"),
								'email' : kw.get("login"),
								'is_company' : True,
							}
							pharmacy_partner = request.env['res.partner'].sudo().create(vals)
							uid_obj.partner_id.parent_id = pharmacy_partner.id
		except Exception, e:
			res['error'] = _(e.message)
		return res

	def custom_validate(self,qcontext):
		res = {}
		res['error'] = ""
		pattern = '^[a-zA-Z0-9._%-+]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6}$'
		values = dict((key, qcontext.get(key)) for key in ('login', 'name', 'password','phone' , 'job_title', 'pharmacy_name'))

		if not all([k for k in values.values()]):
			res['error'] = res.setdefault('error', '') + ",filled"
			return res
		if not re.match(pattern, values.get('login')):
			res['error'] = res.setdefault('error', '') + ",email"
			return res

		users = request.env['res.users'].sudo().search([('login','=',values.get('login'))])
		if len(users):
		 	res['error'] = res.setdefault('error', '')+",register"
		 	return res

		phone = qcontext.get('phone')
		if phone:
			if not phone.isdigit() or not phone.startswith('01') or len(phone) != 11:
			 	res['error'] = res.setdefault('error', '')+",phone"
			 	return res

		if values.get('password') != qcontext.get('confirm_password'):
			res['error'] = res.setdefault('error', '')+",confirm_password"
			return res
		if qcontext.get('t_n_c_checked') == False:
			res['error'] = res.setdefault('error', '')+",t_n_c"
			return res
		return res

class AuthSignupHome(AuthSignupHome):


	@http.route('/website_ajax_login/reset_password', type='json', auth='public', website=True)
	def wk_reset_password(self, *args, **kw):
		qcontext = self.get_auth_signup_qcontext()

		if not qcontext.get('reset_password_enabled'):
			raise werkzeug.exceptions.NotFound()

		if 'error' not in qcontext:
			try:
				login = qcontext.get('login')
				assert login, _("No login provided.")
				_logger.info(
					"Password reset attempt for <%s> by user <%s> from %s",
					login, request.env.user.login, request.httprequest.remote_addr)
				request.env['res.users'].sudo().reset_password(login)
				qcontext['message'] = _("An email has been sent with credentials to reset your password")
			except SignupError:
				qcontext['error'] = _("Could not reset your password")
				_logger.exception('error when resetting password')
			except Exception as e:
				qcontext['error'] = str(e)
		return qcontext


	@http.route('/web/signup', type='http', auth='public', website=True)
	def web_auth_signup(self, *args, **kw):
		qcontext = self.get_auth_signup_qcontext()
		# phone = qcontext.get("phone") if qcontext.get("phone") else False
		# if phone:
		# 	if not phone.isdigit() or not phone.startswith('01') or len(phone) != 11:
		# 		qcontext['error'] = _("Invalid Mobile number")
		# 		return request.render('auth_signup.signup', qcontext)

		response = super(AuthSignupHome, self).web_auth_signup(*args, **kw)
		qcontext = self.get_auth_signup_qcontext()
		# new code added for pharmacistplace
		uid = request.session.get('uid')
		if 'error' not in qcontext and request.httprequest.method == 'POST' and uid:
			if uid:
				uid_obj = request.env['res.users'].sudo().browse(uid)
				if uid_obj:
					uid_obj.partner_id.function = qcontext.get("job_title") if qcontext.get("job_title") else None
					uid_obj.partner_id.mobile = qcontext.get("phone") if qcontext.get("phone") else None
					if qcontext.get("pharmacy_name"):
						vals = {
							'name' : qcontext.get("pharmacy_name"),
							'email' : qcontext.get("login"),
							'is_company' : True,
						}
						pharmacy_partner = request.env['res.partner'].sudo().create(vals)
						uid_obj.partner_id.parent_id = pharmacy_partner.id
		return response

class OAuthLogin(OAuthLogin):
	def list_providers(self):
		root_url = request.httprequest.url_root
		root_url = root_url if root_url[:5] == "https" else "https" + root_url[4:]
		try:
			providers = request.env['auth.oauth.provider'].sudo().search_read([('enabled', '=', True)])
		except Exception:
			providers = []
		for provider in providers:
			return_url = root_url + 'auth_oauth/signin'
			state = self.get_state(provider)
			params = dict(
				response_type='token',
				client_id=provider['client_id'],
				redirect_uri=return_url,
				scope=provider['scope'],
				state=json.dumps(state),
			)
			provider['auth_link'] = "%s?%s" % (provider['auth_endpoint'], werkzeug.url_encode(params))
		return providers

	""" called from js before login form show and provides provider list acivated from Genral setting"""
	""" inherited the OAuthLogin for changing the redirect parameter use in  get_state method """
	@http.route('/wk_modal_login/', type='json', auth='public', website=True)
	def wk_modal_login(self,*args,**kwargs):
		url = kwargs['url']
		if werkzeug.urls.url_parse(url).path.find('/web') != 0:
			request.params['redirect'] = url
		return self.list_providers()
