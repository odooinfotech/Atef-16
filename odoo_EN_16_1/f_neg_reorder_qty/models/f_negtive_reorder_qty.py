# -*- coding: utf-8 -*-

from odoo import models, fields, api,tools,_


class falak_neg_order_report(models.Model):
    _name = 'f.neg_reorder.qty.report'
    _description = "Products Less than Minimum in Re-order Rules"
    _auto = False
  #  _order = "f_report_date asc ,f_last_upadeton asc ,id asc"
  
  
    
    product_id = fields.Many2one('product.product','Product')
    product_tmp_id = fields.Many2one('product.template','Product Template')
    product_min_qty = fields.Float('Product Reordering Min Qty')
    quantity = fields.Float('Product Qty')
    location_id = fields.Many2one('stock.location','location')
    barcode = fields.Char('Barcode')
    default_code = fields.Char('Item No')
    shortage = fields.Char('Shortage')
    
    
  
  
    def _generalselect(self):
        return """
        
        
        Select 
            id , 
             location_id  ,
               product_id   ,
               product_tmp_id  ,
               product_min_qty  ,
               barcode  ,
                default_code  ,
                 quantity   ,
                  case when product_min_qty > quantity  then 'Yes' else 'No' end as shortage
     
         """
    
    
    
    
    def _inner_select(self):
        return """
        
        select  
         ro.id as id,
        l.id as location_id ,
         pp.id as product_id,
         pt.id as product_tmp_id,
         ro.product_min_qty as product_min_qty,
         pp.barcode as barcode,
         pp.default_code as default_code,
                COALESCE ((Select sum (COALESCE (quantity,0) ) from stock_quant sq, stock_location sl where sl.id = sq.location_id and sq.product_id = pp.id 
                AND (POSITION ('/'||l.id||'/' in  sl.parent_path  ) <> 0 OR sl.id = l.id)
                ),0) as quantity
        """
    
    def _generalfrom(self):
        return """  
         FROM 
           stock_warehouse_orderpoint ro , stock_location l,  product_product as pp, product_template pt
                where ro.product_id = pp.id
                and pt.id=pp.product_tmpl_id
                and l.id = ro.location_id

              
   
         """
         
  
  
  
  
    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute("""
            CREATE OR REPLACE VIEW %s AS (
            %s
            FROM(
           %s
           %s
           )neg_qty_report
            )
        """ % (self._table, self._generalselect(), self._inner_select(),self._generalfrom())
        )
        
        
        
