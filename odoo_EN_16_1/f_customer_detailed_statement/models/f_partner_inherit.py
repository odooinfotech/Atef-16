from odoo import fields, models, api, _,tools
from datetime import datetime,timedelta,date
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class FSPartnerInherit(models.Model):
    _inherit = "res.partner"
    
    def print_deatiledstatement(self):
        print("Sta111111111111111111")
         
        tree_id = False
        form_id = self.env.ref('f_customer_detailed_statement.view_customerdeatls_stat_form').id 
        ctx = {'default_partner_id': self.id,}
        action = {
            'name':_('Statement Report'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'f.detailed.customer',
            'context' : ctx,
             'target':'new',
        
            
            }
         
        return action
    
    

   
    
    
    
    
    
