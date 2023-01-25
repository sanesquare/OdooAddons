{
    "name": "Popup Message",
    "summary": """
        Generate Popup Message""",
    "description": """
        Generate Popup Message
    """,
    "author": "Sanesquare Technologies",
    "website": "https://www.sanesquare.com/",
    "support": "odoo@sanesquare.com",
    "license": "AGPL-3",
    "category": "Uncategorized",
    "images": ["static/description/app_image.png"],
    "version": "16.0.1.0.1",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "wizard/popup_views.xml",
        "test/test_view.xml",
    ],
}
