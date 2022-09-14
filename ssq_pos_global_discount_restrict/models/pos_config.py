from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class PosConfig(models.Model):
    _inherit = "pos.config"

    is_global_discount_restrict = fields.Boolean(
        string="Restrict Global Discount",
        help="Restrict global discount in POS",
    )
    global_discount_allowed_employee_ids = fields.Many2many(
        "hr.employee",
        "pos_config_global_discount_allowed_employee_rel",
        string="Employees Allowed to Add Global Discount",
        help="Employees allowed to add Global Discounts in POS",
    )

    @api.constrains("global_discount_allowed_employee_ids", "employee_ids")
    def _check_global_discount_allowed_employee_ids(self):
        for record in self:
            if (
                record.is_global_discount_restrict
                and record.employee_ids
                and record.global_discount_allowed_employee_ids
            ):
                if not set(record.global_discount_allowed_employee_ids.ids).issubset(set(record.employee_ids.ids)):
                    raise ValidationError(
                        _("Employees Allowed to Apply Global Discount should be in Allowed Employees")
                    )
