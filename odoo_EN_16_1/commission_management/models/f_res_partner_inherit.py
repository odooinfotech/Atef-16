from odoo import models, fields, api,_


class FResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    f_customer_type = fields.Selection([('retail','Retail'),('whole','Whole Sale')],default ='whole',required = True,string = 'Customer Type')
    f_bad_debt    = fields.Boolean('Bad Debt',default=False)