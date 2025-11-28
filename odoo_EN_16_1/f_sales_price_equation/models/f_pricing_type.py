from odoo import models, fields, api, _


class FPricingType(models.Model):
    _name = 'f.pricing.type'
    _description = 'Pricing Type'
    _rec_name = 'f_name'

    f_name = fields.Char(string='name')