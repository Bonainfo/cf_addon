/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : https://store.webkul.com/license.html/ */

odoo.define('marketplace_theme_pharmacistplace_compatibility.product_search', function(require) {
    "use strict";

    var ajax = require('web.ajax');
    var core = require('web.core');
    var _t = core._t;

    $(document).ready(function() {

        $('#find_distributor').keypress(function (event) {
            if (event.keyCode == 13) {
                event.preventDefault();
            }
        });

        $('#find_distributor').on('input',function(){
            var $dist_input = $(this);
            var $div = $dist_input.closest('div');
            var dist_ul_list = $div.find('.dist-seller-list');
            var set_distributor = $div.find('#set_distributor');
            var set_sellers = set_distributor.data("set-seller-list")
            var data = $dist_input.val();
            ajax.jsonRpc("/find/distributor", 'call',{
                'distributor': data,
                'set_sellers' : set_sellers,
            })
            .then(function (response) {
                if(typeof(response) != 'boolean'){
                    var str1 = ''
                    $.each(response, function(key, value) {
                        str1 = str1 + '<li class="sel_seller"><div data-seller-id='+ key +'>'+value+'</div></li>'
                    });
                    dist_ul_list.html(str1);
                }
                else{
                    var str1 = '<li>No Record Found</li>'
                    dist_ul_list.html(str1);
                }
                dist_ul_list.show();

            });
        }).on('blur', function () {
            $(this).closest('div').find('.dist-seller-list').hide();
        });;

        $('.dist-seller-list').on('mousedown', function (event) {
            event.preventDefault();
        }).on('click','.sel_seller',function(evt){
            var $this = $(this);
            var $div = $this.closest('div');
            var dist_ul_list = $div.find('.dist-seller-list');
            var find_distributor = $div.find('#find_distributor');
            var set_distributor = $div.find('#set_distributor');
            var seller_id = parseInt($this.find('div').data('seller-id'));
            var set_seller = '<input type="text" name="seller" class="hidden" value="'+ seller_id +'"/>';
            set_distributor.html(set_seller);
            find_distributor.val($this.find('div').html());
            dist_ul_list.hide();
        });

        $('.rem-seller').on('click',function(evt){
            var $this = $(this);
            var $div = $this.closest("div");
            var $form = $this.closest("form");
            $div.remove();
            $form.submit();
        });

    });
});
