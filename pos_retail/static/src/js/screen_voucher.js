"use strict";
odoo.define('pos_retail.screen_voucher', function (require) {

    var screens = require('point_of_sale.screens');
    var core = require('web.core');
    var gui = require('point_of_sale.gui');
    var qweb = core.qweb;
    var PopupWidget = require('point_of_sale.popups');
    var rpc = require('pos.rpc');

    var vouchers_screen = screens.ScreenWidget.extend({
        template: 'vouchers_screen',

        init: function (parent, options) {
            this._super(parent, options);
            this.vouchers = options.vouchers;
        },
        show: function () {
            this._super();
            this.vouchers = this.pos.vouchers;
            this.render_vouchers();
            this.handle_auto_print();
        },
        handle_auto_print: function () {
            if (this.should_auto_print()) {
                this.print();
                if (this.should_close_immediately()) {
                    this.click_back();
                }
            } else {
                this.lock_screen(false);
            }
        },
        should_auto_print: function () {
            return this.pos.config.iface_print_auto;
        },
        should_close_immediately: function () {
            return this.pos.config.iface_print_via_proxy;
        },
        lock_screen: function (locked) {
            this.$('.back').addClass('highlight');
            window.print();
        },
        get_voucher_env: function (voucher) {
            var order = this.pos.get_order();
            var datas = order.export_for_printing();
            return {
                widget: this,
                pos: this.pos,
                order: order,
                datas: datas,
                voucher: voucher
            };
        },
        print_web: function () {
            window.print();
        },
        print_xml: function () {
            if (this.vouchers) {
                for (var i = 0; i < this.vouchers.length; i++) {
                    var voucher_xml = qweb.render('voucher_ticket_xml', this.get_voucher_env(this.vouchers[i]));
                    this.pos.proxy.print_receipt(voucher_xml);
                }
            }
        },
        print: function () {
            var self = this;
            if (!this.pos.config.iface_print_via_proxy) {
                this.lock_screen(true);
                setTimeout(function () {
                    self.lock_screen(false);
                }, 1000);

                this.print_web();
            } else {
                this.print_xml();
                this.lock_screen(false);
            }
        },
        click_back: function () {
            this.pos.gui.show_screen('products');
        },
        renderElement: function () {
            var self = this;
            this._super();
            this.$('.back').click(function () {
                self.click_back();
            });
            this.$('.button.print').click(function () {
                self.print();
            });
        },
        render_change: function () {
            this.$('.change-value').html(this.format_currency(this.pos.get_order().get_change()));
        },
        render_vouchers: function () {
            var $voucher_content = this.$('.pos-receipt-container');
            var url_location = window.location.origin + '/report/barcode/EAN13/';
            $voucher_content.empty();
            if (this.vouchers) {
                for (var i = 0; i < this.vouchers.length; i++) {
                    this.vouchers[i]['url_barcode'] = url_location + this.vouchers[i]['code'];
                    $voucher_content.append(
                        qweb.render('voucher_ticket_html', this.get_voucher_env(this.vouchers[i]))
                    );
                }
            }
        }
    });
    gui.define_screen({name: 'vouchers_screen', widget: vouchers_screen});

    // print vouchers
    var popup_print_vouchers = PopupWidget.extend({
        template: 'popup_print_vouchers',
        show: function (options) {
            var self = this;
            this._super(options);
            this.$('.print-voucher').click(function () {
                var validate;
                var period_days = parseFloat(self.$('.period_days').val());
                var apply_type = self.$('.apply_type').val();
                var voucher_amount = parseFloat(self.$('.voucher_amount').val());
                var quantity_create = parseInt(self.$('.quantity_create').val());
                var method = self.$('.method').val();
                var customer = self.pos.get_order().get_client();
                if (method == "special_customer" && !customer) {
                    this.pos.gui.show_popup('confirm', {
                        title: 'Warning',
                        body: 'Because apply to special customer, required select customer the first',
                    });
                    return self.pos.gui.show_screen('clientlist')
                }
                if (typeof period_days != 'number' || isNaN(period_days)) {
                    self.$('.period_days').css({
                        'box-shadow': '0px 0px 0px 1px rgb(236, 5, 5) inset'
                    });
                    validate = false;
                } else {
                    self.$('.period_days').css({
                        'box-shadow': '0px 0px 0px 1px rgb(34, 206, 3) inset'
                    })
                }
                if (typeof voucher_amount != 'number' || isNaN(voucher_amount)) {
                    self.$('.voucher_amount').css({
                        'box-shadow': '0px 0px 0px 1px rgb(236, 5, 5) inset'
                    });
                    validate = false;
                } else {
                    self.$('.voucher_amount').css({
                        'box-shadow': '0px 0px 0px 1px rgb(34, 206, 3) inset'
                    })
                }
                if (typeof quantity_create != 'number' || isNaN(quantity_create)) {
                    self.$('.quantity_create').css({
                        'box-shadow': '0px 0px 0px 1px rgb(236, 5, 5) inset'
                    });
                    validate = false;
                } else {
                    self.$('.quantity_create').css({
                        'box-shadow': '0px 0px 0px 1px rgb(34, 206, 3) inset'
                    });
                }
                if (validate == false) {
                    return;
                }
                var voucher_data = {
                    apply_type: apply_type,
                    value: voucher_amount,
                    method: method,
                    period_days: period_days,
                    total_available: quantity_create
                };
                if (customer) {
                    voucher_data['customer_id'] = customer['id'];
                }
                self.gui.close_popup();
                return rpc.query({
                    model: 'pos.voucher',
                    method: 'create_voucher',
                    args: [voucher_data]
                }).then(function (vouchers) {
                    self.pos.vouchers = vouchers;
                    self.pos.gui.show_screen('vouchers_screen');
                }).fail(function (type, error) {
                    return self.pos.query_backend_fail(type, error);
                });
            });
            this.$('.cancel').click(function () {
                self.click_cancel();
            });
        }
    });
    gui.define_popup({
        name: 'popup_print_vouchers',
        widget: popup_print_vouchers
    });

    var button_print_voucher = screens.ActionButtonWidget.extend({
        template: 'button_print_voucher',
        button_click: function () {
            this.gui.show_popup('popup_print_vouchers', {});

        }
    });
    screens.define_action_button({
        'name': 'button_print_voucher',
        'widget': button_print_voucher,
        'condition': function () {
            return this.pos.config.print_voucher;
        }
    });
});
