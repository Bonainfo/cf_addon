odoo.define('website_sale_offer.slider_filter', function (require) {
    "use strict";
    var ajax = require('web.ajax');
    $(document).ready(function () {
        // Website Sale Filter Controls

        // Produc discount Slider
        $('#enable_offer_filter').on('change', function () {
            if ($('#enable_offer_filter').is(':checked')) {
                // var min_discount = 'No Terms and Conditions.';
                // var max_discount = 'No Terms and Conditions.';
                // var min_bonus = 'No Terms and Conditions.';
                // var max_bonus = 'No Terms and Conditions.';

                ajax.jsonRpc("/discount/bonus/filter", 'call', {
                    'min_discount': parseInt($("#min_discount").val()),
                    'max_discount': parseInt($("#max_discount").val()),
                    'min_bonus': parseInt($("#min_bonus").val()),
                    'max_bonus': parseInt($("#max_bonus").val()),
                })
                    .then(function (result) {
                        console.log("Discount and bonus filter has been applied.");
                        window.location.reload();
                    });

            }
        });

        // Produc bonus Slider
        $("#pp_bonus_slider").slider({
            animate: "slow",
            range: true,
            min: parseInt($("#min_bonus").data('min_bonus_range')),
            max: parseInt($("#max_bonus").data('max_bonus_range')),
            step: 1,
            values: [parseInt($("#min_bonus").data('default_min_bonus_range')), parseInt($("#max_bonus").data('default_max_bonus_range'))],
            slide: function (event, ui) {
                console.log(ui.values[0], ui.values[1]);
                $("#min_bonus").val(ui.values[0]);
                $("#max_bonus").val(ui.values[1]);
            },
            stop: function (e, ui) {
                $('#enable_offer_filter').selected(true);
                $(this).closest("form").submit();
                $(".offer_loader").show().delay(3000).animate({
                    opacity: 0,
                    width: 0,
                    height: 0
                }, 500);
            },
        });

        $("#pp_discount_slider").slider({
            animate: "slow",
            range: true,
            min: parseInt($("#min_discount").data('min_discount_range')),
            max: parseInt($("#max_discount").data('max_discount_range')),
            step: 1,
            values: [parseInt($("#min_discount").data('default_min_discount_range')), parseInt($("#max_discount").data('default_max_discount_range'))],
            slide: function (event, ui) {
                $("#min_discount").val(ui.values[0]);
                $("#max_discount").val(ui.values[1]);
            },
            stop: function (e, ui) {
                $('#enable_offer_filter').selected(true);
                $(this).closest("form").submit();
                $(".offer_loader").show().delay(3000).animate({
                    opacity: 0,
                    width: 0,
                    height: 0
                }, 500);

            },
        });
    });
});
