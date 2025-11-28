# -*- coding: utf-8 -*-

from odoo import models, tools, api, fields



                    

class cashBasisperiodtypeReport(models.Model):

    _name = "fs.cash.basis.period.type"
    _description = "Cash Basis Period Type Report"
    _auto = False
    _order = 'date asc , id asc'

    
    date = fields.Date(string='Date',store=True)
    balance = fields.Float(string="Functional Balance", readonly=True,store=True)
    type = fields.Char(string="Type" ,readonly=True,store=True)
    acum_balance = fields.Float('Total Balance', readonly=True , default=0)
    
   
    
    def init(self):
        tools.drop_view_if_exists(self._cr, 'fs_cash_basis_period_type')
        self.env.cr.execute('''
            CREATE OR REPLACE VIEW fs_cash_basis_period_type AS (
            
  
               SELECT  
            sum(balance) over(order by date asc,type) as acum_balance,   
            id,
                date,
               balance,
                type
          
            
            
            
            from (
            select 
            max(fs.id) as id ,
             date(date_trunc('month',fs.date) + interval '1 month' - interval '1 day') as date,
               sum(fs.balance) as balance,
                fs.type as type
                from fs_cash_basis fs
                group by date(date_trunc('month',fs.date) + interval '1 month' - interval '1 day'), fs.type
            
            ) cash_period
            
            
            )
            '''
            )