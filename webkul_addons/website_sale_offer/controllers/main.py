# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# License URL : https://store.webkul.com/license.html/
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################

from odoo import http, tools, _
import werkzeug

from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
import re

import logging
_logger = logging.getLogger(__name__)


class WebsiteSale(WebsiteSale):

    @http.route(['/shop/pricelist'], type='http', auth="public", website=True)
    def pricelist(self, promo, **post):
        result = super(WebsiteSale, self).pricelist(promo, **post)
        redirect = post.get('r', '/shop/payment')
        # sale_order = request.website.sale_get_order(seller_id= self._get_active_so_seller_id())
        sale_order_id = request.session.get('sale_order_id')
        sale_order = request.env['sale.order'].sudo().browse(
            sale_order_id).exists() if sale_order_id else None
        domain = [('promo_code', '=', promo)]
        sale_offer = False
        if sale_order:
            if sale_order.marketplace_seller_id:
                domain.append(("marketplace_seller_id", "=", sale_order.marketplace_seller_id.id))
            else:
                domain.append(
                    ("marketplace_seller_id", "=", False))
            sale_offer = request.env['sale.offer'].sudo().search(domain, limit=1)
            sale_order.remove_sale_offer()

        acquirers = request.env['payment.acquirer'].search(
            [('website_published', '=', True)]
        )
        if sale_offer and sale_order:
            sale_offer.apply_offer_on_order(
                sale_order=sale_order,
                payment_acquirer_id=post.get("payment_acquirer_id", False) or acquirers[0].id if acquirers else False,
            )
            return request.redirect("%s?code_applied=1" % redirect)
        return result

    @http.route(['/apply/sale_offer'], type='json', auth="public", website=True)
    def paymnet_sale_offer_json(self, promo_code, payment_acquirer_id, **post):
        if promo_code and payment_acquirer_id:
            post.update({"payment_acquirer_id": payment_acquirer_id})
            self.pricelist(str(promo_code), **post)
            # sale_order = request.website.sale_get_order(seller_id= self._get_active_so_seller_id())
            sale_order_id = request.session.get('sale_order_id')
            sale_order = request.env['sale.order'].sudo().browse(sale_order_id).exists() if sale_order_id else None
            return ({
                "global_discount": format(round(sale_order.global_discount, 2), '.2f'),
                "amount_total": format(round(sale_order.amount_total, 2), '.2f'),
            })

    @http.route(['/shop/cart'], type='http', auth="public", website=True)
    # def cart(self, access_token=None, revive='', **post):
    def cart(self, **post):
        self.pricelist("", **post)
        return super(WebsiteSale, self).cart(**post)

    @http.route(
        ['/shop',
         '/shop/page/<int:page>',
         '/shop/category/<model("product.public.category"):category>',
         '/shop/category/<model("product.public.category"):category>/'
         'page/<int:page>'],
        type='http', auth="public", website=True)
    def shop(self, page=0, category=None, search='', ppg=False, **post):
        response= super(WebsiteSale, self).shop(page, category, search,ppg,**post)
        bonus_offer_list = request.env['bogo.offer.rule'].search([('free_qty', '>', 0), ('free_qty_type', '=', 'percentage')], order='free_qty asc')
        discount_product_list = request.env['product.template'].search([('pharmacy_discount', '>', 0)], order='pharmacy_discount asc')
        current_discount_min_range = discount_product_list[0].pharmacy_discount if discount_product_list else 0
        current_discount_max_range = discount_product_list[-1].pharmacy_discount if discount_product_list else 0
        current_bonus_min_range = bonus_offer_list[0].free_qty if bonus_offer_list else 0
        current_bonus_max_range = bonus_offer_list[-1].free_qty if bonus_offer_list else 0
        if request.session.get("discount_offer_domain") and len(request.session.get("discount_offer_domain")[2]):
            current_discount_min_range = request.session.get("discount_offer_domain")[2][0]
            current_discount_max_range = request.session.get("discount_offer_domain")[2][-1]
            response.qcontext.update(
                {"filter_count": response.qcontext.get("filter_count", 0) + 1 })
        if request.session.get("bonus_offer_domain") and len(request.session.get("bonus_offer_domain")[2]):
            current_bonus_min_range = request.session.get("bonus_offer_domain")[2][0]
            current_bonus_max_range = request.session.get("bonus_offer_domain")[2][-1]
            response.qcontext.update(
                {"filter_count": response.qcontext.get("filter_count", 0) + 1})
        response.qcontext.update({
            "bonus_offer_list": bonus_offer_list,
            "discount_product_list": discount_product_list,
            "current_discount_range": [current_discount_min_range, current_discount_max_range],
            "current_bonus_range": [current_bonus_min_range, current_bonus_max_range],
        })
        _logger.info("------shop---------------%r--=======================%r----",request.session, response.qcontext )
        return response

    def _get_search_domain(self, search, category, attrib_values):
        res= super(WebsiteSale,self)._get_search_domain(search, category, attrib_values)
        ids = []
        domain = []
        if request.session.get("discount_offer_domain") and len(request.session.get("discount_offer_domain")[2]):
            less , great =request.session.get("discount_offer_domain")[2][0],request.session.get("discount_offer_domain")[2][-1]
            domain.append("&")
            domain.append(("pharmacy_discount", ">=", less))
            domain.append(("pharmacy_discount", "<=", great))
        if request.session.get("bonus_offer_domain") and len(request.session.get("bonus_offer_domain")[2]):
            less , great =request.session.get("bonus_offer_domain")[2][0],request.session.get("bonus_offer_domain")[2][-1]
            domain.append("&")
            domain.append(("max_percentage_bonus", ">=", less))
            domain.append(("max_percentage_bonus", "<=", great))
        _logger.info(
            "----------domain-----------------%r---------------------------", domain)
        return res + domain

    @http.route(
        ['/discount/bonus/filter'],
        type='json', auth="public", website=True, csrf=False)
    def discount_bonus_range(self, **post):
        _logger.info("------discount_bonus_range---------------%r-------", post)
        vals={}
        for key,value in post.items():
            if str(value) not in [False,None,'']:
                vals[key]= re.sub("\D", "",str(value))
        min_discount = int(vals.get('min_discount') or 1)
        max_discount = int(vals.get('max_discount') or 100)
        if min_discount>=0 and max_discount>0 and max_discount >= min_discount:
            request.session['discount_offer_domain'] = ('pharmacy_discount', 'in', [min_discount, max_discount])
        min_bonus = int(vals.get('min_bonus') or 1)
        max_bonus = int(vals.get('max_bonus') or 100)
        if min_bonus >= 0 and max_bonus > 0 and max_bonus >= min_bonus:
            request.session['bonus_offer_domain'] = ('bonus', 'in', [min_bonus, max_bonus])
        _logger.info("------shop---------------%r--=======================----",request.session )
    	return True
        

    @http.route(
        ['/product/discount/range'],
        type='http', auth="public", website=True,csrf=False)
    def price_discount_range(self, **post):
        _logger.info("------price_discount_range---------------%r-------", post)
    	vals={}
        for key,value in post.items():
            if str(value) not in [False,None,'']:
                vals[key]= re.sub("\D", "",str(value))
        min_discount = int(vals.get('min_discount') or 1)
        max_discount = int(vals.get('max_discount') or 100)
        if min_discount>=0 and max_discount>0 and max_discount >= min_discount:
            request.session['discount_offer_domain'] = ('pharmacy_discount', 'in', [min_discount, max_discount])
        _logger.info("------shop---------------%r--=======================----",request.session )
        
    	return request.redirect(request.httprequest.referrer or '/shop')
    
    @http.route(
        ['/product/bonus/range'],
        type='http', auth="public", website=True,csrf=False)
    def price_bonus_range(self, **post):
        _logger.info("---price_bonus_range---------------%r----------", post)
    	vals={}
        for key,value in post.items():
            if str(value) not in [False,None,'']:
                vals[key]= re.sub("\D", "",str(value))
        min_bonus = int(vals.get('min_bonus') or 1)
        max_bonus = int(vals.get('max_bonus') or 100)
        if min_bonus >= 0 and max_bonus > 0 and max_bonus >= min_bonus:
            request.session['bonus_offer_domain'] = ('bonus', 'in', [min_bonus, max_bonus])
    	return request.redirect(request.httprequest.referrer or '/shop')
    
    @http.route(
        ['/clear/offer/filter'],
        type='http', auth="public", website=True)
    def clear_offer_filter(self, **post):
    	referrer  = request.httprequest.referrer or '/shop'
        if post.get("remove_discount_filter", False):
            _logger.info("------------clear_offer_filter--------1----------------------")
            request.session['discount_offer_domain']=None
        elif post.get("remove_bonus_filter", False):
            _logger.info("------------clear_offer_filter--------2----------------------")
            request.session['bonus_offer_domain']=None
        else:
            _logger.info("------------clear_offer_filter--------3----------------------")
            request.session['discount_offer_domain']=None
            request.session['bonus_offer_domain']=None
    	return werkzeug.utils.redirect(referrer)

    @http.route(
        ['/clear/all-filter'],
        type='http', auth="public", website=True)
    def clear_all_filter(self, **post):
        self.clear_offer_filter(**post)
        return super(WebsiteSale, self).clear_all_filter(**post)