from datetime import datetime

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char(required=True)
    description = fields.Text()
    post_code = fields.Char()
    date_availability = fields.Date(
        copy=False, 
        default=lambda self: datetime.today() + relativedelta(months=3)
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ]
    )
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer received", "Offer Received"),
            ("offer accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        required=True,
        copy=False,
        default="new",
    )
    active = fields.Boolean(default=True)
    property_type_id = fields.Many2one(
        "estate.property.type", 
        string="Property types"
    )
    salesman_id = fields.Many2one(
        "res.users",
        string="Salesperson",
        index=True,
        default=lambda self: self.env.user,
    )
    buyer_id = fields.Many2one(
        "res.partner",
        string="Buyer",
        index=True,
        copy=False
    )
    tag_ids = fields.Many2many(
        "estate.property.tag",
        string="Property Tags"
    )
    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_id",
        string="Property Offers"
    )
    total_area = fields.Char(compute="_compute_total_area")
    
    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            total = record.living_area + record.garden_area
            record.total_area = total
