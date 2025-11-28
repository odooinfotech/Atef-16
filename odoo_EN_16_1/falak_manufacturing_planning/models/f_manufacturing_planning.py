# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class F_Manufacturing_Planning(models.Model):
    _name ='f.man.plan'
    _description = 'Manufacturing Planning Process'
    _inherit = ['mail.thread','mail.activity.mixin']
    _rec_name="f_man_planning_name"

    #fields
    f_man_planning_name =fields.Char(string="Manufacturing Plan Name" ,default='New' ,required=True ,index=True ,copy=False)
    
    @api.model
    def create(self, vals):
        vals['f_man_planning_name'] = self.env['ir.sequence'].next_by_code('f.man.plan')
        return super(F_Manufacturing_Planning, self).create(vals)
    

    def unlink(self):
        if self.f_man_order_count > 0:
            raise ValidationError("This plan has mrp, you Can't delete it !!")
        return super(F_Manufacturing_Planning, self).unlink()
    
    def get_department(self):
        department_id_xml_id = 'falak_manufacturing_planning.f_mrp_planning_department'
        department_id = self.env.ref(department_id_xml_id, raise_if_not_found=False)
        if department_id:
            return department_id.id
        else:
            return False
            

    
    #f_planning_order_for =fields.Many2one('f.planning.order',string="Planning Order For",copy=True)
    f_responsible =fields.Many2one('res.users',string="Responsible" ,required=True,tracking=True ,copy=True)
    f_date_start = fields.Date(string='Start Date',required=True ,copy=True)
    f_date_end = fields.Date(string='End Date', index=True, tracking=True,required=True ,copy=True )
    f_plan_products =fields.One2many('f.man.plan.products','f_man_planning_id',string="Products" ,copy=True)
    f_man_order_count = fields.Integer(compute ='compute_man_order_count' , string="Manufacturing Order")
    f_man_qty_count = fields.Integer(compute ='compute_man_qty_count' , string="Manufacturing Quantity")
    f_note = fields.Html(string="Note",copy=True)
    f_mp_status =fields.Selection([('draft', 'Draft'),('running', 'Running'),('done', 'Done'),('cancel', 'Cancelled'),('onhold', 'On Hold')],string="Status", default = 'draft',tracking=True,copy=False)
    active = fields.Boolean(default=True)
    f_user =fields.Many2one('res.users',string="User",compute="get_login_user",readonly=True)
    f_mrp_categ = fields.Many2one('f.mp.categ',string = 'MRP Category')
    f_batch_number =fields.Char(string="Batch Number")
    f_mrp_wcg= fields.Many2one('mrp.workcenter.management',string="Work Center Group")
    f_first_responsible =fields.Many2one('res.users',string="Shift 1 Responsible" )
    f_sec_responsible =fields.Many2one('res.users',string="Shift 2 Responsible" )
    f_third_responsible =fields.Many2one('res.users',string="Shift 3 Responsible" )
    
    f_department_id = fields.Many2one('hr.department',string="Department",default=get_department)
    f_first_employee =fields.Many2one('hr.employee',string="Shift 1 Responsible" ,required=True,tracking=True ,copy=True)
    f_sec_employee =fields.Many2one('hr.employee',string="Shift 2 Responsible" ,required=True,tracking=True ,copy=True)
    f_third_employee =fields.Many2one('hr.employee',string="Shift 3 Responsible" ,required=True,tracking=True ,copy=True)
    
    
    
    @api.onchange('f_department_id')
    def _onchange_f_department_id(self):
        # Update the domain of f_first_employee, f_sec_employee, and f_third_employee
        # based on the value of f_department_id
        if self.f_department_id:
            domain = [('department_id', '=', self.f_department_id.id)]
        else:
            domain = []

        return {
            'domain': {
                'f_first_employee': domain,
                'f_sec_employee': domain,
                'f_third_employee': domain,
            }
        }
    
    
    def get_login_user(self):
        uid = self.env['res.users'].search([('id', '=', self.env.uid)]) 
        loginuser = uid.name
        self.f_user =uid

    def compute_man_order_count(self):
        for record in self:
            record.f_man_order_count = self.env['mrp.production'].search_count([('f_man_plan_id', '=', record.id)]) 
            
    def action_view_man_order(self):
        self.ensure_one()
        return {
          'type': 'ir.actions.act_window',
          'name':'Manufacturing Order',
          'view_mode': 'tree,form',
          'res_model': 'mrp.production',
          'domain': [('f_man_plan_id', '=', self.id)],
          'context':{'create':True,
                     'default_f_man_plan_id':self.id,
                       },
                }  
    def compute_man_qty_count(self):
        for record in self:
            record.f_man_qty_count = self.env['f.man.plan.products'].search_count([('f_man_planning_id', '=', record.id)]) 
                 
    def action_view_man_qty(self):
        self.ensure_one()
        self.compute_analyze_quantities()
        return {
          'type': 'ir.actions.act_window',
          'name':'Planning Quantities',
          'view_mode': 'tree',
          'res_model': 'f.man.plan.products',
          'domain': [('f_man_planning_id', '=', self.id)],
          'context':{'default_f_man_planning_id':self.id,
                     'search_default_not_done':1,
                     },
                }    
      
    def compute_analyze_quantities(self):
        print('0979')
       #initial values

        remaining_qty =0.0
            
            
        mo_result_done =self.env['mrp.production'].read_group([('f_man_plan_id','=',self.id),('state','=','done'),('state','!=','cancel')],['qty_producing','product_id','product_uom_id','workcenter_id'],['product_id','product_uom_id','workcenter_id'],lazy=False)    
        mo_result_not_done =self.env['mrp.production'].read_group([('f_man_plan_id','=',self.id),('state','not in',('done','cancel'))],['product_qty','product_id','product_uom_id','workcenter_id'],['product_id','product_uom_id','workcenter_id'],lazy=False)
        #in process quantities created outside the plan 
        mo_result_not_done_no_plan =self.env['mrp.production'].read_group([('f_man_plan_id','!=',self.id),('state','not in',('done','cancel'))],['product_qty','product_id','product_uom_id','workcenter_id'],['product_id','product_uom_id','workcenter_id'],lazy=False)

        
        
        
        for line in self.f_plan_products:
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

     
     
    def f_get_min_qty_products(self):
        print('99')
        return {
          'type': 'ir.actions.act_window',
          'name':'Minimum Quantities For Products',
          'view_mode': 'form',
          'res_model': 'f.min.qty.prods',
          'target':'new',
          'context':{'f_mrp_plan':self.id,
                     'default_f_mrp_wcg': self.f_mrp_wcg.id,
                     'default_f_mrp_categ':self.f_mrp_categ.id}
                }     
        
        
    
