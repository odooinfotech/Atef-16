# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class f_location_qtys_cost_report(models.Model):
#     _name = 'f_location_qtys_cost_report.f_location_qtys_cost_report'
#     _description = 'f_location_qtys_cost_report.f_location_qtys_cost_report'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
