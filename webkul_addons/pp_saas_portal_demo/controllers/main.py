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
from odoo.addons.saas_portal_demo.controllers.main import WebsiteAccount
import logging
_logger = logging.getLogger(__name__)


class WebsiteAccount(WebsiteAccount):

    @http.route(['/my/instances'], type='http', auth="user", website=True)
    def portal_my_instances(self, **kw):
        res = super(WebsiteAccount, self).portal_my_instances(**kw)
        res.qcontext.update({
            "instance_active": True,
        })
        return res
