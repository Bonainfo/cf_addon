# coding: utf-8
import logging
from odoo import api, fields, models, _
from odoo.addons.payment.models.payment_acquirer import ValidationError
_logger = logging.getLogger(__name__)
import hashlib
import urlparse

class AcquirerPaypal(models.Model):
    _inherit = 'payment.acquirer'


    provider = fields.Selection(selection_add=[('payfort', 'Payfort')])
    access_code = fields.Char(string='Access Code', required_if_provider='payfort')
    merchant_identifier = fields.Char(string='Merchant Identifier', required_if_provider='payfort')
    request_phrase = fields.Char('Request Phrase', groups='base.group_user',help='Request Phrase of Payfort')

    def _payfort_generate_signature(self,values):
        keys = values.keys()
        keys.sort()
        sign = ""
        for k in keys:
            sign = sign + k + "=" +str(values[k])
        sign = self.request_phrase + sign + self.request_phrase
        sha256sign = hashlib.sha256(sign.encode()).hexdigest()
        return sha256sign

    def _signature_values(self,values):
        keys = values.keys()
        keys.sort()
        sign = ""
        for k in keys:
            sign = sign + k + "=" +str(values[k])
        sign = self.request_phrase + sign + self.request_phrase
        return sign

    @api.multi
    def payfort_form_generate_values(self, values):
        base_url = self.env['ir.config_parameter'].get_param('web.base.url')
        payfort_form_values = dict(values)
        if values['reference'] != "/":
            payfort_tx_values = {
                'command': "PURCHASE",
                'customer_email': values['partner_email'],
                'amount' : int(values['amount']*100),
                'currency' :values['currency'].name,
                'customer_name': values['partner_name'],
                'merchant_reference' : values['reference'],
                'access_code' : self.access_code,
                'merchant_identifier' : self.merchant_identifier,
                'language' :'en' ,
                'eci': 'ECOMMERCE',
            }
            payfort_tx_values['return_url'] =  '%s' % urlparse.urljoin(base_url,'/payment/payfort/return')
            payfort_tx_values['signature'] = self._payfort_generate_signature(payfort_tx_values)
            payfort_tx_values['tx_url'] = self.payfort_get_form_action_url()
            payfort_form_values.update(payfort_tx_values)
        else:
            _logger.info("--NO refernece values---values-----")
        return payfort_form_values

    @api.model
    def _get_payfort_urls(self, environment):
        """ PayFort URLS """
        if environment == 'prod':
            return {
                'payfort_form_url': 'https://checkout.PayFort.com/FortAPI/paymentPage'

            }
        else:
            return {
                'payfort_form_url': 'https://sbcheckout.PayFort.com/FortAPI/paymentPage',
            }


    @api.multi
    def payfort_get_form_action_url(self):
        return self._get_payfort_urls(self.environment)['payfort_form_url']


class TxPaypal(models.Model):
    _inherit = 'payment.transaction'

    @api.model
    def _payfort_form_get_tx_from_data(self, data):
        if data.get('merchant_reference'):
            reference = data.get('merchant_reference')
            if not reference:
                error_msg = _(
                    'payfort: received data with missing '
                    'reference (%s)') % (reference)
                _logger.info(error_msg)
                raise ValidationError(error_msg)
            transaction = self.search([('reference', '=', reference)])
            if not transaction:
                error_msg = (_('payfort: received data for reference %s; no '
                               'order found') % (reference))
                raise ValidationError(error_msg)
            elif len(transaction) > 1:
                error_msg = (_('payfort: received data for reference %s; '
                               'multiple orders found') % (reference))
                raise ValidationError(error_msg)
            return transaction

    @api.multi
    def _payfort_form_validate(self, data):
        res = {}
        if data.get('status') == '14':
            _logger.info(
                'Validated payfort payment for tx %s: '
                'set as done' % (self.reference))
            res.update(state='done', date_validate=data.get(
                'payment_date', fields.datetime.now()),
                acquirer_reference=data.get('authorization_code'))
            return self.write(res)
        else:
            error = 'Received unrecognized data for payfort payment %s, set as error' % (self.reference)
            _logger.info(error)
            res.update(state='error', state_message=error)
            return self.write(res)
