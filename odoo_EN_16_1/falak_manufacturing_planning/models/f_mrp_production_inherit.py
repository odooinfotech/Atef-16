# -*- coding: utf-8 -*-
from odoo import models, fields, api


class F_Mrp_Production_Inherit(models.Model):
    _inherit ='mrp.production'
    
    
    f_shift =fields.Many2one('f.shift',string="Shift")
    f_man_plan_id =fields.Many2one('f.man.plan',string="Manufacturing Plan")
    workcenter_id = fields.Many2one('mrp.workcenter', 'Work Center', readonly=True,
                                    states={'draft': [('readonly', False)]}, check_company=True,
                                    help="""Allow users to pass specific workcenter and
                                    replace Related BOM work center from the header automatically
                                    """)
    
    
    f_batch_num =fields.Char(string="Batch Number")
    f_actual_production_date = fields.Date(string='Actual Production Date',copy=True)
    
    def button_mark_done(self):
        
        res = super(F_Mrp_Production_Inherit,self).button_mark_done()
        for rec in self:
            if rec.f_man_plan_id:
                records = self.env['f.man.plan.products'].sudo().search([('f_man_planning_id','=',rec.f_man_plan_id.id)])
                records.compute_analyze_quantities()
        
        
        # return {
        #         'type': 'ir.actions.act_window',
        #         'name':'Set Actual Date',
        #         'view_mode': 'form',
        #         'res_model': 'f.set.actual.date.wizard',
        #         'target':'new',
        #         'context' : {
        #             'f_mrp_orders': self.ids,
        #             'result': res,
        #             'skip_f_set_date': True
        #             },
        #     } 
        
        return res 
        
            
        
    
    



    
        
        
        
        
