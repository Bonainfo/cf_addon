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
import logging
_logger = logging.getLogger(__name__)
class WebsiteSale(WebsiteSale):
    def _get_search_domain(self, search, category, attrib_values):
        res = super(WebsiteSale,self)._get_search_domain(search, category, attrib_values)
        alphabet_list = request.httprequest.args.getlist('alphabet')
        if alphabet_list:
            res+=[('name','=ilike',"%s"%(''.join(alphabet_list))+'%')]
        return res
    @http.route(
        ['/shop',
         '/shop/page/<int:page>',
         '/shop/category/<model("product.public.category"):category>',
         '/shop/category/<model("product.public.category"):category>/'
         'page/<int:page>'],
        type='http', auth="public", website=True)
    def shop(self, page=0, category=None, search='', ppg=False, **post):
        response= super(WebsiteSale, self).shop(page, category, search,ppg,**post)
        alphabet_list = request.httprequest.args.getlist('alphabet')
        response.qcontext['alphabet_list']= alphabet_list
        return response
