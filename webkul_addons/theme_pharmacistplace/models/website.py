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

from odoo import api, models, fields, _
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import time
import logging
_logger = logging.getLogger(__name__)


class Website(models.Model):

    _inherit = "website"

    @api.multi
    def get_footer_menu_groups(self):
        self.ensure_one()
        return self.env["footer.menu.group"].search([("website_published", "=", True)])