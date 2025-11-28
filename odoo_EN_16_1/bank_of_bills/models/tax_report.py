# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, date, time, timedelta
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT



class f_tax_reportline(models.Model):
    
    _inherit = 'account.move.line'
    
    f_mobile_partner = fields.Char(related="move_id.f_mobile_partner" , string="Mobile No")
    f_tax_id_partner = fields.Char(related="move_id.f_tax_id_partner" , string = "Tax id")
    f_partners_name=fields.Char(related="move_id.f_partners_name" ,string="Partner")
    f_accounting_date = fields.Char(related="move_id.f_accounting_date" , string="Period")
    f_bill_date_dd = fields.Char(related="move_id.f_bill_date_dd", string= "Day")
    f_bill_date_mm = fields.Char(related="move_id.f_bill_date_mm", string= "Month")
    f_bill_date_yy = fields.Char(related="move_id.f_bill_date_yy", string= "Year")





class tax_report(models.Model):
   # _name = 'tax.report'
    _inherit = 'account.move'
    
    
    
    f_mobile_partner = fields.Char(related="partner_id.mobile" , string="Mobile No")
    f_tax_id_partner = fields.Char(related="partner_id.vat" , string = "Tax id")
    f_partners_name=fields.Char(related="partner_id.name" ,string="Vendor")
    f_accounting_date = fields.Char(compute='_get_date' , string="Period")
    f_bill_date_dd = fields.Char(compute='_get_day_date', string= "Day")
    f_bill_date_mm = fields.Char(compute='_get_month_date', string= "Month")
    f_bill_date_yy = fields.Char(compute='_get_year_date', string= "Year")
    
    



    @api.depends('date')
    def _get_date(self):
        DATETIME_FORMAT = "%Y-%m-%d"
        for record in self:
            date = record.date
            date_obj = datetime.strptime(str(date), DATETIME_FORMAT)  
            record.f_accounting_date = datetime.strftime(date_obj, '%b - %y')
            
            
            
            
    @api.depends('date')
    def _get_day_date(self):
        DATETIME_FORMAT = "%Y-%m-%d"
        for record in self:
            date = record.date
            date_obj = datetime.strptime(str(date), DATETIME_FORMAT)  
            record.f_bill_date_dd = datetime.strftime(date_obj, '%d') 
            
    @api.depends('date')
    def _get_month_date(self):
        DATETIME_FORMAT = "%Y-%m-%d"
        for record in self:
            date = record.date
            date_obj = datetime.strptime(str(date), DATETIME_FORMAT)  
            record.f_bill_date_mm = datetime.strftime(date_obj, '%m') 
            
            
            
            
    @api.depends('date')
    def _get_year_date(self):
        DATETIME_FORMAT = "%Y-%m-%d"
        for record in self:
            date = record.date
            date_obj = datetime.strptime(str(date), DATETIME_FORMAT)  
            record.f_bill_date_yy = datetime.strftime(date_obj, '%Y') 


        

        

    

