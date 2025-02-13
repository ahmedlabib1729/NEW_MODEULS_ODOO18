from odoo import models, fields, api,_
from odoo.exceptions import ValidationError


class DeliveryOperationPaymentWizard(models.TransientModel):
    _name = 'delivery.operation.payment.wizard'
    _description = 'Payment Wizard for Delivery Operation'

    delivery_operation_id = fields.Many2one('delivery.operation', string="Delivery Operation", required=True)
    partner_id = fields.Many2one('res.partner', string="Customer", required=True)
    amount = fields.Float(string="Payment Amount", required=True)
    type = fields.Selection([('send','send'),('received','received')])


    journal_id = fields.Many2one(
        'account.journal', string="Journal",
        domain=[('type', '=', 'bank')])

    @api.constrains('amount')
    def _check_amount(self):
        for record in self:
            if self.type == 'received':
                operation = self.delivery_operation_id
                total_collection = sum(record.delivery_operation_id.line_ids.mapped('collection'))
                if record.amount + operation.total_amount_received > total_collection:
                    raise ValidationError("Payment amount cannot exceed the total collection amount.")
            elif self.type == 'send':
                operation = self.delivery_operation_id
                if record.amount > operation.total_amount_received:
                    raise ValidationError("Payment amount cannot exceed the total received amount.")

    def action_confirm_payment(self):
        """Create Payment Record"""
        operation = self.delivery_operation_id
        if self.type == 'received':
            payment_vals = {
                'partner_id': self.partner_id.id,
                'amount': self.amount,
                'payment_type': 'inbound',
                'partner_type': 'customer',
                'journal_id': self.journal_id.id,
                'delivery_operation_received_id': self.delivery_operation_id.id,
            }
            operation.total_amount_received += self.amount
            payment = self.env['account.payment'].create(payment_vals)
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'account.payment',
                'view_mode': 'form',
                'res_id': payment.id,
                'target': 'current',
            }
        elif self.type == 'send':
            payment_vals = {
                'partner_id': self.partner_id.id,
                'amount': self.amount,
                'payment_type': 'outbound',
                'partner_type': 'customer',
                'journal_id': self.journal_id.id,
                'delivery_operation_send_id': self.delivery_operation_id.id,
            }
            operation.total_amount_send += self.amount
            payment = self.env['account.payment'].create(payment_vals)
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'account.payment',
                'view_mode': 'form',
                'res_id': payment.id,
                'target': 'current',
            }


