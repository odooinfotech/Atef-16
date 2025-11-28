# -*- coding: utf-8 -*-

from odoo import models, fields, api

class FPricingEquation(models.Model):
    _name = 'f.pricing.equation'
    _description = 'Pricing Equation Model'
    _rec_name = 'f_name'

    f_name = fields.Char(string='Name')
    f_factor = fields.Float(string='Factor')
