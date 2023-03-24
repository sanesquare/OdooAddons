from odoo import fields, models


class ProjectSummaryReportWizard(models.TransientModel):
    _name = "wizard.project.summary.report"

    project_ids = fields.Many2many("project.project", string="Select Projects")
    employee_ids = fields.Many2many("hr.employee", string="Select Employees")

    def print(self):
        return self.env.ref("ssq_timesheet_summary_report.project_summary_report").report_action(self)
