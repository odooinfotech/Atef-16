# -*- coding: utf-8 -*-

from odoo import models, fields, api,tools,_


class f_mo_cost_analysis(models.Model):
    _name = 'f.mo.cost.analysis'
    _description = "MO Cost Analysis Report"
    _auto = False
    
    date_planned_start = fields.Datetime('Date',readonly=True)
    mo_id = fields.Many2one('mrp.production','MO Order',readonly=True)
    product_id = fields.Many2one('product.product','Component Product',readonly=True)
    mo_product = fields.Many2one('product.product','Product',readonly=True)
    qty = fields.Float('Quantity',readonly=True)
    cost = fields.Float('Unit Cost',readonly=True)
    total_cost = fields.Float('Total Cost',readonly=True)
    f_bussniess_purop = fields.Many2one('f.bussniess.purpose',string='Business Purpose')
    
    
    
    
    
    
    
    def _generalselect(self):
        return """
        SELECT
        MAX(sm.id) as id,
            mo.date_planned_start as date_planned_start,
             sm.product_id as product_id,
             mo.id as mo_id,
             mo.product_id as mo_product,
             abs(SUM(svl.quantity)) as qty,
             case when (abs(SUM(svl.quantity)) = 0 )then 0 else (abs(SUM(svl.value)) /abs(SUM(svl.quantity))  )end as cost,
             abs(SUM(svl.value)) as total_cost,
             
             MAX(pt.f_bussniess_purop)  as f_bussniess_purop
                             
            
             
         """
    
    
    
    
    def _generalfrom(self):
        return """  
         FROM 
         stock_move AS sm
                       INNER JOIN stock_valuation_layer AS svl ON svl.stock_move_id = sm.id
                       LEFT JOIN mrp_production AS mo on sm.raw_material_production_id = mo.id
                       LEFT JOIN product_product AS pp on sm.product_id = pp.id
                        LEFT JOIN product_template AS pt on pp.product_tmpl_id = pt.id
                       
                            WHERE  sm.state != 'cancel' AND sm.product_qty != 0 AND scrapped != 't'
                            AND mo.id is not null 
                         

              
   
         """
    
    def _generalgroupby(self):
        return """ 
        GROUP BY sm.product_id, mo.id
        """
         
  
  
  
  
    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute("""
            CREATE OR REPLACE VIEW %s AS (
            %s
           %s
           %s
            )
        """ % (self._table, self._generalselect(), self._generalfrom(),self._generalgroupby())
        )
         
  
  
  
  



