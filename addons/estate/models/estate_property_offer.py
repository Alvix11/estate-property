import datetime

from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"
    _sql_constraints = [
        (
            "check_price",
            "CHECK(price > 0)",
            "The expected price must be strictly positive.",
        ),
    ]

    price = fields.Float(required=True)
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

    def action_set_status_accepted(self):
        self.ensure_one()
        if self.property_id and self.property_id.selling_price == self.price:
            self.status = "accepted"
            return
        
        if self.property_id.selling_price:
            raise UserError("To accept this offer, you must refuse the other one.")
        
        self.property_id.write(
                {
                    "selling_price": self.price,
                    "buyer_id": self.partner_id
                }
        )
        self.status = "accepted"

    def action_set_status_refused(self):
        self.ensure_one()
        if self.status == "accepted" or (
            self.property_id and self.property_id.selling_price == self.price
        ):
            self.property_id.write(
                {
                    "selling_price": False,
                    "buyer_id": False,
                }
            )
        self.status = "refused"

    def unlink(self):
        self.ensure_one()
        if self.status == "accepted" or (
            self.property_id and self.property_id.selling_price == self.price
        ):
            self.property_id.write(
                {
                    "selling_price": False,
                    "buyer_id": False
                }
            )
        return super().unlink()

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

    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
