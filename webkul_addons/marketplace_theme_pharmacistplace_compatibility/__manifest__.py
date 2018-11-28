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
  "name"                 :  "Odoo Marketplace Theme Compatiblity",
  "summary"              :  "Containes Theme Pharmacistplace compatiblity features of Odoo Marketplace.",
  "category"             :  "Website",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "description"          :  """Containes Theme customized features of Odoo Marketplace.""",
  "depends"              :  [
                              'odoo_marketplace',
                              "theme_pharmacistplace",
                              "website_base_filter_attribute",
                            ],
  "data"                 :  [
                              'data/marketplace_menu_data.xml',
                              'views/res_config_view.xml',
                              'views/product_view.xml',
                              'views/mo_sol_view.xml',
                              'views/theme_pharmacistplace_template.xml',
                              'views/ecommerce_template.xml',
                              'views/views.xml',
                            ],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
}
