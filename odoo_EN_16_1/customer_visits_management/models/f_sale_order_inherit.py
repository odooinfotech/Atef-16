from odoo import models, fields, api, SUPERUSER_ID

class FSaleOrderInherit(models.Model):
    _inherit="sale.order"

    f_visit = fields.Many2one("f.visits" ,string="Visit", domain ="[('f_customer', '=', partner_id),('state', '!=','cancel')]")
#     
#     def action_confirm(self):
#         res = super(FSaleOrderInherit, self).action_confirm()
#          
#         visit = self.env['f.visits'].with_user(SUPERUSER_ID).search([('id','=',self.f_visit.id)],limit=1)
#         print('visit',visit)
#         print('self.amount_total',self.amount_total)
#         if visit:
#             visit.sudo().write({'f_sales_total':visit.f_sales_total+self.amount_total})
# 
#         return res
            
