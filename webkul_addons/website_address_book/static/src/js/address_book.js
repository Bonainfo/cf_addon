odoo.define('website_address_book.address_book', function (require) {
'use strict';

    var ajax = require('web.ajax');
    var base = require("web_editor.base");

    $(document).ready(function() {
        $('.oe_cart').on('click', '.js_change_billing', function() {
          if (!$('body.editor_enable').length) { 
            var $old = $('.all_billing').find('.panel.border_primary');
            $old.find('.btn-inv').toggle();
            $old.addClass('js_change_billing');
            $old.removeClass('border_primary');

            var $new = $(this).parent('div.one_kanban').find('.panel');
            $new.find('.btn-inv').toggle();
            $new.removeClass('js_change_billing');
            $new.addClass('border_primary');

            var $form = $(this).parent('div.one_kanban').find('form.hide');
            $.post($form.attr('action'), $form.serialize()+'&xhr=1');
          }
        });
    })

});
