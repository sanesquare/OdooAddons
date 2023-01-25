{
    "name": "Customer Sequence Number",
    "summary": """
        This module can be used to generate unique sequence number for customers.
    """,
    "description": """
        This module can be used to generate unique sequence number for customers.
    """,
    "author": "Sanesquare Technologies",
    "website": "https://www.sanesquare.com/",
    "support": "odoo@sanesquare.com",
    "license": "AGPL-3",
    "category": "Uncategorized",
    "images": ["static/description/app_image.png"],
    "version": "16.0.1.0.1",
    "depends": ["base", "contacts", "base_setup"],
    "data": [
        "data/data.xml",
        "views/partner_views.xml",
        "views/res_config_views.xml",
    ],
}
