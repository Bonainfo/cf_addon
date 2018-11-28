/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : https://store.webkul.com/license.html/ */

odoo.define('website_notification_pharmacistplace.notification_popover', function (require) {
    "use strict";
    var core = require('web.core');
    var _t = core._t;
    $(document).ready(function () {

        $('.my_notification_date').each(function () {
            var my_notification_date = $(this).text();
            $(this).text(moment(moment.utc(my_notification_date).local()).fromNow());
            // $(this).text(moment(my_notification_date).fromNow());
        });
       
        $('#notification_li').on('click', function (e) {
            var self = this;
            $('#notification_li').popover({
                animation: true,
                container: 'body',
                html: true,
                placement: 'bottom',
                title: "",
                trigger: 'click',
                template: '<div class="popover notification-popover" role="tooltip"><div class="arrow"></div><h3 class="popover-title"></h3><div class="popover-content"></div></div>'

            });
            if ($(self).is(':hover') && !$(".notification-popover:visible").length) {
                return $.get("/website/notifications", {})
                    .then(function (data) {
                        $(self).data("bs.popover").options.content = data;
                        $(self).popover("show");
                        $("#notification_li sup").remove();
                        $('.notification_date').each(function () {
                            var notificatio_time = $(this).text();
                            $(this).text(moment(moment.utc(notificatio_time).local()).fromNow());
                            // $(this).text(moment(notificatio_time).fromNow());
                        });
                    });
                }
            else{
                $(self).popover('destroy');
            }
        });
        $("html").on('click', function (e) {
            if ($('.notification-popover:visible')) {
                $('.notification-popover').popover('destroy');
            }
        })
    });
});
