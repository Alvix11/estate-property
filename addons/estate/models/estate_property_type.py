from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"
    _sql_constraints = [
        ("unique_name", "UNIQUE(name)",
        "The name must be unique.")
    ]
    
    name = fields.Char(required=True)