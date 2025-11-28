# -*- coding: utf-8 -*-
from odoo import models, fields, api, _,tools
from datetime import date,datetime

class F_Product_Product_Inherit(models.Model):
    _inherit = 'product.product'

    
    def f_open_price_history(self):
        
        
        tools.drop_view_if_exists(self.env.cr, 'f_product_price_history_p')
        self.env.cr.execute('''
            CREATE or REPLACE VIEW f_product_price_history_p AS (
                    SELECT %s
                    FROM %s
                    WHERE %s
                    UNION ALL
                    SELECT %s
                    FROM %s
                    WHERE %s
                    UNION ALL
                    SELECT %s
                    FROM %s
                    WHERE %s
            )''' % (self._f_select_invoice_query(),
                    self._f_from_invoice_query(),
                    self._f_where_invoice_query(),
                    self._f_select_legacy_query(),
                    self._f_from_legacy_query(),
                    self._f_where_legacy_query(),
                    self._f_select_pos_query(),
                    self._f_from_pos_query(),
                    self._f_where_pos_query())
        )
        
        res = {
                'type': 'ir.actions.act_window',
                'name': 'Price history',
                'target': 'new',
                'view_mode': 'tree',
                'res_model': 'f.product.price.history.p',
                'view_id': self.env.ref('falak_product_prices_history.f_product_price_history_view_tree').id,
                
                
            }  
    
    
        return res
    
    def _f_select_pos_query(self):
        return '''
            posl.ID AS ID,
            'pos' AS SOURCE,
            posl.ID AS SOURCE_ORDER_LINE_ID,
            posl.qty AS PRODUCT_UOM_QTY,
            posl.PRICE_UNIT AS PRICE_UNIT,
            posl.DISCOUNT AS DISCOUNT_ID,
            pos.NAME AS ORDER_ID,
            pos.date_order AS SOURCE_ORDER_DATE_ORDER,
            RP.ID AS PARTNER_ID,
            RC.ID AS CURRENCY_ID
        
        '''
        
    def _f_from_pos_query(self):
        return '''
            pos_order_line posl
            INNER JOIN pos_order pos ON posl.order_id = pos.ID
            INNER JOIN res_company RCO ON pos.company_id = RCO.ID
            INNER JOIN RES_PARTNER RP ON pos.PARTNER_ID = RP.ID
            INNER JOIN RES_CURRENCY RC ON RCO.CURRENCY_ID = RC.ID
        '''
    
    def _f_where_pos_query(self):
        return ''' 
            posl.PRODUCT_ID = %s
            
        ''' % (self.id)

        
        
class F_Product_Template_Inherit(models.Model):
    _inherit = 'product.template'

    
    def f_open_price_history(self):
        
        
        tools.drop_view_if_exists(self.env.cr, 'f_product_price_history_p')
        query = '''
            CREATE or REPLACE VIEW f_product_price_history_p AS (
                    SELECT %s
                    FROM %s
                    WHERE %s
                    UNION ALL
                    SELECT %s
                    FROM %s
                    WHERE %s
                    UNION ALL
                    SELECT %s
                    FROM %s
                    WHERE %s
            )''' % (self._f_select_invoice_query(),
                    self._f_from_invoice_query(),
                    self._f_where_invoice_query(),
                    self._f_select_legacy_query(),
                    self._f_from_legacy_query(),
                    self._f_where_legacy_query(),
                    self._f_select_pos_query(),
                    self._f_from_pos_query(),
                    self._f_where_pos_query())
        self.env.cr.execute(query)
        
        res = {
                'type': 'ir.actions.act_window',
                'name': 'Price history',
                'target': 'new',
                'view_mode': 'tree',
                'res_model': 'f.product.price.history.p',
                'view_id': self.env.ref('falak_product_prices_history.f_product_price_history_view_tree').id,
                
                
            }  
    
    
        return res

    def _f_select_pos_query(self):
        return '''
            posl.ID AS ID,
            'pos' AS SOURCE,
            posl.ID AS SOURCE_ORDER_LINE_ID,
            posl.qty AS PRODUCT_UOM_QTY,
            posl.PRICE_UNIT AS PRICE_UNIT,
            posl.DISCOUNT AS DISCOUNT_ID,
            pos.NAME AS ORDER_ID,
            pos.date_order AS SOURCE_ORDER_DATE_ORDER,
            RP.ID AS PARTNER_ID,
            RC.ID AS CURRENCY_ID

        '''

    def _f_from_pos_query(self):
        return '''
            pos_order_line posl
            INNER JOIN pos_order pos ON posl.order_id = pos.ID
            INNER JOIN res_company RCO ON pos.company_id = RCO.ID
            LEFT OUTER JOIN RES_PARTNER RP ON pos.PARTNER_ID = RP.ID
            INNER JOIN RES_CURRENCY RC ON RCO.CURRENCY_ID = RC.ID
        '''

    def _f_where_pos_query(self):
        product_id = self.env['product.product'].search([('product_tmpl_id', '=', self.id)]).ids
        if len(product_id) == 1:
            return ''' 
                        posl.PRODUCT_ID = %s

                    ''' % (product_id[0])
        return ''' 
            posl.PRODUCT_ID in %s

        ''' % ((tuple(product_id),))

    
