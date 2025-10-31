from odoo import Command, models
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _inherit = "estate.property"
    
    def action_set_sold(self):
        if self.state != "offer accepted":
            raise UserError(
                "You cannot sell the property if you have not accepted an offer.")
        
        self.env["account.move"].create({
            "partner_id": self.buyer_id.id,
            "move_type": "out_invoice",
            "invoice_line_ids": [
                Command.create({
                    "name": f"Sales commission for {self.name}",
                    "quantity": 1,
                    "price_unit": self.selling_price * 0.06
                }),
                Command.create({
                    "name": "Administrative expenses",
                    "quantity": 1,
                    "price_unit": 100
                })
            ]
        })
        
        return super().action_set_sold()