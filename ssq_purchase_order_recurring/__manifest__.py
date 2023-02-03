{
    "name": "Purchase Order Recurring",
    "summary": """
        Create recurring purchase orders for your regular vendors
    """,
    "description": """
        Create recurring purchase orders for your regular vendors
    """,
    "author": "Sanesquare Technologies",
    "website": "https://www.sanesquare.com/",
    "support": "odoo@sanesquare.com",
    "license": "AGPL-3",
    "category": "Purchase",
    "version": "16.0.1.0.1",
    "images": ["static/description/app_image.png"],
    "depends": ["base", "purchase"],
    "data": [
        "data/sequence.xml",
        "data/cron.xml",
        "security/security.xml",
        "views/purchase_views.xml",
    ],
    "external_dependencies": {"python": ["pandas"]},
}
