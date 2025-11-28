# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class FProductCustom(models.Model):
    _inherit = 'res.company'
    
    f_company_name = fields.Char("Company Name")



class CustomProductReport(models.Model):
    _inherit = "product.product"
    
     
   
    def product_report_print(self):
        
        datas = {'ids': self._ids,
                 'form': self.read()[0],
                
                 'model': 'product.product'}
        return self.env.ref('products_customs.product_product_rep').report_action(self, data=datas)
    
    
    
    
class CustomProducttemplateReport(models.Model):
    _inherit = "product.template"
    
   
    def product_report_print(self):
        datas = {'ids': self._ids,
                 'form': self.read()[0],
                 'model': 'product.template'}
        return self.env.ref('products_customs.product_template_rep').report_action(self, data=datas)
    
    
    
    