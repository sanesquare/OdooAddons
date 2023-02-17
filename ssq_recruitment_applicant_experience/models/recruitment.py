from odoo import models, fields, api
from dateutil import relativedelta

MONTH_SELECTION = [
    ("0", "0"),
    ("1", "1"),
    ("2", "2"),
    ("3", "3"),
    ("4", "4"),
    ("5", "5"),
    ("6", "6"),
    ("7", "7"),
    ("8", "8"),
    ("9", "9"),
    ("10", "10"),
    ("11", "11"),
]


class HrApplicant(models.Model):
    _inherit = "hr.applicant"

    date_application = fields.Date("Application Date", default=fields.Date.today(), required=True)
    year_experience = fields.Integer(help="Experience on the application date.")
    month_experience = fields.Selection(MONTH_SELECTION, default="0", required=True)
    current_year_experience = fields.Integer(
        store=True, compute="_compute_current_experience", help="Expected experience of the applicant till date."
    )
    current_month_experience = fields.Selection(MONTH_SELECTION, store=True, compute="_compute_current_experience")

    @api.depends("year_experience", "month_experience", "date_application")
    def _compute_current_experience(self):
        for applicant in self:
            application_date = applicant.date_application
            today = fields.Date.today()
            if application_date <= today:
                delta = relativedelta.relativedelta(today, application_date)
                total_years = applicant.year_experience + delta.years
                total_months = int(applicant.month_experience) + delta.months
                if total_months > 11:
                    total_years += 1
                    total_months = total_months % 12
                applicant.current_year_experience = total_years
                applicant.current_month_experience = str(total_months)

    @api.model
    def _update_applicant_experience(self):
        for applicant in self.env["hr.applicant"].search([]):
            applicant._compute_current_experience()

    @api.model
    def _compute_imported_applicant_experience(self):
        for applicant in self.env["hr.applicant"].search([("probability", ">", 0)]):
            experience = applicant.probability
            applicant.write(
                {
                    "year_experience": int(experience / 1),
                    "month_experience": str(experience).split(".")[1],
                    "probability": 0,
                }
            )
