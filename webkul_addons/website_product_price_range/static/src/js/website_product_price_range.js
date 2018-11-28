$(document).ready(function() {

    $('input[name="price_range"]').on('click', function() {
        $(this).closest("form").submit();
    });
    var default_min_price = parseInt($("#min_price").data('default_min_price_range'));
    var default_max_price = parseInt($("#max_price").data('default_max_price_range'));
    var min_price_range = parseInt($("#min_price").data('min_price_range'));
    var max_price_range = parseInt($("#max_price").data('max_price_range'));
    jQuery("#wk_slider").slider({
        animate: "slow",
        range: true,
        min: min_price_range,
        max: max_price_range,
        step: 1,
        values: [default_min_price, default_max_price],
        slide: function(event, ui) {
            $("#min_price").val(ui.values[0]);
            $("#max_price").val(ui.values[1]);


        },
        stop: function(e, ui) {
          $(this).closest("form").submit();
          $(".price_range_loader").show().delay(3000).animate({
            opacity:0,
            width: 0,
            height:0
          }, 500);

        },
    });
});
