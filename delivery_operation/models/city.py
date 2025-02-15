from odoo import models, fields

class DeliveryCity(models.Model):
    _name = 'delivery.city'
    _description = 'Delivery City'

    name = fields.Char(string="City Name", required=True)
