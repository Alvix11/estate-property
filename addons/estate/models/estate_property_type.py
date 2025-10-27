from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"
    _order = "name desc"
    _sql_constraints = [
        ("unique_name", "UNIQUE(name)",
        "The name must be unique.")
    ]
    
    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")