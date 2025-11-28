from odoo import models, api, fields

class FResPartnerInherit(models.Model):
    _inherit = "res.partner"
    

    
    def set_default_comp(self):
         company_id = False
         print('self.ref_company_ids',self.ref_company_ids,self._context.get('default_is_company'),self._context)
         if self._context.get('default_is_company'):
                 company_id = self.env.company.id
                 self.company_id = company_id
                 return company_id
         

    
    company_id = fields.Many2one(
        'res.company', 'Company', index=1 ,default=set_default_comp)