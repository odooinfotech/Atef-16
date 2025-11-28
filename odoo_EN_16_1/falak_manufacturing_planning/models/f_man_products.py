from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime,timedelta


class FManPlanProducts(models.Model):
    _name ='f.man.plan.products'
    _description = 'Manufacturing Plan Products'
    _rec_name='f_product_id'
    _order ='f_priority desc ,f_increment_num_prods asc'
    
   
    _sql_constraints = [
         ('prod_uniq', 'unique(f_product_id,f_man_planning_id,f_work_center)', 'Product is already added !'),]
    


    f_mrp_production =fields.Many2one('mrp.production',string="Mrp Production")
    f_man_planning_id =fields.Many2one(comodel_name='f.man.plan',string="Manufacturing Planning")
    f_product_id =fields.Many2one(comodel_name='product.product',string="Product" ,ondelete="cascade", required= True ,domain=[('product_tmpl_id.type','=','product'),('f_is_manufactured','=',True)])
    f_demand_qty =fields.Float(string="Demand / Planning Qty" ,default=1.0,copy=True)
    f_increment_num_prods = fields.Integer(string="Number", default=lambda self: self.env['ir.sequence'].next_by_code('f.man.plan.products'))

    f_product_uom = fields.Many2one(related='f_product_id.uom_id',string="Unit of Measure",copy=True)
    product_uom_category_id = fields.Many2one(related='f_product_id.uom_id.category_id',copy=True)  
    f_demand_product_uom = fields.Many2one(comodel_name='uom.uom',string='Demand Unit of Measure', domain="[('category_id', '=', product_uom_category_id)]",copy=True)

    f_inprocess_qty =fields.Float(string="Plan In Process Qty" ,default=0.0)
    f_no_plan_qty =fields.Float(string=" In Process Qty" ,default=0.0)

    f_done_qty =fields.Float(string="Done Qty" ,default=0.0,store=True)
    f_remaining_qty =fields.Float(string="Remaining Qty",compute='compute_analyze_quantities',default=0.0,store=True,readonly=True)

    f_work_center =fields.Many2one('mrp.workcenter',string="Work Center")
    workcenter_group_id = fields.Many2one('mrp.workcenter.management', string='Work Center Group', related='f_man_planning_id.f_mrp_wcg')
    
    
    
    #pass product
    @api.onchange('f_product_id')
    def onChangeProduct(self):
        self.f_initial_qty= self.f_product_id.qty_available
        self.f_demand_product_uom= self.f_product_id.uom_id
    
        domain = []
        if self.f_man_planning_id.f_mrp_wcg : 
            domain = [('type','=','product'),('f_is_manufactured','=',True),('f_mrp_wcg','=',self.f_man_planning_id.f_mrp_wcg.id)]
        if self.f_man_planning_id.f_mrp_categ :
             domain += [('type','=','product'),('f_is_manufactured','=',True),('f_mrp_categ','=',self.f_man_planning_id.f_mrp_categ.id)]
    
        elif not self.f_man_planning_id.f_mrp_categ or not self.f_man_planning_id.f_mrp_wcg:
            domain += [('type','=','product'),('f_is_manufactured','=',True)]
       
        print('domain',domain)    
        return   {'domain':{'f_product_id':domain }}
    
    
    

    
    f_initial_qty =fields.Char(string="Initial Quantity", default = onChangeProduct,copy=True)
    
    f_priority =fields.Selection([('0', 'Normal'),('1', 'Good'),('2', 'Very Good'),('3', 'Excellent'),('4', 'Very Excellent'),('5', 'Full')],string="Priority")
    f_mp_status =fields.Selection([('draft', 'Draft'),('running', 'Running'),('done', 'Done'),('cancel', 'Cancelled'),('onhold', 'On Hold')],string="Status", default = 'draft')
    company_id = fields.Many2one('res.company',string="Company")
    f_shift_one_qty =fields.Float(string="Shift 1 Qty")
    f_shift_two_qty =fields.Float(string="Shift 2 Qty")
    f_shift_three_qty =fields.Float(string="Shift 3 Qty")
   
    def get_mo_values(self,rec,bill_of_material,shift_qty,shift_num,shift_responsible):

            return {   
                   'origin': rec.f_man_planning_id.f_man_planning_name,          
                   'product_id':rec.f_product_id.id,
                   'product_qty':shift_qty,
                   'product_uom_id' :rec.f_demand_product_uom.id,
                   'date_planned_start' :datetime.today(),
                   'date_planned_finished':rec.f_man_planning_id.f_date_end,
                   'f_man_plan_id':rec.f_man_planning_id.id,
                   'user_id' : shift_responsible.id,                  
                   'bom_id':bill_of_material.id,
                   'workcenter_id': rec.f_work_center.id,
                   'f_shift':shift_num,
                   'f_batch_num':rec.f_man_planning_id.f_batch_number,
                                       }
    #Create MO for each Shift Qty Conditions , default bill o material true in BOM for each product
    def create_man_order(self):

        new_orders = False
        for rec in self:
            if ( rec.f_shift_one_qty > 0 or rec.f_shift_two_qty > 0 or rec.f_shift_three_qty > 0 ) and rec.f_mp_status in ('draft','running'):
                bill_of_material =self.env['mrp.bom'].sudo().search([('product_tmpl_id','=',rec.f_product_id.product_tmpl_id.id),('f_default_bom','=',True)])
                if bill_of_material :

                    if rec.f_shift_one_qty > 0 :
                       
                        shift_num_1 =self.env['f.shift'].search([('f_increment_num','=',1)])
                        shift_1 = shift_num_1.id
                        mo_values_1 = self.get_mo_values(rec,bill_of_material,rec.f_shift_one_qty,shift_1,rec.f_man_planning_id.f_responsible)
                        man_order_1 = rec.env['mrp.production'].sudo().create(mo_values_1)
                        man_order_1.action_confirm()

                    if rec.f_shift_two_qty  >0 :
                       
                        shift_num_2 =self.env['f.shift'].search([('f_increment_num','=',2)])
                        mo_values_2 = self.get_mo_values(rec,bill_of_material,rec.f_shift_two_qty,shift_num_2.id,rec.f_man_planning_id.f_responsible)
                        man_order_2 = rec.env['mrp.production'].sudo().create(mo_values_2)
                        man_order_2.action_confirm()

                    if rec.f_shift_three_qty >0 :
                        shift_num_3 =self.env['f.shift'].search([('f_increment_num','=',3)])
                        mo_values_3 = self.get_mo_values(rec,bill_of_material,rec.f_shift_three_qty,shift_num_3.id,rec.f_man_planning_id.f_responsible)
                        man_order_3= rec.env['mrp.production'].sudo().create(mo_values_3)
                        man_order_3.action_confirm()

                    new_orders = True
                    rec.f_mp_status = 'running'
                    rec.f_shift_one_qty =0  
                    rec.f_shift_two_qty =0
                    rec.f_shift_three_qty =0
          
        if new_orders : 
            self.compute_analyze_quantities()
            return {
                    'type': 'ir.actions.act_window',
                    'name':'Manufacturing Order',
                    'view_mode': 'tree,form',
                    'res_model': 'mrp.production',
                    'domain':[('f_man_plan_id','=',rec.f_man_planning_id.id)],
                    }  
            
    @api.depends('f_demand_qty')
    def compute_analyze_quantities(self):

        remaining_qty =0.0
            
            
        mo_result_done =self.env['mrp.production'].read_group([('f_man_plan_id','=',self.f_man_planning_id.id),('state','=','done'),('state','!=','cancel')],['qty_producing','product_id','product_uom_id','workcenter_id'],['product_id','product_uom_id','workcenter_id'],lazy=False)    
        mo_result_not_done =self.env['mrp.production'].read_group([('f_man_plan_id','=',self.f_man_planning_id.id),('state','not in',('done','cancel'))],['product_qty','product_id','product_uom_id','workcenter_id'],['product_id','product_uom_id','workcenter_id'],lazy=False)
        #in process quantities created outside the plan 
        mo_result_not_done_no_plan =self.env['mrp.production'].read_group([('f_man_plan_id','!=',self.f_man_planning_id.id),('state','not in',('done','cancel'))],['product_qty','product_id','product_uom_id','workcenter_id'],['product_id','product_uom_id','workcenter_id'],lazy=False)

        for line in self:
            line.f_inprocess_qty = 0
            line.f_done_qty = 0
            line.f_remaining_qty =0
            line.f_no_plan_qty =0
            
            print('res_no_plan',mo_result_not_done_no_plan) 
            for res_no_plan in mo_result_not_done_no_plan :
                print('res_no_plan>>>>>',res_no_plan,res_no_plan['workcenter_id'], line.f_work_center )  
                
                if line.f_product_id.id == res_no_plan['product_id'][0] and ( (line.f_work_center and res_no_plan['workcenter_id'] and  (line.f_work_center.id ==res_no_plan['workcenter_id'][0]) ) or (res_no_plan['workcenter_id'] == False and not  line.f_work_center )):
                    
                    print('res_uom',res_no_plan['product_uom_id'])
                    uom_ratio =self.env['uom.uom'].search([('id','=',res_no_plan['product_uom_id'][0])])
                    print('uom_ratio>>>>>>>>>>>>>',uom_ratio.ratio,res_no_plan['product_qty'])
                    line.f_no_plan_qty += res_no_plan['product_qty'] * uom_ratio.ratio
                    
                    
            for res in mo_result_not_done :
                print('res',res)  
                
                if line.f_product_id.id == res['product_id'][0] and ( (line.f_work_center and res['workcenter_id'] and  (line.f_work_center.id ==res['workcenter_id'][0]) ) or (res['workcenter_id'] == False and not  line.f_work_center )): 
                    
                        print('res_uom',res['product_uom_id'])
                        uom_ratio =self.env['uom.uom'].search([('id','=',res['product_uom_id'][0])])
                        print('uom_ratio>>>>>>>>>>>>>',uom_ratio.ratio,res['product_qty'])
                        line.f_inprocess_qty += res['product_qty'] * uom_ratio.ratio
                        
                    
            for res_d in mo_result_done:
                print('res_d',res_d)
                if line.f_product_id.id == res_d['product_id'][0] and ( (line.f_work_center and res_d['workcenter_id'] and  (line.f_work_center.id ==res_d['workcenter_id'][0]) ) or (res_d['workcenter_id'] == False and not  line.f_work_center )):
                    
                        uom_ratio_done =self.env['uom.uom'].search([('id','=',res_d['product_uom_id'][0])])      
                        line.f_done_qty += res_d['qty_producing'] *  uom_ratio_done.ratio
                
            demand_uom_ratio =self.env['uom.uom'].search([('id','=',line.f_product_uom.id)])
            
            remaining_qty = (line.f_demand_qty*demand_uom_ratio.ratio) -line.f_done_qty -line.f_inprocess_qty 
            line.f_remaining_qty = remaining_qty
            if remaining_qty < 0 :
                line.f_remaining_qty =0.0

