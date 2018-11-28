# -*- coding: utf-8 -*-
##########################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2016-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# License URL :<https://store.webkul.com/license.html/>
##########################################################################

import re
import base64
import uuid
from werkzeug import urls
import logging
import email

from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.addons.website.models.website import slug
from odoo.exceptions import AccessError
_logger = logging.getLogger(__name__)


class HelpdeskTicket(models.Model):
    _name = "helpdesk.ticket"
    _description = "Helpdesk Tickets"
    _inherit = ['mail.thread']
    _order = "priority desc, create_date desc"
    _mail_post_access = 'read'

    @api.model
    def _get_default_stage_id(self):
        return self.env['helpdesk.stage'].search([], order='sequence', limit=1)

    name = fields.Char(
        string='Number')
    subject = fields.Char(
        string='Subject', track_visibility='always', required=True)
    description = fields.Text('Private Note')
    partner_id = fields.Many2one(
        'res.partner', string='Customer', track_visibility='onchange',
        index=True)
    contact_name = fields.Char('Contact Name')
    email = fields.Char(
        'Email', help="Email address of the contact", index=True)
    user_id = fields.Many2one('res.users', string='Assigned to',
                              track_visibility='onchange', index=True,
                              default=False)
    team_id = fields.Many2one('wk.team', string='Support Team',
                              track_visibility='onchange',
                              index=True, help='When sending mails, the \
                              default email address is taken from the support \
                              team.')
    date_deadline = fields.Datetime(
        string='Deadline', track_visibility='onchange')
    date_closed = fields.Datetime("Closed", readonly=True, index=True)

    stage_id = fields.Many2one('helpdesk.stage', string='Stage', index=True,
                               track_visibility='onchange',
                               domain="[]",
                               copy=False,
                               group_expand='_read_group_stage_ids',
                               default=_get_default_stage_id)
    priority = fields.Selection([('0', 'Low'), ('1', 'Normal'), ('2', 'High'),
                                 ('3', 'Urgent')], 'Priority', index=True,
                                default='1', track_visibility='onchange')
    date_last_stage_update = fields.Datetime(
        "Last Stage Update", index=True, default=fields.Datetime.now)
    kanban_state = fields.Selection([('normal', 'Normal'),
                                     ('blocked', 'Blocked'),
                                     ('done', 'Ready for next stage')],
                                    string='Kanban State',
                                    track_visibility='onchange',
                                    required=True, default='normal',
                                    help="""A Ticket's kanban state indicates \
                                    special situations affecting it:\n
                                           * Normal is the default situation\n
                                           * Blocked indicates something is \
                                           preventing the progress of this \
                                           ticket\n
                                           * Ready for next stage indicates \
                                           the ticket is ready to go to next \
                                           stage""")

    color = fields.Integer('Color Index')
    active = fields.Boolean(default=True)
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.user.company_id)
    category_id = fields.Many2one("helpdesk.category", string="Category")
    attachment_ids = fields.One2many('ir.attachment', 'res_id', domain=[(
        'res_model', '=', 'helpdesk.ticket')], string='Attachments')
    topic_id = fields.Many2one('helpdesk.topic', string="Topic",
                               domain="[('category_id','=',category_id)]",
                               )
    reviews = fields.One2many('helpdesk.review', 'ticket_id', 'Reviews')
    resolve = fields.Boolean(string="Resolved")
    cancel = fields.Boolean(string="Cancelled")

    @api.multi
    def get_access_action(self):
        """ Instead of the classic form view, redirect to website for portal users
        that can read the project. """
        self.ensure_one()
        user, record = self.env.user, self
        if user.share:
            try:
                record.check_access_rule('read')
            except AccessError:
                pass
            else:
                return {
                    'type': 'ir.actions.act_url',
                    'url': '/my/helpdesk/%s' % self.id,
                    'target': 'self',
                    'res_id': self.id,
                }
        return super(HelpdeskTicket, self).get_access_action()

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        """ This function sets partner email address based on partner
        """
        self.email = self.partner_id.email
        self.contact_name = self.partner_id.name

    @api.multi
    def copy(self, default=None):
        if default is None:
            default = {}
        default.update(name=_('%s (copy)') % (self.name))
        return super(HelpdeskTicket, self).copy(default=default)

    @api.multi
    def message_get_suggested_recipients(self):
        recipients = super(
            HelpdeskTicket, self).message_get_suggested_recipients()
        try:
            for tic in self:
                if tic.partner_id:
                    tic._message_add_suggested_recipient(
                        recipients, partner=tic.partner_id,
                        reason=_('Customer'))
                elif tic.email:
                    tic._message_add_suggested_recipient(
                        recipients, email=tic.email,
                        reason=_('Customer Email'))
        except AccessError:  
            # no read access rights -> just ignore suggested recipients
            # because this imply modifying followers
            pass
        return recipients

    @api.onchange('category_id')
    def onchange_category_id(self):
        if self.category_id and self.category_id.default_team_id:
            self.team_id = self.category_id.default_team_id
            self.user_id = self.category_id.manager_id

    @api.onchange('team_id')
    def onchange_team_id(self):
        if self.team_id and not self.user_id:
            self.user_id = self.team_id.manager_id

    def get_url(self):
        base_url = '/' if self.env.context.get('relative_url') else \
                   self.env['ir.config_parameter'].sudo(
        ).get_param('web.base.url')
        return urls.url_join(base_url, "my/helpdesk/%s" % (self.id))

    @api.model
    def message_new(self, msg, custom_values=None):
        """ Overrides mail_thread message_new that is called by the mailgateway
            through message_process.
            This override updates the document according to the email.
        """
        # remove default author when going through the mail gateway. Indeed we
        # do not want to explicitly set user_id to False; however we do not
        # want the gateway user to be responsible if no other responsible is
        # found.
        desc = False
        contact_name, email = re.match(
            r"(.*) *<(.*)>", msg.get('from')).group(1, 2)
        body = tools.html2plaintext(msg.get('body'))
        bre = re.match(r"(.*)^-- *$", body, re.MULTILINE |
                       re.DOTALL | re.UNICODE)
        if bre:
            desc = bre.group(1)
        defaults = {
            'name':  msg.get('subject') or _("No Subject"),
            'email_from': email_from if email_from else self.email,
            'contact_name': contact_name,
            'description':  desc or body,
        }

        create_context = dict(self.env.context or {})

        if custom_values:
            defaults.update(custom_values)

        return super(HelpdeskTicket, self.with_context(
            create_context)).message_new(msg, custom_values=defaults)

    def _onchange_stage_id_internal(self, stage_id):
        if not stage_id:
            return {'value': {}}
        stage = self.env['helpdesk.stage'].browse(stage_id)
        if stage.fold:
            return {'value': {'date_closed': fields.datetime.now()}}
        return {'value': {'date_closed': False}}

    @api.model
    def create(self, vals):
        if 'company_id' in vals:
            vals['name'] = self.env['ir.sequence'].with_context(
                force_company=vals['company_id']).next_by_code(
                    'helpdesk.ticket') or _('New')
        else:
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'helpdesk.ticket') or _('New')
        partner_id = vals.get('partner_id')
        email = vals.get('email')
        if not partner_id:
            partner = self.env['res.partner'].sudo().search(
                [('email', '=ilike', email)], limit=1)
            partner_id = partner.id
            if partner_id:
                vals.update({
                    'partner_id': partner_id,
                })
                del vals['contact_name']
        context = dict(self.env.context)
        context.update({
            'mail_create_nosubscribe': True,
        })
        if 'stage_id' in vals:
            vals.update(self._onchange_stage_id_internal(
                vals.get('stage_id'))['value'])
        res = super(HelpdeskTicket, self.with_context(context)).create(vals)
        template = self.env['ir.model.data'].sudo().xmlid_to_object(
            'website_helpdesk_system.email_template_ticket_create_admin')
        if template:
            template.send_mail(res.id, True)
        template = self.env['ir.model.data'].sudo().xmlid_to_object(
            'website_helpdesk_system.email_template_ticket_create_customer')
        if template:
            template.send_mail(res.id, True)
        return res

    @api.model
    def create_helpdesk_ticket(self, vals):
        if vals.get('partner_id') == '5':
            vals.pop('partner_id')
        vals['contact_name'] = vals.get('name')
        attachment = vals.get('attachment')
        vals.pop('submitted')
        vals.pop('callback')
        vals.pop('phone')
        vals.pop('attachment')
        try:
            ticket = self.sudo().create(vals)
            if not ticket.team_id:
                ticket.sudo().onchange_category_id()
            else:
                ticket.sudo().onchange_team_id()
            name = attachment.filename
            file = attachment
            if file:
                base64Data = base64.encodestring(file.read())
                zipAttachment = self.env['ir.attachment'].sudo().create({
                    'datas': base64Data,
                    'type': 'binary',
                    'res_model': 'helpdesk.ticket',
                    'res_id': ticket.id,
                    'datas_fname': name,
                    'name': name})
            return {
                'title': 'Ticket Created',
                'message': 'Ticket has been created successfully. \
                Your Ticket Number is %s' % (ticket.name), 'ticket': ticket}
        except Exception as e:
            _logger.info('=======%r', e)
            return {'title': 'Error', 'message': 'Sorry. Ticket has not been \
            created'}

    @api.multi
    def write(self, vals):
        if 'stage_id' in vals:
            vals['date_last_stage_update'] = fields.Datetime.now()
            vals.update(self._onchange_stage_id_internal(
                vals.get('stage_id'))['value'])
            if 'kanban_state' not in vals:
                vals['kanban_state'] = 'normal'
        return super(HelpdeskTicket, self).write(vals)

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):

        search_domain = []

        # perform search
        stage_ids = stages._search(
            search_domain, order=order, access_rights_uid=SUPERUSER_ID)
        return stages.browse(stage_ids)

    @api.multi
    def takeit(self):
        self.ensure_one()
        vals = {'user_id': self.env.uid}
        return super(HelpdeskTicket, self).write(vals)


