{
    "name": "Timesheet XLSX Report",
    "summary": """
            Timesheet XLSX Report
        """,
    "description": """
        This module can be used to generate xlsx report from timesheets.
    """,
    "author": "Sanesquare Technologies",
    "website": "https://www.sanesquare.com/",
    "support": "odoo@sanesquare.com",
    "license": "OPL-1",
    "category": "Uncategorized",
    "version": "16.0.1.0.1",
    "images": ["static/description/app_image.png"],
    "depends": ["base", "analytic", "hr_timesheet", "report_xlsx"],
    "data": [
        "report/report_timesheet.xml",
    ],
}
