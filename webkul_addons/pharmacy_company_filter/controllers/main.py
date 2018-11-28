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
from odoo.addons.theme_pharmacistplace.controllers.main import WebsiteSale
from odoo.addons.website.controllers.main import QueryURL
import re

import logging
_logger = logging.getLogger(__name__)

class WebsiteSale(WebsiteSale):

    def _get_pharma_company_search_domain(self, search, set_sellers_ids):
        domain = [("supplier", "=", True), ('id','not in',set_sellers_ids),('name','ilike',search)]
        return domain

    @http.route(['/find/manufacturer'], type='json', auth="public", methods=['POST'], website=True)
    def find_manufacturer(self, **post):
        search_pharma_company = post.get('manufacturer', False)
        set_pharma_company = post.get('set_manufacturers',False)
        set_pharma_company_ids = set_pharma_company if set_pharma_company else []
        if not search_pharma_company:
            return False
        seller_domain = self._get_pharma_company_search_domain(search_pharma_company, set_pharma_company_ids)
        seller_list_obj = request.env["res.partner"].search(seller_domain)
        if not seller_list_obj:
            return False
        pharma_company_list = dict(map(lambda item :(item.id,str(item.name)),seller_list_obj))
        return pharma_company_list

    def _get_search_domain(self, search, category, attrib_values):
        product_ids = False
        res = super(WebsiteSale,self)._get_search_domain(search, category, attrib_values)
        seller_list = request.httprequest.args.getlist('pharma_company')
        seller_list_ids = [int(v) for v in seller_list if v]

        if seller_list_ids:
            res+=[('manufacture', 'in', seller_list_ids)]
        return res

    @http.route([
        '/shop',
        '/shop/page/<int:page>',
        '/shop/category/<model("product.public.category"):category>',
        '/shop/category/<model("product.public.category"):category>/page/<int:page>'
    ], type='http', auth="public", website=True)
    def shop(self, page=0, category=None, search='', ppg=False, **post):
        attrib_list = request.httprequest.args.getlist('attrib')
        pharma_company_list = request.httprequest.args.getlist('pharma_company')

        pharma_company_ids = [int(v) for v in pharma_company_list if v]
        pharma_company_obj = request.env["res.partner"].browse(pharma_company_ids)

        keep = QueryURL('/shop', category=category and int(category), search=search, attrib=attrib_list, pharma_company=pharma_company_list, order=post.get('order'))

        res = super(WebsiteSale, self).shop(page, category, search, ppg, **post)
        res.qcontext.update({
            'set_pharma_company_filter' : pharma_company_obj if pharma_company_obj else False,
            'keep': keep,
        })
        return res

    def get_countable_filters(self):
        res = super(WebsiteSale, self).get_countable_filters()
        res.append("pharma_company")
        return res
