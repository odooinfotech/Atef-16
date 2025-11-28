from odoo import models, api, fields

class Fproductnherit(models.Model):
    _inherit = "product.template"
    

    
    company_id = fields.Many2one(
        'res.company', 'Company', index=1 ,default=lambda self: self.env.company.id)