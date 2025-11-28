# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class f_cash_flow_report(models.Model):
#     _name = 'f_cash_flow_report.f_cash_flow_report'
#     _description = 'f_cash_flow_report.f_cash_flow_report'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
