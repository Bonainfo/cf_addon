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
    'name'          :   'Odoo Marketplace Pharmacy Details',
    'author'        :   'Webkul Software Pvt. Ltd.',
    'sequence'      :   0,
    'summary'       :   'Stores the Details of Unique Id given by seller to customers.',
    "license"       :   "Other proprietary",
    "version"       :   "1.0.0",
    'description'   :   """Stores the Details of Unique Id given by seller to customers.""",
    'depends'       :   [
        'theme_pharmacistplace',
        'marketplace_seller_wise_checkout',
    ],
    'data'          :   [
        'security/access_control_security.xml',
        'security/ir.model.access.csv',
        'data/mp_pharmacist_detail_demo_data.xml',
        'views/mp_pharmacist_details_view.xml',
        'views/mp_pharmacy_account_form.xml',
        'views/pharmacy_detail_template.xml',
        'views/inherit_sale_views.xml',
        'views/inherit_res_partner_view.xml',
        'views/inherit_mp_dashboard.xml',
        'report/inherit_report_templates.xml',
    ],
    "application"          :  True,
    "installable"          :  True,
    "auto_install"         :  True,
    "pre_init_hook"        :  "pre_init_check",
}
