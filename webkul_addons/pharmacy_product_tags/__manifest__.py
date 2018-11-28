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
  "name"                 :  "Pharmacy Product Tags",
  "summary"              :  "This module will add product tag for pharmacy.",
  "category"             :  "Website",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "description"          :  """This module will add product tag for pharmacy.""",
  "depends"              :  [
                              "marketplace_theme_pharmacistplace_compatibility"
                              # "odoo_marketplace",
                            ],
  "data"                 :  [
                              'security/ir.model.access.csv',
                              'views/pharmacy_tag_view.xml',
                              'views/template.xml',
                            ],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
}
