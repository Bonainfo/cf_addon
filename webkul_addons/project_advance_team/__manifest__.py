# -*- coding: utf-8 -*-
##########################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2017-Present Webkul Software Pvt. Ltd.
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
    'name': 'Project Advance Team Management',
    'summary': 'This module helps a user for easily managing team and extra members on task.',
    'category': 'Project Management',
    'version': '1.0.0',
    'sequence': 1,
    'author': "Webkul Software Pvt. Ltd.",
    "license":  "Other proprietary",
    'website': 'https://store.webkul.com/Odoo-Project-Advance-Team-Management.html',
    'description': """https://webkul.com/blog/odoo-project-advance-team-management/""",
    "live_test_url":  "http://odoodemo.webkul.com/?module=project_advance_team&version=10.0",
    'depends': ['project', 'project_issue','hr'],
    'data': [
        'data/data.xml',
        'security/project_security.xml',
        'security/ir.model.access.csv',
        'views/wk_team_view.xml',
        'views/project_team_view.xml',
    ],
    'demo':[
        'data/demo_data.xml',
    ],
    "images":  ['static/description/Banner.png'],
    "application":  True,
    "installable":  True,
    "auto_install":  False,
    "price":  35,
    "currency":  "EUR",
    "pre_init_hook":  "pre_init_check",
}
