odoo.define('ssq_pos_global_discount_limit.DiscountButton', function(require) {
    'use strict';

    const DiscountButton = require('pos_discount.DiscountButton');
    const Registries = require('point_of_sale.Registries');

    const LimitDiscountButton = (DiscountButton) =>
        class extends DiscountButton {

            async onClick() {
                var self = this;
                const { confirmed, payload } = await this.showPopup('NumberPopup',{
                    title: this.env._t('Discount Percentage'),
                    startingValue: this.env.pos.config.discount_pc,
                    isInputSelected: true
                });
                if (confirmed) {
                    const val = Math.round(Math.max(0,Math.min(100,parseFloat(payload))));
                    if (this.env.pos.config.is_enable_global_discount_limit && val > this.env.pos.config.global_discount_limit) {
                        await this.showPopup('ErrorPopup', {
                            title : this.env._t("Discount limit exceeded"),
                            body  : this.env._t("The global discount limit is set to " + this.env.pos.config.global_discount_limit + "."),
                        });
                    } else {
                        await self.apply_discount(val);
                    }
                }
            }
        };

    Registries.Component.extend(DiscountButton, LimitDiscountButton);
    return DiscountButton;

});
