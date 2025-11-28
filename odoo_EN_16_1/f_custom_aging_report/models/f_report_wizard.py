# -*- coding: utf-8 -*-
from odoo import fields, models, api, _,tools






class FxlsProductaging(models.TransientModel):
    _name= 'f.product.aging' 
    _description = "Aging Details wizard"
   
   
   
    date = fields.Datetime("Date")
    product_ids = fields.Many2many('product.product', string='Products',required=False)
    company = fields.Many2one('res.company', string='Company',
                              default=lambda self: self.env.user.company_id.id)
    
    breakdown_days = fields.Integer("Breakdown Days", default=30)
    warehouse = fields.Many2one("stock.warehouse","Warehouse")

    f_type = fields.Selection([('list', 'List'), ('xls', 'Excel')],
                            string="Report Type", default="list")


    
    def _intialselect(self):
        return """
        
        SELECT d.product_id as id,d.product_id, company_id, name, barcode , default_code, COALESCE ( (total_cost), 0) total_cost,on_hand_quantity,
       CASE WHEN b1 < 0 THEN 0 ELSE b1 END days,
       COALESCE ( (CASE WHEN b1 < 0 THEN 0 ELSE ( b1 * avg_cost) END), 0) cost0,
       CASE WHEN b2 < 0 THEN 0 ELSE b2 END days1,
       COALESCE ( (CASE WHEN b2 < 0 THEN 0 ELSE ( b2 * avg_cost) END), 0) cost1,
       CASE WHEN b3 < 0 THEN 0 ELSE b3 END days2,
       COALESCE ( (CASE WHEN b3 < 0 THEN 0 ELSE ( b3 * avg_cost) END), 0) cost2,
       CASE WHEN b4 < 0 THEN 0 ELSE b4 END days3,
       COALESCE ( (CASE WHEN b4 < 0 THEN 0 ELSE ( b4 * avg_cost) END), 0) cost3,
       CASE WHEN b5 < 0 THEN 0 ELSE b5 END days4,
       COALESCE ( (CASE WHEN b5 < 0 THEN 0 ELSE ( b5 * avg_cost) END), 0) cost4,
       CASE WHEN b6 < 0 THEN 0 ELSE b6 END days5,
       COALESCE ( (CASE WHEN b6 < 0 THEN 0 ELSE ( b6 * avg_cost) END), 0) cost5,
       CASE WHEN b7 < 0 THEN 0 ELSE b7 END days6,
       COALESCE ( (CASE WHEN b7 < 0 THEN 0 ELSE ( b7 * avg_cost) END), 0) cost6
       
        
        """
        
    def _firstselect(self):
        return """
        
        SELECT product_id, company_id, name,barcode ,default_code,on_hand_quantity, issued_qty,
               (CASE WHEN (bucket2 + bucket3 + bucket4 + bucket5 + bucket6 + bucket7 + issued_qty) < 0 THEN (bucket1 + bucket2 + bucket3 + bucket4 + bucket5 + bucket6 + bucket7 + issued_qty) ELSE bucket1 END) b1,
               (CASE WHEN (bucket3 + bucket4 + bucket5 + bucket6 + bucket7 + issued_qty) < 0 THEN (bucket2 + bucket3 + bucket4 + bucket5 + bucket6 + bucket7 + issued_qty) ELSE bucket2 END) b2,
               (CASE WHEN (bucket4 + bucket5 + bucket6 + bucket7 + issued_qty) < 0 THEN (bucket3 + bucket4 + bucket5 + bucket6 + bucket7 + issued_qty) ELSE bucket3 END) b3,
               (CASE WHEN (bucket5 + bucket6 + bucket7 + issued_qty) < 0 THEN (bucket4 + bucket5 + bucket6 + bucket7 + issued_qty) ELSE bucket4 END) b4,
               (CASE WHEN (bucket6 + bucket7 + issued_qty) < 0 THEN (bucket5 + bucket6 + bucket7 + issued_qty) ELSE bucket5 END) b5,
               (CASE WHEN (bucket7 + issued_qty) < 0 THEN (bucket6 + bucket7 + issued_qty) ELSE bucket6 END) b6,
               (bucket7 + issued_qty) b7  
           
        """
        
        
    def _secselect(self):
        return """
        
        SELECT product_id, company_id, name, barcode,default_code,
                       COALESCE ( (bucket1), 0) bucket1,
                       COALESCE ( (bucket2), 0) bucket2,
                       COALESCE ( (bucket3), 0) bucket3,
                       COALESCE ( (bucket4), 0) bucket4,
                       COALESCE ( (bucket5), 0) bucket5,
                       COALESCE ( (bucket6), 0) bucket6,
                       COALESCE ( (bucket7), 0) bucket7,
                       COALESCE ( (issued_qty), 0) issued_qty,
                       on_hand_quantity 
           
        """
        
    def _thirdselect(self):
        return """
        
        SELECT a.product_id, a.company_id, a.name,a.barcode,a.default_code,on_hand_quantity,
                               bucket1, bucket2, bucket3, bucket4, bucket5,
                               bucket6, bucket7, issued_qty
           
        """
        
        
    def _fourthselect(self):
        
        if self.warehouse :
            x = True
        else:
            x = False
            
            
        return """
        
        SELECT m.company_id, m.product_id, pt.name,p.barcode , p.default_code,
        
        
             SUM ( case when (%s IS NOT False) then (case when (
              ((POSITION ('/'||'%s'||'/' in  source.parent_path) <> 0 ) and (POSITION ('/'||'%s'||'/' in  dest.parent_path) = 0  ) AND  source.usage = 'internal')
               )  then (m.qty_done/ u.factor * u2.factor)*-1 else  (m.qty_done/ u.factor * u2.factor)  *1 end) 
           else (CASE WHEN source.usage = 'internal' THEN (m.qty_done/ u.factor * u2.factor)*-1 ELSE (m.qty_done/ u.factor * u2.factor)  *1 END)end) AS on_hand_quantity,
           
           
           
            
           
            
             SUM ( case when (%s IS NOT False) then (case when (
            ((POSITION ('/'||'%s'||'/' in  source.parent_path) <> 0  ) and (POSITION ('/'||'%s'||'/' in  dest.parent_path) = 0  )AND  source.usage = 'internal')
           
           
               )  then (m.qty_done/ u.factor * u2.factor)*-1 else 0 end) 
           else (CASE WHEN source.usage = 'internal' THEN (m.qty_done/ u.factor * u2.factor)*-1 ELSE 0 END)end) AS issued_qty,
           
           
           
            
            
          
           

          SUM ( case when (%s IS NOT False) then (case when (
         
                 
                 ((POSITION ('/'||'%s'||'/' in  dest.parent_path) <> 0  ) and (POSITION ('/'||'%s'||'/' in  source.parent_path) = 0  ) and dest.usage = 'internal' )
              
            and (date (m.date) BETWEEN (date ('%s') - (%s)) AND date ('%s') )
           
               )  then (m.qty_done/ u.factor * u2.factor) else 0 end) 
           else (CASE WHEN source.usage <> 'internal' AND dest.usage = 'internal' AND date (m.date) BETWEEN (date ('%s') - (%s)) AND date ('%s') THEN (m.qty_done/ u.factor * u2.factor) ELSE 0 END)end) AS bucket1,
           
            
           
           SUM ( case when (%s IS NOT False) then (case when (
            ((POSITION ('/'||'%s'||'/' in  dest.parent_path) <> 0  ) and (POSITION ('/'||'%s'||'/' in  source.parent_path) = 0  ) and dest.usage = 'internal' )
           
            and (date (m.date) BETWEEN (date ('%s') - (%s)*2) AND (date ('%s') - ((%s)+1)) )
         
               )  then (m.qty_done/ u.factor * u2.factor) else 0 end) 
           else (CASE WHEN source.usage <> 'internal' AND dest.usage = 'internal' AND date (m.date) BETWEEN (date ('%s') - (%s)*2) AND (date ('%s') - ((%s)+1)) THEN (m.qty_done/ u.factor * u2.factor) ELSE 0 END)end) AS bucket2,
           




         
         
         
         
            SUM ( case when (%s IS NOT False) then (case when (
           ((POSITION ('/'||'%s'||'/' in  dest.parent_path) <> 0 ) and (POSITION ('/'||'%s'||'/' in  source.parent_path) = 0 ) and dest.usage = 'internal' )
       
            and (date (m.date) BETWEEN (date ('%s') - (%s)*3) AND (date ('%s') - (((%s)*2)+1)))
    
               )  then (m.qty_done/ u.factor * u2.factor) else 0 end) 
           else (CASE WHEN source.usage <> 'internal' AND dest.usage = 'internal' AND date (m.date) BETWEEN (date ('%s') - (%s)*3) AND (date ('%s') - (((%s)*2)+1)) THEN (m.qty_done/ u.factor * u2.factor) ELSE 0 END)end) AS bucket3,
           
              
           
           
           SUM ( case when (%s IS NOT False) then (case when (
           ((POSITION ('/'||'%s'||'/' in  dest.parent_path) <> 0 ) and (POSITION ('/'||'%s'||'/' in  source.parent_path) = 0 ) and dest.usage = 'internal' )
              
            
            and (date (m.date) BETWEEN (date ('%s') - (%s)*6) AND (date ('%s') - (((%s)*3)+1)))
           
               )  then (m.qty_done/ u.factor * u2.factor) else 0 end) 
           else (CASE WHEN source.usage <> 'internal' AND dest.usage = 'internal' AND date (m.date) BETWEEN (date ('%s') - (%s)*6) AND (date ('%s') - (((%s)*3)+1)) THEN (m.qty_done/ u.factor * u2.factor) ELSE 0 END)end) AS bucket4,
           
            
           
           SUM ( case when (%s IS NOT False) then (case when (
            ((POSITION ('/'||'%s'||'/' in  dest.parent_path) <> 0 ) and (POSITION ('/'||'%s'||'/' in  source.parent_path) = 0 ) and dest.usage = 'internal' )
              
            and (date (m.date) BETWEEN (date ('%s') - (%s)*8) AND (date ('%s') - (((%s)*6)+1 )))
       
               )  then (m.qty_done/ u.factor * u2.factor) else 0 end) 
           else (CASE WHEN source.usage <> 'internal' AND dest.usage = 'internal' AND date (m.date) BETWEEN (date ('%s') - (%s)*8) AND (date ('%s') - (((%s)*6)+1 )) THEN (m.qty_done/ u.factor * u2.factor) ELSE 0 END)end) AS bucket5,
           
      
             
           
           SUM ( case when (%s IS NOT False) then (case when (
           ((POSITION ('/'||'%s'||'/' in  dest.parent_path) <> 0  ) and (POSITION ('/'||'%s'||'/' in  source.parent_path) = 0 ) and dest.usage = 'internal' )
              
            and(date (m.date) BETWEEN (date ('%s') - (%s)*12 ) AND (date ('%s') - (((%s)*8)+1)))
         
               )  then (m.qty_done/ u.factor * u2.factor) else 0 end) 
           else (CASE WHEN source.usage <> 'internal' AND dest.usage = 'internal' AND date (m.date) BETWEEN (date ('%s') - (%s)*12 ) AND (date ('%s') - (((%s)*8)+1)) THEN (m.qty_done/ u.factor * u2.factor) ELSE 0 END)end) AS bucket6,
           
    
    
    



           SUM ( case when (%s IS NOT False) then (case when (
           ((POSITION ('/'||'%s'||'/' in  dest.parent_path) <> 0 ) and (POSITION ('/'||'%s'||'/' in  source.parent_path) = 0) and dest.usage = 'internal' )
              
            and(date (m.date) <= (date ('%s') - (((%s)*12)+1)) )
     
               )  then (m.qty_done/ u.factor * u2.factor) else 0 end) 
           else (CASE WHEN source.usage <> 'internal' AND dest.usage = 'internal' AND date (m.date) <= (date ('%s') - (((%s)*12)+1)) THEN (m.qty_done/ u.factor * u2.factor) ELSE 0 END)end) AS bucket7
           

                                 
           
        """%(x,self.warehouse.view_location_id.id,self.warehouse.view_location_id.id,
             x,self.warehouse.view_location_id.id,self.warehouse.view_location_id.id,  
             x,self.warehouse.view_location_id.id,self.warehouse.view_location_id.id,self.date,self.breakdown_days,self.date, self.date,self.breakdown_days,self.date,       x,self.warehouse.view_location_id.id,self.warehouse.view_location_id.id,self.date,self.breakdown_days,self.date,self.breakdown_days,self.date,self.breakdown_days,self.date,self.breakdown_days, 
x,self.warehouse.view_location_id.id,self.warehouse.view_location_id.id,self.date,self.breakdown_days,self.date,self.breakdown_days,self.date,self.breakdown_days,self.date,self.breakdown_days,   x,self.warehouse.view_location_id.id,self.warehouse.view_location_id.id,self.date,self.breakdown_days,self.date,self.breakdown_days,self.date,self.breakdown_days,self.date,self.breakdown_days,   x,self.warehouse.view_location_id.id,self.warehouse.view_location_id.id,self.date,self.breakdown_days,self.date,self.breakdown_days,self.date,self.breakdown_days,self.date,self.breakdown_days,   x,self.warehouse.view_location_id.id,self.warehouse.view_location_id.id,self.date,self.breakdown_days,self.date,self.breakdown_days,self.date,self.breakdown_days,self.date,self.breakdown_days,   x,self.warehouse.view_location_id.id,self.warehouse.view_location_id.id,self.date,self.breakdown_days,self.date,self.breakdown_days)
        
        
    def _fromstat(self):
        
        return """
        
        FROM stock_move_line m,
            stock_location source,
            stock_location dest,
            product_product p,
            product_template pt,
            uom_uom u ,
            uom_uom u2 
        
        """
        
    def _wherestat(self):
        
        
        wherestr = """
        WHERE
        m.location_id = source.id
        AND m.location_dest_id = dest.id
        and u.id= m.product_uom_id
        and u2.id=pt.uom_id
        
        AND m.state = 'done'
        AND m.product_id = p.id
        AND p.product_tmpl_id = pt.id
        AND m.company_id = (%s)
        AND m.date <= ('%s')
       
        """%(self.env.company.id,self.date)
        
        
        if not self.warehouse:
                wherestr = wherestr + """  
                AND ((source.usage = 'internal' AND dest.usage <> 'internal') OR (source.usage <>'internal' AND dest.usage = 'internal'))
                
                """
        
        if self.warehouse:
                wherestr = wherestr + """    
                 AND (
             
                 ((POSITION ('/'||'%s'||'/' in  dest.parent_path) <> 0 OR dest.id = %s ) and (POSITION ('/'||'%s'||'/' in  source.parent_path) = 0 OR source.id = %s ) and dest.usage = 'internal' )
                 
                 
                 or 
                 
                 ((POSITION ('/'||'%s'||'/' in  source.parent_path) <> 0 OR source.id = %s ) and (POSITION ('/'||'%s'||'/' in  dest.parent_path) = 0 OR dest.id = %s ) and source.usage = 'internal' )
                 
                 
            
                 )
                 """%(self.warehouse.view_location_id.id,self.warehouse.view_location_id.id,self.warehouse.view_location_id.id,self.warehouse.view_location_id.id,
                      self.warehouse.view_location_id.id,self.warehouse.view_location_id.id,self.warehouse.view_location_id.id,self.warehouse.view_location_id.id) 
                 
                 
                 
        return wherestr 
        
    def _groupbystat(self):
        
        return """  
        
        GROUP BY m.product_id, m.company_id, pt.name,p.barcode , p.default_code
        """  
        
        
    def _havingstat(self):
        
        if self.warehouse:
                return """
                 HAVING (SUM (CASE WHEN
                 ((POSITION ('/'||'%s'||'/' in  source.parent_path) <> 0 ) and (POSITION ('/'||'%s'||'/' in  dest.parent_path) = 0  ) AND  source.usage = 'internal')  then (m.qty_done/ u.factor * u2.factor) * -1 ELSE  (m.qty_done/ u.factor * u2.factor) * 1 END)) > 0
                 
                 
       
        
        """%(self.warehouse.view_location_id.id,self.warehouse.view_location_id.id)
                
                
        if not self.warehouse:
                return """
        HAVING (SUM (CASE WHEN source.usage ='internal'  THEN (m.qty_done/ u.factor * u2.factor) * -1 ELSE (m.qty_done/ u.factor * u2.factor) * 1 END)) > 0
        
        """
                
        
        
        
    def _leftselect(self):
        return """
        
        select l.product_id , sum (l.value) total_cost, (sum (l.value)/sum(l.quantity)) avg_cost  
          from stock_valuation_layer  l  
          where l.create_date <= ('%s') group by l.product_id having sum(l.quantity) > 0
          
           
        """%(self.date)
        
        
        
    def _finalcondition(self):
        return"""
         ON (d.product_id = l.product_id)
                                                                                                  
        ORDER BY d.product_id
        
        """
        
    def get_aging_product_details(self):
        print("55555555555555555")
        
        tools.drop_view_if_exists(self.env.cr, 'f_aging_details')
        
        self.env.cr.execute("""
        CREATE OR REPLACE VIEW f_aging_details AS (
        %s
        FROM(
            %s
        FROM(
            %s
        FROM(
            %s
        FROM(
            %s
            %s
            %s
            %s
            %s
        )a
        )b
        )c
        )d
        LEFT JOIN 
        (%s)l
        %s
        
        
        
        
        )""" % (self._intialselect(),self._firstselect(),self._secselect(),self._thirdselect(),self._fourthselect(),self._fromstat(),self._wherestat(),self._groupbystat(),self._havingstat(),
                self._leftselect(),self._finalcondition()))
        
        
        if self.f_type == 'list':
            tree_id = self.env.ref('f_custom_aging_report.view_report_aging_custom_tree').id
            form_id = False
            action = {
                'name':_('Product Aging Report'),
                'type': 'ir.actions.act_window',
                'view_mode': 'tree',
                'res_model': 'f.aging.details',
                }

            return action
        if self.f_type == 'xls':
            return self.env.ref('f_custom_aging_report.f_aging_details_report_xls').report_action(self)

        
    
        
  
        
    
        
    
    
    
