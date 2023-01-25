{
    "name": "Whatsapp Message from Contacts",
    "summary": """
        Send Whatsapp messages directly from contacts module
    """,
    "description": """
       Send Whatsapp messages directly from contacts module
    """,
    "author": "Sanesquare Technologies",
    "website": "https://www.sanesquare.com/",
    "support": "odoo@sanesquare.com",
    "license": "AGPL-3",
    "category": "Contacts",
    "version": "16.0.1.0.1",
    "images": ["static/description/app_image.png"],
    "depends": ["base", "contacts"],
    "data": [
        "security/ir.model.access.csv",
        "views/res_partner_view.xml",
        "wizard/wizard_partner.xml",
    ],
}
