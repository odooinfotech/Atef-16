from odoo import models, fields, api, _


class FProdIdentity(models.Model):
    _name = 'f.prod.identity'
    _description = "Product Identity"
    _rec_name = 'fprodidentity_name'

    fprodidentity_name = fields.Char(string='Product Identity Name')
