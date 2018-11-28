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
from odoo.addons.website_portal.controllers.main import website_account
from odoo.addons.marketplace_pharmacist_details.controllers.main import PharmacyCustomerForm
from odoo.exceptions import AccessError
from odoo.addons.website.controllers.main import QueryURL

import logging
_logger = logging.getLogger(__name__)


class website_account(website_account):

    website_account.MANDATORY_BILLING_FIELDS = website_account.MANDATORY_BILLING_FIELDS + ["function", "mobile"]

    @http.route()
    def account(self, **kw):
        response = super(website_account, self).account()
        distributor_list_count = request.env['pharmacist.id.details'].search_count([
            ('pharmacist_customer_id', '=', request.env.user.partner_id.id)
        ])
        response.qcontext.update({
            'distributor_list_count': distributor_list_count,
        })
        return response

    @http.route(['/my/orders', '/my/orders/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_orders(self, page=1, date_begin=None, date_end=None, **kw):
        res = super(website_account, self).portal_my_orders(page, date_begin, date_end, **kw)
        values = res.qcontext
        partner = request.env.user.partner_id
        SaleOrder = request.env['sale.order']
        domain = [
            ('message_partner_ids', 'child_of', [partner.commercial_partner_id.id]),
        ]
        archive_groups = self._get_archive_groups('sale.order', domain)
        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]
        order_count = SaleOrder.search_count(domain)
        pager = request.website.pager(
            url="/my/orders",
            url_args={'date_begin': date_begin, 'date_end': date_end},
            total=order_count,
            page=page,
            step=self._items_per_page
        )
        orders = SaleOrder.search(domain, limit=self._items_per_page, offset=pager['offset'])
        values.update({
            'date': date_begin,
            'orders': orders,
            'pager': pager,
            'archive_groups': archive_groups,
        })
        res.qcontext.update(values)
        return res

    @http.route(['/my/distributor/list', '/my/distributor/list/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_distributor_list(self, page=1, date_begin=None, date_end=None, **kw):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id

        DistributorList = request.env['pharmacist.id.details']

        domain = [
                ('pharmacist_customer_id', '=', request.env.user.partner_id.id)
        ]
        archive_groups = self._get_archive_groups('pharmacist.id.details', domain)
        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        # count for pager
        distributor_count = DistributorList.search_count(domain)
        # pager
        pager = request.website.pager(
            url="/my/distributor/list",
            url_args={'date_begin': date_begin, 'date_end': date_end},
            total=distributor_count,
            page=page,
            step=self._items_per_page
        )
        # content according to pager and archive selected
        distributors = DistributorList.search(domain, limit=self._items_per_page, offset=pager['offset'])

        all_dist_list = request.env['res.partner'].sudo().search([('seller','!=', False),('state','=','approved')]) or []
        remain_dist_list = DistributorList.search([('pharmacist_customer_id','=',partner.id)]) or []
        if remain_dist_list:
            remain_dist_list = remain_dist_list.mapped(lambda d: d.marketplace_seller_id)
            remain_dist_list = [d.id for d in all_dist_list if d not in remain_dist_list]

        values.update({
            'date': date_begin,
            'distributor_list': distributors,
            'page_name': 'distributors',
            'pager': pager,
            'archive_groups': archive_groups,
            'phar_distributor_list': request.env['res.partner'].sudo().browse(remain_dist_list) if remain_dist_list else all_dist_list,
            'distributor_list_active': True,
        })
        return request.render("mp_seller_wise_checkout_theme_compatibility.theme_pharmacistplace_distributor_list", values)

class PharmacyCustomerForm(PharmacyCustomerForm):

    @http.route(["/create/pharmacy/account"], type='http', auth="public", website=True)
    def create_pharmacy_account(self, **post):
        res = super(PharmacyCustomerForm, self).create_pharmacy_account(**post)
        if post.get("redirect_distruibutor_list"):
            return request.redirect("/my/distributor/list")
        return res
