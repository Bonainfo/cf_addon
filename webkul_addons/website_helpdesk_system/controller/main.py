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


import logging
from collections import OrderedDict
import requests
from odoo import http, tools, _
from odoo.http import request
from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.website_portal.controllers.main import website_account
from odoo.addons.website_mail.controllers.main import WebsiteMail
from odoo.tools.misc import consteq
from odoo.osv.expression import OR
_logger = logging.getLogger(__name__)


class WebsiteMailController(WebsiteMail):

    @http.route(['/website_mail/post/post'], type='http', methods=['POST'], auth='public', website=True)
    def chatter_post(self, res_model='', res_id=None, message='', redirect=None, **kw):
        if res_model == 'helpdesk.review':
            review = request.env['helpdesk.review'].browse(int(res_id))
            review.write({'rating': int(kw.get('rating') or 0),'comment':message,'state':'done'})
            super(WebsiteMailController, self).chatter_post(res_model, res_id, message, **kw)
            return request.render(
                "website_helpdesk_system.ticket_created",
                {'title': 'Thank You', 'message': 'Review Successfully Added'})
        return super(WebsiteMailController, self).chatter_post(res_model, res_id, message, **kw)


class WebsiteAccount(website_account):

    def _prepare_portal_layout_values(self):
        values = super(WebsiteAccount, self)._prepare_portal_layout_values()
        ticket_count = request.env['helpdesk.ticket'].search_count([])
        values.update({
            'ticket_count': ticket_count,
        })
        return values

    @http.route(['/my/helpdesk', '/my/helpdesk/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_helpdesk(self, page=1, date_begin=None, date_end=None, category=None, sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        sortings = {
            'date': {'label': _('Newest'), 'order': 'create_date desc'},
            'name': {'label': _('Name'), 'order': 'name'},
            'stage': {'label': _('Stage'), 'order': 'stage_id'},
            'update': {'label': _('Last Update'), 'order': 'date_last_stage_update desc'},
        }
        if not sortby:
            sortby = 'date'
        order = sortings[sortby]['order']
        domain = []
        archive_groups = self._get_archive_groups('helpdesk.ticket', domain)
        searchbar_filters = {
            'all': {'label': _('All'), 'domain': []},
        }
        categories = request.env['helpdesk.category'].search([])
        for cate in categories:
            searchbar_filters.update({
                str(cate.id): {'label': cate.name, 'domain': [('category_id', '=', cate.id)]}
            })
        if not category:
            category = 'all'
        domain += searchbar_filters.get(category)['domain']

        partner = request.env.user.partner_id
        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        # pager
        ticket_count = request.env['helpdesk.ticket'].search_count(domain)

        pager = request.website.pager(
            url="/my/helpdesk",
            url_args={'date_begin': date_begin, 'date_end': date_end},
            total=ticket_count,
            page=page,
            step=self._items_per_page
        )
        # content according to pager and archive selected
        tickets = request.env['helpdesk.ticket'].search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])
        request.session['my_tickets_history'] = tickets.ids[:100]
        values.update({
            'date': date_begin,
            'date_end': date_end,
            'sortings': sortings,
            'sortby': sortby,
            'helpdesks': tickets,
            'ticket_category': category,
            'page_name': 'helpdesk',
            'archive_groups': archive_groups,
            'default_url': '/my/helpdesk',
            'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
            'pager': pager,
        })
        return request.render("website_helpdesk_system.my_tickets", values)

    @http.route(['/my/helpdesk/<int:helpdesk_id>'], type='http', auth="user", website=True)
    def portal_my_ticket(self, helpdesk_id=None, **kw):
        helpdesk = request.env['helpdesk.ticket'].browse(helpdesk_id)
        vals = {'helpdesk': helpdesk}
        return request.render("website_helpdesk_system.my_ticket", vals)

    
