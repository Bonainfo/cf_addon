# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
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
# If not, see <https://store.webkul.com/license.html/>
#################################################################################
from odoo import http, tools, api, _, SUPERUSER_ID
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.report import report_sxw
from odoo.addons import decimal_precision as dp

import logging
_logger = logging.getLogger(__name__)


class WebsiteSale(WebsiteSale):

    @http.route(['/shop/checkout'], type='http', auth="public", website=True)
    def checkout(self, **post):
        order = request.website.sale_get_order()

        redirection = self.checkout_redirection(order)
        if redirection:
            return redirection

        if order.partner_id.id == request.website.user_id.sudo().partner_id.id:
            return request.redirect('/shop/address')
        
        for f in self._get_mandatory_billing_fields():
            if not order.partner_id[f]:
                return request.redirect('/shop/address?partner_id=%d' % order.partner_id.id)


        values = self.checkout_values(**post)
        if post.get('xhr'):
            return 'ok'
        
        if order:
            from_currency = order.company_id.currency_id
            to_currency = order.pricelist_id.currency_id
            compute_currency = lambda price: from_currency.compute(price, to_currency)
        else:
            compute_currency = lambda price: price

        # Check that this option is activated
        extra_step = request.env.ref('website_sale.extra_info_option')
        if extra_step.active:
            values.update({
                'extra_step_active': True,
                'website_sale_order': order,
                'post': post,
                'escape': lambda x: x.replace("'", r"\'")
            })
            values.update(request.env['sale.order']._get_website_data(order))
        result = self.payment(**post)
        values.update(result.qcontext)

        if values.get('errors'):
            shipping_partner_id = False
            if order:
                if order.partner_shipping_id.id:
                    shipping_partner_id = order.partner_shipping_id.id
                else:
                    shipping_partner_id = order.partner_invoice_id.id

            acquirers = request.env['payment.acquirer'].search(
                [('website_published', '=', True), ('company_id', '=', order.company_id.id)]
            )
            values['acquirers'] = []
            for acquirer in acquirers:
                acquirer_button = acquirer.with_context(submit_class='btn btn-primary', submit_txt=_('Pay Now')).sudo().render(
                    '/',
                    order.amount_total,
                    order.pricelist_id.currency_id.id,
                    values={
                        'return_url': '/shop/payment/validate',
                        'partner_id': shipping_partner_id,
                        'billing_partner_id': order.partner_invoice_id.id,
                    }
                )
                acquirer.button = acquirer_button
                values['acquirers'].append(acquirer)

            values['tokens'] = request.env['payment.token'].search([('partner_id', '=', order.partner_id.id), ('acquirer_id', 'in', acquirers.ids)])
        request.session['sale_last_order_id'] = order.id
        values.update({
            'country': order.partner_id.country_id,
            'countries': request.env["res.country"].get_website_sale_countries(),
            "states": request.env["res.country"].get_website_sale_states(),
            "compute_currency": compute_currency
        })

        if post.get('code_not_available'):
            values['code_not_available'] = post.get('code_not_available')

        return request.render("website_single_page_checkout.single_page_checkout", values)

    @http.route(['/save_address'], type='json', auth="public", methods=['POST'], website=True, csrf=False)
    def save_address(self, wk_name, wk_email, wk_phone, wk_street, wk_city, wk_country, wk_state=None, wk_zip=None):
        Partner = request.env['res.partner']
        order = request.website.sale_get_order()
        vals={
            "customer": True,
            "team_id": request.website.salesteam_id and request.website.salesteam_id.id,
            'lang': request.lang if request.lang in request.website.mapped('language_ids.code') else None,
            'parent_id': order.partner_id.commercial_partner_id.id,
            'type': 'delivery',
            "name": str(wk_name),
            "email": str(wk_email),
            "phone": str(wk_phone),
            "street": str(wk_street),
            "city": str(wk_city),
            "zip": str(wk_zip) if wk_zip else False,
            "country_id": int(wk_country),
            "state_id": int(wk_state) if wk_state else False,

        }
        partner_obj = Partner.sudo().create(vals)
        if partner_obj:
            order.partner_shipping_id = partner_obj.id
            return request.env.ref("website_single_page_checkout.test_address").render({'contact':partner_obj},engine='ir.qweb')
        return False


    @http.route(['/shop/pricelist'], type='http', auth="public", website=True)
    def pricelist(self, promo, **post):
        res = super(WebsiteSale, self).pricelist(promo, **post)
        if post.get("checkout_page"):
            pricelist = request.env['product.pricelist'].sudo().search([('code', '=', promo)], limit=1)
            if not pricelist:
                return request.redirect("/shop/checkout?code_not_available=1")
            if pricelist and not request.website.is_pricelist_available(pricelist.id):
                return request.redirect("/shop/checkout?code_not_available=1")

            request.website.sale_get_order(code=promo)
            return request.redirect("/shop/checkout")
        return res

    def change_delivery_option(self, carrier_id, **post):
        order = request.website.sale_get_order()
        if not order or not carrier_id:
            return {'success': False}
        if not request.context.get('order_id'):
            request.context = dict(request.context, order_id=order.id)
        order._check_carrier_quotation(force_carrier_id=carrier_id)
        updated_order = request.website.sale_get_order()
        price_digits = dp.get_precision('Product Price')
        values = {
            'success': True,
            'order_total': order.amount_total,
            # 'order_subtotal': order.amount_subtotal,
            'order_total_taxes': order.amount_tax,
            'order_total_delivery': order.amount_delivery,
        }
        return values

    @http.route(['/shop/checkout/delivery_option'], type='json', auth="public", website=True)
    def change_delivery(self, carrier_id=None, **post):
        return self.change_delivery_option(int(carrier_id), **post)

    @http.route(['/single/ckeck/email'], type='json', auth="public", website=True)
    def single_ckeck_email(self, email=None, **post):
        values = {"status": True, "error": ""}
        if email:
            if not tools.single_email_re.match(email):
                values["error"] = _(
                    'Invalid Email! Please enter a valid email address.')
                values["status"] = False

            elif request.env["res.users"].sudo().search([("login", "=", email)]):
                values["error"] = _(
                    "Another user is already registered using this email address.")
                values["status"] = False
        return values

    @http.route()
    def address(self, **kw):
        result = super(WebsiteSale, self).address(**kw)
        order = request.website.sale_get_order()
        if order:
            from_currency = order.company_id.currency_id
            to_currency = order.pricelist_id.currency_id

            def compute_currency(price): return from_currency.compute(
                price, to_currency)
        else:
            def compute_currency(price): return price

        partner = order.partner_id
        if not result.qcontext.get('error') and kw.get('create_user') == 'true' and partner:
            partner.signup_prepare()
            vals = {
                'email': partner.email,
                'login': partner.email,
            }
            request.env['res.users'].sudo().signup(
                values=vals, token=partner.signup_token)
            # sent password reset mail
            partner_user = partner.user_ids and partner.user_ids[0] or False
            if partner_user:
                partner_user.with_context(
                    create_user=1).action_reset_password()
        result.qcontext['compute_currency'] = compute_currency
        return result
