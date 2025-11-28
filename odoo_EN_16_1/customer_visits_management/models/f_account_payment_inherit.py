from odoo import models, fields, api, SUPERUSER_ID

class FAccountPaymentInherit(models.Model):
    _inherit="account.payment"

    f_visit = fields.Many2one("f.visits" ,string="Visit" ,domain ="[('f_customer', '=', partner_id),('state', '!=','cancel')]")
   
    
#     def action_post(self):
#         res = super(FAccountPaymentInherit, self).action_post()
#          
#         visit = self.env['f.visits'].with_user(SUPERUSER_ID).search([('id','=',self.f_visit.id)],limit=1)
#         print('visit.f_payments_total',visit.f_payments_total)
#         print('self.amount',self.amount)
#         
#         if visit:
#             visit.sudo().write({'f_payments_total':visit.f_payments_total+self.amount_company_currency_signed})
# 
#         return res


# class FMultiPaymentInherit(models.Model):
#     _inherit="f.multi.payments"
#
#     f_visit = fields.Many2one("f.visits" ,string="Visit")
#
#     def f_post_payment(self):
#         res = super(FMultiPaymentInherit, self).f_post_payment()
#          
#         visit = self.env['f.visits'].with_user(SUPERUSER_ID).search([('id','=',self.f_visit.id)],limit=1)
#         print('visit.f_payments_total',visit.f_payments_total)
#         print('self.f_payment_total',self.f_payment_total)
#         
#         if visit:
#             visit.sudo().write({'f_payments_total':visit.f_payments_total+self.f_payment_total})
# 
#         return res
            
            