class WebsiteHelpdesk(http.Controller):

    @http.route(['/review/start/<model("helpdesk.review"):review>',
                 '/review/start/<model("helpdesk.review"):review>/<string:token>'],
                type='http', auth='user', website=True)
    def start_review(self, review, token=None, **post):
        Review = request.env['helpdesk.review']

        user_review = Review.sudo().search([('token', '=', token)], limit=1)
        if not user_review:
            return request.render("website.403")

        # Select the right page
        if user_review.state == 'new':  # Intro page
            rating_message_values = dict([])
            data = {'review': user_review, 'token': user_review.token,'display_rating':True,'rating_message_values':rating_message_values}
            return request.render('website_helpdesk_system.review_template', data)
        else:
            return request.render("website_helpdesk_system.ticket_created", {'title':'Thank You','message':'Review already Added'})

    
    def values_preprocess(self, values):
        return values
    
    def checkout_form_validate(self,  all_form_values, data):
        # all_form_values: all values before preprocess
        # data: values after preprocess
        error = dict()
        error_message = []

        # Required fields from form
        required_fields = self._get_mandatory_fields()
        # error message for empty required fields
        for field_name in required_fields:
            if not data.get(field_name):
                error[field_name] = 'missing'

        # email validation
        if data.get('email') and not tools.single_email_re.match(data.get('email')):
            error["email"] = 'error'
            error_message.append(_('Invalid Email! Please enter a valid email address.'))

        if [err for err in error.items() if err == 'missing']:
            error_message.append(_('Some required fields are empty.'))

        return error, error_message

    def _get_mandatory_fields(self):
        return ["name", "email", "phone", "category_id", "subject",'description']


    @http.route('/helpdesk/view', type='http', auth="public", website=True)
    def helpdesk_view(self, **post):
        if request.env.user.partner_id.id == request.website.user_id.sudo().partner_id.id:
            return request.render("website_helpdesk_system.login_required", {})
        return request.render("website_helpdesk_system.helpdesk_view", {})

    @http.route('/helpdesk', type='http', auth="public", website=True)
    def helpdesk(self, page=0, category=None, topic=None, search='', ppg=False, **post):
        default =request.env['helpdesk.config.settings'].sudo().get_values()
        request.context = dict(request.context, partner=request.env.user.partner_id)
        Partner = request.env['res.partner'].with_context(show_address=1).sudo()
        mode = False
        checkout_values, errors = {}, {}
        partner_id = request.env.user.partner_id.id
        if request.env.user.partner_id.id == request.website.user_id.sudo().partner_id.id:
            return request.render("website_helpdesk_system.login_required", {})
        checkout_values = Partner.browse(partner_id)
        request.context = dict(request.context, partner=request.env.user.partner_id)
        categs = request.env['helpdesk.category'].search([])
        if category:
            topics = request.env['helpdesk.topic'].search([('category_id', '=', category.id)])
        else:
            topics = []
        keep = QueryURL('/helpdesk')
        values = {
            'search': search,
            'category': category,
            'categories': categs,
            'topics':topics,
            'partner_id':request.env.user.partner_id.id,
            'keep':keep,
            'error':errors,
            'checkout':checkout_values,
            'recaptcha_security_enable':default.get('enabled_recaptcha')
        }
        if category:
            values['main_object'] = category
        return request.render("website_helpdesk_system.helpdesk_view", values)

    @http.route('/helpdesk/validate', type='http', auth="public", website=True)
    def helpdesk_validate(self, **post):
        default =request.env['helpdesk.config.settings'].sudo().get_values()
        pre_values = self.values_preprocess(post)
        errors, error_msg = self.checkout_form_validate( post, post)
        categs = request.env['helpdesk.category'].search([])
        values = post
        vals = {
            'category': request.env['helpdesk.category'].browse(int(post.get('category_id'))) if post.get('category_id') else False,
            'categories': categs,
            'partner_id':request.env.user.partner_id.id,
            'error':errors,
            'checkout':values,
        }
        if errors:
            errors['error_message'] = error_msg
            
            return request.render("website_helpdesk_system.helpdesk_view", vals)
        if 'recaptcha_security_enable' in post and default.get('enabled_recaptcha'):
            secret_key= default.get('recaptcha_private_key')
            captcha_result= self.verify_recaptcha(post.get('g-recaptcha-response'),secret_key)
            if not captcha_result.get("success", False):
                errors['error_message'] = self.custom_recaptcha_error_message(captcha_result.get('error-codes', None))
                vals.update({'error':errors})
                return request.render("website_helpdesk_system.helpdesk_view", vals)
        helpdesk = request.env['helpdesk.ticket'].create_helpdesk_ticket(post)
        if helpdesk:
            return request.render("website_helpdesk_system.ticket_created", helpdesk)
        return request.render("website_helpdesk_system.helpdesk_view", {})



    @http.route(['/helpdesk/category/<model("helpdesk.category"):category>'], type='json', auth="public", methods=['POST'], website=True)
    def sub_category_infos(self, category, **kw):
        topics = request.env['helpdesk.topic'].search([('category_id', '=', category.id)])
        return dict(
            topic=[(st.id, st.name) for st in topics],
        )

    def custom_recaptcha_error_message(self,error_code):
        error_code_mapper={
            'missing-input-secret':'Secret parameter is missing,Please Inform the Site-Admin',
            'invalid-input-secret':'Secret parameter is invalid or malformed,Please Inform the Site-Admin.',
            'missing-input-response':'CAPTCHA is missing,Please Try Again.',
            'invalid-input-response':'CAPTCHA is missing is invalid or malformed,,Please Try Again.'
        }
        return error_code_mapper.get(error_code[0] if error_code else None,'Please Fill All Entry and Submit Recaptcha Again.')

    def verify_recaptcha(self,response,secret_key ):
        url = "https://www.google.com/recaptcha/api/siteverify"
        params = {
            'secret':secret_key ,
            'response': response,
            'remoteip': request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        }
        verify_rs = requests.get(url, params=params, verify=True)
        verify_rs = verify_rs.json()
        return verify_rs
