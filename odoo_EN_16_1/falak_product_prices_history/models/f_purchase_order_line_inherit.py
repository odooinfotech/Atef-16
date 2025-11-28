# -*- coding: utf-8 -*-
from odoo import models, fields, api, _,tools
from datetime import date,datetime

class F_Purchase_Order_Line_Inherit(models.Model):
    _inherit = 'purchase.order.line'
    
    f_purchase_history = fields.Boolean(string = "Purchase History",compute='_compute_purchase_history_access',readonly=True)
    
    def f_open_price_history(self):
     

        tools.drop_view_if_exists(self.env.cr, 'f_purchase_order_line_price_history_po')
        self.env.cr.execute('''
            CREATE or REPLACE VIEW f_purchase_order_line_price_history_po AS (
                    SELECT %s
                    FROM %s
                    WHERE %s
            )''' % (self._f_select_bill_query(),self._f_from_bill_query(),self._f_where_bill_query())
        )
        
        res = {
                'type': 'ir.actions.act_window',
                'name':'Price history',
                'target': 'new',
                'view_mode': 'tree',
                'res_model': 'f.purchase.order.line.price.history.po',
                'view_id': self.env.ref('falak_product_prices_history.f_purchase_order_line_price_history_view_tree').id,
                'context': {
                    'search_default_partner_id_filter':1,
                    
                }
                
            }  
    
    
        return res
    

    def _f_select_bill_query(self):
        return '''
            AML.ID AS ID,
            AML.ID AS purchase_order_line_id,
            %s AS f_purchase_order_line_id
        
        ''' % (self.id)
        
    def _f_from_bill_query(self):
        return '''
            ACCOUNT_MOVE_LINE AML
            INNER JOIN ACCOUNT_MOVE AM ON AML.MOVE_ID = AM.ID
        '''
    
    def _f_where_bill_query(self):
        return ''' 
            AML.PRODUCT_ID = %s
            AND AM.MOVE_TYPE = 'in_invoice'
            AND AML.DISPLAY_TYPE = 'product'
            AND AM.STATE = 'posted'
        ''' % (self.product_id.id)

        
    def _compute_purchase_history_access(self):
        self.f_purchase_history = self.env["ir.config_parameter"].sudo().get_param('falak_product_prices_history.f_purchase_history') 
        
