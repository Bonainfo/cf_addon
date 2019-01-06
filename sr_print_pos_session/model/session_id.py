# -*- coding: utf-8 -*-
#  Copyright (C) 2004-2018 CodeFish (<http://www.codefish.com.eg>).
#  Copyright 2018 CodeFish
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api, _


class PosOrderLine(models.Model):
    _inherit = 'pos.order.line'

    session_id = fields.Many2one('pos.session', string="Session", related='order_id.session_id')


class PosOrder(models.Model):
    _inherit = 'pos.order'

    product_ids = fields.One2many('pos.order.line', 'product_id', 'Product')


class PosSession(models.Model):
    _inherit = 'pos.session'

    product_ids = fields.One2many('pos.order.line', 'product_id', 'Product')
