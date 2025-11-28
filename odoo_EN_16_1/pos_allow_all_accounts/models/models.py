from odoo import models, fields, api

class pos_allow_all_accounts(models.Model):
    
    _inherit= 'pos.payment.method'
    
    #Remove the Domain from the field Definition 
    receivable_account_id = fields.Many2one('account.account',
        string='Intermediary Account',
        required=True,
        domain=[],
        ondelete='restrict',
        help='Account used as counterpart of the income account in the accounting entry representing the pos sales.')