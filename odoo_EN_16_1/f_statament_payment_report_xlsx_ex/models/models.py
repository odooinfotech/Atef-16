# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class f_statament_payment_report_xlsx_ex(models.Model):
#     _name = 'f_statament_payment_report_xlsx_ex.f_statament_payment_report_xlsx_ex'
#     _description = 'f_statament_payment_report_xlsx_ex.f_statament_payment_report_xlsx_ex'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
