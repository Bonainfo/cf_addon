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
from odoo.addons.website_portal_contract.controllers.main import WebsiteContract
import logging
_logger = logging.getLogger(__name__)


class WebsiteContract(WebsiteContract):

    @http.route(['/my/contracts'], type='http', auth="user", website=True)
    def portal_my_contracts(self, **kw):
        res = super(WebsiteContract, self).portal_my_contracts(**kw)
        res.qcontext.update({
            "contract_active": True,
        })
        return res
