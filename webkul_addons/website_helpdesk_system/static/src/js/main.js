odoo.define('website_helpdesk_system.website_helpdesk_system', function(require) {
    "use strict";
    var ajax = require('web.ajax');
    $(document).ready(function() {  
        $('.oe_website_sale').on('change', "select[name='category_id']", function() {
            if ($("#category_id").val()) {
                ajax.jsonRpc("/helpdesk/category/" + $("#category_id").val(), 'call', {}).then(
                    function(data) {
                        // populate sub category and display
                        var Topics = $("select[name='topic_id']");
                        // dont reload sub category at first loading (done in qweb)
                        if (Topics.data('init') === 0 || Topics.find('option').length === 1) {
                            if (data.topic.length) {
                                Topics.html('');
                                var opt = $('<option>').text('Topic...')
                                    .attr('value', '');
                                Topics.append(opt);
                                _.each(data.topic, function(x) {
                                    var opt = $('<option>').text(x[1])
                                        .attr('value', x[0]);
                                    Topics.append(opt);
                                });
                                Topics.parent('div').show();
                            } else {
                                Topics.val('').parent('div').hide();
                            }
                            Topics.data('init', 0);
                        } else {
                            Topics.data('init', 0);
                        }

                    }
                );
            }
        });

    });



});