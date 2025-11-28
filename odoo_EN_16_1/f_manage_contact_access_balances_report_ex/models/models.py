# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class f_manage_contact_access_balances_report_ex(models.Model):
#     _name = 'f_manage_contact_access_balances_report_ex.f_manage_contact_access_balances_report_ex'
#     _description = 'f_manage_contact_access_balances_report_ex.f_manage_contact_access_balances_report_ex'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
