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



class Stage(models.Model):
    """ Model for case stages. This models the main stages of a document
        management flow. Tickets will now use only stages, instead of state and stages.
        Stages are for example used to display the kanban view of records.
    """
    _name = "helpdesk.stage"
    _description = "Stage of case"
    _rec_name = 'name'
    _order = "sequence, name, id"

    name = fields.Char('Stage Name', required=True, translate=True)
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    requirements = fields.Text('Requirements', help="Enter here the internal requirements for this stage (ex: Offer sent to customer). It will appear as a tooltip over the stage's name.")
    fold = fields.Boolean('Folded in Pipeline',
        help='This stage is folded in the kanban view when there are no records in that stage to display.')
    legend_blocked = fields.Char(
        string='Kanban Blocked Explanation', translate=True,
        help='Override the default value displayed for the blocked state for kanban selection, when the ticket is in that stage.')
    legend_done = fields.Char(
        string='Kanban Valid Explanation', translate=True,
        help='Override the default value displayed for the done state for kanban selection, when the ticket is in that stage.')
    legend_normal = fields.Char(
        string='Kanban Ongoing Explanation', translate=True,
        help='Override the default value displayed for the normal state for kanban selection, when the ticket is in that stage.')
