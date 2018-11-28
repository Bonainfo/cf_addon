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
    'name': 'Payfort Payment Acquirer',
    'version': '1.0',
    "description"          :  "Integrate Payfort Payment Gateway with Odoo for accepting payments from customers",
    'summary'              :  """ Website Payfort Payment Acquirer """,
    "category"             :  "Website/Payment Acquirer",
    "version"              :  "1.0.0",
    "author"               :  "Webkul Software Pvt. Ltd.",
    "license"              :  "Other proprietary",
    "maintainer"           :  "Saurabh Gupta",
    "website"              :  "https://store.webkul.com/Odoo.html",
    # "live_test_url"        : "http://odoodemo.webkul.com/?module=payment_payfort&version=10.0&custom_url=/shop/payment",

    'depends': [
                'payment',
                'website_sale'],
    'data': [
        'views/payment_view.xml',
        'views/payfort_acquirer_data.xml',
        'views/template.xml',
        'data/payment_payfort_data.xml'
    ],
   "demo":[
        # 'data/demo_paytabs.xml',
           ],

    "images"               :  ['static/description/banner.png'],
    "application"          :  True,
    "installable"          :  True,
    "price"                :  69.0,
    "currency"             :  "EUR",
}
