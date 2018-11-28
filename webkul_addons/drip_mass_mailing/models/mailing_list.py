# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
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

import logging

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError
from datetime import datetime

_logger = logging.getLogger(__name__)

class DripMassMailingTemplate(models.Model):
    """Model of a drip template """

    _name = 'drip.mass_mailing.template'
    

    name = fields.Char(string="Name", required=True)
    after_days = fields.Integer(string="After(Days)", help="Number of days after mail will send using this template",required=True)
    template_id = fields.Many2one('mail.template', string="Drip Template", domain=[('model','=','mail.mass_mailing.contact')], required=True, copy=False)
    mailing_list_id = fields.Many2one('mail.mass_mailing.list', string="Mailing list", required=True, copy=False)
    drip_mailing_history_ids = fields.One2many('drip.mailing.history','drip_template_id', string="Drip Followup"
    )

    @api.one
    @api.constrains('after_days')
    def _check_days(self):
        if self.after_days < 0:
            raise ValidationError(_('Please re-check the After(Days), It always greater than or equals to zero.'))

    

class MassMailingList(models.Model):
    """Model of a contact list. """

    _inherit = 'mail.mass_mailing.list'

    enable_drip_mailing = fields.Boolean(string="Enable drip mass mailing feature for this mailing list", copy=False, help="If enabled, then automatic mail will get send automatically using drip mailing templates.")
    state = fields.Selection([('draft','Draft'),('inprogress','Drip Mailing : Inprogress'),('drip_stop','Drip Mailing : Stop'),('done','Stoped')], string='Status', default='draft', copy=False)
    drip_mailing_template_ids = fields.One2many('drip.mass_mailing.template', 'mailing_list_id', string="Drip Templates", copy=False)
    start_date = fields.Date(string="Start Date", default=fields.Date.context_today, help="Date on or after which cron automatic send drip mails")
    end_date = fields.Date(string="End Date",  help="Date on which cron automatic stop drip mails")
    outgoing_mail_server = fields.Many2one(
        "ir.mail_server", string="Outgoing Mail Server", help="Select an outgoing mail server that you want to use for mailing.")

    
    @api.model
    def send_drip_mailing(self):
        mailing_lists = self.search([('enable_drip_mailing','=',True),'|',('start_date','<=',fields.Date.today()),('state','=','inprogress')])
        _logger.info('========%r',mailing_lists)
        if mailing_lists:
            for mailing_list in mailing_lists:
                if mailing_list.state == 'draft':
                    mailing_list.state = 'inprogress'
                contract_ids = self.env['mail.mass_mailing.contact'].search([('list_id','in',[mailing_list.id]),('opt_out','=',False)])
                for drip_template in mailing_list.drip_mailing_template_ids:
                    sent_contacts = []
                    if drip_template.drip_mailing_history_ids:
                        sent_contacts = [drip_mailing_history_id.contact_id for drip_mailing_history_id in drip_template.drip_mailing_history_ids]
                    for contract_id in contract_ids:
                        if contract_id not in sent_contacts:
                            days = 0
                            if contract_id.drip_mailing_history_ids:
                                date_format = '%Y-%m-%d %H:%M:%S'
                                last_date = contract_id.drip_mailing_history_ids[0].sent_date
                                d1 = datetime.strptime(last_date, date_format).date()
                                d2 = datetime.now().date()
                                days = (d2-d1).days
                            _logger.info('===%r===========%r',days,drip_template.after_days)
                            if days >= drip_template.after_days:
                                drip_template.template_id.with_context({'default_mail_server_id':self.outgoing_mail_server.id if self.outgoing_mail_server else False}).send_mail(contract_id.id, True)
                                self.env['drip.mailing.history'].create({'contact_id':contract_id.id,'mailing_list_id':mailing_list.id,'drip_template_id':drip_template.id,'sent_date':fields.Datetime.now()})
                if mailing_list.end_date and mailing_list.end_date <= fields.Date.today():
                    mailing_list.state = 'done'



class MassMailingContact(models.Model):
    """Model of a contact. This model is different from the partner model
    because it holds only some basic information: name, email. The purpose is to
    be able to deal with large contact list to email without bloating the partner
    base."""
    _inherit = 'mail.mass_mailing.contact'


    drip_mailing_history_ids = fields.One2many('drip.mailing.history','contact_id', string="Drip Followup", copy=False)


class DripMailingHistory(models.Model):

    _name = 'drip.mailing.history'
    _order = 'sent_date desc'
    _rec_name = 'contact_id'

    contact_id = fields.Many2one('mail.mass_mailing.contact', string="Contact", copy=False, required=True)
    mailing_list_id = fields.Many2one('mail.mass_mailing.list', string="Mailing List", copy=False, required=True)
    drip_template_id = fields.Many2one('drip.mass_mailing.template', string="Drip Template", copy=False, required=True)
    sent_date = fields.Datetime(string="Sent Date", copy=False, required=True)
