odoo.define('ssq_pos_global_discount_restrict.DiscountButton', function(require) {
    'use strict';

    const DiscountButton = require('pos_discount.DiscountButton');
    const ProductScreen = require('point_of_sale.ProductScreen');

    ProductScreen.addControlButton({
        component: DiscountButton,
        condition: function () {
            var cashier = this.env.pos.get('cashier') || this.env.pos.get_cashier();
            var has_global_discount_rights = false;
            if (this.env.pos.config.module_pos_discount && this.env.pos.config.discount_product_id) {
                has_global_discount_rights = true;
                if (this.env.pos.config.is_global_discount_restrict) {
                    has_global_discount_rights = false;
                    if (this.env.pos.config.global_discount_allowed_employee_ids.includes(cashier.id)) {
                        has_global_discount_rights = true;
                    }
                }
            }
            return has_global_discount_rights;
        },
        position: ['replace', 'DiscountButton'],
    });

});
