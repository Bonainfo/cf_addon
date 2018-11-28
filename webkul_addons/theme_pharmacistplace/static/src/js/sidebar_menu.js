odoo.define('sidebar_menu.sidebar_menu', function (require) {
    "use strict";

    $(document).ready(function () {
        $.fn.isInViewport = function () {
            var elementTop = $(this).offset().top;
            var elementBottom = elementTop + $(this).outerHeight();

            var viewportTop = $(window).scrollTop();
            var viewportBottom = viewportTop + $(window).height();

            return elementBottom > viewportTop && elementTop < viewportBottom;
        };

        $(window).on('resize scroll', function () {
            if ($('.menu_icon').isInViewport()) {
                $("#menu_hide_arrow").hide();
            } else {
                $("#menu_hide_arrow").show();
            }
        });

        window.onscroll = function () {
            myFunction()
        };

        function myFunction() {
            var mobile_view_filter = $("#mobile_view_filter");
            if (mobile_view_filter && $(".main_menu_justify")) {
                if (mobile_view_filter.offset() && 'top' in mobile_view_filter.offset() && window.pageYOffset > mobile_view_filter.offset().top) {
                    mobile_view_filter.addClass("mob_sticky");
                    $("#products_grid").addClass("pt_for_sticky");
                    // $("#mob-sort").addClass("fix_mob_filter");
                } else if ($('.main_menu_justify').isInViewport()){
                    mobile_view_filter.removeClass("mob_sticky").removeClass("no_shadow");
                    $("#products_grid").removeClass("pt_for_sticky");
                    // $("#mob-sort").removeClass("fix_mob_filter");
                    $("#mob-sort div:first-child, #products_grid_before").addClass("hidden-xs");
                    $("#mob-sort, #mob-filter").removeClass("fix_mob_filter");
                    $("#mobile_view_filter li").removeClass("active");
                    $(".close-sort-filter").removeClass("show").addClass("hide");
                    // $(".close-sort-filter").css("display", "none !important");
                }
            }
        }

        $(".close-sort-filter").on('click', function name(e) {
            $("#mob-sort div:first-child, #products_grid_before").addClass("hidden-xs");
            $("#mob-sort, #mob-filter").removeClass("fix_mob_filter");
            $("#mobile_view_filter li").removeClass("active");
            $(".close-sort-filter").removeClass("show").addClass("hide");
        });

        $('.menu_icon, #menu_hide_arrow').on('click', function () {
            $("body").toggleClass("stop_page_scroll");
            $('.menu_icon, #sidebar').toggleClass('active');
            $('#wrapwrap, #oe_main_menu_navbar').toggleClass('srink_wrapwrap');
            // Need when sidebar position not fixed
            // $("#sidebar").height($(document).height()); 
        });
    });
    
});