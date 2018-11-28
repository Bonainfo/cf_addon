/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : https://store.webkul.com/license.html/ */

odoo.define('marketplace_pharmacist_details.mp_pharmacist_details', function (require) {

    var core = require('web.core');
    var ajax = require('web.ajax');


    $(document).ready(function() {

            $('.comm_reg_browse_btn').click(function(e){
                $('#comm_reg').trigger('click');
            });

            $('input[type="file"][name="comm_reg"]').change(function(e){
                var fileName = e.target.files[0].name;
                $("#comm_reg_file_name").text(fileName)
            });

            $('input[type="file"][name="tax_card"]').change(function(e){
                var fileName = e.target.files[0].name;
                $("#tax_card_file_name").text(fileName)
            });

            $('.tax_card_browse_btn').click(function(){
                $('#tax_card').trigger('click');
            });

            $('#pharmacy_form_submit').on('click', function(event){
                pharmacy_account_exist = $(this).data('pharmacy_account_exist')
                if (pharmacy_account_exist=="True"){
                    $(document).find(".pharmacy_account_exist").css("display","grid")
                    $(document).find(".pharmacy_form_checkout_button").prev().addClass(" pull-left")
                    $(document).find(".pharmacy_form_checkout_button").removeAttr("style")
                    event.preventDefault();
                }
                seller_not_found = $(this).data('seller_not_found')
                if (seller_not_found=="1"){
                    $(document).find(".seller_not_found").css("display","grid")
                    event.preventDefault();
                }
            })

            $('#pharmacy_account_search').on('click', function(event){
                pharmacy_account_id = document.getElementById("pharmacy_account_id").value
                if (pharmacy_account_id == ''){

                }
                else{
                    ajax.jsonRpc("/pharmacy/account/search", "call", {
                        "pharmacy_account_id": pharmacy_account_id,
                    })
                    .then(function (data) {
                        if (data){
                            $(document.getElementById("pharmacy_account_id")).parent().next().html("Pharmacy Id Found :-)")
                        }
                        else{
                            $(document.getElementById("pharmacy_account_id")).parent().next().html("Pharmacy Id Not Found :-(")
                        }
                        $(document.getElementById("pharmacy_account_id")).parent().next().next().css("display","block");
                    })
                }

            })

            $('.create_pharmacy_account_div').on('change', "select[name='country_id']", function (){
                ajax.jsonRpc("/shop/country_infos/" + $("#country_id").val(), 'call', {mode: 'shipping'}).then(
                    function(data) {
                    var selectStates = $("select[name='state_id']");
                    if (selectStates.data('init')===0 || selectStates.find('option').length===1) {
                        if (data.states.length) {
                            selectStates.html('');
                            _.each(data.states, function(x) {
                                var opt = $('<option>').text(x[1])
                                    .attr('value', x[0])
                                    .attr('data-code', x[2]);
                                selectStates.append(opt);
                            });
                            selectStates.parent('div').show();
                            selectStates.attr('required', 1);
                        }
                        else {
                            selectStates.val('').parent('div').hide();
                        }
                        selectStates.data('init', 0);
                    }
                })
            })
    })

})
