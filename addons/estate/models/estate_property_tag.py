from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Tag"
    _order = "name desc"
    _sql_constraints = [
        ("unique_name", "UNIQUE(name)",
        "The name must be unique.")
    ]
    
    name = fields.Char(required=True)
    color = fields.Integer()