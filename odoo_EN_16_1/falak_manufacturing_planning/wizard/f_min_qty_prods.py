from odoo import models, fields, api


class F_Minimum_Quantities_Products(models.Model):
    _name='f.min.qty.prods'
    _description ='Minimum Quantities For Products'
    _rec_name='f_mrp_location'
    
    
    f_mrp_wcg =fields.Many2one('mrp.workcenter.management',string="Work Center Group")
    f_mrp_categ = fields.Many2one('f.mp.categ', string='MRP Category')


    
    
    @api.model
    def get_mrp_location(self):
    
         location_from_setting = self.env['ir.config_parameter'].sudo().get_param('falak_manufacturing_planning.f_mrp_location') or False
         print('location',location_from_setting)
         return int(location_from_setting)
    
    
    f_mrp_location = fields.Many2one('stock.location',string="Location",default=get_mrp_location,required= True)

    #f_category_planning =fields.Many2one('f.planning.order',string="Category")


     
    def get_reorder_prods(self):
        
        domain = [('location_id', 'child_of', self.f_mrp_location.id),('product_min_qty', '!=',0),('product_max_qty', '!=',0)]
        if self.f_mrp_wcg : 
            domain += [('f_mrp_wcg','=',self.f_mrp_wcg.id)]
        if self.f_mrp_categ :
             domain += [('f_mrp_categ','=',self.f_mrp_categ.id)]
        print('domain',domain)
       
        
        reorder_products = self.env['stock.warehouse.orderpoint'].sudo().search(domain)

        return reorder_products
        
    def get_products(self):
        
        if  self.f_mrp_location : 
            
            mrp_plan_id = self._context.get('f_mrp_plan') 
            
            reorder_products = self.get_reorder_prods()
            print('reorder_products',reorder_products,self.f_mrp_location.id)
            products_toorder =[]                     
            for product in reorder_products:
                min_qty = product.product_min_qty
                max_qty = product.product_max_qty
                
                product_qty = self.env['stock.quant'].sudo().read_group([('location_id', 'child_of', self.f_mrp_location.id),('product_id','=',product.product_id.id)],['available_quantity'],['product_id'])
                
                print('product_qty',product_qty)
                
                if product_qty and product_qty[0]['available_quantity'] < min_qty : 
                    products_toorder.append(product.product_id.id)
            print('products_toorder',products_toorder)      
            if not products_toorder : 
                return True
            else :
                return {
                      'type': 'ir.actions.act_window',
                      'name':'Minimum Quantities',
                      'view_mode': 'tree',
                      'res_model': 'stock.warehouse.orderpoint',
                      'domain': [('product_id', 'in', products_toorder),('location_id', 'child_of', self.f_mrp_location.id)],
                      'context' : {'f_mrp_plan_id':mrp_plan_id},
                    }  
            
            