from odoo import models, fields, api, _


class F_Account_Move_Line_Inherit(models.Model):
    _inherit = 'account.move.line'
    
    f_can_edit_price =fields.Boolean(compute="can_edit",string="Can Edit Price")
    
    @api.onchange('product_id')
    def can_edit(self):
        self.f_can_edit_price=False
        
        f_restrict_price  = self.env['ir.config_parameter'].sudo().get_param('price_access_management.f_restrict_price')
        f_user_has_access = self.env.user.has_group('price_access_management.f_can_edit_invoices')
        print('f_restrict_price',f_restrict_price)

        print('f_user_has_access',f_user_has_access)

        if f_restrict_price and f_user_has_access:
            
            self.f_can_edit_price=True
            
        elif not f_restrict_price :
            
            self.f_can_edit_price=True
