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

from odoo import http
from odoo.http import request
from odoo.addons.rma.controllers.main import website_account
import logging
_logger = logging.getLogger(__name__)


class WebsiteAccount(website_account):

    @http.route(['/my/rma/<int:rma>'], type='http', auth="user", website=True)
    def rma_followup(self, rma=None):
        res = super(WebsiteAccount, self).rma_followup(rma=rma)
        res.qcontext.update({
            "rma_active": True,
        })
        return res
    
    @http.route(['/my/rma', '/my/rma/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_rma(self, page=1, date_begin=None, date_end=None, **kw):
        res = super(WebsiteAccount, self).portal_my_rma(
            page=page, date_begin=date_begin, date_end=date_end, **kw)
        res.qcontext.update({
            "rma_active": True,
        })
        return res
