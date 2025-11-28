from odoo import models, fields, api, _


class FAgedBalanceMatrixLine(models.Model):
    _name = 'f.aged.balance.matrix.line'
    _description = 'Aged Balance Matrix Line'
    _rec_name = 'f_commission_percent'

    f_matrix_id = fields.Many2one('f.aged.balance.matrix', string='Matrix')
    f_operator = fields.Selection([('between', 'Between'), ('less', 'Less'), ('great', 'greater')], string='Operator')
    f_from_value = fields.Float(string='From')
    f_to_value = fields.Float(string='To')
    f_commission_percent = fields.Float(string='Commission Percent')