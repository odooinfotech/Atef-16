from odoo import models, tools, api, fields,_



class FIjournalentryline(models.Model):
    _inherit = "account.move.line"
    
    f_balance = fields.Monetary(related="partner_id.f_balance",currency_field='company_currency_id')


class FIinheritaccountmove(models.Model):
    _inherit = "account.move"
    
    
    
    
    f_balance = fields.Monetary(related="partner_id.f_balance",currency_field='company_currency_id')
