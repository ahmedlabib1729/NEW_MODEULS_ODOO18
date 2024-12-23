from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    company_registry_label = fields.Char(string="Company Registry Label")
