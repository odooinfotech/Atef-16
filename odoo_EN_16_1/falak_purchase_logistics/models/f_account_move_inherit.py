from odoo import models, fields, api

class FAccountMoveInherit(models.Model):
    _inherit ='account.move'


    f_bill_ref = fields.Char('Bill Reference')
    
