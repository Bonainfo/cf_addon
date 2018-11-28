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
{
  "name"                 :  "Website Product Price Range",
  "summary"              :  "Plug-in Providing Price based Filtration on Website .",
  "category"             :  "Website",
  "version"              :  "0.3",
  "sequence"             :  1.0,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "maintainer"           :  "Prakash Kumar",
  "website"              :  "https://store.webkul.com/Odoo-Website-Product-Price-Range.html",
  "description"          :  """https://webkul.com/blog/odoo-website-product-price-range
  Website Product Price Range Filter For odoo.
  """,
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=website_product_price_range&version=10.0",
  "depends"              :  [
                             'website_sale',
                             'website_webkul_addons',
                            ],
  "data"                 :  [
                             'data/data.xml',
                             'views/template.xml',
                             'views/res_config.xml',
                             'views/webkul_addons_config_inherit_view.xml',
                            ],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "price"                :  25,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}
