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
  "name"                 :  "Pharmacistplace Product Comparison & Offers compatiblity",
  "summary"              :  "Containing Pharmacistplace product comparison & Offers compatiblity features.",
  "category"             :  "Website",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "description"          :  """Containes Theme customized features of Odoo Marketplace.""",
  "depends"              :  [
                              'pp_product_comparison_compatibility',
                              "website_sale_offer",
                            ],
  "data"                 :  [
                              'views/template.xml',
                            ],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  True,
}
