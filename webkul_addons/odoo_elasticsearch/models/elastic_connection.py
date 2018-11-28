# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#    See LICENSE file for full copyright and licensing details.
#################################################################################
import logging
_logger = logging.getLogger(__name__)
from odoo import api, fields, models
from odoo.exceptions import UserError
import requests
import certifi

ELASTIC_STATUS = False
try:
    from elasticsearch import Elasticsearch
    ELASTIC_STATUS = True
except Exception as e:
    _logger.info("< WARNING : No module name Elasticsearch>")



class ElasticConnection(models.Model):
    _name = 'elastic.connection'

    name = fields.Char(string="Name", required=True)
    host = fields.Char(string="Host ( ip / name)", required=True)
    port = fields.Integer(string="Port", required=True)
    url_prefix = fields.Selection(
        [
            ('http', 'http'),
            ('https', 'https')
        ], string="Url Prefix", required=True)
    timeout = fields.Integer(string="Timeout", required=True, default=10)

    @api.multi
    def test_connection(self):
        url = ("%s://%s:%s" % (self.url_prefix, self.host, self.port))
        try:
            res = requests.get(url)
            raise UserError(res.content)
        except Exception as e:
            raise UserError(e)


    def check_connection(self, record):
        result = {'status': False, 'message': ''}
        url = ("%s://%s:%s" % (record.url_prefix,record.host, record.port))
        try:
            res = requests.get(url)
            result.update({"status": True, "message": "Connection created successfully","url":url,"reponse":res})
        except Exception as e:
            result.update({"status": False, "message": "Connection not created","url":url})
        return result



    @api.model
    def _getConfiguration(self):
        result = {'status':False, 'message':''}
        record = self.search([],limit=1)
        if ELASTIC_STATUS:
            if record:
                connectionStatus = self.check_connection(record)
                if connectionStatus['status']:
                    result.update({"host":record.host,"port":record.port,"status":True})
                else:
                    result.update(connectionStatus)
            else:
                result.update({"message":"No Configuration Found !!!"})
        else:
            result.update({"message":"No module name Elasticsearch !!!"})
        return result

    @api.model
    def _getConnectionData(self):
        result = self._getConfiguration()
        if result['status']:
            result['elastic_obj'] = Elasticsearch(
                                                hosts = [{"host":result["host"],"port":result["port"]}],
						#hosts=[{"host":host,"port":port}],
						use_ssl=True,
						ca_certs="/usr/local/lib/python2.7/dist-packages/certifi/cacert.pem",

				    )
        return result

