odoo.define('website_single_page_checkout.website_single_page_checkout', function(require) {
    "use strict";

    var core = require('web.core');
    var ajax = require('web.ajax');
    var _t = core._t;

    $(document).ready(function() {
        
        var new_add = false;
        $('.shipping_address').hide();
        $('#shipping-addr-' + $('select[name="shipping_id"]').val()).show();

        $('select[name="shipping_id"]').on('change', function () {
            $('.shipping_address').hide();

            $('#shipping-addr-' + this.value).show();
            $('#shipping-addr-' + this.value).find('.js_change_shipping').trigger('click');
            if (this.value === '-1') {
                new_add = true;
                add_new_address();
            }
            if (this.value != '-1' && (new_add)) {
                hide_add_new_address();
                new_add = false;
            }
        });

        $('.create_user').on('change', function () {
            var create_user = $(this).is(":checked");
            $('input[name="create_user"]').val(create_user);
            var email = $('input[name="email"]').val();
            if ((create_user) && (validate_email(email))) {
                check_email_availabilty(email);
            } else {
                $('.already_register').hide();

                if (validate_email(email)) {
                    $('input[name="email"]').parent('div').removeClass('has-error');
                    $('.invalid_email').hide();
                    $('.checkout_autoformat').find('.btn-primary').show();
                } else {
                    $('input[name="email"]').parent('div').addClass('has-error');
                    $('.invalid_email').show();
                    $('.checkout_autoformat').find('.btn-primary').hide();
                }
            }
        });

        $('.consent-checkbox').on('change', function () {
            var opt_out = $("input[name='opt_out']").is(":checked");
            var post_opt_out = $("input[name='post_opt_out']").is(":checked");
            ajax.jsonRpc('/partner/update/consent', 'call', {
                'opt_out': opt_out,
                'post_opt_out': post_opt_out,
            })
                .done(function (result) {
                    console.log('Updated');
                })
                .fail(function (result) {
                    console.log('fail executed');
                });
        });

        function check_email_availabilty(email) {
            if (email) {
                ajax.jsonRpc('/single/ckeck/email', 'call', {
                    'email': email.trim(),
                })
                    .done(function (result) {
                        if (!result.status) {
                            $('.already_register').text(result.error).show();
                            $('input[name="email"]').parent('div').addClass('has-error');
                            $('.checkout_autoformat').find('.btn-primary').hide();
                        } else {
                            $('.already_register').hide();
                            $('input[name="email"]').parent('div').removeClass('has-error');
                            $('.checkout_autoformat').find('.btn-primary').show();
                        }
                    })
                    .fail(function (result) {
                        console.log('fail executed');
                    });
            }
        }

        function add_new_address() {
            $("#signle_page_checkout_address, #add_new_address, .show_all_shipping, .all_shipping").toggle();
            $("input[name='is_new_address']").prop('value', true);
            $(".oe_sale_acquirer_button").addClass("disabled_payment_div");
            $(".wk_has_error input").val("").prop("disabled", false);
            $(".wk_has_error input, select").prop("disabled", false);
            $("#save_selected").hide();
            var save_address = $("#save_address");
            save_address.show();
            save_address.removeClass("disabled");
            // $("#save_address").removeClass("disabled");
            save_address.find("span.fa").removeClass("fa-spinner fa-pulse");
            save_address.find("span.fa").addClass("fa-long-arrow-right ");
        }

        function hide_add_new_address() {
            $("#signle_page_checkout_address, .show_all_shipping, #add_new_address, .all_shipping").toggle();
            $("input[name='is_new_address']").prop('value', false);
            $(".oe_sale_acquirer_button").removeClass("disabled_payment_div");
            $(".all_shipping").find(".one_kanban").find("div.border_primary").find("a.btn-default").click();
        }


        $('input[name="email"]').on('change', function () {
            var email = $(this).val();
            if (validate_email(email)) {
                $(this).parent('div').removeClass('has-error');
                $('.invalid_email').hide();
                $('.checkout_autoformat').find('.btn-primary').show();
            } else {
                $(this).parent('div').addClass('has-error');
                $('.invalid_email').show();
                $('.checkout_autoformat').find('.btn-primary').hide();
            }

            var create_user = $('.create_user').is(":checked");
            if ((create_user) && (validate_email(email))) {
                check_email_availabilty(email);
            }
        });

        function validate_email(email) {
            var expr = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
            return expr.test(email);
        }

        function validate_phone_number(email) {
            var expr = /[0-9 -()+]+$/;
            return expr.test(email);
        }

        $("#save_address").on('click', function (ev) {
            var self = this;
            var wk_div_name = $("input[name='wk_name']").val();
            var wk_div_email = $("input[name='wk_email']").val();
            var wk_div_phone = $("input[name='wk_phone']").val();
            var wk_div_street = $("input[name='wk_street']").val();
            var wk_div_city = $("[name='wk_city']").val();
            var wk_div_zip = $("input[name='wk_zip']").val();
            var wk_div_country = $("#country_id").val();
            var wk_div_state = $("#wk_state_id").val()
            var is_state_visible = $("#wk_state_id").is(":visible");

            if (!wk_div_name) {
                $("#wk_div_name").addClass("has-error");
            }
            else{
                $("#wk_div_name").removeClass("has-error");
            }
            if (!wk_div_email) {
                $("#wk_div_email").addClass("has-error");
            }
            else{
                $("#wk_div_email").removeClass("has-error");
            }
            if (!wk_div_phone) {
                $("#wk_div_phone").addClass("has-error");
            }
            else{
                $("#wk_div_phone").removeClass("has-error");
            }
            if (!wk_div_street) {
                $("#wk_div_street").addClass("has-error");
            }
            else{
                $("#wk_div_street").removeClass("has-error");
            }
            if (!wk_div_city) {
                $("#wk_div_city").addClass("has-error");
            }
            else{
                $("#wk_div_city").removeClass("has-error");
            }
            if (!wk_div_country) {
                $("#wk_div_country").addClass("has-error");
            }
            else{
                $("#wk_div_country").removeClass("has-error");
            }
            if (!wk_div_state) {
                $("#wk_div_state").addClass("has-error");
            }
            else{
                $("#wk_div_state").removeClass("has-error");
            }
            if (wk_div_name && wk_div_email && wk_div_phone && wk_div_street && wk_div_city && wk_div_country && (is_state_visible ? wk_div_state : true ) ){
                $('#signle_page_checkout_address div').removeClass("has-error");
                $(this).addClass("disabled");
                $(this).find("span.fa").removeClass("fa-long-arrow-right ");
                $(this).find("span.fa").addClass("fa-spinner fa-pulse");
                ajax.jsonRpc('/save_address', 'call', {
                        'wk_name' : wk_div_name,
                        'wk_email' : wk_div_email,
                        'wk_phone' : wk_div_phone,
                        'wk_street' : wk_div_street,
                        'wk_city': wk_div_city,
                        "wk_zip": wk_div_zip,
                        'wk_country' : wk_div_country,
                        'wk_state' : wk_div_state,
                }).done(function (result) {
                    if (result) {
                        $(self).toggle();
                        $(".disabled_payment_div").removeClass("disabled_payment_div");
                        $(".wk_has_error input, select").prop('disabled', true);
                        $("#save_selected").toggle();
                        var $modal = $(result);
                        $(".all_shipping").find(".border_primary").removeClass("border_primary").addClass("js_change_shipping").find('.btn-ship').toggle();
                        $modal.insertBefore($(".all_shipping").find(".one_kanban").first());
                    } else {
                        console.log("else");
                        window.location.href = '/shop/checkout';
                    }
                }).fail(function (result) {
                    console.log(false);
                    window.location.href = '/shop/checkout';
                });
            }
        });
        $(document).on('click', '.single_page_delivery', function(ev) {
            var carrierId = $(ev.currentTarget).val();
            console.log(carrierId);
            ajax.jsonRpc('/shop/checkout/delivery_option', 'call', {
                'carrier_id': carrierId
            })
            .done(function(result) {
                if (result) {
                    if (result.success) {
                        set_order_amount(document, result);
                    } else {
                        console.log('not success');
                    }
                } else {
                    window.location.href = '/shop';
                }
            })
            .fail(function(result) {
                console.log('fail executed');
            });
        });

        function set_order_amount(document, result) {
            // order final total
            console.log(result);
            $('#order_total .oe_currency_value').text(result.order_total.toFixed(2));
            $('#onepage_total .oe_currency_value').text(result.order_total.toFixed(2));
            var total_ammount = (result.order_total).toString().replace(',', '');
            $(document).find('input[name="amount"]').val(total_ammount);

            // order tax amount
            $('#order_total_taxes .oe_currency_value').text(result.order_total_taxes.toFixed(2));
            $('#onepage_taxes .oe_currency_value').text(result.order_total_taxes.toFixed(2));

            // order total without tax and delivery
            // $('#order_total_untaxed .oe_currency_value').text(result.order_subtotal.toFixed(2));
            // $('#onepage_subtotal .oe_currency_value').text(result.order_subtotal.toFixed(2));

            // order delivery amount
            $('#order_delivery .oe_currency_value').text(result.order_total_delivery.toFixed(2));
            $('#onepage_delivery .oe_currency_value').text(result.order_total_delivery.toFixed(2));

        }
    });
});
