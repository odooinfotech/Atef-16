from odoo import models, fields, api


class FAccountPaymentInherit(models.Model):
    _inherit = 'account.payment'
    
    f_cust_type = fields.Selection(related ='partner_id.f_customer_type',store = True)
    #f_sale_person = fields.Many2one(related = 'partner_id.user_id',store=True)
    f_commission_exclude = fields.Boolean(string='Exclude Commission', default=False)
    f_commission_note = fields.Text(string='Notes')
