# -*- coding: utf-8 -*-
from odoo import models, fields, api


class F_Mass_Manufacturing(models.Model):
    _name ='f.mass.man'
    _description = 'Mass Manufacturing Process'
    _inherit = ['mail.thread','mail.activity.mixin']
    _rec_name="f_mass_man_name"
    
    #fields
    f_mass_man_name =fields.Char(string="Mass Manufacturing Name"  ,index=True ,copy=False)
    f_responsible =fields.Many2one('res.users',string="Responsible" ,required=True,tracking=True ,copy=True)
    f_date = fields.Date(string='Date',required=True ,copy=True)
    f_plan_products =fields.One2many('f.mass.man.products','f_mass_man_id',string="Products" ,copy=True)
    f_man_order_count = fields.Integer(compute ='compute_man_order_count' , string="Manufacturing Orders",copy=False)
    f_mp_status =fields.Selection([('draft', 'Draft'),('done', 'Done'),('cancel', 'Cancelled')],string="Status", default = 'draft',copy=False,tracking=True)
    f_man_qty_count = fields.Integer(compute ='compute_man_qty_count',string="Products",copy=False)
    f_note = fields.Html(string="Note",copy=True)
    f_shift = fields.Many2one('f.shift',string='shift',copy=True)
    f_work_center =fields.Many2one('mrp.workcenter',string="Work Center",copy=True)
    active = fields.Boolean(string = 'Active', default=True)    
    
    
    @api.model
    def create(self, vals):
        print('VVVVVVVVVVVVVVVVVVVV')
        vals['f_mass_man_name'] = self.env['ir.sequence'].next_by_code('f.mass.man')
        return super(F_Mass_Manufacturing, self).create(vals)
    

 
    def compute_man_order_count(self):
        for record in self:
            record.f_man_order_count = self.env['mrp.production'].search_count([('f_mass_man_id', '=', record.id)]) 
    
    
            
    def action_view_man_order(self):
        self.ensure_one()
        return {
          'type': 'ir.actions.act_window',
          'name':'Manufacturing Orders',
          'view_mode': 'tree,form',
          'res_model': 'mrp.production',
          'domain': [('f_mass_man_id', '=', self.id)],
          'context':{'create':True,
                     'default_f_mass_man_id':self.id,
                       },
                } 
         
    def compute_man_qty_count(self):
        for record in self:
            record.f_man_qty_count = self.env['f.mass.man.products'].search_count([('f_mass_man_id', '=', record.id)]) 
                 
                 
    def action_view_man_qty(self):
        self.ensure_one()
        
        return {
          'type': 'ir.actions.act_window',
          'name':'Products',
          'view_mode': 'tree',
          'res_model': 'f.mass.man.products',
          'domain': [('f_mass_man_id', '=', self.id)],
          'context':{'default_f_mass_man_id':self.id,
                     'default_f_shift':self.f_shift.id,
                     'search_default_not_done':1,
                     },
                }    
      
 