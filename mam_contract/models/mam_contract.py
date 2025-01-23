from odoo import models, fields, api


class mam_contract(models.Model):
    _name = 'mam.contract'
    _description = 'MAM Contract'

    name = fields.Char()
    date_from = fields.Date()
    date_to = fields.Date()
    no_employees = fields.Integer('NO. Of Employees')
    company_id = fields.Many2one('res.company',default=lambda self: self.env.company)
    partner_id = fields.Many2one('res.partner')
    batch_count = fields.Integer(compute='calc_batch_count')

    def calc_batch_count(self):
        for r in self:
            r.batch_count = self.env['contract.batch'].search_count([('contract_id','=',r.id)])

    def generate_batch(self):
        self.env['contract.batch'].create({
            'contract_id':self.id,
        })

    def action_view_batch(self):
        '''
        This function returns an action that displays the opportunities from partner.
        '''
        action = self.env['ir.actions.act_window']._for_xml_id('mam_contract.batch_contract_action')
        action['context'] = {'no_create':True}
        action['domain'] = [('contract_id', 'in', self.ids)]
        return action



