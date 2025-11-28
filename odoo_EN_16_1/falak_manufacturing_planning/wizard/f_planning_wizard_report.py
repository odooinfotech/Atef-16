from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import  ValidationError



class FPlanningReportWizard(models.TransientModel):
    _name='f.plan.report.wizard'
    _description ='MO Planning Products Report'
    
    f_plan_id =fields.Many2one('f.man.plan',string="Planning")
    f_date_from =fields.Date(string="From Date",default=datetime.today(),required=True)
    f_date_to = fields.Date(string="Date To",default=datetime.today(),required=True)
    f_shift =fields.Many2one('f.shift',string="Shift Number",required=True)
    f_work_center =fields.Many2one('mrp.workcenter',string="Work Center")
    
   
   
    @api.constrains('f_date_to', 'f_date_from')
    def date_constrains(self):

      if self.f_date_to < self.f_date_from:

            raise ValidationError('Sorry, Date To Must be greater Than From Date.')


    def generate_report(self):
        print('77777')
        mo_orders =self.env['mrp.production'].search([('f_man_plan_id','=',self.f_plan_id.id),('date_planned_start','>=',self.f_date_from),('date_planned_start','<=',self.f_date_to)])                         
        for mo_order in mo_orders:
            print('mo_order',mo_order.date_planned_start)
        if self.f_shift.f_increment_num == 1:
            responsible = self.f_plan_id.f_first_employee
        elif self.f_shift.f_increment_num == 2:
            responsible = self.f_plan_id.f_sec_employee
        elif self.f_shift.f_increment_num == 3:
            responsible = self.f_plan_id.f_third_employee
            
        data = {
                'f_plan_id':self.f_plan_id.f_man_planning_name,
                'f_date_from': self.f_date_from,
                'f_date_to': self.f_date_to,
                'f_shift': self.f_shift.f_shift,
                'f_work_center':self.f_work_center.name,
                'f_batch_number':self.f_plan_id.f_batch_number,
                'f_responsible':responsible.name,
                'f_note':self.f_plan_id.f_note,
                'mo_orders': mo_orders.ids,
                }
        print('99+',data)
        return self.env.ref('falak_manufacturing_planning.f_plan_shift_prods').report_action([], data=data)








        