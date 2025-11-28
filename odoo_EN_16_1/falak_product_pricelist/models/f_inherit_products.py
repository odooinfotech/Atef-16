# -*- coding: utf-8 -*-

from odoo import models, fields, api,_


class falak_product_pricelist(models.Model):
    _inherit = 'product.template'
    
    
    f_price1=fields.Float("Price 1")
    f_price2=fields.Float("Price 2")
    f_price3=fields.Float("Price 3")
    f_price4=fields.Float("Price 4")
    f_price5=fields.Float("Price 5")
 