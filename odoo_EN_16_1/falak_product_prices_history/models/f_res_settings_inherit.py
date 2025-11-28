from odoo import models, fields, api, _


class F_Config_Settings(models.TransientModel):
    _inherit = 'res.config.settings'
    
  
   
    f_sale_history = fields.Boolean(string = "Sale History")
    f_purchase_history = fields.Boolean(string = "Purchase History")
    f_product_history = fields.Boolean(string = "Product Sale History")
    f_product_purchase_history = fields.Boolean(string="Product Purchase History")
    f_invoice_history = fields.Boolean(string = "Invoice History")
    f_credit_note_history = fields.Boolean(string = "Credit Note History")
    
    
    def set_values(self):
    
        super(F_Config_Settings, self).set_values()
        config_parameters = self.env["ir.config_parameter"].sudo()
    
        f_sale_history = self.f_sale_history
        f_purchase_history = self.f_purchase_history
        f_product_history = self.f_product_history
        f_product_purchase_history = self.f_product_purchase_history
        f_invoice_history = self.f_invoice_history
        f_credit_note_history = self.f_credit_note_history
        
        config_parameters.sudo().set_param('falak_product_prices_history.f_sale_history', f_sale_history)
        config_parameters.sudo().set_param('falak_product_prices_history.f_purchase_history', f_purchase_history)
        config_parameters.sudo().set_param('falak_product_prices_history.f_product_history', f_product_history)
        config_parameters.sudo().set_param('falak_product_prices_history.f_product_purchase_history', f_product_purchase_history)
        config_parameters.sudo().set_param('falak_product_prices_history.f_invoice_history', f_invoice_history)
        config_parameters.sudo().set_param('falak_product_prices_history.f_credit_note_history', f_credit_note_history)
 
    def get_values(self):
    
        res = super(F_Config_Settings, self).get_values()
     
        res.update(
            
            f_sale_history = self.env["ir.config_parameter"].sudo().get_param('falak_product_prices_history.f_sale_history') ,
            f_purchase_history = self.env["ir.config_parameter"].sudo().get_param('falak_product_prices_history.f_purchase_history') ,
            f_product_history = self.env["ir.config_parameter"].sudo().get_param('falak_product_prices_history.f_product_history') ,
            f_product_purchase_history=self.env["ir.config_parameter"].sudo().get_param('falak_product_prices_history.f_product_purchase_history'),
            f_invoice_history = self.env["ir.config_parameter"].sudo().get_param('falak_product_prices_history.f_invoice_history') ,
            f_credit_note_history = self.env["ir.config_parameter"].sudo().get_param('falak_product_prices_history.f_credit_note_history') 
            
           
            )
        print('res',res)
        return res