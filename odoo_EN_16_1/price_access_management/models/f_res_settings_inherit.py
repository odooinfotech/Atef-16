from odoo import models, fields, api, _


class FConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
  
   
    f_restrict_price = fields.Boolean(string = "Restrict Price Editing",store=True)
    #f_prevent_access =fields.Char(string="Prevent Access",store=True,compute='set_values')
    
    
    def set_values(self):
    
        super(FConfigSettings, self).set_values()
        config_parameters = self.env["ir.config_parameter"].sudo()
    
        f_restrict_price =self.f_restrict_price
        config_parameters.set_param('price_access_management.f_restrict_price',f_restrict_price)
          
          
    def get_values(self):
    
        res = super(FConfigSettings, self).get_values()
    
        res.update(
            
            f_restrict_price=self.env["ir.config_parameter"].sudo().get_param('price_access_management.f_restrict_price')    
        )
    
        return res
    