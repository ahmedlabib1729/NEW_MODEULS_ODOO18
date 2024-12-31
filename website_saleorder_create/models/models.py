# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class website_saleorder_create(models.Model):
#     _name = 'website_saleorder_create.website_saleorder_create'
#     _description = 'website_saleorder_create.website_saleorder_create'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

