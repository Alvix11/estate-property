{
    "name": "estate",
    "version": "1.0",
    "author": "Alvix.exe",
    "license": "LGPL-3",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "views/estate_property_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_property_offer_views.xml",
        "views/estate_property_type_views.xml",
        "views/res_users.xml",
        "report/estate_property_templates.xml",
        "report/estate_property_reports.xml",
        "views/estate_menus.xml",
    ],
    "demo": [
        "data/estate_demo.xml"
    ],
    "application": True,
    "installable": True,
}