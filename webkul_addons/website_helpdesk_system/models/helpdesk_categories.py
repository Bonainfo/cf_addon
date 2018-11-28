# -*- coding: utf-8 -*-
##########################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2016-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# License URL :<https://store.webkul.com/license.html/>
##########################################################################

from odoo import api, fields, models



class Categories(models.Model):

    _name = "helpdesk.category"
    _description = "Helpdesk Categories"
    _rec_name = 'name'
    _order = "sequence, name, id"

    name = fields.Char('Category Name', required=True, translate=True)
    sequence = fields.Integer('Sequence', default=1, help="Used to order category.")
    default_team_id = fields.Many2one('wk.team', string="Resonsible Team", required=True)
    description = fields.Text(string="Description")
    manager_id = fields.Many2one("res.users", string="Responsible User", required=True)
    categories_topic_ids = fields.One2many('helpdesk.topic', 'category_id', string="Related Topics")

    @api.onchange('default_team_id')
    def onchange_team_id(self):
        if self.default_team_id and not self.manager_id:
            self.manager_id = self.default_team_id.manager.id
        



class Topic(models.Model):
    
    _name = "helpdesk.topic"
    _description = "Helpdesk Topics"
    _rec_name = 'name'
    _order = "sequence, name, id"

    name = fields.Char('Topic Name', required=True, translate=True)
    sequence = fields.Integer('Sequence', default=1, help="Category related Topic.")
    description = fields.Text(string="Description")
    category_id = fields.Many2one("helpdesk.category", required=True)