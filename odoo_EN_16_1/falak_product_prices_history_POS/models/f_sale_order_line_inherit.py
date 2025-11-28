# -*- coding: utf-8 -*-
from odoo import models, fields, api, _,tools
from datetime import date,datetime

class F_Sale_Order_Line_Inherit(models.Model):
    _inherit = 'sale.order.line'
    
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
                'res_model': 'f.sale.order.line.price.history.s',
                'view_id': self.env.ref('falak_product_prices_history.f_sale_order_line_price_history_view_tree').id,
                'context': {
                    'search_default_partner_id_filter':1,
                    
                    
                }
                
            }  
        
    
        return res

    def _f_select_pos_query(self):
        return '''
            posl.ID AS ID,
            'pos' AS SOURCE,
            %s AS F_SALE_ORDER_LINE_ID,
            posl.ID AS SOURCE_ORDER_LINE_ID,
            posl.qty AS PRODUCT_UOM_QTY,
            posl.PRICE_UNIT AS PRICE_UNIT,
            posl.DISCOUNT AS DISCOUNT_ID,
            pos.NAME AS ORDER_ID,
            pos.date_order AS SOURCE_ORDER_DATE_ORDER,
            RP.ID AS PARTNER_ID,
            RC.ID AS CURRENCY_ID
        ''' % (self.id)

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
        return ''' 
            posl.PRODUCT_ID = %s

        ''' % (self.product_id.id)

