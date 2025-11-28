# -*- coding: utf-8 -*-
from odoo import models, fields, api, _,tools
from datetime import date,datetime

class F_Sale_Order_Line_Inherit(models.Model):
    _inherit = 'sale.order.line'
    
    f_sale_history = fields.Boolean(string = "Sale History",compute='_compute_sale_history_access',readonly=True)
    
    def f_open_price_history(self):
        
        print("/////////////////////////////////")
        tools.drop_view_if_exists(self.env.cr, 'f_sale_order_line_price_history_s')
        self.env.cr.execute('''
            CREATE or REPLACE VIEW f_sale_order_line_price_history_s AS (
                    SELECT %s
                    FROM %s
                    WHERE %s
                    UNION ALL
                    SELECT %s
                    FROM %s
                    WHERE %s
            )''' % (self._f_select_invoice_query(),self._f_from_invoice_query(),self._f_where_invoice_query(),self._f_select_legacy_query(),self._f_from_legacy_query(),self._f_where_legacy_query())
        )
        
        
        
        res = {
                'type': 'ir.actions.act_window',
                'name':'Price history',
                'target': 'new',
                'view_mode': 'tree',
                'res_model': 'f.sale.order.line.price.history.s',
                'view_id': self.env.ref('falak_product_prices_history.f_sale_order_line_price_history_view_tree').id,
                'context': {
                    'search_default_partner_id_filter':1,
                    
                    
                }
                
            }  
        
    
        return res
    
    
    def _f_select_invoice_query(self):
        return '''
            AML.ID AS ID,
            'invoice' AS SOURCE,
            %s AS F_SALE_ORDER_LINE_ID,
            AML.ID AS SOURCE_ORDER_LINE_ID,
            AML.QUANTITY AS PRODUCT_UOM_QTY,
            AML.PRICE_UNIT AS PRICE_UNIT,
            AML.DISCOUNT AS DISCOUNT_ID,
            AM.NAME AS ORDER_ID,
            AM.INVOICE_DATE AS SOURCE_ORDER_DATE_ORDER,
            RP.ID AS PARTNER_ID,
            RC.ID AS CURRENCY_ID
        
        ''' % (self.id)
        
    def _f_from_invoice_query(self):
        return '''
            ACCOUNT_MOVE_LINE AML
            INNER JOIN ACCOUNT_MOVE AM ON AML.MOVE_ID = AM.ID
            INNER JOIN RES_PARTNER RP ON AM.PARTNER_ID = RP.ID
            INNER JOIN RES_CURRENCY RC ON AM.CURRENCY_ID = RC.ID
        '''
    
    def _f_where_invoice_query(self):
        return ''' 
            AML.PRODUCT_ID = %s
            AND AM.MOVE_TYPE = 'out_invoice'
            AND AML.DISPLAY_TYPE = 'product'
            AND AM.STATE = 'posted'
        ''' % (self.product_id.id)
        
    def _f_select_legacy_query(self):
        return '''
            LPH.ID AS ID,
            'legacy' AS SOURCE,
            %s AS F_SALE_ORDER_LINE_ID,
            CAST(NULL AS integer) AS SOURCE_ORDER_LINE_ID,
            LPH.F_QTY AS PRODUCT_UOM_QTY,
            LPH.F_PRICE AS PRICE_UNIT,
            LPH.F_DISCOUNT AS DISCOUNT_ID,
            LPH.F_LEGACY_ORDER_ID AS ORDER_ID,
            LPH.F_LEGACY_ORDER_DATE AS SOURCE_ORDER_DATE_ORDER,
            RP.ID AS PARTNER_ID,
            RC.ID AS CURRENCY_ID
        
        ''' % (self.id)
        
    def _f_from_legacy_query(self):
        return '''
            F_LEGACY_PRICE_HISTORY_LINES LPH
            INNER JOIN RES_PARTNER RP ON LPH.PARTNER_ID = RP.ID
            INNER JOIN RES_CURRENCY RC ON LPH.F_CURRENCY_ID = RC.ID
        '''
    
    def _f_where_legacy_query(self):
        return ''' 
            LPH.PRODUCT_ID = %s
        ''' % (self.product_id.id)
    
    def _compute_sale_history_access(self):
        self.f_sale_history = self.env["ir.config_parameter"].sudo().get_param('falak_product_prices_history.f_sale_history') 
        
