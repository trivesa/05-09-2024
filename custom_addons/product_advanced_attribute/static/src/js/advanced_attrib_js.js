/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.as_prod_detail = publicWidget.Widget.extend({
    selector: "#product_full_spec",

    start: function(){
        var show_spec = $("#wrapwrap").find(".table").children('tbody').children('tr').children('td');
        if (show_spec.length == 0){
            $("#wrapwrap").find("#product_full_spec").addClass("d-none");
        }
    },
});
