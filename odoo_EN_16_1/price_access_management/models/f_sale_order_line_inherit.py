from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError



class F_Sale_Order_Line_Inherit(models.Model):
    _inherit = 'sale.order.line'
#     
  #  f_price_unit = fields.Float(compute='get_price_unit' , string = 'Unit Price')
    f_can_edit_price =fields.Boolean(related="order_id.f_can_edit_price")
    f_can_readonly_price =fields.Boolean(related="order_id.f_can_readonly_price")
    f_enable_restrict =fields.Boolean(related="order_id.f_enable_restrict")
    
#     @api.onchange('price_unit')
#     def get_price_unit (self):
#         for rec in self :
#             rec.f_price_unit = rec.price_unit
        


class F_Sale_Order_Inherit(models.Model):
    _inherit = 'sale.order'
    
    
    def f_get_stateedit(self):
        self.f_can_edit_price=False
         
        f_restrict_price  = self.env['ir.config_parameter'].sudo().get_param('price_access_management.f_restrict_price')
        f_user_has_access = self.env.user.has_group('price_access_management.f_can_edit_sales')
        print('f_restrict_price',f_restrict_price,'f_user_has_access',f_user_has_access) 
 
 
        if f_restrict_price and f_user_has_access:
             
            return True
             
        elif not f_restrict_price :
             
            return True
        
        return False
            
            
    
        
    def f_get_stateread(self):
        
        self.f_can_readonly_price=False
         
        f_restrict_price  = self.env['ir.config_parameter'].sudo().get_param('price_access_management.f_restrict_price')
        f_user_readonly_has_access = self.env.user.has_group('price_access_management.f_readonly_sales_prices')
 
            
        if f_restrict_price and f_user_readonly_has_access:
             
            return True
             
        elif not f_restrict_price :
             
            return True
        return False
      
            
            
    def f_get_retrict_state(self):
        f_restrict_price  = self.env['ir.config_parameter'].sudo().get_param('price_access_management.f_restrict_price')
        
        return f_restrict_price
            
        
    f_can_edit_price =fields.Boolean(string="Can Edit Price",default=f_get_stateedit,copy=False,compute='can_edit')
    f_can_readonly_price =fields.Boolean(string="Can ReadOnly Price",default=f_get_stateread,copy=False,compute='can_edit')
    f_enable_restrict = fields.Boolean(string="Enable Restrict Price",default=f_get_retrict_state,copy=False,compute='can_edit')
     
#     
    def can_edit(self):
        print("11111111111 PRICE ACCESS")
        self.f_can_edit_price=False
        self.f_can_readonly_price=False
        self.f_enable_restrict= False
          
        f_restrict_price  = self.env['ir.config_parameter'].sudo().get_param('price_access_management.f_restrict_price')
        f_user_has_access = self.env.user.has_group('price_access_management.f_can_edit_sales')
        f_user_readonly_has_access = self.env.user.has_group('price_access_management.f_readonly_sales_prices')
  
        if f_restrict_price and f_user_has_access:
              
            self.f_can_edit_price=True
              
        elif not f_restrict_price :
              
            self.f_can_edit_price=True
             
             
        if f_restrict_price and f_user_readonly_has_access:
              
            self.f_can_readonly_price=True
              
        elif not f_restrict_price :
              
            self.f_can_readonly_price=True
            
            
        if f_restrict_price :
              
            self.f_enable_restrict=True
              
        elif not f_restrict_price :
              
            self.f_enable_restrict=False
#             
#             
   
#     
#     @api.onchange('price_unit')
#     def check_can_edit(self):
#         
#         print('self',self.product_uom,self._origin.product_uom)
#         
#         f_restrict_price = False
#         f_user_has_access  = False
#         
#         f_restrict_price  = self.env['ir.config_parameter'].sudo().get_param('price_access_management.f_restrict_price')
#         f_user_has_access = self.env.user.has_group('price_access_management.f_can_edit_sales')
#         
#         if self.product_uom.id == self._origin.product_uom.id :
#             if f_restrict_price and not f_user_has_access:
#                 
#                 raise UserError('تعديل السعر غير مسموح ')
#             
            
            