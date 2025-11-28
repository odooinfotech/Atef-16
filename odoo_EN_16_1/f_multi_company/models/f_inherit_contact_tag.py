from odoo import models, api, fields

class FResPartnerCategoryInherit(models.Model):
    _inherit = "res.partner.category"
    

    
    company_id = fields.Many2one(
        'res.company', 'Company', index=1 ,default=lambda self: self.env.company.id)