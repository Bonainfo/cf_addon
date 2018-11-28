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

class FooterMenuGroup(models.Model):
    _name = 'footer.menu.group'
    _inherit = 'website.published.mixin'
    _description = "Model to manage footer menu groups"
    _order = "sequence, website_published"

    name = fields.Char("Group Name", required=True, help="Footer menu group name.", translate=True)
    sequence = fields.Integer("Sequence")

    @api.multi
    def get_all_linked_menu(self):
        self.ensure_one()
        return self.env["footer.menu.link"].search([("footer_menu_group_id", "=", self.id), ("website_published", "=", True)])


class FooterMenuLink(models.Model):
    _name = 'footer.menu.link'
    _inherit = 'website.published.mixin'
    _description = "Model to manage footer menu groups"
    _order = "sequence, website_published"

    name = fields.Char("Menu Link Label", required=True, help="Footer menu link label.", translate=True)
    sequence = fields.Integer("Sequence")
    url = fields.Char('Url', default='')
    footer_menu_group_id = fields.Many2one("footer.menu.group", "Footer Menu Group", help="Footer manu group under which this menu link will visible. If not set then will not display on website.")
    