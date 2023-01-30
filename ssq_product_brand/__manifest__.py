{
    "name": "Product Brand",
    "summary": """
        Create brands and select brand on product.
    """,
    "description": """
        Create brands and select brand on product.
    """,
    "author": "Sanesquare Technologies",
    "website": "https://www.sanesquare.com/",
    "support": "odoo@sanesquare.com",
    "license": "AGPL-3",
    "category": "Product",
    "version": "16.0.1.0.1",
    "images": ["static/description/app_image.png"],
    "depends": ["base", "product"],
    "data": [
        "security/ir.model.access.csv",
        "views/brand_views.xml",
        "views/product_views.xml",
    ],
}
