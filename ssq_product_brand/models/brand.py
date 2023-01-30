from odoo import fields, models


class ProductBrand(models.Model):
    _name = "product.brand"
    _description = "Brands"

    name = fields.Char("Brand Name", required=True)
    description = fields.Text("Description")
    brand_logo = fields.Binary("Logo")
