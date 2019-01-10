# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
import logging
import ast

_logger = logging.getLogger(__name__)


class res_partner(models.Model):
    _inherit = "res.partner"

    balance = fields.Float(digits=(16, 2), compute='_compute_debit_credit_balance', string='Balance')

    @api.multi
    @api.depends('credit', 'debit', 'balance')
    def _compute_debit_credit_balance(self):
        for partner in self:
            partner.balance = partner.credit - partner.debit
