
from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    vat_label = fields.Char(string="VAT Label")
