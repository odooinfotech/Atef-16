from odoo import fields, models, api, _,tools
from datetime import datetime,timedelta,date
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from odoo.tools import date_utils
import calendar
import logging
_logger = logging.getLogger(__name__)



class FCustStatdetailedreport(models.TransientModel):
    _name= 'f.detailed.customer' 
    _description = "Customer Statement Wizard"
    
    def get_enddate(self):
        
        
        today = date.today()
        return today.strftime("%Y-%m-%d")
        
    
    def get_fromdate(self):
        today = date.today()
        date_m = datetime(today.year, today.month, 1)
        d_from = date_m.strftime("%Y-%m-%d")
        
        return d_from
    
            
   
    from_date = fields.Date("From Date")
    to_date = fields.Date("To Date")
    partner_id = fields.Many2one('res.partner', string='Partner',required=True)
    company_id = fields.Many2one('res.company', string='Company',
                              default=lambda self: self.env.user.company_id.id)
    
    account_type = fields.Selection([('receivable','receivable'),('payable','payable')],string="Account",default="receivable")
    include_details = fields.Boolean('Include Invoices Details')
    include_details_aging = fields.Boolean('Include Aging Details')
    include_details = fields.Boolean('Include Invoice Details')
    include_checkdetails = fields.Boolean('Include Check Details')
    include_check_endorsed_details = fields.Boolean('Include Not Colleted Check Details')
    lang = fields.Selection([('ar_001','Arabic'),('en_US','English'),('he_IL','Hebrew / עִבְרִי')],string="Language",default="ar_001")
    show_product_label = fields.Boolean('Show Product Desc Instead of Product  Name in Detailed Statement ')
    f_report = fields.Selection([('exl','List'),('pdf','PDF'),('breif_pdf','Summary PDF '),('breif_exl','Summary List')],string="Report Type",default="pdf")
    show_customer_info = fields.Boolean('Show  Customer Info in Detailed Statement ',default=True)

    include_details_aging_pay = fields.Boolean('Include Payable Aging Details')
    show_bounced_checks = fields.Boolean('Show Bounced Checks Balance',readonly=True)

    period_date = fields.Selection(
        [('jan', 'Jan'), ('feb', 'Feb'), ('mar', 'Mar'), ('apr', 'Apr'), ('may', 'May'), ('jun', 'Jun'), ('jul', 'Jul'),
         ('aug', 'Aug'),
         ('sep', 'Sep'), ('oct', 'Oct'), ('nov', 'Nov'), ('dec', 'Dec'),
         ('lastyear', 'Last Year'), ('year', 'This Financial Year '),('balance_zero','last Zero Balance')], default='year', string="Select Period ")

    @api.onchange('period_date')
    def get_today_filter(self):
        if self.env['ir.config_parameter'].sudo().get_param('f_customer_detailed_statement.f_show_bounce_checks_stat'):
            self.show_bounced_checks = True
        else:
            self.show_bounced_checks = False

        current_year = date.today().year
        if self.period_date == 'jan':
            self.from_date = date(current_year, 1, 1)
            self.to_date = date(current_year, 1, 31)

        if self.period_date == 'feb':
            last_day = calendar.monthrange(current_year, 2)[1]
            self.from_date = date(current_year, 2, 1)
            self.to_date = date(current_year, 2, last_day)

        if self.period_date == 'mar':
            self.from_date = date(current_year, 3, 1)
            self.to_date = date(current_year, 3, 31)

        if self.period_date == 'apr':
            self.from_date = date(current_year, 4, 1)
            self.to_date = date(current_year, 4, 30)

        if self.period_date == 'may':
            self.from_date = date(current_year, 5, 1)
            self.to_date = date(current_year, 5, 31)

        if self.period_date == 'jun':
            self.from_date = date(current_year, 6, 1)
            self.to_date = date(current_year, 6, 30)

        if self.period_date == 'jul':
            self.from_date = date(current_year, 7, 1)
            self.to_date = date(current_year, 7, 31)

        if self.period_date == 'aug':
            self.from_date = date(current_year, 8, 1)
            self.to_date = date(current_year, 8, 31)

        if self.period_date == 'sep':
            self.from_date = date(current_year, 9, 1)
            self.to_date = date(current_year, 9, 30)

        if self.period_date == 'oct':
            self.from_date = date(current_year, 10, 1)
            self.to_date = date(current_year, 10, 31)

        if self.period_date == 'nov':
            self.from_date = date(current_year, 11, 1)
            self.to_date = date(current_year, 11, 30)

        if self.period_date == 'dec':
            self.from_date = date(current_year, 12, 1)
            self.to_date = date(current_year, 12, 31)

        if self.period_date == 'year':
            today = fields.date.today()
            year = date_utils.subtract(today, year=0)
            self.from_date = date_utils.start_of(year, "year")
            self.to_date = date_utils.end_of(year, "year")
        #    self.to_date = today.strftime("%Y-%m-%d")

        if self.period_date == 'lastyear':
            today = fields.date.today()
            year = date_utils.subtract(today, year=current_year - 1)

            self.from_date = date_utils.start_of(year, "year")
            self.to_date = date_utils.end_of(year, "year")
    
    
    def _generalselect(self):
        return """
        
        select     
        
                    
                    
                    
                    sum(balance) over(partition by partner_id order by f_report_date asc ,f_last_upadeton asc ,id asc ) as acum_balance,  
                    sum(balance) over(partition by partner_id  order by f_report_date asc ,f_last_upadeton asc,id asc ) + credit - debt as f_initial_balance, 
                    nextval('f_customer_detailed_report_id_seq') AS id, 
                    invoice_id,
                    state,
                    date,
                    partner_id,
                    user_id,
                    company_id,
                    company_currency,
                    currency_id,
                    product_list,
                    f_user_id,
                    journal_id,
                    amount_total,
                    balance,
                    payment_id,
            employee_name,
            f_last_upadeton,
               account_type,
                amount_cuurency,
               type,
            debt,
            credit,
            ref,
            check_bounce,
            f_note,
            f_report_date
            
            
        
        """
        
        
    def _initselect(self):
        return """
        
        select     
        
                    
                    
                    
                   
                    id,
                    invoice_id,
                    state,
                    date,
                    partner_id,
                    user_id,
                    company_id,
                    company_currency,
                    currency_id,
                    product_list,
                    f_user_id,
                    journal_id,
                    amount_total,
                    balance,
                    payment_id,
            employee_name,
            f_last_upadeton,
               account_type,
                amount_cuurency,
               type,
            debt,
            credit,
            ref,
            check_bounce,
            f_note,
            f_report_date
            
            
        
        """
        
        
        
        
    def _BEGentryselect(self):
        print("datetet",self.from_date- timedelta(days=1))
        return """
         SELECT
         
         
         -1 as id,
                   
                   NULL::integer as invoice_id,
                    NULL::integer as payment_id,
                    '' as state,
                    date('%s') as date,
                   date('%s') as f_report_date,
                    m_l.partner_id as partner_id,
                    NULL::integer as user_id,
                    m.company_id as company_id,
                    m_l.company_currency_id as currency_id,
                    m_l.company_currency_id as company_currency,
                    '' as product_list,
                  %s as    f_user_id,
                    NULL::integer as journal_id,
                    COALESCE(SUM(m_l.debit - m_l.credit ),0)as balance,
                    0 as amount_total,
                    '' as  employee_name,
                    date('%s') as f_last_upadeton,
                    '' as account_type,
                   0 as amount_cuurency,
                    'beg_bal' as type,
                    
                    0 as debt,
                    0 as credit,
                    'Beg.Balance' as ref,
                    0 as check_bounce,
                    '' as f_note
                    
         
         
         
         
         
         
         """%(self.from_date ,self.from_date- timedelta(days=1),self.env.user.id,self.from_date- timedelta(days=1))
    
    
    
    
    def _BEGentryfrom(self):
        return """  
         FROM 
         account_move_line as m_l
                left join account_move m on(m.id=m_l.move_id)
                left join  account_account ac on(ac.id=m_l.account_id) 
               --- left join account_account_type acc on( ac.user_type_id=acc.id)
                left join  account_journal aj on(aj.id = m.journal_id)
                left join account_payment pay on(pay.id = m.payment_id)
        LEFT JOIN res_partner pat ON (pat.id = m_l.partner_id)
               
                  
                 
              
         
         
         """
         
    def _BEGwhere(self):
        where_str = """
            WHERE
               
                    m.state IN ('posted')
                    and
                   ac.account_type in('asset_receivable','liability_payable')
                    
                    and
                    m_l.partner_id = %s
                   and COALESCE(m.f_exclude_entry, FALSE) = FALSE
                     and m.date <  date('%s') 
                       and m.company_id = %s
                   
        """%(self.partner_id.id,self.from_date,self.env.company.id)

        return where_str   
    
    
    def _BEGgroup_by(self): 
        return"""
         Group By m_l.partner_id,m.company_id ,m_l.company_currency_id
        """    

    #############################################
        
        
    def _entryselect(self):
        return """
         SELECT
         
         
         m_l.id as id,
                   
                    m.id as invoice_id,
                    pay.id as payment_id,
                    m.state as state,
                    m.date as date,
                    m.date as f_report_date,
                    m_l.partner_id as partner_id,
                    m.invoice_user_id as user_id,
                    m.company_id as company_id,
                    m_l.currency_id as currency_id,
                     m_l.company_currency_id as company_currency,
                       prod_list.product_list_val as product_list ,
                       %s as    f_user_id,
                    aj.id as journal_id,
                    (m_l.debit - m_l.credit )as balance,
                    0 as amount_total,
                    '' as  employee_name,
                    m.create_date as f_last_upadeton,
                    ac.account_type as account_type,
                    m_l.amount_currency as amount_cuurency,
                    m.move_type as type,
                    
                    m_l.debit as debt,
                    m_l.credit as credit,
                    m.name as ref,
                    case when (pay.check_state = 'bounced') then (m_l.balance) else 0 end as check_bounce,
                     m.f_note   as f_note
                    
         
         
         
         
         
         
         """%(self.env.user.id)
    
    
    
    
    def _entryfrom(self):
        return """  
         FROM 
         account_move_line as m_l
                left join account_move m on(m.id=m_l.move_id)
                left join product_product pp on(pp.id = m_l.product_id)
                left join product_template pt on(pt.id = pp.product_tmpl_id)
                left join  account_account ac on(ac.id=m_l.account_id) 
               --- left join account_account_type acc on( ac.user_type_id=acc.id)
                left join  account_journal aj on(aj.id = m.journal_id)
                left join account_payment pay on(pay.id = m.payment_id)
        LEFT JOIN res_partner pat ON (pat.id = m_l.partner_id)
        
        
        left join (

                    select   m_list.id as id   ,string_agg(pt_list.name->>'en_US' || '/ ' || ml_list.quantity || '/ ' ||ml_list.price_unit , E'\n' )as product_list_val
                    from account_move m_list 
                    
                    left join  account_move_line as ml_list on (ml_list.move_id = m_list.id   ) 
                     left join  account_account ac_list on(ac_list.id=ml_list.account_id) 
                    left join product_product pp_list on(pp_list.id = ml_list.product_id)
                     left join product_template pt_list on(pt_list.id = pp_list.product_tmpl_id)
                       WHERE
               
                    m_list.state IN ('posted')
                  ---  and
                  --- ac_list.account_type in('asset_receivable','liability_payable')
                    
                    and
                    ml_list.partner_id = %s
                   and COALESCE(m_list.f_exclude_entry, FALSE) = FALSE
                   and m_list.company_id = %s
                   and ml_list.product_id is not null
                  and  m_list.date <=  date('%s') and m_list.date >=   date('%s') 
                     group by m_list.id
                   
       
                  

                   
        
        ) prod_list on (m.id = prod_list.id)
              

             

         
         """%(self.partner_id.id,self.env.company.id,self.to_date,self.from_date)
               

         
    def _where(self):
        where_str = """
            WHERE
               
                    m.state IN ('posted')
                    and
                   ac.account_type in('asset_receivable','liability_payable')
                    
                    and
                    m_l.partner_id = %s
                   and COALESCE(m.f_exclude_entry, FALSE) = FALSE
                   and m.company_id = %s
                   
        """%(self.partner_id.id,self.env.company.id)

        return where_str
    
    
         
    def _debt_where(self):
        
        wherestr = """   where debt.partner_id = %s
        """%(self.partner_id.id)  
        
        
     
        
        
        return wherestr
        
        
        

        
    def _details_where(self):
        
        wherestr = """  WHERE
        details.date <=  date('%s') and details.date >=   date('%s') 
        """%(self.to_date,self.from_date,) 
        
        
        return wherestr   



    def _get_multi_payment_select(self):

        return """"""


    def _get_po_select(self):
            return """"""


    
         
    def _query(self):
        return """
            
            
             %s
                        FROM
                        (
                       %s
                      FROM (
                        
                        (
                            %s
                            %s
                            %s
                            )
                            
                              Union all    
                                  (%s
                                %s
                                 %s
                                %s) 



                                %s


                                %s
                
                )debt
             %s
                
                           
                            
                            
                            )details
                %s
            
            
            
        """ % (
            self._generalselect(),self._initselect(), self._entryselect(), self._entryfrom(),self._where(),
            self._BEGentryselect(),self._BEGentryfrom(),self._BEGwhere(),self._BEGgroup_by(),
            
            self._get_multi_payment_select(),
            self._get_po_select(),
            
            self._debt_where(),self._details_where()
        )
         
 
         
         

         

    
    def f_get_data_dict(self):
        return {
            'include_details_aging':self.include_details_aging,
            'include_check_endorsed_details':self.include_check_endorsed_details,
            'f_date': self.from_date ,
            'to_date': self.to_date,
            'lang': self.lang ,
            'f_report':self.f_report,
            'partner_id':self.partner_id.id,
            'account_type':self.account_type,
            'include_details':self.include_details,
            'include_checkdetails':self.include_checkdetails,
            'show_product_label':self.show_product_label,
            'show_customer_info':self.show_customer_info,
            'include_details_aging_pay':self.include_details_aging_pay,
            'show_bounced_checks':self.show_bounced_checks,
            'period_date':self.period_date
            
            }

    def f_get_column_names(self):
        return """acum_balance,f_initial_balance,id,invoice_id,state,date,partner_id,user_id,company_id,company_currency,currency_id,product_list,f_user_id,journal_id,amount_total,balance,payment_id,employee_name,f_last_upadeton,account_type,amount_cuurency,type,debt,credit,ref,check_bounce,f_note,f_report_date"""
    
    def generate_salereport(self):

        # self.env.cr.execute(''' 
        # delete  from f_customer_detailed_report  where f_user_id = %s
        #   ''' % (self.env.user.id))

        old_data = self.env['f.customer.detailed.report'].sudo().search(
                    [('f_user_id','=',self.env.user.id)])
        if old_data :
            old_data.unlink()

        columns = self.f_get_column_names().replace('\n', '').replace(' ', '')
        query = self._query()

        full_sql = f"""
            INSERT INTO f_customer_detailed_report ({columns})
            {query}
        """

        self.env.cr.execute(full_sql)




        #self.env.cr.execute("""CREATE or REPLACE VIEW f_customer_detailed_report as (%s)""" % ( self._query()))
        ids_balance_zero = []
        if self.period_date == 'balance_zero':
            ids_balance = self.env['f.customer.detailed.report'].sudo().search(
                [('acum_balance', '=', 0),('f_user_id','=',self.env.user.id)], order='f_report_date desc ,f_last_upadeton desc , id desc', limit=1)
            if ids_balance:
                ids_final = self.env['f.customer.detailed.report'].sudo().search(
                    [('date', '>', ids_balance.date),('f_user_id','=',self.env.user.id), ('partner_id', '=', self.partner_id.id),
                     ('company_id', '=', self.env.company.id)], order='f_report_date asc ,f_last_upadeton asc ,id asc')
                if len(ids_final.ids) > 0 :
                    ids_balance_zero = ids_final.ids



        
        if len(ids_balance_zero)> 0 :
            domain = [('company_id', '=', self.env.company.id),('id','in',ids_balance_zero),('f_user_id','=',self.env.user.id)]
        else:
            domain = [('company_id', '=', self.env.company.id),('f_user_id','=',self.env.user.id)]
        if self.f_report == 'exl':
            tree_id = self.env.ref('f_customer_detailed_statement.view_report_partner_detailedt_tree').id  
            form_id = False
            action = {
                'name':_('Partner Statement Report'),
                'type': 'ir.actions.act_window',
                'view_mode': 'tree',
                'res_model': 'f.customer.detailed.report',
                'domain':domain,
                'view_id':tree_id,
                }
            
            return action  
        
        
        if self.f_report == 'breif_exl':
            tree_id = self.env.ref('f_customer_detailed_statement.view_report_partner_thermaldetailedt_tree').id  
            form_id = False
            action = {
                'name':_('Summary Partner Statement  Report'),
                'type': 'ir.actions.act_window',
                'view_mode': 'tree',
                'res_model': 'f.customer.detailed.report',
                'domain':domain,
                'view_id':tree_id,
                }
            
            return action  

        today = date.today()
        d1 = today.strftime("%Y-%m-%d")

        if not self.to_date:
            self.to_date = d1
        date_m = datetime(today.year, today.month, 1)
        d_from = date_m.strftime("%Y-%m-%d")

        if not self.from_date :
            self.from_date = d_from
            
      
        data = self.f_get_data_dict()
        print('final data',data)
        if self.f_report == 'pdf':
            return self.env.ref('f_customer_detailed_statement.f_custstatdetaild_report').report_action(self, data=data)
        
        if self.f_report == 'breif_pdf':
            return self.env.ref('f_customer_detailed_statement.f_custstatdetaild_thermalreport').report_action(self, data=data)


    
