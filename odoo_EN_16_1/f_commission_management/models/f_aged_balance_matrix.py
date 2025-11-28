from odoo import models, fields, api, _


class FAgedBalanceMatrix(models.Model):
    _name = 'f.aged.balance.matrix'
    _description = 'Aged Balance Matrix'
    _rec_name = 'f_name'

    f_name = fields.Char(string='Name')
    f_bad_debt = fields.Integer(string='Aged Balance Period(Days)')
    f_matrix_line = fields.One2many('f.aged.balance.matrix.line', 'f_matrix_id', string='Matrix Line')
