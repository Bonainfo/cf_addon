from odoo import http
from odoo.http import request
import logging
_logger = logging.getLogger(__name__)

from odoo import http, tools, _
from odoo.exceptions import ValidationError
from odoo.addons.website_address_book.controllers.main import website_account


class website_account(website_account):

    @http.route()
    def account(self, **kw):
        response = super(website_account, self).account()
        partner = request.env.user.partner_id
        shippings = partner.search([
            ("id", "child_of", partner.commercial_partner_id.ids),
            '|', ("type", "=", "delivery"), ("id", "=",
                                             partner.commercial_partner_id.id)
        ], order='id desc')
        billings = partner.search([
            ("id", "child_of", partner.commercial_partner_id.ids),
            '|', ("type", "=", "invoice"), ("id", "=",
                                            partner.commercial_partner_id.id)
        ], order='id desc')
        response.qcontext.update({
            'shippings': shippings,
            'billings': billings,
        })
        return response

    @http.route(['/my/addressbook'], type='http', auth="user", website=True)
    def portal_my_addressbook(self, **kw):
        res = super(website_account, self).portal_my_addressbook(**kw)
        res.qcontext.update({"my_address_active": True})
        return res

    @http.route(['/my/address'], type='http', methods=['GET', 'POST'], auth="public", website=True)
    def my_address(self, **kw):
        res = super(website_account, self).my_address(**kw)
        res.qcontext.update({"my_address_active": True})
        return res
