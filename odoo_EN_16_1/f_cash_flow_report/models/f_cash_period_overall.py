# -*- coding: utf-8 -*-

from odoo import models, tools, api, fields



                    

class cashBasisperiodoverallReport(models.Model):

    _name = "fs.cash.basis.period"
    _description = "Cash Basis Period Overall Report"
    _auto = False
    _order = 'date asc , id asc'

    
    date = fields.Date(string='Date',store=True)
    balance = fields.Float(string="Functional Balance", readonly=True,store=True)
    acum_balance = fields.Float('Total Balance', readonly=True , default=0)
    
   
    
    def init(self):
        tools.drop_view_if_exists(self._cr, 'fs_cash_basis_period')
        self.env.cr.execute('''
            CREATE OR REPLACE VIEW fs_cash_basis_period AS (
            
  
               SELECT  
            sum(balance) over(order by date asc) as acum_balance,   
            id,
                date,
               balance
          
            
            
            
            from (
            select 
            max(fs.id) as id ,
             date(date_trunc('month',fs.date) + interval '1 month' - interval '1 day') as date,
               sum(fs.balance) as balance
                from fs_cash_basis fs
                group by date(date_trunc('month',fs.date) + interval '1 month' - interval '1 day')
            
            ) cash_period
            
            
            )
            '''
            )