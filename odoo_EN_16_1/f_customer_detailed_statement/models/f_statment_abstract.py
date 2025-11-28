
# -*- coding: utf-8 -*-

from odoo import models, tools, api, fields,_

from datetime import datetime,timedelta,date
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT



class FReportCustStatement(models.AbstractModel):

    _name = 'report.f_customer_detailed_statement.freport_detial'
    _description = "Statement Report"
    
    def get_check_endorsed_data(self,f_date=False,to_date=False,partner_id=False):

        sum_bounced_checks = 0
        bounced_checks = self.env['account.payment'].sudo().search([('partner_id','=',partner_id),('company_id','=',self.env.company.id),('check_state','=','bounced'),('state','=','posted')],order='due_date asc')
        for rec in bounced_checks:
            sum_bounced_checks = sum_bounced_checks+ rec.amount_company_currency_signed

        endorsed_checks = self.env['account.payment'].sudo().search([('partner_id','=',partner_id),('company_id','=',self.env.company.id),('check_state','in',('in_check_box','under_collection','bounced','endorsed')),('state','=','posted')],order='due_date asc')
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
                                'pay_date':a.date,
                                
                               
                            })

                        sum_endorsed_checks = sum_endorsed_checks + groups[dic_name]['co_amount']
               
            if  a.check_state in ('endorsed') and date.today()  <= (a.due_date + timedelta(days=10)): 
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
                                'pay_date':a.date,
                                
                               
                            })
                        sum_endorsed_checks = sum_endorsed_checks + groups[dic_name]['co_amount']
                        
                        
         
        print('groups',groups)
        
        result = {
            
            'checks_end_values':groups,
            'sum_endorsed_checks':sum_endorsed_checks,

            'sum_bounced_checks':sum_bounced_checks,
            
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
            SUM (CASE WHEN m.balance > 0 AND date (am.date) BETWEEN (date ('%s') - (%s)*4) AND (date ('%s') - (((%s)*3)+1)) THEN m.balance ELSE 0 END) AS bucket4,
            SUM (CASE WHEN m.balance > 0 AND date (am.date) BETWEEN (date ('%s') - (%s)*5) AND (date ('%s') - (((%s)*4)+1 )) THEN m.balance ELSE 0 END) AS bucket5,
            SUM (CASE WHEN m.balance > 0 AND date (am.date) BETWEEN (date ('%s') - (%s)*6 ) AND (date ('%s') - (((%s)*5)+1)) THEN m.balance ELSE 0 END) AS bucket6,
            SUM (CASE WHEN m.balance > 0 AND date (am.date) <= (date ('%s') - (((%s)*6)+1)) THEN m.balance ELSE 0 END) AS bucket7
            
            
            
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
        
     
        
        
        
        """%(datetime.today(),30,datetime.today(),
            datetime.today(),30,datetime.today(),30,
            datetime.today(),30,datetime.today(),30,
            datetime.today(),30,datetime.today(),30,
            datetime.today(),30,datetime.today(),30,
            datetime.today(),30,datetime.today(),30,
            datetime.today(),30,
            self.env.company.id,datetime.today(),partner_id ) 
    )
        
        aging_values = self.env.cr.fetchone() 
        print('aging_values',aging_values)
        
        result = {
            
            'aging_values':aging_values,
            
            }
        
        return result

    def get_payable_aging_data(self, f_date=False, to_date=False, partner_id=False):
        self.env.cr.execute("""


             SELECT row_number() over()  as id,d.partner_id,company_id,
               CASE WHEN b1 < 0 THEN 0 ELSE b1 END days,
               CASE WHEN b2 < 0 THEN 0 ELSE b2 END days1,
               CASE WHEN b3 < 0 THEN 0 ELSE b3 END days2,
               CASE WHEN b4 < 0 THEN 0 ELSE b4 END days3,
               CASE WHEN b5 < 0 THEN 0 ELSE b5 END days4,
               CASE WHEN b6 < 0 THEN 0 ELSE b6 END days5,
               CASE WHEN b7 < 0 THEN 0 ELSE b7 END days6


                FROM(
	
	SELECT partner_id, company_id,  negative_balance,
                       (CASE WHEN (bucket2 + bucket3 + bucket4 + bucket5 + bucket6 + bucket7 + negative_balance) < 0 THEN (bucket1 + bucket2 + bucket3 + bucket4 + bucket5 + bucket6 + bucket7 + negative_balance) ELSE bucket1 END) b1,
                       (CASE WHEN (bucket3 + bucket4 + bucket5 + bucket6 + bucket7 + negative_balance) < 0 THEN (bucket2 + bucket3 + bucket4 + bucket5 + bucket6 + bucket7 + negative_balance) ELSE bucket2 END) b2,
                       (CASE WHEN (bucket4 + bucket5 + bucket6 + bucket7 + negative_balance) < 0 THEN (bucket3 + bucket4 + bucket5 + bucket6 + bucket7 + negative_balance) ELSE bucket3 END) b3,
                       (CASE WHEN (bucket5 + bucket6 + bucket7 + negative_balance) < 0 THEN (bucket4 + bucket5 + bucket6 + bucket7 + negative_balance) ELSE bucket4 END) b4,
                       (CASE WHEN (bucket6 + bucket7 + negative_balance) < 0 THEN (bucket5 + bucket6 + bucket7 + negative_balance) ELSE bucket5 END) b5,
                       (CASE WHEN (bucket7 + negative_balance) < 0 THEN (bucket6 + bucket7 + negative_balance) ELSE bucket6 END) b6,
                       (bucket7 + negative_balance) b7


                FROM(
 
 
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
SELECT m.partner_id,am.company_id, 
                    SUM (CASE WHEN m.balance*-1 < 0  then  m.balance*-1 ELSE 0 END) AS negative_balance,
                    SUM (CASE WHEN m.balance*-1 > 0  AND date (am.date) BETWEEN (date ('%s') - (%s)) AND date ('%s') THEN m.balance*-1 ELSE 0 END) AS bucket1,
                    SUM (CASE WHEN m.balance*-1 > 0 AND date (am.date) BETWEEN (date ('%s') - (%s)*2) AND (date ('%s') - ((%s)+1)) THEN m.balance*-1 ELSE 0 END) AS bucket2,
                    SUM (CASE WHEN m.balance*-1 > 0 AND date (am.date) BETWEEN (date ('%s') - (%s)*3) AND (date ('%s') - (((%s)*2)+1)) THEN m.balance*-1 ELSE 0 END) AS bucket3,
                    SUM (CASE WHEN m.balance*-1 > 0 AND date (am.date) BETWEEN (date ('%s') - (%s)*4) AND (date ('%s') - (((%s)*3)+1)) THEN m.balance*-1 ELSE 0 END) AS bucket4,
                    SUM (CASE WHEN m.balance *-1> 0 AND date (am.date) BETWEEN (date ('%s') - (%s)*5) AND (date ('%s') - (((%s)*4)+1 )) THEN m.balance*-1 ELSE 0 END) AS bucket5,
                    SUM (CASE WHEN m.balance*-1 > 0 AND date (am.date) BETWEEN (date ('%s') - (%s)*6 ) AND (date ('%s') - (((%s)*5)+1)) THEN m.balance*-1 ELSE 0 END) AS bucket6,
                    SUM (CASE WHEN m.balance*-1 > 0 AND date (am.date) <= (date ('%s') - (((%s)*6)+1)) THEN m.balance*-1 ELSE 0 END) AS bucket7



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




                """ % (datetime.today(), 30, datetime.today(),
                       datetime.today(), 30, datetime.today(), 30,
                       datetime.today(), 30, datetime.today(), 30,
                       datetime.today(), 30, datetime.today(), 30,
                       datetime.today(), 30, datetime.today(), 30,
                       datetime.today(), 30, datetime.today(), 30,
                       datetime.today(), 30,
                       self.env.company.id, datetime.today(), partner_id)
                            )

        aging_values = self.env.cr.fetchone()
        print('aging_values', aging_values)

        result = {

            'payable_aging_values': aging_values,

        }

        return result
        
        
        
    
    @api.model
    def get_total_stat(self, f_date=False,to_date=False,partner_id=False,account_type=False,currency_id=False):
        print("111111111111111111111111111111",f_date)
        opening_balance = 0.0

        open_bl = self.env['f.customer.detailed.report'].search([('partner_id','=',partner_id),('f_user_id','=',self.env.user.id),('f_report_date','<',f_date)], order = 'f_report_date desc ,f_last_upadeton desc,id desc',limit=1)
        opening_balance = open_bl.acum_balance
        print(opening_balance,"opening_balance")
        
        
        stat = self.env['f.customer.detailed.report'].search([('partner_id','=',partner_id),('f_user_id','=',self.env.user.id)])
        
        debt = 0.0
        credit=0.0
        balance=0.0
        for x in stat:
            debt = debt +x.debt
            credit = credit +x.credit
            
         
          
        final_bala = self.env['f.customer.detailed.report'].search([('partner_id','=',partner_id),('f_user_id','=',self.env.user.id)], order = 'f_report_date desc ,f_last_upadeton desc ,id desc',limit=1)
        if final_bala :
            balance = balance+final_bala.acum_balance 
        else:
            balance = balance+opening_balance  
            
            
        self.env.cr.execute("""
                    select partner_id, sum(xbalance)as credit from (
                        select  partner_id, xbalance
                        from (
                        select p.id as partner_id,
                         
                          COALESCE(SUM(aml.debit - aml.credit ),0)as xbalance
                        from account_move_line aml,
                            account_move am , 
                            account_account ac, 
                            res_partner p
                        where aml.move_id = am.id
                        AND am.state = 'posted'
                        and am.company_id = %s
                      
                        AND  ac.id = aml.account_id
                          and  ac.account_type IN ('asset_receivable','liability_payable')
                        AND p.id = aml.partner_id
                       
                        group by p.id
                        ) s1 
                        ) s2 
                        where
                         partner_id =%s
                         
                        group by partner_id
                                   
                    """% (self.env.company.id,partner_id))
                    
                    
        total_balance = 0
        credit_result = self.env.cr.fetchone() 
        if credit_result:
            total_balance= credit_result[1] 
                        
                        
            
     
        
        
        
       
        result = {
            
            'opening_balance':opening_balance,
            'debt':debt,
            'credit':credit,
            'balance':balance,
            'total_balance':total_balance,
            }
        print("result",result)
        return  result 
            
            
        
            
    
    
    
    @api.model
    def _get_report_values(self, docids, data=None):
        
        data = dict(data or {})
        data.update(self.get_total_stat(data['f_date'],data['to_date'],data['partner_id'],data['account_type']))
        # partner aging data 
        
        data.update(self.get_aging_data(data['f_date'],data['to_date'],data['partner_id']))
        data.update(self.get_payable_aging_data(data['f_date'], data['to_date'], data['partner_id']))
        
        
        data.update(self.get_check_endorsed_data(data['f_date'],data['to_date'],data['partner_id']))
        
          
                
        partner = self.env['res.partner'].search([('id','=',data['partner_id'])])
        domain_ids= [('partner_id','=',data['partner_id']),('f_user_id','=',self.env.user.id)]
        ids_balance_zero = []
        if data['period_date'] == 'balance_zero':
            ids_balance = self.env['f.customer.detailed.report'].sudo().search(
                [('acum_balance', '=', 0)], order='f_report_date desc ,f_last_upadeton desc , id desc', limit=1)
            if ids_balance:
                ids_final = self.env['f.customer.detailed.report'].sudo().search(
                    [('date', '>', ids_balance.date), ('partner_id', '=', data['partner_id']),
                     ('company_id', '=', self.env.company.id)], order='f_report_date asc ,f_last_upadeton asc ,id asc')
                if len(ids_final.ids) > 0:
                    ids_balance_zero = ids_final.ids
        if len(ids_balance_zero) > 0:
            domain_ids = [('partner_id', '=', data['partner_id']),('id','in',ids_balance_zero),('f_user_id','=',self.env.user.id)]



        ids = self.env['f.customer.detailed.report'].search(domain_ids)
        print("dayta",data)
        
        
        return {
            'doc_ids': self.env['f.customer.detailed.report'].search(domain_ids),
            'data': data,
            'partner_name':partner.name,
            'partner_city':partner.city,
            'partner_ref':partner.ref,
            'report_date': datetime.now().strftime("%Y-%m-%d"),
            'company':self.env.company.name,
            'partner':partner,
            #'docs' : self.env['res.company'].browse(self.env.company.id),
        }
    
    
    
