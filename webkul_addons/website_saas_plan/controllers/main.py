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

import werkzeug
import odoo
from odoo.addons.auth_signup.models.res_users import SignupError
from odoo.addons.web.controllers.main import ensure_db
from odoo import http
from odoo.http import request
from odoo import tools
from odoo.addons.web.controllers.main import binary_content
import base64
from odoo.tools.translate import _
from odoo import SUPERUSER_ID
from odoo.addons.website.models.website import slug
from odoo.addons.website_sale.controllers.main import TableCompute, QueryURL
from odoo.addons.web.controllers.main import Home
from odoo.addons.auth_signup.controllers.main import AuthSignupHome

from odoo.addons.website_mail.controllers.main import WebsiteMail
from odoo.addons.website_sale.controllers.main import WebsiteSale


from werkzeug import url_encode
import logging
_logger = logging.getLogger(__name__)


class SaasPlan(http.Controller):

    @http.route(['/saas-plan'], type='http', auth="public", website=True)
    def saas_plan(self, **post):
        SaasPortalPlanSudo = request.env["saas_portal.plan"].sudo()

        keep = QueryURL('/shop')
        saas_portal_plans = SaasPortalPlanSudo.search([('state', '=', 'confirmed')])

        values = {
            'saas_portal_plans': saas_portal_plans,
            'saas_plan_count': len(saas_portal_plans),
            'keep': keep,
        }
        # _logger.info("-----values-------%r---------", values)
        return request.render("website_saas_plan.pp_saas_plan", values)
