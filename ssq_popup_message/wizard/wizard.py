from odoo import fields, models


class Popup(models.TransientModel):
    _name = "popup.wizard"
    _description = "Popup"

    name = fields.Text("Message", readonly=True)
