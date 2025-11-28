# -*- coding: utf-8 -*-

from odoo import models, fields, api,_


class falak_product_pricelist_item(models.Model):
    _inherit = 'product.pricelist.item'
    
    base = fields.Selection(selection_add=[  ('f_price1', 'Price 1'),  ('f_price2', 'Price 2')
                                           ,  ('f_price3', 'Price 3'),  ('f_price4', 'Price 4')
                                           ,  ('f_price5', 'Price 5')], ondelete = {'f_price1': 'cascade','f_price2': 'cascade' ,'f_price3': 'cascade'
                                                                                                        ,'f_price4': 'cascade'
                                                                                                        ,'f_price5': 'cascade'
                                                                                                      })