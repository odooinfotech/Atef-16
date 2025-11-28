from odoo import models, tools, api, fields,_

class FIinheritsale_order(models.Model):
    _inherit = "sale.order"
    
    company_currency_id = fields.Many2one('res.currency',related='company_id.currency_id')
    
    f_balance = fields.Monetary(related="partner_id.f_balance",currency_field='company_currency_id')