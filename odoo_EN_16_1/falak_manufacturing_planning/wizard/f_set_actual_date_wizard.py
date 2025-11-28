from odoo import models, fields, api
from datetime import datetime,date
from odoo.exceptions import  ValidationError



class FSetActualDateWizard(models.TransientModel):
    _name='f.set.actual.date.wizard'
    
    f_actual_date = fields.Date(string='Actual Production Date',default=lambda self: date.today())
    #f_mrp_orders = fields.One2many('mrp.production',string='mrp orders')
    
    
    def f_set_date(self):
        orders_ids = self._context.get('f_mrp_orders')
        orders = self.env['mrp.production'].sudo().search([('id','in',orders_ids)])
        for order in orders:
            order.f_actual_production_date = self.f_actual_date
            
        res = self._context.get('result')
      
        
        return res