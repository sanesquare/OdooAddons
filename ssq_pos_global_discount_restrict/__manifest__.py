{
    "name": "POS Global Discount Restriction",
    "summary": """Restrict Global Discount in each POS shop to selected employees.""",
    "description": """
        In Odoo Point of Sale, currently there are no restriction in the case of global discounts.
        This module will bring in a restriction in the case of global discounts. The employees who can apply the
        global discount should be selected in each POS shop configuration.
    """,
    "author": "Sanesquare Technologies",
    "website": "https://www.sanesquare.com/",
    "support": "odoo@sanesquare.com",
    "license": "OPL-1",
    "category": "Sales/Point of Sale",
    "version": "15.0.1.0.1",
    "depends": ["pos_hr", "pos_discount"],
    "images": ["static/description/pos_global_discount_restriction_v15.png"],
    "data": [
        "views/pos_config_view.xml",
    ],
    "assets": {
        "point_of_sale.assets": [
            "/ssq_pos_global_discount_restrict/static/src/js/DiscountButton.js",
        ],
    },
}
