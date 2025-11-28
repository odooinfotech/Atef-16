from odoo import models, fields, api, SUPERUSER_ID

class FAccountMoveInherit(models.Model):
    _inherit="account.move"

    f_visit = fields.Many2one("f.visits" ,string="Visit"  ,domain ="[('f_customer', '=', partner_id),('state', '!=','cancel')]")
    
#     @api.model
#     def action_post(self):
#         res = super(FAccountMoveInherit, self).action_post()
#         visit = self.env['f.visits'].with_user(SUPERUSER_ID).search([('id','=',self.f_visit.id)],limit=1)
#         print('visit',visit)
#         if visit:
#             visit.write({'f_invoice_total':visit.f_sales_total+self.amount_total_signed})
# 
#         return res