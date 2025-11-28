# -*- coding: utf-8 -*-

from odoo import models, fields, api

class F_res_city_Inherit(models.Model):
    _inherit = 'res.country'

    f_shipping_period = fields.Integer(string="Shipping Period", default=0)

