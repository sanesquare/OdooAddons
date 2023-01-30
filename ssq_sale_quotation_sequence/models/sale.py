from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    quotation_number = fields.Char("Quotation Number")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals["quotation_number"] = self.env["ir.sequence"].next_by_code("sale.quotation")
        return super().create(vals_list)
