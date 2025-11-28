from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit='res.config.settings'
    
    
    f_mrp_location =fields.Many2one('stock.location',string="Manufacturing Default Location")
    
 
 

    def set_values(self):
    
        super(ResConfigSettings, self).set_values()
        config_parameters = self.env["ir.config_parameter"].sudo()
    
        f_mrp_location =self.f_mrp_location
        print('f mrp',f_mrp_location)
        config_parameters.set_param('falak_manufacturing_planning.f_mrp_location',f_mrp_location.id)
    
    
    def get_values(self):
    
        res = super(ResConfigSettings, self).get_values()
        location= self.env["ir.config_parameter"].sudo().get_param('falak_manufacturing_planning.f_mrp_location') 
        
        
        print('------------------',location)
        res.update(f_mrp_location = int(location)
                    )
        

        return res
    
    
    #
