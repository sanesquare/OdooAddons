{
    "name": "POS Global Discount Limit",
    "summary": """Limit Global Discount % in each POS Shop""",
    "description": """
        In Odoo POS, currently there are no restriction in the case of global discounts limits.
        Bring a new field in POS shop configuration where the administrator can set a limit above which
        no employee/user should be able to apply Global Discount.
    """,
    "author": "Sanesquare Technologies",
    "website": "https://www.sanesquare.com/",
    "support": "odoo@sanesquare.com",
    "license": "OPL-1",
    "category": "Sales/Point of Sale",
    "version": "15.0.1.0.1",
    "depends": ["pos_discount"],
    "images": ["static/description/pos_global_discount_limit_v15.png"],
    "assets": {
        "point_of_sale.assets": [
            "/ssq_pos_global_discount_limit/static/src/js/DiscountButton.js",
        ],
    },
    "data": [
        "views/pos_config_view.xml",
    ],
}
