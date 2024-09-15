/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.as_product_details = publicWidget.Widget.extend({
    selector: ".applied_filters",
    'events': {
        'change .js_applied_attributes .applied_filters-checkbox input[name="attrib"]': '_onChangeAttrib',
    },
    start: function(){
        this._super();
    },
    _onChangeAttrib: function(e){
        if (!e.isDefaultPrevented()) {
            e.preventDefault();
            this.$target.children("form.js_applied_attributes").submit();
            return true;
        }
    },
});
