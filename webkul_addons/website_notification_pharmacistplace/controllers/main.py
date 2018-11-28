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
from odoo.exceptions import AccessError


_logger = logging.getLogger(__name__)


class WebsiteNotification(http.Controller):

    @http.route(['/website/notifications'], type='http', auth="public", website=True, csrf=False)
    def get_website_notification(self, **kwargs):
        # all_message = request.env.user.partner_id.get_notifications()
        all_message = request.env.user.partner_id.with_context(unread=True).get_notifications()
        all_message.filtered(lambda msg: msg.is_notification_read == False).write({"is_notification_read" : True})
        return request.render("website_notification_pharmacistplace.website_notification_popover", {'all_message':all_message,})


class website_account(website_account):

    @http.route()
    def account(self, **kw):
        response = super(website_account, self).account()
        notifications = request.env.user.partner_id.get_notifications()
        response.qcontext.update({
            'notifications': notifications,
        })
        return response

    @http.route(['/my/notifications'], type='http', auth="user", website=True)
    def portal_my_notifications(self, **kw):
        values = self._prepare_portal_layout_values()
        notifications = request.env.user.partner_id.get_notifications()
        notifications.filtered(lambda msg: msg.is_notification_read == False).write({"is_notification_read" : True})
        values.update({
            "notifications": notifications,
            "notification_active": True,
        })
        return request.render("website_notification_pharmacistplace.portal_my_notifications", values)