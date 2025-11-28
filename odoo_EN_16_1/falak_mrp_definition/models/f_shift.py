from odoo import models, fields, api


class FShift(models.Model):
    _name ='f.shift'
    _rec_name='f_shift'
    _description = 'Shift Definition'
    
    f_shift =fields.Char(string="Shift")
    f_increment_num = fields.Integer(string="Number", default=lambda self: self.env['ir.sequence'].next_by_code('f.shift'))
