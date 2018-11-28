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


from odoo import models, fields, api, _
import logging
_logger = logging.getLogger(__name__)


class Picking(models.Model):
    _inherit = "stock.picking"

    # Override this method as per client requirement for not raising the Lot Number Warning
    @api.multi
    def do_new_transfer(self):
        for pick in self:
            if pick.origin:
                so_obj = self.env['sale.order'].sudo().search([('name','=',pick.origin)], limit=1)
                if so_obj and so_obj.marketplace_seller_id:
                    for pick in self:
                        if pick.state == 'done':
                            raise UserError(_('The pick is already validated'))
                        pack_operations_delete = self.env['stock.pack.operation']
                        if not pick.move_lines and not pick.pack_operation_ids:
                            raise UserError(_('Please create some Initial Demand or Mark as Todo and create some Operations. '))
                        # In draft or with no pack operations edited yet, ask if we can just do everything
                        if pick.state == 'draft' or all([x.qty_done == 0.0 for x in pick.pack_operation_ids]):
                            # If no lots when needed, raise error
                            # picking_type = pick.picking_type_id
                            # if (picking_type.use_create_lots or picking_type.use_existing_lots):
                            #     for pack in pick.pack_operation_ids:
                            #         if pack.product_id and pack.product_id.tracking != 'none':
                            #             raise UserError(_('Some products require lots/serial numbers, so you need to specify those first!'))
                            view = self.env.ref('stock.view_immediate_transfer')
                            wiz = self.env['stock.immediate.transfer'].create({'pick_id': pick.id})
                            # TDE FIXME: a return in a loop, what a good idea. Really.
                            return {
                                'name': _('Immediate Transfer?'),
                                'type': 'ir.actions.act_window',
                                'view_type': 'form',
                                'view_mode': 'form',
                                'res_model': 'stock.immediate.transfer',
                                'views': [(view.id, 'form')],
                                'view_id': view.id,
                                'target': 'new',
                                'res_id': wiz.id,
                                'context': self.env.context,
                            }

                        # Check backorder should check for other barcodes
                        if pick.check_backorder():
                            view = self.env.ref('stock.view_backorder_confirmation')
                            wiz = self.env['stock.backorder.confirmation'].create({'pick_id': pick.id})
                            # TDE FIXME: same reamrk as above actually
                            return {
                                'name': _('Create Backorder?'),
                                'type': 'ir.actions.act_window',
                                'view_type': 'form',
                                'view_mode': 'form',
                                'res_model': 'stock.backorder.confirmation',
                                'views': [(view.id, 'form')],
                                'view_id': view.id,
                                'target': 'new',
                                'res_id': wiz.id,
                                'context': self.env.context,
                            }
                        for operation in pick.pack_operation_ids:
                            if operation.qty_done < 0:
                                raise UserError(_('No negative quantities allowed'))
                            if operation.qty_done > 0:
                                operation.write({'product_qty': operation.qty_done})
                            else:
                                pack_operations_delete |= operation
                        if pack_operations_delete:
                            pack_operations_delete.unlink()
                    self.do_transfer()
                    return
                else:
                    res = super(Picking, self).do_new_transfer()
                    return res


class StockMove(models.Model):
    _inherit = "stock.move"

    @api.multi
    def check_tracking(self, pack_operation):
        for pick in self:
            if pick.origin:
                so_obj = self.env['sale.order'].sudo().search([('name','=',pick.origin)], limit=1)
                if so_obj and so_obj.marketplace_seller_id:
                    return
                else:
                    res = super(StockMove, self).check_tracking(pack_operation)
                    return res
