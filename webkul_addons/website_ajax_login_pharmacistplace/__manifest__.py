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
  "name"                 :  "Pharmacistplace Website Ajax Login/Sign-Up",
  "summary"              :  "When the user clicks on Login/Sign-Up, the requested form appears in a very nice Ajax popup, integrated with facebook, odoo, google+.",
  "category"             :  "Website",
  "version"              :  "1.1.1",
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "maintainer"           :  "Prakash Kumar",
  "website"              :  "https://store.webkul.com/Odoo-Website-Login-Sign-Up.html",
  "description"          :  """http://webkul.com/blog/odoo-website-ajax-login-sign-up/""",
  "depends"              :  [
                             'website',
                             'website_sale',
                             'auth_signup',
                             'auth_oauth',
                             'theme_pharmacistplace',
                            ],
  "data"                 :  [
                            'data/website_ajax_config_demo.xml',
                            'view/ajax_login_template.xml',
                            'view/res_config.xml',
                            'view/inherit_auth_signup_login_template.xml',
                            ],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "price"                :  39,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}
