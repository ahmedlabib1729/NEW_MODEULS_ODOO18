
from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    vat_label = fields.Char(string="VAT Label")
    company_registry_label = fields.Char(
        string='Company Registry Label',
        help='This field is used to display a label for the company registry.'
    )
