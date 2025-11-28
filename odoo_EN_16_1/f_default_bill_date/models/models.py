# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class f_default_bill_date(models.Model):
#     _name = 'f_default_bill_date.f_default_bill_date'
#     _description = 'f_default_bill_date.f_default_bill_date'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
