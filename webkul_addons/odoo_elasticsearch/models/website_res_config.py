from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)

class WebsiteConfigSettings(models.TransientModel):

    _inherit = 'website.config.settings'

    default_elastic_set_id = fields.Many2one(related='website_id.default_elastic_set_id',string="Default Elastic Setting")


