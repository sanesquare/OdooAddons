from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class PosConfig(models.Model):
    _inherit = "pos.config"

    is_enable_global_discount_limit = fields.Boolean(string="Enable Global Discount Limit", default=False)
    global_discount_limit = fields.Float(
        string="Global Discount Limit",
        help="The global discount limit %",
        default=100.0,
    )

    @api.constrains("global_discount_limit")
    def _check_global_discount_limit(self):
        for record in self:
            if record.module_pos_discount:
                if record.global_discount_limit < 0:
                    raise ValidationError(_("Global Discount Limit should be greater than or equal to 0."))
                elif record.global_discount_limit > 100:
                    raise ValidationError(_("Global Discount Limit should be less than or equal to 100."))
