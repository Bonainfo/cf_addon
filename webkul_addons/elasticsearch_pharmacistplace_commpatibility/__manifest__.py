# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# License URL : https://store.webkul.com/license.html/
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
{
  "name"                 :  "Theme Pharmacistplace Elasticsearch Compatiblity",
  "summary"              :  "Containes Marketplace compatiblity features with Odoo Elasticsearch for Security Issues.",
  "category"             :  "Website",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "description"          :  """Containes Marketplace security features with Odoo Elasticsearch.""",
  "depends"              :  [
                              "odoo_marketplace",
                              "odoo_elasticsearch",
                            ],
  "data"                 :  [
                              'security/ir.model.access.csv',
                            ],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  True,
}
