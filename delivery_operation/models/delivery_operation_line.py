from odoo import models, fields, api


class DeliveryOperationLine(models.Model):
    _name = 'delivery.operation.line'
    _description = 'Delivery Operation Line'

    operation_id = fields.Many2one('delivery.operation', string='Delivery Reference', required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Product', required=True)
    invoice_number = fields.Char(string='Invoice Number', required=True)
    customer_id = fields.Many2one('res.partner', string='Customer')
    mobile_from = fields.Char(string='Mobile From', )
    mobile_to = fields.Char(string='Mobile To', )
    city_from = fields.Many2one('delivery.city')
    city_to = fields.Many2one('delivery.city')
    driver_id = fields.Many2one('hr.employee', string='Driver')
    collection = fields.Float(string='Collection', required=True)
    price = fields.Float(string='Price', required=True)
