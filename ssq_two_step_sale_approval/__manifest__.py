{
    "name": "Two Step Sale Approval",
    "summary": """
        Two level approval for sale orders before order confirmation.
    """,
    "description": """
        Two level approval for sale orders before order confirmation.
    """,
    "author": "Sanesquare Technologies",
    "website": "https://www.sanesquare.com/",
    "support": "odoo@sanesquare.com",
    "license": "AGPL-3",
    "category": "Sale",
    "version": "16.0.1.0.1",
    "images": ["static/description/app_image.png"],
    "depends": ["base", "sale_management"],
    "data": [
        "views/sale_views.xml",
        "views/res_config_views.xml",
    ],
}
