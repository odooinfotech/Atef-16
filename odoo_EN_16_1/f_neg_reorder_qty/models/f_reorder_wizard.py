# -*- coding: utf-8 -*-

from odoo import models, fields, api,_


class f_stock_reorder_qtys(models.Model):
    _name = 'f.stock.reorder.qtys'
    _description = "Stock Reorder"
    
    
    location_id= fields.Many2one('stock.location' ,domain= [('usage', '=', 'internal')],string='Location')
    
    
    def f_get_reorder_quant(self):

                    
        print("11111111111")
     
        action = {
            'name':_('Reording Qty'),
            'type': 'ir.actions.act_window',
            'view_mode': 'pivot,tree,form',
            'res_model': 'f.neg_reorder.qty.report',
            'domain':[('location_id', 'child_of', self.location_id.id)],
           
            }
        
        return action
