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
  "name"                 :  "Pharmacy Address City Customization",
  "summary"              :  "Pharmacy Address City Customization.",
  "category"             :  "",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "description"          :  """This module will make address city field related type with new M2O city field in partner.""",
  "depends"              :  [
                              "odoo_marketplace",
                              "marketplace_pharmacist_details",
                              "website_single_page_checkout",
                            ],
  "data"                 :  [
                              'data/city_data.xml',
                              'security/ir.model.access.csv',
                              'views/pp_city_view.xml',
                              'views/partner_view.xml',
                              'views/template.xml',
                            ],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
}
