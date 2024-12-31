from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_origin = fields.Char(string="Origin - المنشأ")

