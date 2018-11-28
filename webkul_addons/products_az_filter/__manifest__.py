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
  "name"                 :  "Website Product A-Z Filter",
  "summary"              :  "Provide Product A-Z Filter on Website.",
  "category"             :  "Website",
  "version"              :  "0.1",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "maintainer"           :  "Prakash Kumar",
  "website"              :  "https://store.webkul.com/Odoo-Website-Product-A-Z-Filter.html",
  "description"          :  "https://webkul.com/blog/odoo-website-product-a-z-list Provide Product A-Z Filter on Website.",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=products_az_filter&version=10.0",
  "depends"              :  [
                             'website_sale',
                             'website_webkul_addons',
                            ],
  "data"                 :  ['views/template.xml'],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "price"                :  20.0,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}