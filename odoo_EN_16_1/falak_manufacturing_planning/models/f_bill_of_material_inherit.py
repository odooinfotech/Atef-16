from odoo import models, fields, api


class F_Bill_Of_Material_Inherit(models.Model):
    _inherit='mrp.bom'
    
    
    f_default_bom =fields.Boolean(string="Default Bill Of Material")