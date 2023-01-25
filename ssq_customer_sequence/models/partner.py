from odoo import fields, models, api


class ResPartner(models.Model):
    _inherit = "res.partner"

    code = fields.Char("Customer Code")
    is_seq_auto_create = fields.Boolean(compute="_compute_sequence_creation")

    def _compute_sequence_creation(self):
        for partner in self:
            partner.is_seq_auto_create = (
                self.env["ir.config_parameter"].sudo().get_param("ssq_customer_sequence.is_seq_auto_create")
            )

    @api.model
    def create(self, vals):
        partner = super().create(vals)
        if partner.customer_rank > 0 and partner.is_seq_auto_create:
            partner.code = self.env["ir.sequence"].next_by_code("code.res.partner")
        return partner

    def create_code(self):
        self.code = self.env["ir.sequence"].next_by_code("code.res.partner")
