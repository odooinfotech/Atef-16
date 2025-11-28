# -*- coding: utf-8 -*-

from odoo import models, tools, api, fields



                    

class cashBasisReport(models.Model):

    _name = "fs.cash.basis"
    _description = "Cash Basis Report"
    _auto = False
    _order = 'date asc , id asc'

    
    date = fields.Date(string='Date',store=True)
    account_id = fields.Many2one('account.account', string='Account',store=True)
    balance = fields.Monetary(string="Functional Balance", readonly=True,store=True,currency_field='f_company_currency')
    amount_currency=fields.Monetary(string="Amount Currency",readonly=True,store=True,currency_field='currency_id')
    cash_basis=fields.Many2one('f.cash.basis',string='Cash Basis', readonly=True)
    move_id = fields.Many2one('account.move',string="Move", readonly=True)
    f_company_currency=fields.Many2one('res.currency',string="Company Currency",readonly=True,store=True)
    currency_id=fields.Many2one('res.currency',string="Currency" ,readonly=True,store=True)
    type = fields.Char(string="Reference" ,readonly=True,store=True)
    paymenttype = fields.Char(string="Type" ,readonly=True,store=True)
    acum_balance = fields.Monetary('Total Balance', readonly=True , default=0,currency_field='f_company_currency')
    label = fields.Char(string="Label" ,readonly=True,store=True)
    
   
    
    def init(self):
        tools.drop_view_if_exists(self._cr, 'fs_cash_basis')
        self.env.cr.execute('''
            CREATE OR REPLACE VIEW fs_cash_basis AS (
            
            
            SELECT  
            sum(balance) over( order by date asc ,id asc ) as acum_balance,   
            id,
            currency_id,
             f_company_currency,
                date,
               account_id,
               move_id,
                cash_basis,
             ---  CASE WHEN l.amount_currency = 0 THEN l.balance ELSE l.amount_currency END amount_currency,
               balance,
                paymenttype ,
                type,
                label,
                amount_currency
          
            
            
            
            from (
                  
                  
                  (
            SELECT l.id As id,
            case when l.currency_id is null then l.company_currency_id else l.currency_id  end currency_id,
              l.company_currency_id AS f_company_currency,

               CASE WHEN cb.is_checks = 'Y' THEN (case when app.due_date is null then l.date else app.due_date end  )ELSE l.date END date,
                --- old date   CASE WHEN cb.is_checks = 'Y' THEN (case when l.date_maturity is null then l.date else l.date_maturity end  )ELSE l.date END date,
                l.account_id AS account_id,
                l.move_id AS move_id,
                acct.f_cash_basis AS cash_basis,
             ---  CASE WHEN l.amount_currency = 0 THEN l.balance ELSE l.amount_currency END amount_currency,
               l.balance AS balance,
                cb.name as paymenttype ,
                 'Actual' as type,
                 acct.name as label,
                 CASE WHEN l.amount_currency = 0 THEN l.balance ELSE l.amount_currency END amount_currency
              from  account_account acct, f_cash_basis cb,account_move_line l
              left join account_move am on (am.id = l.move_id)
                left join account_payment app on (app.id = l.f_payment_id)
             WHERE     l.account_id = acct.id
              and  am.state IN ('posted')
               AND cb.id = acct.f_cash_basis
            AND acct.f_cash_basis IS NOT NULL    
            )
            
            
            union all
(
            select COALESCE((select max(id) from account_move_line  ),0) + f.id as id ,

f.currency_id as currency_id,
              c.currency_id AS f_company_currency,
                f.date as  date,
                null::integer as  account_id,
                null::integer AS move_id,
                null::integer cash_basis,
              --- 0 as  amount_currency,
               (f.amount ) / CASE COALESCE(f.currency_rate, 0) WHEN 0 THEN 1.0 ELSE f.currency_rate END AS balance,
                sf.name as  paymenttype ,
                'Sales Forecast' as type,
                f.label as label,
                f.amount as  amount_currency


          
            
            from f_sale_setup_amount f
            left join res_company c on (c.id = f.company_id)
            left join f_sale_forcaste_types sf on (sf.id = f.type_id)

            where f.date >= CURRENT_DATE
)
             union all

          (  select COALESCE((select max(id) from account_move_line ),0) + COALESCE((select max(id) from f_sale_setup_amount ),0)  + f.id as id ,

f.currency_id as currency_id,
              c.currency_id AS f_company_currency,
                f.date as date,
                null::integer as  account_id,
                null::integer AS move_id,
                null::integer cash_basis,
             ---  0 as  amount_currency,
              ( f.amount *-1) / CASE COALESCE(f.currency_rate, 0) WHEN 0 THEN 1.0 ELSE f.currency_rate END AS balance,
                sf.name as  paymenttype ,
                'Purchase Forecast' as type,
                f.label as label,
                f.amount*-1 as  amount_currency


          
            
            from f_po_setup_amount f 
            left join res_company c on (c.id = f.company_id)
            left join f_po_forcaste_types sf on (sf.id = f.type_id)
            
             where f.date >= CURRENT_DATE



)


   union all

          (  select COALESCE((select max(id) from account_move_line ),0) + COALESCE((select max(id) from f_sale_setup_amount ),0) +COALESCE((select max(id) from f_po_setup_amount ),0) + f.id as id ,

                f.currency_id as currency_id,
              c.currency_id AS f_company_currency,
                f.date as date,
                null::integer as  account_id,
                null::integer AS move_id,
                null::integer cash_basis,
             ---  0 as  amount_currency,
               (f.amount *-1) / CASE COALESCE(f.currency_rate, 0) WHEN 0 THEN 1.0 ELSE f.currency_rate END  AS balance,
                sf.name as  paymenttype ,
                'Purchase Payment Forecast' as type,
                po.name as label,
                (f.amount *-1)  as  amount_currency


          
            
           from f_po_payment_forcaste f 
            left join f_po_payment_forcaste_types sf on (sf.id = f.f_name)
            left join purchase_order po on (po.id = f.purchase_id)
            left join res_company c on (c.id = f.company_id)


 where f.date >= CURRENT_DATE
)

            )cash_data
            
            
                
                     
                 
                  
                  )
        ''')
