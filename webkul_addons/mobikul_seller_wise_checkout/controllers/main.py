# -*- coding: utf-8 -*-
##########################################################################
#
#    Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#
##########################################################################

from odoo import _
from odoo.http import request, Controller, route
import logging
_logger = logging.getLogger(__name__)
from odoo.addons.mobikul.controllers.main   import WebServices,_displayWithCurrency,_get_image_url

class WebServicesInherit(WebServices):

    def getCartDetails(self,last_order,response):
        local = response.get('local',{})
        result = {
        "name":last_order.name,
        "orderId": last_order.id,
        "seller":last_order.marketplace_seller_id and last_order.marketplace_seller_id.name or "",
        "subtotal":{"title":"Subtotal",
                    "value":_displayWithCurrency(local.get('lang_obj'),last_order.amount_untaxed, local.get('currencySymbol'), local.get('currencyPosition')),
                },
        "tax":{"title":"Taxes",
                    "value":_displayWithCurrency(local.get('lang_obj'),last_order.amount_tax, local.get('currencySymbol'), local.get('currencyPosition')),
            },
        "grandtotal":{"title":"Total",
                    "value":_displayWithCurrency(local.get('lang_obj'),last_order.amount_total, local.get('currencySymbol'), local.get('currencyPosition')),
            },
        "items":[]
        }
        for item in last_order.order_line:
            if response.get('addons', {}).get('website_sale_delivery') and item.is_delivery:
                shippingMethod = {
                    "tax":[tax.name for tax in item.tax_id],
                    "name":item.order_id.carrier_id.name,
                    "description":item.order_id.carrier_id.website_description or "",
                    "shippingId":item.order_id.carrier_id.id,
                    "total": _displayWithCurrency(local.get('lang_obj'), item.price_subtotal,
                                                  local.get('currencySymbol'), local.get('currencyPosition')),
                }
                result.update({"delivery":shippingMethod})
            else:
                temp = {
                "lineId":item.id,
                "templateId":item.product_id and item.product_id.product_tmpl_id.id or "",
                "name":item.product_id and item.product_id.display_name or item.name,
                "thumbNail":_get_image_url(self.base_url, 'product.product', item.product_id and item.product_id.id or "",'image'),
                "priceReduce":item.price_reduce < item.price_unit and _displayWithCurrency(local.get('lang_obj'),item.price_reduce, local.get('currencySymbol'), local.get('currencyPosition')) or "",
                "priceUnit":_displayWithCurrency(local.get('lang_obj'),item.price_unit, local.get('currencySymbol'), local.get('currencyPosition')),
                "qty":item.product_uom_qty,
                "total":_displayWithCurrency(local.get('lang_obj'),item.price_subtotal, local.get('currencySymbol'), local.get('currencyPosition')),
                # "discount":item.discount and "(%d%% OFF)"%item.discount or "",
                "discount":item.discount and item.discount or "",
                "max_bonus"  : item.product_id.product_tmpl_id.max_percentage_bonus,
                }
                result['items'].append(temp)
        if not len(result['items']):
            result['message'] = _('Your Shopping Bag is empty.')
        return result

    @route(['/mobikul/mycart','/mobikul/mycart/<int:line_id>'], csrf=False, type='http', auth="none", methods=['POST','PUT','DELETE'])
    def getMyCart(self, line_id=0, **kwargs):
        response = self._authenticate(True, **kwargs)
        if response.get('success'):
            result = {}
            PartnerObj = request.env['res.partner'].sudo()
            Partner = PartnerObj.browse(response.get('customerId'))
            if Partner:
                if request.httprequest.method == "POST":
                    last_order = Partner.last_website_so_id
                    if response.get('addons', {}).get('marketplace_seller_wise_checkout'):
                        temp = []
                        for so in Partner.sale_order_ids:
                            if so.state == "draft":
                                details = self.getCartDetails(so, response)
                                if details.get("items"):
                                    temp.append(details)
                        result['sellerWiseOrder'] = temp
                        if not result['sellerWiseOrder']:
                            result = {'message': _('Your Shopping Bag is empty.')}
                    else:
                        if last_order:
                            result = self.getCartDetails(last_order, response)
                        else:
                            result = {'message':_('Your Shopping Bag is empty.')}
                else:
                    OrderLineObj = request.env['sale.order.line'].sudo()
                    OrderLine = OrderLineObj.search([('id','=',line_id)])
                    if OrderLine:
                        if request.httprequest.method == "PUT":
                            result = {'message':'Updated successfully.'}
                            if self._mData.get('set_qty'):
                                OrderLine.product_uom_qty = self._mData.get('set_qty')
                            elif self._mData.get('add_qty'):
                                OrderLine.product_uom_qty +=int(self._mData['add_qty'])
                            else:
                                result = {'message':'Wrong request.'}
                        elif request.httprequest.method == "DELETE":
                            try:
                                result = {'message':'%s'%(OrderLine.product_id and OrderLine.product_id.name or OrderLine.name)+_(' was removed from your Shopping Bag.')}
                                OrderLine.unlink()
                            except:
                                result = {'message':'Please try again after some time.'}
                        else:
                            result = {'message':'Wrong request.'}
                    else:
                        result = {'message':'No matching product found !!!'}
            else:
                result = {'success':False, 'message':'Account not found !!!'}
            response.update(result)
        return self._response('cart', response)


    @route('/mobikul/mycart/setToEmpty', csrf=False, type='http', auth="none", methods=['DELETE'])
    def setToEmpty(self, **kwargs):
        response = self._authenticate(True, **kwargs)
        if response.get('success'):
            result = {}
            PartnerObj = request.env['res.partner'].sudo()
            Partner = PartnerObj.browse(response.get('customerId'))
            if Partner:
                last_order = Partner.last_website_so_id
                if Partner.sale_order_ids:
                    try:
                        result = {'message': _('Your Shopping Bag has been set to Empty.')}
                        if response.get('addons', {}).get('marketplace_seller_wise_checkout'):
                            cartCount = 0
                            for so in Partner.sale_order_ids:
                                if so.state == "draft":
                                    so.order_line.unlink()
                                    cartCount += so.cart_count
                            result['cartCount'] = cartCount
                        else:
                            last_order.order_line.unlink()
                            result['cartCount'] = last_order.cart_count
                    except Exception as e:
                        result = {'message': 'Please try again after some time.'}
                else:
                    result = {'message': _('Your Shopping Bag is already empty.')}
            else:
                result = {'success': False, 'message': 'Account not found !!!'}
            response.update(result)
        return self._response('setToEmpty', response)

    @route('/mobikul/mycart/setToEmpty/<int:order_id>', csrf=False, type='http', auth="none", methods=['DELETE'])
    def setOrderToEmpty(self, order_id=0,**kwargs):
        _logger.info("-------order_id----%r-----",order_id)
        response = self._authenticate(True, **kwargs)
        if response.get('success'):
            result = {}
            PartnerObj = request.env['res.partner'].sudo()
            Partner = PartnerObj.browse(response.get('customerId'))
            if Partner:
                if response.get('success') and order_id:
                    order = request.env['sale.order'].sudo().search([("id","=",int(order_id))])
                    if order:
                        for line in order.order_line:
                            line.unlink()
                        result = {'message': _('Your Shopping Bag has been set to Empty.')}
                    else:
                        result = {'message': _('No orderId has been found.')}
            else:
                result = {'success': False, 'message': 'Account not found !!!'}
            response.update(result)
        return self._response('setOrderToEmpty', response)

    # @route('/mobikul/mycart/addToCart', csrf=False, type='http', auth="none", methods=['POST'])
    # def addToCart(self, **kwargs):
    #     response = self._authenticate(True, **kwargs)
    #     if response.get('success'):
    #         result = {}
    #         Mobikul = request.env['mobikul'].sudo()
    ###########this method Mobikul.add_to_cart is override in Mobikulinherit model###################
    #         result = Mobikul.add_to_cart(response.get('customerId'), self._mData.get("productId"),
    #                                      self._mData.get("set_qty"), self._mData.get("add_qty"), response)
    #         response.update(result)
    #     return self._response('addToCart', response)

    @route('/mobikul/orderReviewData', csrf=False, type='http', auth="none", methods=['POST'])
    def getOrderReviewData(self, **kwargs):
        Mobikul = request.env['mobikul'].sudo()
        response = self._authenticate(True, **kwargs)
        if response.get('success'):
            result = {}
            Acquirer = request.env['payment.acquirer'].sudo().browse(int(self._mData.get('acquirerId')))
            if Acquirer:
                UserObj = request.env['res.users'].sudo()
                user = UserObj.browse(response.get('userId', 0))
                if user:
                    if response.get('addons', {}).get('marketplace_seller_wise_checkout'):
                        user.partner_id.last_website_so_id = int(self._mData.get('orderId'))
                    if response.get('addons', {}).get('email_verification') and Mobikul.email_verification_defaults().get(
                            'restrict_unverified_users'):
                        if user.wk_token_verified:
                            result = self._orderReview(user, response, Acquirer)
                        else:
                            result = {'success': False,
                                      'message': _("You can't place your order, please verify your account")}
                    else:
                        result = self._orderReview(user, response, Acquirer)
                else:
                    result = {'success': False, 'message': _('Account not found !!!')}
            else:
                result = {'success': False, 'message': _('No Payment methods found with given id.')}
            response.update(result)
        return self._response('orderReviewData', response)


    def _sendPaymentAcknowledge(self,last_order,Partner,customerId,result):
        res = super(WebServicesInherit,self)._sendPaymentAcknowledge(last_order,Partner,customerId,result)
        for so in Partner.sale_order_ids:
            if so.state == "draft":
                Partner.last_website_so_id = so.id
                break
        return res
