# -*- coding: utf-8 -*-
#################################################################################
# Author : Webkul Software Pvt. Ltd. (<https://webkul.com/>:wink:
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
# If not, see <https://store.webkul.com/license.html/>;
#################################################################################
import logging
_logger = logging.getLogger(__name__)
from odoo import api, fields, models


class AffiliateConfiguration(models.TransientModel):
    _name = 'affiliate.config.setting'
    _inherit = 'res.config.settings'

    @api.model
    def _get_program(self):
        _logger.info("=========================")
        if len(self.env['affiliate.program'].search([])) == 0:
            program = ''
        else:
            program = self.env['affiliate.program'].search([])[-1]
        return program

    @api.model
    def _get_banner(self):
        _logger.info("======banner===================")
        if len(self.env['affiliate.banner'].search([])) == 0:
            banner = ''
        else:
            banner = self.env['affiliate.banner'].search([])[-1]
        return banner

    affiliate_program_id = fields.Many2one('affiliate.program',string="Program", default=_get_program)
    enable_ppc = fields.Boolean(string= "Enable PPC", default=True )
    auto_approve_request = fields.Boolean(default=False )
    ppc_maturity = fields.Integer(string="PPC Maturity",required=True, default=1)
    ppc_maturity_period = fields.Selection([('days','Days'),('months','Months'),('weeks','Weeks')],required=True,default='days')
    cookie_expire = fields.Integer(string="Cookie expiration",required=True, default=1)
    cookie_expire_period = fields.Selection([('hours','Hours'),('days','Days'),('months','Months')],required=True,default='days')
    payment_day = fields.Integer(string="Payment day",required=True, default=7)
    minimum_amt = fields.Integer(string="Minimum Payout Balance",required=True, default=0)
    currency_id = fields.Many2one('res.currency', 'Currency', required=True,
        default=lambda self: self.env.user.company_id.currency_id.id)
    aff_product_id = fields.Many2one('product.product', 'Product',help="Product used in Invoicing")
    enable_signup = fields.Boolean(string= "Enable Sign Up", default=True  )
    enable_login = fields.Boolean(string= "Enable Log In", default=True  )
    enable_forget_pwd = fields.Boolean(string= "Enable Forget Password", default=True )
    affiliate_banner_id = fields.Many2one('affiliate.banner',string="Bannner", default=_get_banner)

    welcome_mail_template = fields.Many2one('mail.template',string="Approved Request Mail",readonly=True )
    reject_mail_template = fields.Many2one('mail.template',string="Reject Request Mail ",readonly=True)
    Invitation_mail_template = fields.Many2one('mail.template',string="Invitation Request Mail ",readonly=True)

    term_condition = fields.Html(String="Term & condition Text")
    unique_ppc_traffic = fields.Boolean(string= "Unique ppc for product", default=False,help="this field is used to enable unique traffic on product for an Affiliate for a specific ip"  )

    work_title = fields.Text(string="How Does It Work Title")
    work_text = fields.Html(String="How Does It Work Text")



    @api.multi
    def set_default_affiliates(self):
        _logger.info("==========1= set parent config setting==========")
        IrValues = self.env['ir.values']
        if self.env['res.users'].has_group('base.group_erp_manager'):
            IrValues = IrValues.sudo()
        IrValues.set_default('affiliate.config.setting', 'ppc_maturity', self.ppc_maturity)
        IrValues.set_default('affiliate.config.setting', 'ppc_maturity_period', self.ppc_maturity_period)
        IrValues.set_default('affiliate.config.setting', 'enable_ppc', self.enable_ppc)
        IrValues.set_default('affiliate.config.setting', 'auto_approve_request', self.auto_approve_request )
        IrValues.set_default('affiliate.config.setting', 'aff_product_id', self.aff_product_id.id)
        IrValues.set_default('affiliate.config.setting', 'enable_signup', self.enable_signup )
        IrValues.set_default('affiliate.config.setting', 'enable_login', self.enable_login )
        IrValues.set_default('affiliate.config.setting', 'enable_forget_pwd', self.enable_forget_pwd )
        IrValues.set_default('affiliate.config.setting', 'payment_day', self.payment_day)
        IrValues.set_default('affiliate.config.setting', 'minimum_amt', self.minimum_amt)
        IrValues.set_default('affiliate.config.setting', 'term_condition', self.term_condition)
        IrValues.set_default('affiliate.config.setting', 'cookie_expire', self.cookie_expire)
        IrValues.set_default('affiliate.config.setting', 'cookie_expire_period', self.cookie_expire_period)
        IrValues.set_default('affiliate.config.setting', 'unique_ppc_traffic', self.unique_ppc_traffic)
        IrValues.set_default('affiliate.config.setting', 'work_title', self.work_title)
        IrValues.set_default('affiliate.config.setting', 'work_text', self.work_text)

        self.set_scheduler_ppc_maturity()

    @api.model
    def get_default_how_it_works_values(self, fields=None):
        work_title = self.env['ir.values'].get_default('affiliate.config.setting', 'work_title') or ""
        work_text = self.env['ir.values'].get_default('affiliate.config.setting', 'work_text') or "<ol><li><p style='text-align: left; margin-left: 3em;'>Visitor clicks on affiliate links posted on your website/blogs.</p></li><li><p style='text-align: left; margin-left: 3em;'>A cookie is placed in their browser for tracking purposes.</p></li><li><p style='text-align: left; margin-left: 3em;'>The visitor browses our site and may decide to order. </p></li><li><p style='text-align: left; margin-left: 3em;'>If the visitor orders, the order will be registered as a sale for you and you will receive a commission for this sale.</p></li></ol>"
        return {
                'work_title':work_title,
                'work_text':work_text
                }

    def set_scheduler_ppc_maturity(self):

        ppc_maturity_schedular = self.env.ref("affiliate_management.affiliate_ppc_maturity_scheduler_call")
        ppc_maturity_schedular.write({
        'interval_number' : self.ppc_maturity,
        'interval_type' : self.ppc_maturity_period,
        })


    @api.model
    def get_default_values(self, fields=None):
        template_1 = self.env['ir.model.data'].get_object_reference('affiliate_management', 'welcome_affiliate_email')[1]
        template_2 = self.env['ir.model.data'].get_object_reference('affiliate_management', 'reject_affiliate_email')[1]
        template_3 = self.env['ir.model.data'].get_object_reference('affiliate_management', 'join_affiliate_email')[1]

        welcome_mail_template = self.env['ir.values'].get_default('affiliate.config.setting', 'welcome_mail_template') or template_1
        reject_mail_template = self.env['ir.values'].get_default('affiliate.config.setting', 'reject_mail_template') or template_2
        Invitation_mail_template = self.env['ir.values'].get_default('affiliate.config.setting', 'Invitation_mail_template') or template_3
        return {
                'welcome_mail_template':welcome_mail_template,
                'Invitation_mail_template':Invitation_mail_template,
                'reject_mail_template':reject_mail_template,
                }


    @api.model
    def get_unique_ppc_traffic(self, fields=None):
        unique_ppc_traffic = self.env['ir.values'].get_default('referral.config.setting', 'unique_ppc_traffic') or False
        return {
        'unique_ppc_traffic':unique_ppc_traffic,
        }

    @api.multi
    def open_program(self):
        if self.affiliate_program_id.id :
            return {
                'type': 'ir.actions.act_window',
                'name': 'My Affiliate Program',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'affiliate.program',
                'res_id': self.affiliate_program_id.id,
                'target': 'current',
            }
        else:
            return {
                'type': 'ir.actions.act_window',
                'name': 'My Affiliate Program',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'affiliate.program',
                'target': 'current',
            }

    @api.multi
    def open_banner(self):
        if self.affiliate_banner_id.id :
            return {
                'type': 'ir.actions.act_window',
                'name': 'My Affiliate Banner',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'affiliate.banner',
                'res_id': self.affiliate_banner_id.id,
                'target': 'current',
            }
        else:
            return {
                'type': 'ir.actions.act_window',
                'name': 'My Affiliate Bannner',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'affiliate.banner',
                'target': 'current',
            }

    # @api.model
    # def get_default_affiliates(self, fields):
    #     return {
    #         'affiliate_program_id': self.env['ir.values'].get_default('affiliate.config.setting', 'affiliate_program_id')
    #     }
