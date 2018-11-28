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
    'name'          :   'Website Notification Module For Pharmacistplace',
    'author'        :   'Webkul Software Pvt. Ltd.',
    'sequence'      :   0,
    'summary'       :   'This module shows the various notification on website.',
    "license"       :   "Other proprietary",
    "version"       :   "1.0.0",
    'description'   :   """ """,
    'depends'       :   [
        'theme_pharmacistplace',
    ],
    'data'          :   [
        # 'security/access_control_security.xml',
        # 'security/ir.model.access.csv',
        'data/signup_template.xml',
        'views/templates.xml',
    ],
    "application"          :  True,
    "installable"          :  True,
    "auto_install"         :  True,
    "pre_init_hook"        :  "pre_init_check",
}
