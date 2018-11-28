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

from openerp import models, fields, api, _
from openerp.exceptions import except_orm, Warning, RedirectWarning
import datetime
from datetime import datetime, timedelta
from datetime import date
from dateutil.relativedelta import relativedelta
from lxml import etree
from openerp.osv.orm import setup_modifiers
import openerp.addons.decimal_precision as dp
import decimal

import logging
_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.multi
    def publish_all_product(self):
        self.write({"website_published": True})

    @api.multi
    def unpublish_all_product(self):
        self.write({"website_published": False})


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.multi
    def publish_all_product(self):
        self.write({"website_published": True})

    @api.multi
    def unpublish_all_product(self):
        self.write({"website_published": False})
