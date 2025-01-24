from odoo import fields, models, api,_


class ContractBatch(models.Model):
    _name = 'contract.batch'
    _description = 'Contract Batch'

    name = fields.Char(readonly=True)
    contract_id  = fields.Many2one('mam.contract')
    partner_id = fields.Many2one('res.partner',related='contract_id.partner_id',store=True)
    line_ids = fields.One2many('contract.batch.line','batch_id')
    state = fields.Selection([('draft','Draft'),('posted','Posted')],default='draft')
    total = fields.Float(compute='calc_total',store=True)
    invoice_count = fields.Integer(compute='calc_invoice_count')

    @api.depends('line_ids.total')
    def calc_total(self):
        for r in self:
           r.total = sum(self.line_ids.mapped('total'))

    @api.model
    def create(self, vals):
        res = super(ContractBatch, self).create(vals)
        res.name = self.env['ir.sequence'].next_by_code('batch.contract.seq')
        return res

    def confirm(self):
        config_param_sudo = self.env["ir.config_parameter"].sudo()
        product = int(config_param_sudo.get_param("mam_contract.mam_contract_product_id"))
        journal = int(config_param_sudo.get_param("mam_contract.mam_contract_journal_id"))
        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.partner_id.id,
            'journal_id': journal,
            'mam_batch_id':self.id,
            'invoice_line_ids': [(0, 0, {
                'product_id': product,
                'quantity': 1,
                'price_unit': self.total,
            })],
        })

        self.state = 'posted'

    def calc_invoice_count(self):
        for r in self:
            r.invoice_count = self.env['account.move'].search_count([('mam_batch_id','=',r.id)])


    def action_view_invoice(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Invoices'),
            'res_model': 'account.move',
            'view_mode': 'list,form',
            'domain': [('mam_batch_id', 'in', self.ids)],
        }







class ContractBatchLine(models.Model):
    _name = 'contract.batch.line'
    _description = 'Contract Batch Line'

    batch_id = fields.Many2one('contract.batch')
    employee_id = fields.Many2one('hr.employee')
    days = fields.Float()
    day_rate = fields.Float()
    hours = fields.Float()
    hour_rate = fields.Float()
    total = fields.Float(compute='calc_total',store=True)

    @api.depends('days','day_rate','hours','hour_rate')
    def calc_total(self):
        for r in self:
            r.total = (r.days * r.day_rate) + (r.hours * r.hour_rate)

