/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : https://store.webkul.com/license.html/ */

odoo.define('theme_pharmacistplace.theme', function (require) {
    "use strict";

    function numberWithCommas(number) {
        // https://stackoverflow.com/questions/2901102/how-to-print-a-number-with-commas-as-thousands-separators-in-javascript
        return number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    }

    //Simple Animated Counter on Scroll  https://codepen.io/dmcreis/pen/VLLYPo
    function animateNumber($this) {
        var countTo = $this.attr('data-count');
        $({
            countNum: $this.text()
        }).animate({
            countNum: countTo
        },
        {
            duration: 2000,
            easing: 'swing',
            step: function () {
                $this.text(Math.floor(this.countNum));
            },
            complete: function () {
                $this.text(numberWithCommas(this.countNum)); //number with comma
            }
        });
    }

    var scroll_down = 0;
    $(document).ready(function () {
        $('.wk_js_count span').each(function () {
            if ($(".wk_js_count_label")[0].getBoundingClientRect().bottom <= window.innerHeight){
                animateNumber($(this));
                scroll_down = 1;
            }
        });
        var mob_sort = $("#mob-sort")
        var mob_filter = $("#mob-filter")
        var product_category_a = $("#product_category > a")
        
        $('a[href="#mob-sort"], a[href="#mob-filter"]').on('shown.bs.tab', function (e) {
            var target = $(e.target).attr("href") // activated tab
            $('html, body').animate({
                scrollTop: $("#mobile_view_filter").offset().top
            }, 0);
            $(".close-sort-filter").removeClass("hide").addClass("show");
            $("#mobile_view_filter").addClass("no_shadow");
            console.log($(".close-sort-filter").css("display"))
            if (target == '#mob-sort'){
                $(".dropdown_sorty_by>.dropdown>a").dropdown("toggle");
                $("#mob-sort div:first-child").removeClass("hidden-xs");
                mob_sort.addClass("fix_mob_filter");
                $("#products_grid_before").addClass("hidden-xs");
                mob_filter.removeClass("fix_mob_filter");
                if ($("#mob-filter #products_grid_before").hasClass("hidden-xs"))
                    mob_filter.hide();
                $("#mob-sort-line").show();
                $("#mob-filter-line").hide();
                // $("#products_grid_before ul#o_shop_collapse_category > li").addClass("hide");
            }
            if (target == '#mob-filter') {
                $("#products_grid_before").removeClass("hidden-xs");
                mob_filter.addClass("fix_mob_filter");
                mob_filter.show();
                $("#mob-sort div:first-child").addClass("hidden-xs");
                mob_sort.removeClass("fix_mob_filter");
                $("#mob-filter-line").show();
                $("#mob-sort-line").hide();
                if (product_category_a.hasClass("fa-minus")) {
                    product_category_a.addClass("fa-plus");
                    product_category_a.removeClass("fa-minus");
                }
            }
        });
        $("div.flt_heading").on('click', function () {
            $("#o_shop_category, #o_shop_collapse_category").children("li").toggle();
            $(".categ_show_msg").toggle();
            // var fa_icon = product_category_a;
            if (product_category_a.hasClass("fa-plus")) {
                product_category_a.removeClass("fa-plus");
                product_category_a.addClass("fa-minus");
            } else {
                product_category_a.addClass("fa-plus");
                product_category_a.removeClass("fa-minus");
            }
        });

        // $('a[href="#mob-filter"]').on('shown.bs.tab', function (e) {
        //     var target = $(e.target).attr("href") // activated tab
        //     alert(target);
        //     $("#products_grid_before").removeClass("hidden-xs");
        // });
    });

    $(window).scroll(function () {
        if (scroll_down == 0 && $(".wk_js_count_label").get(0) && $(".wk_js_count_label").get(0).getBoundingClientRect().bottom <= window.innerHeight) {
            $('.wk_js_count span').each(function () {
                animateNumber($(this));
            });
            scroll_down = 1;
        }
    });
});
