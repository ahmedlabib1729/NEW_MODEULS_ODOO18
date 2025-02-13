from odoo import models, fields, api,_

class DeliveryOperation(models.Model):
    _name = 'delivery.operation'
    _inherit = ['mail.activity.mixin', 'mail.thread']
    _description = 'Delivery Operation'
    _order = 'name desc'

    name = fields.Char(string='Sequence', required=True, copy=False, readonly=True, default='New')
    date = fields.Date(string='Date', required=True, default=fields.Date.today)
    customer_id = fields.Many2one('res.partner', string='Customer', required=True,copy=True)
    line_ids = fields.One2many('delivery.operation.line', 'operation_id', string='Operation Lines',copy=True)
    status = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirmed')
    ], string='Status', default='draft', required=True,copy=False,tracking=True)
    is_invoice = fields.Boolean(default=False,copy=False)
    total_amount_received = fields.Float()
    total_amount_send = fields.Float()
    total_collection = fields.Float(compute='calc_total_collection',store=True)

    @api.depends('line_ids.collection')
    def calc_total_collection(self):
        for r in self:
            r.total_collection = sum(r.line_ids.mapped('collection'))
    total_price = fields.Float(compute='calc_total_price',store=True)

    @api.depends('line_ids.price')
    def calc_total_price(self):
        for r in self:
            r.total_price = sum(r.line_ids.mapped('price'))

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('delivery.operation') or 'New'
        return super(DeliveryOperation, self).create(vals)


    def action_confirm(self):
        """Set status to Confirmed"""
        self.write({'status': 'confirm'})
    def reset_to_draft(self):
        """Set status to Confirmed"""
        self.write({'status': 'draft'})

    def action_create_invoice(self):
        """Create an invoice with total price of lines"""
        invoice_vals = {
            'partner_id': self.customer_id.id,
            'move_type': 'out_invoice',
            'delivery_operation_id': self.id,
            'invoice_line_ids': [],
        }

        total_price = 0
        for line in self.line_ids:
            invoice_vals['invoice_line_ids'].append((0, 0, {
                # 'product_id': line.product_id.id,
                'name': line.product_id.name,
                'quantity': 1,
                'price_unit': line.price,
            }))
            total_price += line.price

        if not invoice_vals['invoice_line_ids']:
            raise ValueError("No lines to invoice")

        invoice = self.env['account.move'].create(invoice_vals)
        self.is_invoice = True
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': invoice.id,
            'target': 'current',
        }

    received = fields.Integer(string="Received", compute="_compute_payment_count")

    def _compute_payment_count(self):
        for record in self:
            record.received = self.env['account.payment'].search_count([('delivery_operation_received_id', '=', record.id),('payment_type','=','inbound')])
    send = fields.Integer(string="Send", compute="_compute_send")

    def _compute_send(self):
        for record in self:
            record.send = self.env['account.payment'].search_count([('delivery_operation_send_id', '=', record.id),('payment_type','=','outbound')])

    def action_receive_payment(self):
        """Open Payment Wizard"""
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'delivery.operation.payment.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_delivery_operation_id': self.id, 'default_partner_id': self.customer_id.id,'default_type': 'received'}
        }
    def action_send_payment(self):
        """Open Payment Wizard"""
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'delivery.operation.payment.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_delivery_operation_id': self.id, 'default_partner_id': self.customer_id.id,'default_type': 'send'}
        }



    def action_view_invoice(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Invoices'),
            'res_model': 'account.move',
            'view_mode': 'list,form',
            'domain': [('delivery_operation_id', 'in', self.ids)],
        }

