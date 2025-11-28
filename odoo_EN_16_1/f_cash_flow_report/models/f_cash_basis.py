from odoo import models, tools, api, fields



class FaccountMove(models.Model):
    _inherit = 'account.account'
    

    f_cash_basis = fields.Many2one("f.cash.basis" , 'Cash Basis')
    
    
class Fcashbasis(models.Model):
    _name='f.cash.basis'
    _rec_name = "name"
    _description = 'Cash Basis'
    name = fields.Char("Name")
    is_checks=fields.Boolean("Is Checks")


    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'Name must be unique!'),]