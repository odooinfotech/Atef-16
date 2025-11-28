
from odoo import models, fields, api
from odoo.tools import add, float_compare, frozendict, split_every


class F_Stock_OrderPoint_Inherit(models.Model):
    _inherit ='stock.warehouse.orderpoint'
    
    

    f_min_qty_id =fields.Many2one('f.min.qty.prods',string="Min Qty")

    f_available_qty = fields.Float(related= 'product_id.qty_available')
    
    f_mrp_wcg  = fields.Many2one('mrp.workcenter.management',string="Work Center Group",related = 'product_id.f_mrp_wcg')
    f_mrp_categ = fields.Many2one('f.mp.categ', string='Manufacturing Category',related = 'product_id.f_mrp_categ')
    
    
    def create_plan_prod(self):
        
        mrp_plan_id =  self._context.get('f_mrp_plan_id') 
        print('mrp_plan_id>>>>>>>>>',mrp_plan_id)
        
        mrp_plan = self.env['f.man.plan'].search([('id','=',mrp_plan_id)])
        
        for rec in self :
            f_qty_to_manufacture = 0.0
            qty_to_order = 0.0
            rounding = rec.product_uom.rounding
            if float_compare(rec.qty_forecast, rec.product_min_qty, precision_rounding=rounding) < 0:
                qty_to_order = max(rec.product_min_qty, rec.product_max_qty) - rec.qty_forecast

                remainder = rec.qty_multiple > 0 and qty_to_order % rec.qty_multiple or 0.0
                if float_compare(remainder, 0.0, precision_rounding=rounding) > 0:
                    qty_to_order += rec.qty_multiple - remainder
            
            f_qty_to_manufacture = qty_to_order
            if rec.product_id.id in mrp_plan.f_plan_products.f_product_id.ids :
                print('exists')
                
                to_update = self.env['f.man.plan.products'].sudo().search([('f_product_id','=',rec.product_id.id )],limit=1)
                 
                
                if to_update :
                    to_update.f_demand_qty = f_qty_to_manufacture 
   
                
            else :
                print('create')
                self.env['f.man.plan.products'].sudo().create({
                                    'f_product_id':rec.product_id.id,
                                    'f_initial_qty':rec.product_id.qty_available,
                                    'f_demand_qty':f_qty_to_manufacture,
                                   # 'f_demand_product_uom':rec.product_id.uom_id.id,
                                    'f_man_planning_id':mrp_plan.id,        
                                    })  
            
            return {
                  'type': 'ir.actions.act_window',
                  'name':'Planning Quantities',
                  'view_mode': 'tree',
                  'res_model': 'f.man.plan.products',
                  'domain': [('f_man_planning_id', '=', mrp_plan.id)],
                
                }    
        
        
        
        
        
