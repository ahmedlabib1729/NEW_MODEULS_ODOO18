from odoo import models, fields

class AccountPayment(models.Model):
    _inherit = 'account.payment'

    delivery_operation_received_id = fields.Many2one('delivery.operation', string="Delivery Received Operation")
    delivery_operation_send_id = fields.Many2one('delivery.operation', string="Delivery send Operation")
