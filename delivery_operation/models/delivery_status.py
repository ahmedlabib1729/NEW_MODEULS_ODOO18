from odoo import models, fields

class DeliveryStatus(models.Model):
    _name = 'delivery.status'
    _description = 'Delivery Status'

    name = fields.Char(string="Status Name", required=True)
