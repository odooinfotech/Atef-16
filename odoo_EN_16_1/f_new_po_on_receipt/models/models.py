# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class f_new_po_on_receipt(models.Model):
#     _name = 'f_new_po_on_receipt.f_new_po_on_receipt'
#     _description = 'f_new_po_on_receipt.f_new_po_on_receipt'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
