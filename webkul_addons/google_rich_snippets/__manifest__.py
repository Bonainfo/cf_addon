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
{"name": "Google Rich Snippets",
    "summary": "This module adds structured Data Markup which is used to generate Rich Snippets in search engine results.",
    "category": "Website",
    "version": "1.0.0",
    "sequence": 1,
    "author": "Webkul Software Pvt. Ltd.",
    "license": "Other proprietary",
    "website": "https://store.webkul.com/Odoo-Google-Rich-Snippets.html",
    "description": """
Structured Data Markup is used to generate Rich Snippets in search engine results. It is a way for website owners to send structured data to search engine robots, helping them to understand your content and create well-presented search results.

Google supports a number of rich snippets for content types, including: Reviews, People, Products, Businesses, Events and Organizations.

Odoo implements micro data as defined in the schema.org specification for events, eCommerce products, forum posts and contact addresses. This allows your product pages to be displayed in Google using extra information like the price and rating of a product
    """,
    "live_test_url": "http://odoodemo.webkul.com/?module=google_rich_snippets&version=10.0",
    "depends": ['website_sale_stock', 'website_webkul_addons'],
    "data": [
        'views/snippets_template.xml',
        'views/res_config.xml',
    ],
    "images": ['static/description/Banner.png'],
    "application": True,
    "price": 45,
    "currency": "EUR",
    "pre_init_hook": "pre_init_check",
 }
