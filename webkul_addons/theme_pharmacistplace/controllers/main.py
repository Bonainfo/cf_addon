# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import json
import logging

from odoo import http, tools, _
from odoo.http import request
from odoo.exceptions import ValidationError
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.website_portal.controllers.main import website_account
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from urlparse import parse_qs, urlparse

_logger = logging.getLogger(__name__)


class WebsiteSale(WebsiteSale):

    @http.route(['/shop/cart'], type='http', auth="public", website=True)
    def cart(self, **post):
        res = super(WebsiteSale, self).cart(**post)

        # Check cart related customized enabled template is activated or not
        try:
            res.qcontext.update({
                'extra_info': request.env.ref('website_sale.extra_info_option').active or False,
                'continue_shopping': request.env.ref('website_sale.continue_shopping').active or False,
                'coupon_code': request.env.ref('website_sale.reduction_code').active or False,
            })
        except Exception as e:
            _logger.info("----Exception on cart page-----%r-----", str(e))

        return res

    @http.route(['/clear/cart'], type='http', auth="public", website=True)
    def clear_cart(self, **post):
        if post.get("cart_so_id"):
            request.env["sale.order.line"].sudo().search(
                [("order_id.id", "=", int(post.get("cart_so_id")))]).unlink()
        return request.redirect("/shop/cart")

    @http.route(['/shop/payment/transaction/<int:acquirer_id>'], type='json', auth="public", website=True)
    def payment_transaction(self, acquirer_id, tx_type='form', token=None, **kwargs):
        res = super(WebsiteSale, self).payment_transaction(
            acquirer_id=acquirer_id, tx_type=tx_type, token=token, **kwargs)
        if type(res) is str and '<form' in res:
            res = res.replace('<form', '<form class="hide"')
        return res

    @http.route(
        ['/clear/all-filter'],
        type='http', auth="public", website=True)
    def clear_all_filter(self, **post):
    	return request.redirect("/shop")

    def get_countable_filters(self):
        return ["category", "search", "attrib"]

    @http.route()
    def shop(self, page=0, category=None, search='', ppg=False, **post):
        response = super(WebsiteSale, self).shop(
            page, category, search, ppg, **post)
        filter_count = 0
        # query_dict = parse_qs(urlparse(request.httprequest.url).query)
        query_dict = parse_qs(request.httprequest.query_string)
        countable_filter = self.get_countable_filters()
        for key in query_dict:
            if key in countable_filter and query_dict.get(key):
                filter_count += len(query_dict.get(key))
        if not query_dict.get("category", False) and response.qcontext.get("category", False):
            filter_count += 1
        response.qcontext.update({"filter_count": filter_count})
        return response
        

class website_account(website_account):

    @http.route(['/my/account'], type='http', auth='user', website=True)
    def details(self, redirect=None, **post):
        res = super(website_account, self).details(redirect, **post)
        res.qcontext.update({"my_profile": True})
        if not len(res.qcontext.keys()) != 1:
            # res.qcontext.update({
            #     'error': {},
            #     'error_message': []
            # })
            return request.redirect('/my/account')
        return request.render("theme_pharmacistplace.theme_pharmacistplace_portal_my_account", res.qcontext)

    # @http.route('/change_password', type='http', auth='user', website=True)
    # def change_password(self, *args, **kw):
    #     values = {
    #         "change_password" : True,
    #     }
    #     return request.render(
    #         "theme_pharmacistplace.theme_pharmacistplace_change_password",
    #         values)


class AuthSignupHome(AuthSignupHome):

    @http.route('/web/reset_password', type='http', auth='public', website=True)
    def web_auth_reset_password(self, *args, **kw):
        res = super(AuthSignupHome, self).web_auth_reset_password(*args, **kw)
        if request.env.user == request.website.user_id or not res.qcontext:
            return res
        res.qcontext.update({
            "change_password": True,
        })
        return request.render(
            "theme_pharmacistplace.theme_pharmacistplace_change_password",
            res.qcontext)
