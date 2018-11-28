# -*- coding: utf-8 -*-
##########################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2016-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# License URL :<https://store.webkul.com/license.html/>
##########################################################################


import logging
from odoo import http, tools, _
from odoo.http import request
from odoo.addons.website_helpdesk_system.controller.main import WebsiteAccount, WebsiteHelpdesk
# from odoo.addons.website_helpdesk_system.controller.main import WebsiteHelpdesk

_logger = logging.getLogger(__name__)


class WebsiteAccount(WebsiteAccount):

    @http.route(['/my/helpdesk', '/my/helpdesk/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_helpdesk(self, page=1, date_begin=None, date_end=None, category=None, sortby=None, **kw):
        result = super(WebsiteAccount, self).portal_my_helpdesk(page, date_begin, date_end, category, sortby, **kw)
        result.qcontext.update({
            "helpdesk_active": True
        })
        return result
    
    @http.route(['/my/helpdesk/<int:helpdesk_id>'], type='http', auth="user", website=True)
    def portal_my_ticket(self, helpdesk_id=None, **kw):
        result = super(WebsiteAccount, self).portal_my_ticket(helpdesk_id, **kw)
        result.qcontext.update({
            "helpdesk_active": True
        })
        return result
    

class WebsiteHelpdesk(WebsiteHelpdesk):

    @http.route('/helpdesk', type='http', auth="public", website=True)
    def helpdesk(self, page=0, category=None, topic=None, search='', ppg=False, **post):
        result = super(WebsiteHelpdesk, self).helpdesk(page, category, topic, search, ppg, **post)
        result.qcontext.update({
            "helpdesk_active": True
        })
        return result

    @http.route('/helpdesk/validate', type='http', auth="public", website=True)
    def helpdesk_validate(self, **post):
        result = super(WebsiteHelpdesk, self).helpdesk_validate(**post)
        result.qcontext.update({
            "helpdesk_active": True
        })
        return result
