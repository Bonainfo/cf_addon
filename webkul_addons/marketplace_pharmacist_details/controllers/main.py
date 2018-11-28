from odoo import http
from odoo.http import request
import logging
_logger = logging.getLogger(__name__)

import json
import logging
import base64
from odoo import http, tools, _
from odoo.http import request
from odoo.exceptions import ValidationError
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.website_portal.controllers.main import website_account



class website_account(website_account):
    website_account.OPTIONAL_BILLING_FIELDS += [
        "comm_registration_file", "tax_card", 'state_id']


class WebsiteSale(WebsiteSale):

    @http.route(['/shop/distributor_activate'], type='http', auth="public", website=True)
    def distributor_activate(self, **post):
        # check that cart is valid
        order = request.website.sale_get_order()
        redirection = self.checkout_redirection(order)
        if redirection:
            return redirection

        # if form posted
        if 'post_values' in post:
            values = {}
            return request.redirect("/shop/checkout")

        values = {}

        # check for pharmacy_account already exist
        sale_order_id = request.website.sale_get_order()
        if sale_order_id and not sale_order_id.marketplace_seller_id:
            return request.redirect("/shop/checkout")
        if sale_order_id and sale_order_id.marketplace_seller_id:
            pharmacy_account = request.env['pharmacist.id.details'].sudo().search([
                ('pharmacist_customer_id','=', request.env.user.partner_id.id),
                ('marketplace_seller_id','=', sale_order_id.marketplace_seller_id.id)]
            )
            if pharmacy_account:
                sale_order_id.pharmacy_id = pharmacy_account.id
            values.update({
                "pharmacy_account": pharmacy_account,
                "marketplace_seller_id": sale_order_id.marketplace_seller_id,
            })
            if pharmacy_account:
                so_ids = request.env['sale.order'].sudo().search([('marketplace_seller_id','!=', False), ('pharmacy_id','=', sale_order_id.pharmacy_id.id)])
                if so_ids and len(so_ids) != 1:
                    url= "/shop/checkout?seller=" + str(sale_order_id.marketplace_seller_id.id)
                    return request.redirect(url)

        return request.render("marketplace_pharmacist_details.distributor_activate",
                              values)

class PharmacyCustomerForm(http.Controller):

    @http.route(["/pharmacy/account"], type='http', auth="public", website=True)
    def pharmacy_account(self, **post):
        vals = {}
        sale_order_id = request.session.get('sale_order_id') if request.session.get('sale_order_id') else False
        sale_order_id = request.env['sale.order'].sudo().browse(int(sale_order_id))
        if not sale_order_id:
            return request.redirect("/shop")
        if sale_order_id and not sale_order_id.marketplace_seller_id:
            return request.redirect("/shop/checkout")
        if sale_order_id and sale_order_id.marketplace_seller_id:
            pharmacy_account_exist = request.env['pharmacist.id.details'].sudo().search([
                ('pharmacist_customer_id','=', request.env.user.partner_id.id),
                ('marketplace_seller_id','=', sale_order_id.marketplace_seller_id.id)]
            )
            vals.update({
                "pharmacy_account_exist": True if pharmacy_account_exist else False,
                "marketplace_seller_id":  sale_order_id.marketplace_seller_id,
            })

            # code for the autofilling of details
            if not pharmacy_account_exist:
                pharmacy_account_for_other_seller_exist = request.env['pharmacist.id.details'].sudo().search([
                    ('pharmacist_customer_id','=', request.env.user.partner_id.id)], limit=1)
                if pharmacy_account_for_other_seller_exist:
                    vals.update({
                        'default_account_vals': pharmacy_account_for_other_seller_exist,
                    })

        vals.update({
            'countries': request.env['res.country'].sudo().get_website_sale_countries(),
            "states": request.env['res.country'].sudo().get_website_sale_states(),
        })
        return request.render("marketplace_pharmacist_details.pharmacy_account_registration_form", vals)

    @http.route(["/create/pharmacy/account"], type='http', auth="public", website=True)
    def create_pharmacy_account(self, **post):
        name = post.get("name")
        pharmacy_name = post.get("pharmacy_name")
        email = post.get("email")
        phone = post.get("phone")
        street = post.get("street")
        city = post.get("city")
        zip = post.get("zip")
        country_id = post.get("country_id")
        state_id = post.get("state_id")
        marketplace_seller_id = int(post.get("marketplace_seller_id")) if post.get("marketplace_seller_id") else False
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
            'street1':street,
            'city':city,
            'zipcode':zip,
            'country_id':int(country_id) if country_id else None,
            'state_id':int(state_id) if state_id else None,
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
            pharmacy_account_id = request.env["pharmacist.id.details"].sudo().create(values)
            if pharmacy_account_id:
                order = request.website.sale_get_order()
                if order and order.marketplace_seller_id:
                    order.pharmacy_id = pharmacy_account_id.id
            pharmacy_partner = request.env.user.partner_id
            pharmacy_partner_parent_id = pharmacy_partner.parent_id if pharmacy_partner.parent_id else False
            if not pharmacy_partner_parent_id:
                vals = {
                    'name' : pharmacy_name,
                    'email' : email,
                    'is_company' : True,
                }
                pharmacy_partner_parent_id = request.env['res.partner'].sudo().create(vals)
                pharmacy_partner.parent_id = pharmacy_partner_parent_id.id

            pharmacy_partner_parent_id.phone = phone if phone else ''
            pharmacy_partner_parent_id.street = street if street else False
            pharmacy_partner_parent_id.city = city if city else ''
            pharmacy_partner_parent_id.zip = zip if zip else ''
            pharmacy_partner_parent_id.country_id = int(country_id) if country_id else False
            pharmacy_partner_parent_id.state_id = int(state_id) if state_id else False
            pharmacy_partner.comm_registration_file = base64.encodestring(comm_reg.read())
            pharmacy_partner.comm_registration_filename = comm_reg.filename
            pharmacy_partner.tax_card = base64.encodestring(tax_card.read())
            pharmacy_partner.tax_card_filename = tax_card.filename

        except Exception as e:
            _logger.info("---------------------------- Record Not Created ---------------------%r -----", e)
        return request.redirect("/shop/checkout")

    @http.route(["/pharmacy/account/search"], type='json', auth="public", website=True)
    def search_pharmacy_account(self, pharmacy_account_id):
        pharmacy_account_id = request.env['pharmacist.id.details'].sudo().search([
            ('pharmacist_customer_id','=', request.env.user.partner_id.id),
            ('pharmacist_id','=',pharmacy_account_id),
        ], limit=1)
        if pharmacy_account_id:
            return True
        return
