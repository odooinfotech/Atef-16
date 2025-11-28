from odoo import models, api, fields

class Fproductcategorynherit(models.Model):
    _inherit = "product.category"
    
    
    name = fields.Char('Name', index='trigram', required=True, company_dependent=True)
    

    
