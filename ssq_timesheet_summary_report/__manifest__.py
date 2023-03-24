{
    "name": "Timesheet Summary Report",
    "summary": """
        Project-wise employee timesheet summary report
    """,
    "description": """
        Project-wise employee timesheet summary report
    """,
    "author": "Sanesquare Technologies",
    "website": "https://www.sanesquare.com/",
    "support": "odoo@sanesquare.com",
    "license": "AGPL-3",
    "category": "Project",
    "version": "16.0.1.0.1",
    "images": ["static/description/app_image.png"],
    "depends": ["project", "hr_timesheet", "report_xlsx"],
    "data": [
        "security/ir.model.access.csv",
        "wizard/project_summary_report_wizard_views.xml",
        "report/report_project_summary.xml",
    ],
}
