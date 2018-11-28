# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#################################################################################
import werkzeug
from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
import re
class WebsiteSale(WebsiteSale):
    @http.route(
        ['/shop',
         '/shop/page/<int:page>',
         '/shop/category/<model("product.public.category"):category>',
         '/shop/category/<model("product.public.category"):category>/'
         'page/<int:page>'],
        type='http', auth="public", website=True)
    def shop(self, page=0, category=None, search='', ppg=False, **post):
        response= super(WebsiteSale, self).shop(page, category, search,ppg,**post)
        current_price_range= request.website.get_current_price_range()
        price_range_limits= request.website.get_price_range_limits()
        response.qcontext['current_price_range'] =current_price_range
        response.qcontext['price_range_limits'] =price_range_limits
        response.qcontext['clear_range'] =request.session.get('new_domain') and len(request.session.get('new_domain')[2])
        return response

    def _get_search_domain(self, search, category, attrib_values):
        res= super(WebsiteSale,self)._get_search_domain(search, category, attrib_values)
        if request.session.get("new_domain") and len(request.session.get("new_domain")[2]):
            less , great =request.session.get("new_domain")[2][0],request.session.get("new_domain")[2][-1]
            template_ids = request.env['product.template'].search(res).filtered(lambda pt:pt.website_price>=less and pt.website_price<=great)
            res+=[('id','in',template_ids.ids)]
        return res

    @http.route(
        ['/price/range'],
        type='http', auth="public", website=True,csrf=False)
    def price_range(self, **post):
    	vals={}
    	for key,value in post.items():
    		if str(value) not in [False,None,'']:
    			vals[key]= re.sub("\D", "",str(value))
        min_price = int(vals.get('min_price') or 0)
        max_price = int(vals.get('max_price') or 100000)
        if min_price>=0 and max_price>0 and max_price>min_price:
            request.session['new_domain']=('lst_price','in',[min_price,max_price])
    	return request.redirect(request.httprequest.referrer or '/shop')
    @http.route(
        ['/clear/range'],
        type='http', auth="public", website=True)
    def clear_range(self, **post):
    	referrer  = request.httprequest.referrer or '/shop'
    	request.session['new_domain']=None
    	return werkzeug.utils.redirect(referrer)