class WkTeam(models.Model):

    _inherit = 'wk.team'

    ticket_ids = fields.One2many(
        "helpdesk.ticket", 'team_id', string="Tickets")
    ticket_count = fields.Integer(string="Tickets", compute="get_count")

    @api.multi
    def get_count(self):
        res = super(WkTeam, self).get_count()
        for record in self:
            record.ticket_count = len(record.ticket_ids)

    @api.multi
    def helpdesk_ticket_action(self):
        tickets = self.mapped('ticket_ids')
        result = {
            "type": "ir.actions.act_window",
            "res_model": "helpdesk.ticket",
            "views": [[False, "tree"], [False, "form"]],
            "domain": [["id", "in", tickets.ids]],
            "context": {"create": False},
            "name": "Tickets",
        }
        if len(tickets) == 1:
            result['views'] = [(False, "form")]
            result['res_id'] = tickets.id
        return result


class HelpdeskReview(models.Model):

    _name = "helpdesk.review"
    _description = "Helpdesk Review"
    _inherit = ['website.published.mixin', 'mail.thread']
    _order = "website_published desc, create_date desc"
    _mail_post_access = 'read'
    _mail_post_token_field = 'token'

    def _compute_review_url(self):
        """ Computes a public URL for the review """
        base_url = '/' if self.env.context.get('relative_url') else \
                   self.env['ir.config_parameter'].sudo(
        ).get_param('web.base.url')
        for record in self:
            record.public_url = urls.url_join(
                base_url, "review/start/%s" % (slug(record)))

    @api.multi
    def _get_rating(self):
        """ """
        for obj in self:
            obj.rating2 = obj.rating

    @api.model
    def _get_mail(self):
        res_obj = self.env['res.users'].browse(self._uid)
        email = res_obj.email
        return email

    ticket_id = fields.Many2one(
        'helpdesk.ticket', string='Ticket', required=True, readonly=True,
        ondelete='restrict')
    state = fields.Selection([
        ('new', 'Not started yet'),
        ('done', 'Completed')], string='Status', default='new', readonly=True)
    token = fields.Char('Identification token', default=lambda self: str(
        uuid.uuid4()), readonly=True, required=True, copy=False)
    public_url = fields.Char(
        compute="_compute_review_url", string="Public url")

    # Optional Identification data
    partner_id = fields.Many2one(
        'res.partner', string='Partner', readonly=True)
    # email = fields.Char('E-mail', readonly=True)
    comment = fields.Text(string="Comment")

    website_message_ids = fields.One2many(
        'mail.message', 'res_id',
        domain=lambda self: [
            '&', ('model', '=', self._name), ('message_type', '=', 'comment')],
        string='Website Seller Review Comments',
    )
    rating = fields.Integer(string='Rating', default=1, copy=False)
    rating2 = fields.Integer(compute="_get_rating",
                             string="Rating", copy=False)
    email = fields.Char(string='Email', default=_get_mail, copy=False)
