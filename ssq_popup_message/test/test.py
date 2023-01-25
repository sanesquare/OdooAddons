from odoo import models


class Module(models.Model):
    _inherit = "ir.module.module"

    def test_app(self):
        view_id = self.env.ref("ssq_popup_message.popup_message_form").id
        message = "Test Message"
        return {
            "name": "Success",
            "type": "ir.actions.act_window",
            "view_type": "form",
            "view_mode": "form",
            "res_model": "popup.wizard",
            "target": "new",
            "view_id": view_id,
            "context": {"default_name": message},
        }
