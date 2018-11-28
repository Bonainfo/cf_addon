/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : https://store.webkul.com/license.html/ */

odoo.define('pharmacy_company_filter.pharma_company_search', function (require) {
    "use strict";

    var ajax = require('web.ajax');
    var core = require('web.core');
    var _t = core._t;

    $(document).ready(function () {

        $('#find_pharma_company').keypress(function (event) {
            if (event.keyCode == 13) {
                event.preventDefault();
            }
        });

        $('#find_pharma_company').on('input', function () {
            var $dist_input = $(this);
            var $div = $dist_input.closest('div');
            var manufacturer_ul_list = $div.find('.pharma-company-list');
            var set_manufacturer = $div.find('#set_pharma_company');
            var set_manufacturers = set_manufacturer.data("set-pharma-company-list")
            var data = $dist_input.val();
            ajax.jsonRpc("/find/manufacturer", 'call', {
                'manufacturer': data,
                'set_manufacturers': set_manufacturers,
            })
                .then(function (response) {
                    if (typeof (response) != 'boolean') {
                        var str1 = ''
                        $.each(response, function (key, value) {
                            str1 = str1 + '<li class="set_manufacturer" style="cursor: pointer;"><div data-manufacturer-id=' + key + '>' + value + '</div></li>'
                        });
                        manufacturer_ul_list.html(str1);
                    }
                    else {
                        var str1 = '<li>No Record Found</li>'
                        manufacturer_ul_list.html(str1);
                    }
                    manufacturer_ul_list.show();

                });
        }).on('blur', function () {
            $(this).closest('div').find('.pharma-company-list').hide();
        });

        $('.pharma-company-list').on('mousedown', function (event) {
            event.preventDefault();
        }).on('click', '.set_manufacturer', function (evt) {
            var $this = $(this);
            var $div = $this.closest('div');
            var manufacturer_ul_list = $div.find('.pharma-company-list');
            var find_manufacturer = $div.find('#find_pharma_company');
            var set_pharma_company = $div.find('#set_pharma_company');
            var manufacturer_id = parseInt($this.find('div').data('manufacturer-id'));
            var set_manufacturer = '<input type="text" name="pharma_company" class="hidden" value="' + manufacturer_id + '"/>';
            set_pharma_company.html(set_manufacturer);
            find_manufacturer.val($this.find('div').html());
            manufacturer_ul_list.hide();
        });

        $('.remove-manufacturer').on('click', function (evt) {
            var $this = $(this);
            var $div = $this.closest("div");
            var $form = $this.closest("form");
            $div.remove();
            $form.submit();
        });

    });
});
