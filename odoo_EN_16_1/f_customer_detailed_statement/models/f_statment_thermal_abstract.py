
# -*- coding: utf-8 -*-

from odoo import models, tools, api, fields,_

from datetime import datetime,timedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT



class FReportThermalCustStatement(models.AbstractModel):

    _name = 'report.f_customer_detailed_statement.thermalfreport_detial'
    _description = "Thermal Statement Report"
    
    
    def get_check_endorsed_data(self,f_date=False,to_date=False,partner_id=False):
        
        endorsed_checks = self.env['account.payment'].search([('partner_id','=',partner_id),('company_id','=',self.env.company.id),('check_state','in',('in_check_box','under_collection','bounced','endorsed')),('state','=','posted')])
        groups={}
        sum_endorsed_checks = 0
        for a in endorsed_checks:
            if a.exchange_rate == 0:
                a.exchange_rate = 1
                
                
            if a.check_state in ('in_check_box','under_collection','bounced') :
                    dic_name = a.id
                    if not groups.get(dic_name):
                        groups[dic_name] = {}
                        groups[dic_name].update({
                                'name': a.name,
                                'date':a.due_date,
                                'bank':a.bank_id.name,
                                'check_no':a.check_number,
                                'amount':a.amount,
                                'currency_id':a.currency_id,
                                'currency_name':a.currency_id.name,
                                'account_number':a.account_number,
                                'check_state':a.check_state,
                                'co_amount':a.amount_company_currency_signed,
                                
                               
                            })

                        sum_endorsed_checks = sum_endorsed_checks + groups[dic_name]['co_amount']
               
            if  a.check_state in ('endorsed') and to_date   <= (a.due_date + timedelta(days=10)).strftime("%Y-%m-%d"): 
                dic_name = a.id
                if not groups.get(dic_name):
                        groups[dic_name] = {}
                        groups[dic_name].update({
                                'name': a.name,
                                'date':a.due_date,
                                'bank':a.bank_id.name,
                                'check_no':a.check_number,
                                'amount':a.amount,
                                'currency_id':a.currency_id,
                                'currency_name':a.currency_id.name,
                                'account_number':a.account_number,
                                'check_state':a.check_state,
                                'co_amount':a.amount_company_currency_signed,
                                
                               
                            })
                        sum_endorsed_checks = sum_endorsed_checks + groups[dic_name]['co_amount']
                        
                        
         
        print('groups',groups)
        
        result = {
            
            'checks_end_values':groups,
            'sum_endorsed_checks':sum_endorsed_checks,
            
            }
        
        return result
    
    
        
        
    
    def get_aging_data(self,f_date=False,to_date=False,partner_id=False):
        self.env.cr.execute("""
        
        
       --- initial select 
          SELECT row_number() over()  as id,d.partner_id,company_id,
       CASE WHEN b1 < 0 THEN 0 ELSE b1 END days,
       CASE WHEN b2 < 0 THEN 0 ELSE b2 END days1,
       CASE WHEN b3 < 0 THEN 0 ELSE b3 END days2,
       CASE WHEN b4 < 0 THEN 0 ELSE b4 END days3,
       CASE WHEN b5 < 0 THEN 0 ELSE b5 END days4,
       CASE WHEN b6 < 0 THEN 0 ELSE b6 END days5,
       CASE WHEN b7 < 0 THEN 0 ELSE b7 END days6
       
       
        FROM(
        
        ---- first select 
             SELECT partner_id, company_id,  negative_balance,
               (CASE WHEN (bucket2 + bucket3 + bucket4 + bucket5 + bucket6 + bucket7 + negative_balance) < 0 THEN (bucket1 + bucket2 + bucket3 + bucket4 + bucket5 + bucket6 + bucket7 + negative_balance) ELSE bucket1 END) b1,
               (CASE WHEN (bucket3 + bucket4 + bucket5 + bucket6 + bucket7 + negative_balance) < 0 THEN (bucket2 + bucket3 + bucket4 + bucket5 + bucket6 + bucket7 + negative_balance) ELSE bucket2 END) b2,
               (CASE WHEN (bucket4 + bucket5 + bucket6 + bucket7 + negative_balance) < 0 THEN (bucket3 + bucket4 + bucket5 + bucket6 + bucket7 + negative_balance) ELSE bucket3 END) b3,
               (CASE WHEN (bucket5 + bucket6 + bucket7 + negative_balance) < 0 THEN (bucket4 + bucket5 + bucket6 + bucket7 + negative_balance) ELSE bucket4 END) b4,
               (CASE WHEN (bucket6 + bucket7 + negative_balance) < 0 THEN (bucket5 + bucket6 + bucket7 + negative_balance) ELSE bucket5 END) b5,
               (CASE WHEN (bucket7 + negative_balance) < 0 THEN (bucket6 + bucket7 + negative_balance) ELSE bucket6 END) b6,
               (bucket7 + negative_balance) b7
               
               
        FROM(
            ----- sec select 
             SELECT partner_id, company_id, 
                       COALESCE ( (bucket1), 0) bucket1,
                       COALESCE ( (bucket2), 0) bucket2,
                       COALESCE ( (bucket3), 0) bucket3,
                       COALESCE ( (bucket4), 0) bucket4,
                       COALESCE ( (bucket5), 0) bucket5,
                       COALESCE ( (bucket6), 0) bucket6,
                       COALESCE ( (bucket7), 0) bucket7,
                       COALESCE ( (negative_balance), 0) negative_balance 
                       
                       
        FROM(
            ----- third select 
              SELECT a.partner_id, a.company_id, 
                               bucket1, bucket2, bucket3, bucket4, bucket5,
                               bucket6, bucket7,  negative_balance
                               
                               
        FROM(
            ----- fourth select 
            SELECT m.partner_id,am.company_id, 
            SUM (CASE WHEN m.balance < 0  then  m.balance ELSE 0 END) AS negative_balance,
            SUM (CASE WHEN m.balance > 0  AND date (am.date) BETWEEN (date ('%s') - (%s)) AND date ('%s') THEN m.balance ELSE 0 END) AS bucket1,
            SUM (CASE WHEN m.balance > 0 AND date (am.date) BETWEEN (date ('%s') - (%s)*2) AND (date ('%s') - ((%s)+1)) THEN m.balance ELSE 0 END) AS bucket2,
            SUM (CASE WHEN m.balance > 0 AND date (am.date) BETWEEN (date ('%s') - (%s)*3) AND (date ('%s') - (((%s)*2)+1)) THEN m.balance ELSE 0 END) AS bucket3,
            SUM (CASE WHEN m.balance > 0 AND date (am.date) BETWEEN (date ('%s') - (%s)*6) AND (date ('%s') - (((%s)*3)+1)) THEN m.balance ELSE 0 END) AS bucket4,
            SUM (CASE WHEN m.balance > 0 AND date (am.date) BETWEEN (date ('%s') - (%s)*8) AND (date ('%s') - (((%s)*6)+1 )) THEN m.balance ELSE 0 END) AS bucket5,
            SUM (CASE WHEN m.balance > 0 AND date (am.date) BETWEEN (date ('%s') - (%s)*12 ) AND (date ('%s') - (((%s)*8)+1)) THEN m.balance ELSE 0 END) AS bucket6,
            SUM (CASE WHEN m.balance > 0 AND date (am.date) <= (date ('%s') - (((%s)*12)+1)) THEN m.balance ELSE 0 END) AS bucket7
            
            
            
           ----- fourth form
           FROM account_move_line m
        left join account_move am on (m.move_id = am.id)
        left join account_account ac on (m.account_id = ac.id)
        left join res_partner part on (part.id = m.partner_id)
         
         
         --- fourth where 
           WHERE
        am.state = 'posted'
        and ac.account_type in('asset_receivable','liability_payable')
        AND am.company_id = (%s)
        AND am.date <= ('%s')
        and m.partner_id = (%s)
         
        --- fourth group by 
             GROUP BY m.partner_id, am.company_id
           
        )a
        )b
        )c
        )d
        
     
        
        
        
        """%(to_date,30,to_date,
            to_date,30,to_date,30,
            to_date,30,to_date,30,
            to_date,30,to_date,30,
            to_date,30,to_date,30,
            to_date,30,to_date,30,
            to_date,30,
            self.env.company.id,to_date,partner_id ) 
    )
        
        aging_values = self.env.cr.fetchone() 
        print('aging_values',aging_values)
        
        result = {
            
            'aging_values':aging_values,
            
            }
        
        return result
        
        
        
        
    
    @api.model
    def get_total_stat(self, f_date=False,to_date=False,partner_id=False,account_type=False,currency_id=False):
        print("111111111111111111111111111111",f_date)
        opening_balance = 0.0

        open_bl = self.env['f.customer.detailed.report'].search([('partner_id','=',partner_id),('f_report_date','<',f_date)], order = 'f_report_date desc ,f_last_upadeton desc ,id desc',limit=1)
        print("222222222222222222",open_bl.acum_balance)
            
        opening_balance = open_bl.acum_balance
        print(opening_balance,"opening_balance")
        
        
        stat = self.env['f.customer.detailed.report'].search([('partner_id','=',partner_id),('f_report_date','<=',to_date),('f_report_date','>=',f_date)])
        
        debt = 0.0
        credit=0.0
        balance=0.0
        for x in stat:
            debt = debt +x.debt
            credit = credit +x.credit
            
         
          
        final_bala = self.env['f.customer.detailed.report'].search([('partner_id','=',partner_id),('f_report_date','<=',to_date),('f_report_date','>=',f_date)], order = 'f_report_date desc ,id desc',limit=1)   
        if final_bala:
            balance = balance+final_bala.acum_balance 
        else:
            balance = balance+opening_balance  
            
        
   

        
        result = {
            
            'opening_balance':opening_balance,
            'debt':debt,
            'credit':credit,
            'balance':balance,
            }
            
        print("result",result)
        return  result 
            
            
        
            
    
    
    
    @api.model
    def _get_report_values(self, docids, data=None):
        
        data = dict(data or {})
        data.update(self.get_total_stat(data['f_date'],data['to_date'],data['partner_id'],data['account_type']))
        
        data.update(self.get_aging_data(data['f_date'],data['to_date'],data['partner_id']))
        
        
        data.update(self.get_check_endorsed_data(data['f_date'],data['to_date'],data['partner_id']))
        
        
          
                
        partner = self.env['res.partner'].search([('id','=',data['partner_id'])])   
        ids = self.env['f.customer.detailed.report'].search([('partner_id','=',data['partner_id']),('date','<=',data['to_date']),('date','>=',data['f_date'])])
        print("dayta",data)
        
        
        return {
            'doc_ids': self.env['f.customer.detailed.report'].search([('partner_id','=',data['partner_id']),('f_report_date','<=',data['to_date']),('f_report_date','>=',data['f_date'])]),
            'data': data,
            'partner_name':partner.name,
            'report_date': datetime.now().strftime("%Y-%m-%d"),
            'company':self.env.company.name,
            #'docs' : self.env['res.company'].browse(self.env.company.id),
        }
    
    
    
