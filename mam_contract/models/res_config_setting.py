from odoo import fields, models, api


class Account_move(models.Model):
    _inherit = 'account.move'

    mam_batch_id = fields.Many2one('contract.batch')


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    mam_contract_product_id = fields.Many2one('product.product',config_parameter='mam_contract.mam_contract_product_id', readonly=False)
    mam_contract_journal_id = fields.Many2one('account.journal',config_parameter='mam_contract.mam_contract_journal_id', readonly=False)
