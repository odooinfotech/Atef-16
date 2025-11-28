from odoo import models, fields, api,_
from odoo.exceptions import UserError

class FConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    f_prevent_sell = fields.Boolean("Prevent sales if 0 or Negative Qtys",default= False)
    f_include_rese_sale = fields.Boolean("Include Reserved Qtys of product in sale orders",default= False)
    f_prevent_transfer = fields.Boolean("Prevent transfer if 0 or Negative Qtys",default= False)
    

    def set_values(self):
        super(FConfigSettings, self).set_values()
        config_parameters = self.env["ir.config_parameter"].sudo()

        for record in self:
            config_parameters.sudo().set_param("prevent_sell_negative_qty.f_prevent_sell", record.f_prevent_sell)
            config_parameters.sudo().set_param("prevent_sell_negative_qty.f_include_rese_sale", record.f_include_rese_sale)
            config_parameters.sudo().set_param("prevent_sell_negative_qty.f_prevent_transfer", record.f_prevent_transfer)
        
        
        

    def get_values(self):
        res = super(FConfigSettings, self).get_values()
        f_prevent_sell = self.env['ir.config_parameter'].sudo().get_param('prevent_sell_negative_qty.f_prevent_sell')
        f_include_rese_sale = self.env['ir.config_parameter'].sudo().get_param('prevent_sell_negative_qty.f_include_rese_sale')
        f_prevent_transfer = self.env['ir.config_parameter'].sudo().get_param('prevent_sell_negative_qty.f_prevent_transfer')
        res.update(
            f_prevent_sell = f_prevent_sell,
            f_include_rese_sale = f_include_rese_sale,
            f_prevent_transfer = f_prevent_transfer,
            
        )
        
        return res
    

