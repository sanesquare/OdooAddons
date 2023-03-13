from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    first_level_user_ids = fields.Many2many("res.users", "res_company_res_users_first")
    second_level_user_ids = fields.Many2many("res.users", "res_company_res_users_second")
