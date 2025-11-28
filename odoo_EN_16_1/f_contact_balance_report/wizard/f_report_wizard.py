# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, tools, api, fields, _
from datetime import datetime,timedelta,date


class PartnerBlancerReport(models.TransientModel):
    _name = 'f.partner.allb.balance.wizard'
    _description = 'Partner Wizard Balance '


    def _get_enddate(self):
        today = date.today()
        return today.strftime("%Y-%m-%d")

    to_date = fields.Date("Date",default=_get_enddate)


    def _f_select(self):
        print('5555')
        return """
           select part.id as id ,
            part.ref as ref,
            part.id as partner_id,
            part.mobile as mobile,
            part.city as city,
            part.city_id as city_id,
            COALESCE(sum(m_l.balance ),0) as balance ,
            m.company_id as company_id,
            part.user_id as user_id,
            COALESCE(abs(sum(case when (pay.check_state = 'bounced') then (m_l.balance) else 0 end)),0) as check_bounce,
            COALESCE(sum(m_l.balance ),0) + COALESCE (abs(sum(case when (pay.check_state = 'bounced') then (m_l.balance) else 0 end)),0)  as balance_check_bounce
           """

    def _f_from(self):
        return """
              from res_partner part
            left join account_move_line m_l on (part.id = m_l.partner_id)
            left join account_move m on(m.id=m_l.move_id)
            left join  account_account ac on(ac.id=m_l.account_id) 
            left join account_payment pay on(pay.id = m.payment_id)
          
            
           """


    def _f_where(self):
        return """
              where 
            part.id is not null 
            and 
            m.state IN ('posted')
            and
            ac.account_type in('asset_receivable','liability_payable')

            and m.date <= date('%s')
           """%(self.to_date)


    def _f_group_by(self):
        return """
            group by part.id,part.ref, part.mobile,m.company_id,part.city 
           
           """


    def get_deatils(self):
        print('11111')
        tools.drop_view_if_exists(self.env.cr, 'f_contatc_balance_report')
        self.env.cr.execute("""
                CREATE OR REPLACE VIEW f_contatc_balance_report AS (
                
                %s
                %s
                %s
                %s
            
         
                )
                """
                            % (self._f_select(),self._f_from(),self._f_where(),self._f_group_by()))


        action = {
                'name':_('Partner Balances Report'),
                'type': 'ir.actions.act_window',
                'view_mode': 'tree',
                'res_model': 'f.contatc.balance.report',
                'domain':[('company_id', '=', self.env.company.id)],
                }
            
        return action 




    


        

