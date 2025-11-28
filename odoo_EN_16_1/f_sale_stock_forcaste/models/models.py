# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class f_sale_stock_forcaste(models.Model):
#     _name = 'f_sale_stock_forcaste.f_sale_stock_forcaste'
#     _description = 'f_sale_stock_forcaste.f_sale_stock_forcaste'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
