from odoo import fields, models, api, _
from odoo.exceptions import AccessError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    is_two_step_sale_approval = fields.Boolean(
        compute="_compute_sale_approval", string="Two Step Sale Approval", store=True
    )

    def _default_approval_state(self):
        if self.env["ir.config_parameter"].sudo().get_param("ssq_two_step_sale_approval.is_two_step_sale_approval"):
            return "waiting_approval_1"

    approval_state = fields.Selection(
        [("waiting_approval_1", "First Approval"), ("waiting_approval_2", "Second Approval"), ("approved", "Approved")],
        default=lambda self: self._default_approval_state(),
    )

    @api.depends("company_id")
    def _compute_sale_approval(self):
        is_two_step_sale_approval = (
            self.env["ir.config_parameter"].sudo().get_param("ssq_two_step_sale_approval.is_two_step_sale_approval")
        )
        for sale in self:
            sale.is_two_step_sale_approval = is_two_step_sale_approval

    def first_approve(self):
        if self.env.user.id not in self.company_id.first_level_user_ids.ids:
            raise AccessError(_("Sorry you are not allowed to approve this order."))
        self.approval_state = "waiting_approval_2"

    def second_approve(self):
        if self.env.user.id not in self.company_id.second_level_user_ids.ids:
            raise AccessError(_("Sorry you are not allowed to approve this order."))
        self.approval_state = False
