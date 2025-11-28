from odoo import models, tools, api, fields,_

class FIinheritmultipay(models.Model):
    _inherit = "f.multi.payments"
    
    f_balance = fields.Monetary(related="f_partner_id.f_balance",currency_field='company_currency_id')