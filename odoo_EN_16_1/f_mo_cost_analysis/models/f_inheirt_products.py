
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class f_product_bussnis_(models.Model):
    _name = 'f.bussniess.purpose'
    _rec_name = 'f_name'
    
    f_name = fields.Char(string='Business Purpose')



class f_inheritproduct_bussnis(models.Model):
    _inherit = 'product.template'
    
    
    f_bussniess_purop = fields.Many2one('f.bussniess.purpose',string='Business Purpose')