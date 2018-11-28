# -*- coding: utf-8 -*-
##########################################################################
#
#    Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#
##########################################################################
from ast import literal_eval
from odoo import api, fields, models, _, SUPERUSER_ID

class MobikulInherit(models.Model):
    _inherit = "mobikul"

    def check_mobikul_addons(self):
        result = {}
        result = super(MobikulInherit,self).check_mobikul_addons()
        ir_model_obj = self.env['ir.module.module'].sudo()
        result['marketplace_seller_wise_checkout'] = ir_model_obj.search([('state', '=', 'installed'),('name', '=', 'marketplace_seller_wise_checkout')]) and True or False
        return result

    def findMpSaleOrder(self,Partner,Product):
        sale_order = False
        for so in Partner.sale_order_ids:
            if so.state == "draft" and so.marketplace_seller_id == Product.marketplace_seller_id:
                sale_order = so
        return sale_order

    def add_to_cart(self, partner, product_id, set_qty, add_qty, response):
        PartnerObj = self.env['res.partner'].sudo()
        Partner = PartnerObj.browse(partner)
        if Partner:
            Product = self.env['product.product'].sudo().search([('id', '=', product_id)])
            if Product:
                last_order = self.findMpSaleOrder(Partner,Product)
                seller_id = Product.marketplace_seller_id and Product.marketplace_seller_id.id or False
                if last_order:
                    flag = 0
                    for line in last_order.order_line:
                        if line.product_id == Product:
                            if set_qty:
                                line.product_uom_qty = set_qty
                                line.product_uom_change()
                                line._onchange_discount()
                                flag = 1
                            elif add_qty:
                                line.product_uom_qty += int(add_qty)
                                line.product_uom_change()
                                line._onchange_discount()
                                flag = 1
                            else:
                                flag = -1
                                result = {'message': 'Insufficient data.', 'success': False}
                    if not flag:
                        # Create order line
                        self._create_so_line(last_order, Product, int(add_qty),marketplace_seller_id=seller_id)
                        flag = True
                    if flag == 1:
                        result = {'message': 'Added Successfully.', 'productName': Product.display_name,
                                  'success': True}
                    result['cartCount'] = last_order.cart_count
                    result['orderId'] = last_order.id
                    return result

                else:
                    # create Order
                    local = response.get('local', {})
                    res = self._create_so(Partner, local,marketplace_seller_id=seller_id)
                    self._create_so_line(res['order'], Product, int(add_qty),marketplace_seller_id=seller_id)
                    result = {'message': 'Added Successfully.', 'cartCount': res['order'].cart_count,"orderId":res['order'].id,
                              'productName': Product.display_name, 'success': True}
                    return result
            else:
                result = {'success': False, 'message': 'Insufficient data.'}
                return result
        else:
            result = {'success': False, 'message': 'Account not found !!!'}
            return result

    @api.model
    def _create_so(self, partner, local,marketplace_seller_id=False):
        local = local or {}
        result = {"success": True}
        addr = partner.address_get(['delivery'])
        so_data = {
            'partner_id': partner.id,
            'pricelist_id': self._context.get('pricelist'),
            'payment_term_id': partner.property_payment_term_id.id,
            'team_id': local.get("teamId"),
            'partner_invoice_id': partner.id,
            'partner_shipping_id': addr['delivery'],
            'user_id': local.get("salespersonId"),
            "marketplace_seller_id":marketplace_seller_id
        }
        company = self.env['product.pricelist'].browse(self._context.get('pricelist')).sudo().company_id
        if company:
            so_data['company_id'] = company.id
        result['order'] = self.env['sale.order'].sudo().create(so_data)
#        if not marketplace_seller_id:
        partner.write({'last_website_so_id': result['order'].id})
        result['cartId'] = result['order'].id
        return result

    @api.model
    def _create_so_line(self, order, Product, qty=1,marketplace_seller_id=False):
        result = {"success": True}
        SaleOrderLineSudo = self.env['sale.order.line'].sudo()

        product_context = dict(self.env.context)
        product_context.setdefault('lang', order.partner_id.lang)
        product_context.update({
            'partner': order.partner_id.id,
            'quantity': qty,
            'date': order.date_order,
            'pricelist': order.pricelist_id.id,
        })
        product = Product.with_context(product_context)

        so_line_data = {
            'name': product.name,
            'product_id': product.id,
            'product_uom_qty': qty,
            'order_id': order.id,
            'product_uom': product.uom_id.id,
            'price_unit': product.price,
            "marketplace_seller_id ":marketplace_seller_id
        }
        order_line = SaleOrderLineSudo.create(so_line_data)
        order_line.product_id_change()
        order_line.product_uom_change()
        order_line._onchange_discount()
        return result
