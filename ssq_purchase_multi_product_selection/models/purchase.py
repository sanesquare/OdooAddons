from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def select_products(self):
        return {
            "name": "Select Products",
            "type": "ir.actions.act_window",
            "res_model": "select.product.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {"default_purchase_id": self.id},
        }


class SelectProductWizard(models.TransientModel):
    _name = "select.product.wizard"

    purchase_id = fields.Many2one("purchase.order")
    product_ids = fields.Many2many("product.product")

    def select_products(self):
        product_list = []
        for product in self.product_ids:
            product_list.append((0, 0, {"product_id": product.id}))
        self.purchase_id.write({"order_line": product_list})
