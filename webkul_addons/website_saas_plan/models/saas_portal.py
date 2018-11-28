# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime, timedelta
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
import logging
_logger = logging.getLogger(__name__)


class SaasPortalPlan(models.Model):
    _inherit = 'saas_portal.plan'

    @api.multi
    def get_product_tmpl(self):
        _logger.info("--------self------%r-----------------",self )
        self.ensure_one()
        if self.product_tmpl_id:
            return self.product_tmpl_id
        else:
            return self.env["product.product"]