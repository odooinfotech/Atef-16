# -*- coding: utf-8 -*-
from odoo import models, fields, api, _,tools
from datetime import date,datetime

class F_Product_Product_Inherit(models.Model):
    _inherit = 'product.product'
    
    f_product_history = fields.Boolean(string = "Product Sale History",compute='_compute_product_history_access',readonly=True)
    f_product_purchase_history = fields.Boolean(string="Product Purchase History", compute='_compute_purchase_product_history_access',readonly=True)
    
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
            )''' % (self._f_select_invoice_query(),self._f_from_invoice_query(),self._f_where_invoice_query(),self._f_select_legacy_query(),self._f_from_legacy_query(),self._f_where_legacy_query())
        )
        
        res = {
                'type': 'ir.actions.act_window',
                'name':'Price history',
                'target': 'new',
                'view_mode': 'tree',
                'res_model': 'f.product.price.history.p',
                'view_id': self.env.ref('falak_product_prices_history.f_product_price_history_view_tree').id,
                
                
            }  
    
    
        return res

    def f_open_purchase_price_history(self):
        tools.drop_view_if_exists(self.env.cr, 'f_product_purchase_price_history_p')
        self.env.cr.execute('''
            CREATE or REPLACE VIEW f_product_purchase_price_history_p AS (
                    SELECT %s
                    FROM %s
                    WHERE %s
            )''' % (self._f_select_bill_query(), self._f_from_bill_query(), self._f_where_bill_query()))

        res = {
            'type': 'ir.actions.act_window',
            'name': 'Purchase Price history',
            'target': 'new',
            'view_mode': 'tree',
            'res_model': 'f.product.purchase.price.history.p',
            'view_id': self.env.ref('falak_product_prices_history.f_product_purchase_price_history_view_tree').id,

        }

        return res
    
    def _f_select_invoice_query(self):
        return '''
            AML.ID AS ID,
            'invoice' AS SOURCE,
            AML.ID AS SOURCE_ORDER_LINE_ID,
            AML.QUANTITY AS PRODUCT_UOM_QTY,
            AML.PRICE_UNIT AS PRICE_UNIT,
            AML.DISCOUNT AS DISCOUNT_ID,
            AM.NAME AS ORDER_ID,
            AM.INVOICE_DATE AS SOURCE_ORDER_DATE_ORDER,
            RP.ID AS PARTNER_ID,
            RC.ID AS CURRENCY_ID
        
        '''
        
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
            
        ''' % (self.id)
        
    def _f_select_legacy_query(self):
        return '''
            LPH.ID AS ID,
            'legacy' AS SOURCE,
            CAST(NULL AS integer) AS SOURCE_ORDER_LINE_ID,
            LPH.F_QTY AS PRODUCT_UOM_QTY,
            LPH.F_PRICE AS PRICE_UNIT,
            LPH.F_DISCOUNT AS DISCOUNT_ID,
            LPH.F_LEGACY_ORDER_ID AS ORDER_ID,
            LPH.F_LEGACY_ORDER_DATE AS SOURCE_ORDER_DATE_ORDER,
            RP.ID AS PARTNER_ID,
            RC.ID AS CURRENCY_ID
        
        '''
        
    def _f_from_legacy_query(self):
        return '''
            F_LEGACY_PRICE_HISTORY_LINES LPH
            INNER JOIN RES_PARTNER RP ON LPH.PARTNER_ID = RP.ID
            INNER JOIN RES_CURRENCY RC ON LPH.F_CURRENCY_ID = RC.ID
        '''
    
    def _f_where_legacy_query(self):
        return ''' 
            LPH.PRODUCT_ID = %s
        ''' % (self.id)

    def _f_select_bill_query(self):
        return '''
            AML.ID AS ID,
            AML.ID AS purchase_order_line_id,
            AM.ID AS ORDER_ID,
            RP.ID AS PARTNER_ID,
            AM.INVOICE_DATE AS purchase_order_date_order
        '''

    def _f_from_bill_query(self):
        return '''
            ACCOUNT_MOVE_LINE AML
            INNER JOIN ACCOUNT_MOVE AM ON AML.MOVE_ID = AM.ID
            INNER JOIN RES_PARTNER RP ON AM.PARTNER_ID = RP.ID
        '''

    def _f_where_bill_query(self):
        return ''' 
            AML.PRODUCT_ID = %s
            AND AM.MOVE_TYPE = 'in_invoice'
            AND AML.DISPLAY_TYPE = 'product'
            AND AM.STATE = 'posted'
        ''' % (self.id)

    def _compute_purchase_product_history_access(self):
        self.f_product_purchase_history = self.env["ir.config_parameter"].sudo().get_param('falak_product_prices_history.f_product_purchase_history')

    def _compute_product_history_access(self):
        self.f_product_history = self.env["ir.config_parameter"].sudo().get_param('falak_product_prices_history.f_product_history') 
    
        
        
