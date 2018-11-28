
from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)

class WebsiteInherit(models.Model):

    _inherit = "website"

    default_elastic_set_id = fields.Many2one("elastic.search.config", string="Default Elastic Server")

    @api.model
    def _get_elasticDefaults(self):
        params = {"status":False,"message":""}
        if self.default_elastic_set_id:
            vals ={
                "start_limit" : self.default_elastic_set_id.start_limit,
                "text_color":self.default_elastic_set_id.text_color,
                "hover_text_color":self.default_elastic_set_id.hover_text_color,
                "hover_background_color":self.default_elastic_set_id.hover_background_color,

            }

            if self.default_elastic_set_id.enable_product:
                vals.update({
                    "enable_product" : True,
                    "product_index":self.default_elastic_set_id.product_index_id.name,
                    "prdct_sugg_position": self.default_elastic_set_id.prdct_sugg_position,
                    "max_prdct_sugg":self.default_elastic_set_id.max_prdct_sugg,
                    "max_prdct_desc": self.default_elastic_set_id.max_prdct_desc ,
                    "is_prdct_desc":self.default_elastic_set_id.is_prdct_desc,
                    "is_prdct_thumb": self.default_elastic_set_id.is_prdct_thumb,
                })
            params.update(vals)
        else:
            params = params
        return params