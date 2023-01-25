{
    "name": "Create Purchase from Sale",
    "summary": """
        Create purchase order directly from a sale order""",
    "description": """
        Create purchase order directly from a sale order
    """,
    "author": "Sanesquare Private Limited",
    "website": "https://www.sanesquare.com/",
    "support": "odoo@sanesquare.com",
    "license": "AGPL-3",
    "category": "Sale",
    "images": ["static/description/app_image.png"],
    "version": "16.0.1.0.1",
    "depends": ["base", "sale_management", "purchase"],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/views.xml",
        "wizard/create_purchase_order_view.xml",
    ],
}
