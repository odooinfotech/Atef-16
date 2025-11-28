from odoo import models, fields, api,_

class FAccountMoveLineInherit(models.Model):      
    _inherit = 'account.move.line'#
     
#     move_type_line = fields.Selection(related = 'move_id.move_type',store=True)
#     amount_total_signed_line = fields.Monetary(related = 'move_id.amount_total_signed',store=True)
#     
    f_sale_person = fields.Many2one(related = 'move_id.invoice_user_id',store=True)
    f_product_tmpl = fields.Many2one(related = 'product_id.product_tmpl_id',store=True)
    f_prod_family_id = fields.Many2one(related = 'product_id.product_tmpl_id.f_product_family',store=True)
    f_prod_identity_id = fields.Many2one(related = 'product_id.product_tmpl_id.fprodidentity',store=True)
    f_cust_type = fields.Selection(related ='partner_id.f_customer_type',store = True)
    f_bad_debt    = fields.Boolean(related ='partner_id.f_bad_debt',store = True)

 
# class FAccountMoveInherit(models.Model):
#     _inherit = 'account.move'
#
#     f_sale_person = fields.Many2one(related = 'partner_id.user_id',store=True)





