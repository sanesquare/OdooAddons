from odoo import _, models


class PartnerWhatsappContact(models.Model):
    _inherit = "res.partner"

    def contact_whatsapp(self):
        return {
            "type": "ir.actions.act_window",
            "name": _("Whatsapp Message"),
            "res_model": "whatsapp.wizard.partner",
            "target": "new",
            "view_mode": "form",
            "view_type": "form",
        }
