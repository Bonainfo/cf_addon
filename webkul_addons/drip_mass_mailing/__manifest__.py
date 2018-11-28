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
  "name"                 :  "Drip Mass Mailing",
  "summary"              :  "Events, News, Offers or Sales- design about anything and rope in the multiple benefits of the Drip mailing.",
  "category"             :  "Marketing",
  "version"              :  "1.0.0",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-Drip-Mass-Mailing.html ",
  "description"          :  """https://webkul.com/blog/odoo-drip-mass-mailing/""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=drip_mass_mailing&version=10.0",
  "depends"              :  [
                             'mass_mailing',
                            ],
  "data"                 :  [
                             'data/cron.xml',
                             'security/ir.model.access.csv',
                             'view/mailing_list_view.xml',
                            ],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  69,
  "currency"             :  "EUR",
  "pre_init_hook": "pre_init_check",
}