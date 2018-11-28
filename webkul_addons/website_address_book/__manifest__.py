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
  "name"                 :  "Odoo Website Customer Address Book",
  "summary"              :  "Odoo Website Customer Address Book",
  "category"             :  "Website",
  "version"              :  "1.0.0",
  "sequence"             :  1,
  "license"              :  "Other proprietary",
  "author"               :  "Webkul Software Pvt. Ltd.",
  "website"              :  "https://store.webkul.com/",
  "description"          :  "Manages customer address book in Website",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=website_address_book&version=10.0",
  "depends"              :  [
                             'website_sale',
                            ],
  "data"                 :  [
                             'views/address_book_template.xml',
                             'views/portal_templates.xml',
                            ],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  45,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}
