from odoo import models
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _inherit = "estate.property"
    
    def action_set_sold(self):
        if self.state != "offer accepted":
            raise UserError("You cannot sell the property if you have not accepted an offer.")
        
        return super().action_set_sold()