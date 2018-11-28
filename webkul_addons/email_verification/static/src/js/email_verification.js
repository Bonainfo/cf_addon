odoo.define('email_verification.email_verification', function (require) {
	var ajax = require('web.ajax');
 $(document).ready(function(){
        var oe_website_sale = this;
       $('#restrict_checkout').on("click",function(event){
            if (('disabled' in this.attributes) &&  this.attributes.disabled.value == 'True')
            {
                event.preventDefault();
                $(this).popover({
                  content:"You have not verified your email yet, please verify your email for proceeding further.",
                  title:"WARNING!!",
                  placement:"top",
                  trigger:'focus',
                });
                $(this).popover('show');
            }
        });
 });
});
