# -*- coding: utf-8 -*-


from odoo import tools
from odoo import models, fields, api



class JOReportInvoiceWithPaymentCustom(models.AbstractModel):
    _name = 'report.products_reports.jo_report_product_temp'

    @api.model
    def _get_report_values(self, docids, data=None):
        print("111111")
        report = self.env['ir.actions.report']._get_report_from_name('products_reports.jo_report_product_labels')
        if data and data.get('form') and data.get('form').get('user_ids'):
            docs = self.env['product.template'].browse(data['form']['user_ids'])
        comapny_name = self.env.company_id.f_company_name
        print(comapny_name,"comapny_name")
        return {
                'doc_model': report.model,
                'docs': self.env['product.template'].browse(data.get('ids')),
                'data': data,
          
                }
        
        
class JOReportproductCustom(models.AbstractModel):
    _name = 'report.products_reports.jo_report_product_product'

    @api.model
    def _get_report_values(self, docids, data=None):
        
        report = self.env['ir.actions.report']._get_report_from_name('products_reports.jo_report_product_prod_labels')
        if data and data.get('form') and data.get('form').get('user_ids'):
            docs = self.env['product.product'].browse(data['form']['user_ids'])
        
        return {
                'doc_model': report.model,
                'docs': self.env['product.product'].browse(data.get('ids')),
                'data': data,
               
                }

