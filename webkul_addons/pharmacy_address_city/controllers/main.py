# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http, _
from odoo.exceptions import AccessError
from odoo.http import request
import base64

from odoo.addons.website_portal.controllers.main import website_account
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.marketplace_pharmacist_details.controllers.main import PharmacyCustomerForm

import logging
_logger = logging.getLogger(__name__)

class website_account(website_account):
    website_account.MANDATORY_BILLING_FIELDS.remove("city")
    website_account.MANDATORY_BILLING_FIELDS += ["pp_city_id"] 

    @http.route(['/my/account'], type='http', auth='user', website=True)
    def details(self, redirect=None, **post):
        res = super(website_account, self).details(redirect=redirect, **post)
        pp_cities = request.env['pp.city'].sudo().search([])
        res.qcontext.update({
            "pp_cities": pp_cities,
        })
        return res


class WebsiteSale(WebsiteSale):

    def _get_mandatory_billing_fields(self):
        res = super(WebsiteSale, self)._get_mandatory_billing_fields()
        res.remove("city")
        return res + ["pp_city_id"]

    def _get_mandatory_shipping_fields(self):
        res = super(WebsiteSale, self)._get_mandatory_shipping_fields()
        res.remove("city")
        return res + ["pp_city_id"]

    def _checkout_form_save(self, mode, checkout, all_values):
        if all_values.get("pp_city_id", False):
            checkout.update({"pp_city_id": all_values.get("pp_city_id", False)})
        return super(WebsiteSale, self)._checkout_form_save(mode, checkout, all_values)

    @http.route(['/save_address'], type='json', auth="public", methods=['POST'], website=True, csrf=False)
    def save_address(self, wk_name, wk_email, wk_phone, wk_street, wk_city, wk_country, wk_state=None, wk_zip=None):
        Partner = request.env['res.partner']
        order = request.website.sale_get_order()
        vals = {
            "customer": True,
            "team_id": request.website.salesteam_id and request.website.salesteam_id.id,
            'lang': request.lang if request.lang in request.website.mapped('language_ids.code') else None,
            'parent_id': order.partner_id.commercial_partner_id.id,
            'type': 'delivery',
            "name": str(wk_name),
            "email": str(wk_email),
            "phone": str(wk_phone),
            "street": str(wk_street),
            "pp_city_id": str(wk_city),
            "zip": str(wk_zip) if wk_zip else False,
            "country_id": int(wk_country),
            "state_id": int(wk_state) if wk_state else False,

        }
        partner_obj = Partner.sudo().create(vals)
        if partner_obj:
            order.partner_shipping_id = partner_obj.id
            return request.env.ref("website_single_page_checkout.test_address").render({'contact': partner_obj}, engine='ir.qweb')
        return False


class PharmacyCustomerForm(PharmacyCustomerForm):

    @http.route(["/create/pharmacy/account"], type='http', auth="public", website=True)
    def create_pharmacy_account(self, **post):
        name = str(post.get("name")) if post.get("name") else ""
        pharmacy_name = str(post.get("pharmacy_name")) if post.get("pharmacy_name") else ""
        email = str(post.get("email")) if post.get("email") else ""
        phone = str(post.get("phone")) if post.get("phone") else ""
        street = str(post.get("street")) if post.get("street") else ""
        pp_city_id = int(post.get("pp_city_id")) if post.get("pp_city_id") else False
        zip = post.get("zip")
        country_id = int(post.get("country_id")) if post.get("country_id") else False
        state_id = int(post.get("state_id")) if post.get("state_id") else False
        marketplace_seller_id = int(post.get("marketplace_seller_id")) if post.get(
            "marketplace_seller_id") else False
        comm_reg = post.get("comm_reg")
        tax_card = post.get("tax_card")
        customer_id = request.env.user.partner_id
        values = {
            'name': name,
            'pharmacist_name': pharmacy_name,
            'marketplace_seller_id': marketplace_seller_id,
            'pharmacist_customer_id': customer_id.id,
            'email': email,
            'phone': phone,
            'street1': street,
            'pp_city_id': pp_city_id,
            'zipcode': zip,
            'country_id': int(country_id) if country_id else None,
            'state_id': int(state_id) if state_id else None,
        }
        if comm_reg:
            values.update({
                'comm_registration_file': base64.encodestring(comm_reg.read()),
                'comm_registration_filename': comm_reg.filename,
            })
        if tax_card:
            values.update({
                'tax_card': base64.encodestring(tax_card.read()),
                'tax_card_filename': tax_card.filename,
            })
        try:
            pharmacy_account_id = request.env["pharmacist.id.details"].sudo().create(
                values)
            if pharmacy_account_id:
                order = request.website.sale_get_order()
                if order and order.marketplace_seller_id:
                    order.pharmacy_id = pharmacy_account_id.id
            pharmacy_partner = request.env.user.partner_id
            pharmacy_partner_parent_id = pharmacy_partner.parent_id if pharmacy_partner.parent_id else False
            if not pharmacy_partner_parent_id:
                vals = {
                    'name': pharmacy_name,
                    'email': email,
                    'is_company': True,
                }
                pharmacy_partner_parent_id = request.env['res.partner'].sudo().create(
                    vals)
                pharmacy_partner.parent_id = pharmacy_partner_parent_id.id

            pharmacy_partner_parent_id.phone = phone if phone else ''
            pharmacy_partner_parent_id.street = street if street else False
            pharmacy_partner_parent_id.pp_city_id = pp_city_id if pp_city_id else ''
            pharmacy_partner_parent_id.zip = zip if zip else ''
            pharmacy_partner_parent_id.country_id = int(
                country_id) if country_id else False
            pharmacy_partner_parent_id.state_id = int(
                state_id) if state_id else False

        except Exception as e:
            _logger.info(
                "---------------------------- Record Not Created -2--------------------%r -----", e)
            return request.redirect("/pharmacy/account") #need to show some error message

        return request.redirect("/shop/checkout")
