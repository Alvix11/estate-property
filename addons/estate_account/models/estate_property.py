from odoo import models
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _inherit = "estate.property"
    
    def action_set_sold(self):
        if self.state != "offer accepted":
            raise UserError("No puedes venderla si no has aceptado una oferta")
        
        return super().action_set_sold()