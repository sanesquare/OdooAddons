{
    "name": "HR Recruitment - Applicant Experience",
    "summary": """
        Option to add applicant experience
    """,
    "description": """
        Option to add application date.
        Option to add applicant experience as on application date.
        Auto updation of current experience based on the experience specified in the application date.
    """,
    "author": "Sanesquare Technologies",
    "website": "https://www.sanesquare.com/",
    "support": "odoo@sanesquare.com",
    "license": "AGPL-3",
    "category": "Recruitment",
    "version": "16.0.1.0.1",
    "images": ["static/description/app_image.png"],
    "depends": ["hr_recruitment"],
    "data": [
        "data/cron.xml",
        "views/recruitment_views.xml",
    ],
}
