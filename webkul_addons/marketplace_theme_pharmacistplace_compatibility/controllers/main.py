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
from odoo.addons.website_portal.controllers.main import website_account
from odoo.exceptions import AccessError
from odoo.addons.website.controllers.main import QueryURL
import re

import logging
_logger = logging.getLogger(__name__)


class WebsiteSale(WebsiteSale):

    def _get_seller_search_domain(self, search, set_sellers_ids):
        domain = [('website_published','=',True),('state','=','approved'),('seller','=',True),('id','not in',set_sellers_ids),('name','ilike',search)]
        return domain

    @http.route(['/find/distributor'], type='json', auth="public", methods=['POST'], website=True)
    def find_distributor(self, **post):
        search_seller = post.get('distributor',False)
        set_sellers = post.get('set_sellers',False)
        set_sellers_ids = set_sellers if set_sellers else []
        if not search_seller:
            return False
        seller_domain = self._get_seller_search_domain(search_seller, set_sellers_ids)
        seller_list_obj = request.env["res.partner"].search(seller_domain)
        if not seller_list_obj:
            return False
        search_sellers_list = dict(map(lambda item :(item.id,str(item.name)),seller_list_obj))
        return search_sellers_list

    def _get_search_domain(self, search, category, attrib_values):
        product_ids = False
        res = super(WebsiteSale,self)._get_search_domain(search, category, attrib_values)
        seller_list = request.httprequest.args.getlist('seller')
        seller_list_ids = [int(v) for v in seller_list if v]

        if seller_list_ids:
            res+=[('marketplace_seller_id','in',seller_list_ids)]
        return res

    @http.route([
        '/shop',
        '/shop/page/<int:page>',
        '/shop/category/<model("product.public.category"):category>',
        '/shop/category/<model("product.public.category"):category>/page/<int:page>'
    ], type='http', auth="public", website=True)
    def shop(self, page=0, category=None, search='', ppg=False, **post):
        attrib_list = request.httprequest.args.getlist('attrib')
        seller_list = request.httprequest.args.getlist('seller')

        seller_list_ids = [int(v) for v in seller_list if v]
        seller_list_obj = request.env["res.partner"].browse(seller_list_ids)

        keep = QueryURL('/shop', category=category and int(category), search=search, attrib=attrib_list, seller=seller_list, order=post.get('order'))

        res = super(WebsiteSale, self).shop(page, category, search, ppg, **post)
        res.qcontext.update({
            'set_seller_filter' : seller_list_obj if seller_list_obj else False,
            'keep': keep,
        })
        return res

    def get_countable_filters(self):
        res = super(WebsiteSale, self).get_countable_filters()
        res.append("seller")
        return res

class website_account(website_account):

    @http.route()
    def account(self, **kw):
        response = super(website_account, self).account()
        pharmacy_order_count = request.env['sale.order'].search_count([
            ('marketplace_seller_id', '=', request.env.user.partner_id.id)
        ])
        response.qcontext.update({
            'pharmacy_order_count': pharmacy_order_count,
        })
        return response

    @http.route(['/my/pharmacy/orders', '/my/pharmacy/orders/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_pharmacy_orders(self, page=1, date_begin=None, date_end=None, **kw):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        SaleOrder = request.env['sale.order']

        domain = [
            ('marketplace_seller_id', '=', partner.id)
        ]
        archive_groups = self._get_archive_groups('sale.order', domain)
        if date_begin and date_end:
            domain += [('create_date', '>', date_begin),
                       ('create_date', '<=', date_end)]

        # count for pager
        order_count = SaleOrder.search_count(domain)
        # pager
        pager = request.website.pager(
            url="/my/orders",
            url_args={'date_begin': date_begin, 'date_end': date_end},
            total=order_count,
            page=page,
            step=self._items_per_page
        )
        # content according to pager and archive selected
        orders = SaleOrder.search(
            domain, limit=self._items_per_page, offset=pager['offset'])

        values.update({
            'date': date_begin,
            'pharmacy_orders': orders,
            'page_name': 'order',
            'pager': pager,
            'archive_groups': archive_groups,
            'default_url': '/my/orders',
            'pharmacy_order_active': True
        })
        return request.render("marketplace_theme_pharmacistplace_compatibility.theme_pharmacistplace_pharmacy_order", values)
