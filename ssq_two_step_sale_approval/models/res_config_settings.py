from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    is_two_step_sale_approval = fields.Boolean(
        "Two Step Sale Approval",
        default=False,
        config_parameter="ssq_two_step_sale_approval.is_two_step_sale_approval",
        store=True,
    )
    first_level_user_ids = fields.Many2many(
        "res.users", "res_config_settings_res_users_first", related="company_id.first_level_user_ids", readonly=False
    )
    second_level_user_ids = fields.Many2many(
        "res.users", "res_config_settings_res_users_second", related="company_id.second_level_user_ids", readonly=False
    )