class F_Product_Template_Inherit(models.Model):
    _inherit = 'product.template'
    
    f_product_history = fields.Boolean(string = "Product History",compute='_compute_product_history_access',readonly=True)
    f_product_purchase_history = fields.Boolean(string="Product Purchase History",compute='_compute_purchase_product_history_access', readonly=True)
    
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
            )''' % (self._f_select_invoice_query(),self._f_from_invoice_query(),self._f_where_invoice_query(),self._f_select_legacy_query(),self._f_from_legacy_query(),self._f_where_legacy_query())
        )
        
        res = {
                'type': 'ir.actions.act_window',
                'name':'Price history',
                'target': 'new',
                'view_mode': 'tree',
                'res_model': 'f.product.price.history.p',
                'view_id': self.env.ref('falak_product_prices_history.f_product_price_history_view_tree').id,
                
                
            }  

        return res

    def f_open_purchase_price_history(self):
        tools.drop_view_if_exists(self.env.cr, 'f_product_purchase_price_history_p')
        self.env.cr.execute('''
            CREATE or REPLACE VIEW f_product_purchase_price_history_p AS (
                    SELECT %s
                    FROM %s
                    WHERE %s
            )''' % (self._f_select_bill_query(), self._f_from_bill_query(), self._f_where_bill_query()))

        res = {
            'type': 'ir.actions.act_window',
            'name': 'Purchase Price history',
            'target': 'new',
            'view_mode': 'tree',
            'res_model': 'f.product.purchase.price.history.p',
            'view_id': self.env.ref('falak_product_prices_history.f_product_purchase_price_history_view_tree').id,

        }

        return res

    def _f_select_invoice_query(self):
        return '''
            AML.ID AS ID,
            'invoice' AS SOURCE,
            AML.ID AS SOURCE_ORDER_LINE_ID,
            AML.QUANTITY AS PRODUCT_UOM_QTY,
            AML.PRICE_UNIT AS PRICE_UNIT,
            AML.DISCOUNT AS DISCOUNT_ID,
            AM.NAME AS ORDER_ID,
            AM.INVOICE_DATE AS SOURCE_ORDER_DATE_ORDER,
            RP.ID AS PARTNER_ID,
            RC.ID AS CURRENCY_ID
        
        '''
        
    def _f_from_invoice_query(self):
        return '''
            ACCOUNT_MOVE_LINE AML
            INNER JOIN ACCOUNT_MOVE AM ON AML.MOVE_ID = AM.ID
            INNER JOIN RES_PARTNER RP ON AM.PARTNER_ID = RP.ID
            INNER JOIN RES_CURRENCY RC ON AM.CURRENCY_ID = RC.ID
        '''
    
    def _f_where_invoice_query(self):
        product_id = self.env['product.product'].search([('product_tmpl_id', '=', self.id)]).ids
        if len(product_id) == 1:
            return ''' 
                        AML.PRODUCT_ID = %s
                        AND AM.MOVE_TYPE = 'out_invoice'
                        AND AML.DISPLAY_TYPE = 'product'
                        AND AM.STATE = 'posted'
                    ''' % (product_id[0])
        return ''' 
            AML.PRODUCT_ID in %s
            AND AM.MOVE_TYPE = 'out_invoice'
            AND AML.DISPLAY_TYPE = 'product'
            AND AM.STATE = 'posted'
        ''' % ((tuple(product_id),))
        
    def _f_select_legacy_query(self):
        return '''
            LPH.ID AS ID,
            'legacy' AS SOURCE,
            CAST(NULL AS integer) AS SOURCE_ORDER_LINE_ID,
            LPH.F_QTY AS PRODUCT_UOM_QTY,
            LPH.F_PRICE AS PRICE_UNIT,
            LPH.F_DISCOUNT AS DISCOUNT_ID,
            LPH.F_LEGACY_ORDER_ID AS ORDER_ID,
            LPH.F_LEGACY_ORDER_DATE AS SOURCE_ORDER_DATE_ORDER,
            RP.ID AS PARTNER_ID,
            RC.ID AS CURRENCY_ID
        
        '''
        
    def _f_from_legacy_query(self):
        return '''
            F_LEGACY_PRICE_HISTORY_LINES LPH
            INNER JOIN RES_PARTNER RP ON LPH.PARTNER_ID = RP.ID
            INNER JOIN RES_CURRENCY RC ON LPH.F_CURRENCY_ID = RC.ID
        '''
    
    def _f_where_legacy_query(self):
        product_id = self.env['product.product'].search([('product_tmpl_id', '=', self.id)]).ids
        if len(product_id) == 1:
            return ''' 
                        LPH.PRODUCT_ID = %s
                    ''' % (product_id[0])
        return ''' 
            LPH.PRODUCT_ID in %s
        ''' % ((tuple(product_id),))

    def _f_select_bill_query(self):
        return '''
            AML.ID AS ID,
            AML.ID AS purchase_order_line_id,
            AM.ID AS ORDER_ID,
            RP.ID AS PARTNER_ID,
            AM.INVOICE_DATE AS purchase_order_date_order
        '''

    def _f_from_bill_query(self):
        return '''
            ACCOUNT_MOVE_LINE AML
            INNER JOIN ACCOUNT_MOVE AM ON AML.MOVE_ID = AM.ID
            INNER JOIN RES_PARTNER RP ON AM.PARTNER_ID = RP.ID
        '''

    def _f_where_bill_query(self):
        product_id = self.env['product.product'].search([('product_tmpl_id', '=', self.id)]).ids
        if len(product_id) == 1:
            return ''' 
                        AML.PRODUCT_ID = %s
                        AND AM.MOVE_TYPE = 'in_invoice'
                        AND AML.DISPLAY_TYPE = 'product'
                        AND AM.STATE = 'posted'
                    ''' % (product_id[0])
        return ''' 
            AML.PRODUCT_ID in %s
            AND AM.MOVE_TYPE = 'in_invoice'
            AND AML.DISPLAY_TYPE = 'product'
            AND AM.STATE = 'posted'
        ''' % ((tuple(product_id),))

    def _compute_purchase_product_history_access(self):
        self.f_product_purchase_history = self.env["ir.config_parameter"].sudo().get_param('falak_product_prices_history.f_product_purchase_history')
        
        
    def _compute_product_history_access(self):
        self.f_product_history = self.env["ir.config_parameter"].sudo().get_param('falak_product_prices_history.f_product_history') 
