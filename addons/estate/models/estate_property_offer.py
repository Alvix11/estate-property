import datetime

from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"

    price = fields.Float()
    status = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        copy=False,
    )
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_date_deadline", inverse="_inverse_date_deadline"
    )

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            start_dt = record.create_date or fields.Datetime.now()
            date_deadline = start_dt + datetime.timedelta(days=record.validity or 0)
            record.date_deadline = date_deadline.date()

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline:
                start_dt = record.create_date or fields.Datetime.now()
                start_date = (
                    start_dt.date()
                    if isinstance(start_dt, datetime.datetime)
                    else start_dt
                )
                record.validity = (record.date_deadline - start_date).days
            else:
                record.validity = 0
    
    partner_id = fields.Many2one(
        "res.partner",
        string="Partner",
        required=True
        )
    property_id = fields.Many2one(
        "estate.property",
        string="Property",
        required=True
        )
