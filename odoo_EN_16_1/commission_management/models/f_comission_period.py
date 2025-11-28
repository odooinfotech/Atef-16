from odoo import models, fields, api


class FComissionPeriod(models.Model):
    _name = 'f.comisson.period'
    _rec_name = 'f_name'
    
    f_name = fields.Char(string = 'Name', required = True )
    f_from = fields.Date(string = 'From',required = True)
    f_to = fields.Date(string = 'To',required = True)
    f_colsed = fields.Boolean(string = 'Closed')