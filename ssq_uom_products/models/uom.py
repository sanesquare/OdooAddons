from odoo import fields, models


class ProductUOM(models.Model):
    _inherit = "uom.uom"

    product_count = fields.Float(compute="_compute_count")
    po_product_count = fields.Float(compute="_compute_count")

    def _compute_count(self):
        for record in self:
            record.product_count = len(self.env["product.template"].search([("uom_id", "=", self.id)]))
            record.po_product_count = len(self.env["product.template"].search([("uom_po_id", "=", self.id)]))

    def action_view_products(self):
        product_ids = self.env["product.template"].search([("uom_id", "=", self.id)]).ids
        return {
            "name": "Products",
            "type": "ir.actions.act_window",
            "res_model": "product.template",
            "view_mode": "tree,form",
            "domain": [("id", "in", product_ids)],
        }

    def action_view_po_products(self):
        product_ids = self.env["product.template"].search([("uom_po_id", "=", self.id)]).ids
        return {
            "name": "Products",
            "type": "ir.actions.act_window",
            "res_model": "product.template",
            "view_mode": "tree,form",
            "domain": [("id", "in", product_ids)],
        }
