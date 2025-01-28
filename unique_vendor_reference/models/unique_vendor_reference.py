from odoo import models, api
from odoo.exceptions import ValidationError

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.constrains('partner_ref')
    def _check_unique_partner_reference(self):
        for order in self:
            if order.partner_ref:
                existing_orders = self.search([
                    ('partner_ref', '=', order.partner_ref),
                    ('id', '!=', order.id)
                ])
                if existing_orders:
                    raise ValidationError(f"Vendor Reference '{order.partner_ref}' is already used in another Purchase Order!")
