# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
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
# If not, see <https://store.webkul.com/license.html/>
#################################################################################
#client Pharmacistplace.com
{
  "name"                 :  "Pharmacist Place: Mobile App Builder",
  "summary"              :  "This module allows you to convert your shop sales very easily with a native mobile application.",
  "category"             :  "Sales",
  "version"              :  "1.2.0",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "",
  "description"          :  """""",
  "live_test_url"        :  "http://demo.webkul.com/web/login",
  "depends"              :  [
                            'website_sale',
                            'website_sale_offer',
                            'odoo_marketplace',
                            "pharmacy_product_tags",
                            'marketplace_theme_pharmacistplace_compatibility',
                            'smart_pharmacy_codefish',
                            "website_ajax_login_pharmacistplace",
                            "marketplace_pharmacist_details",
                            ],
  "data"                 :  [
                             'security/mobikul_security.xml',
                             'security/ir.model.access.csv',
                             'data/mobikul_data.xml',
                             'views/product_view.xml',
                             'views/order_view.xml',
                             'views/mobikul_views.xml',
                             'views/res_config_view.xml',
                             'views/menus.xml',
                             'views/sync_cat_view.xml',

                            ],
  "demo"                 :  ['data/demo_data_view.xml'],
  "css"                  :  [],
  "js"                   :  [],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  599,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}
