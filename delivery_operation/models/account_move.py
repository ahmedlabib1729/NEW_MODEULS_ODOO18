from odoo import models, fields

class AccountMove(models.Model):
    _inherit = 'account.move'

    delivery_operation_id = fields.Many2one('delivery.operation', string="Delivery Operation")
