# -*- coding: utf-8 -*-
#  Copyright (C) 2004-2018 CodeFish (<http://www.codefish.com.eg>).
#  Copyright 2018 CodeFish
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import datetime
from datetime import timedelta
import logging
import pytz
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools.translate import _


class DoctorPartner(models.Model):
    # _name = 'res.partner'
    _inherit = 'res.partner'
    _description = 'Doctor Partner'

    @api.model
    def _get_default_country(self):
        country = self.env['res.country'].search([('code', '=', 'EG')], limit=1)
        return country

    is_doctor = fields.Boolean(string='Doctor', help='Check if the party is a patient')
    country_id = fields.Many2one(default=_get_default_country)


class MedicalDoctor(models.Model):
    _name = 'medical.doctor'
    _inherits = {
        'res.partner': 'partner_id',
    }

    partner_id = fields.Many2one('res.partner', string='Related Partner', required=True, ondelete='cascade',
                                 help='Partner-related data of the doctor')
    doctor_user_id = fields.Many2one('res.users', string='Existing Partner')

    _sql_constraints = [
        ('code_doctor_userid_uniq', 'unique (doctor_user_id)',
         "Selected 'Responsible' user is already assigned to another Doctor !")
    ]

    @api.model
    def create(self, vals):
        vals['is_doctor'] = True
        health_doctor = super(MedicalDoctor, self).create(vals)
        return health_doctor

    @api.multi
    def onchange_state(self, state_id):
        if state_id:
            state = self.env['res.country.state'].browse(state_id)
            return {'value': {'country_id': state.country_id.id}}
        return {}


