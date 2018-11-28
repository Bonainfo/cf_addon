# -*- coding: utf-8 -*-
##########################################################################
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
##########################################################################
{
    "name":  "Website Helpdesk & Support System",
    "summary":  "Website Helpdesk & Support System is used to provide information and support to the end users/customers regarding the products and services of the organization.",
    "category":  "Marketing",
    "version":  "1.0.1",
    "sequence":  1,
    "license":  "Other proprietary",
    "author":  "Webkul Software Pvt. Ltd.",
    "website":  "https://www.webkul.com/",
    "description":  "Website Helpdesk & Support System is used to provide information and support to the end users/customers regarding the products and services of the organization.",
    "live_test_url":  "http://odoodemo.webkul.com/?module=website_helpdesk_system&version=10.0",
    "depends":  [
        'project_advance_team', 'website_sale', 'website_portal'
    ],
    "data":  [
        'security/helpdesk_security.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'data/email_template.xml',
        'wizard/stage_update_view.xml',
        'views/helpdesk_data.xml',
        'views/helpdesk_tickets.xml',
        'views/helpdesk_stage_views.xml',
        'views/res_config_views.xml',
        'views/template.xml',
        'views/templates.xml',
        'demo/data.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    "images":  ['static/description/Banner.png'],
    "application":  True,
    "installable":  True,
    "auto_install":  False,
    "price":  65,
    "currency":  "EUR",
    "pre_init_hook":  "pre_init_check",
}
