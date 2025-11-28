from odoo import models, tools, api, fields, _
from lxml import etree
from odoo.http import request
from datetime import datetime, timedelta, date


class f_falak_partner_brefi_balance_details(models.Model):
    _name = 'f.partner.breif.balance.report'
    _auto = False
    _order = 'balance desc'
    _description = 'Balance Report Details'

    partner_id = fields.Many2one('res.partner', string='Parner', readonly=True)
    mobile = fields.Char(string="Mobile", readonly=True)
    ref = fields.Char(string="Ref", readonly=True)

    balance = fields.Float(string='Based Balance', readonly=True)
    due_balance = fields.Float(string='Due Balance',  readonly=True)
    currency_balance = fields.Float(string=' Balance', readonly=True)
    check_returned = fields.Float(string='Returned Checks', readonly=True)
    check_undercollected = fields.Float(string='Un-collected Checks', readonly=True)

    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as
           select max(a.id) as id from product_product a
           """ % (self._table))


class f_falak_partner_general_balance_details(models.Model):
    _name = 'f.partner.general.balance.report'
    _auto = False
    _order = 'balance desc'
    _description = 'General Balance Report Details'

    partner_id = fields.Many2one('res.partner', string='Partner', readonly=True)
    ref = fields.Char(string="Ref", readonly=True)

    balance = fields.Float(string='Based Balance', readonly=True)
    general_balance = fields.Float(string=' Balance', readonly=True)
    check_returned = fields.Float(string='Returned Checks', readonly=True)

    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as
           select max(a.id) as id from product_product a
           """ % (self._table))


class f_falak_partner_brefi_balance_wizard(models.TransientModel):
    _name = 'f.partner.breif.balance.wizard'
    _description = 'Balance Report Wizard Details'

    def get_enddate(self):
        today = date.today()
        return today.strftime("%Y-%m-%d")

    to_date = fields.Date("Date", default=get_enddate)

    def _query(self):
        return """
        
        select part.id as id ,
        part.ref as ref,
        part.id as partner_id,
        part.mobile as mobile,
        COALESCE(sum( move.balance),0) as balance ,
        COALESCE(sum(move.currency_balance),0) as currency_balance,
        COALESCE(sum(move.check_returned),0) as check_returned,                  
        COALESCE(sum( move.check_undercollected),0) as check_undercollected,
         COALESCE(sum(move.due_balance),0) as due_balance
           
        from res_partner part
        left join (
            select m_l.partner_id,
            COALESCE(
                sum(
                    case when date(m.date) <= date('%s') then ((m_l.balance )) else 0 
                end), 0) as balance ,
            COALESCE(
                sum(
                    case when date(m.date) <= date('%s') then ((m_l.balance )) else 0 
                end) ,0) as currency_balance,
            COALESCE(
                SUM(
                    case when (td.f_is_returened = '1') then m_l.balance else 0 
                end),0)as check_returned,
            COALESCE(
                sum(
                    CASE WHEN ((DATE('%s') <=  date( pay.due_date) + %s) and pay.check_state in ('endorsed')) THEN 
                        COALESCE(pay.amount_company_currency_signed,0) ELSE 0 
                END) +
                sum(
                    CASE WHEN pay.check_state in ('in_check_box','under_collection','bounced') THEN 
                        COALESCE(pay.amount_company_currency_signed,0)  ELSE 0 
                END),0)as check_undercollected,

  sum(CASE WHEN date(m.date)<  date('%s') -  (case when (COALESCE(limit_de.aging,0) = 0 ) then %s else limit_de.aging end )  THEN COALESCE(m_l.debit,0) ELSE 0 END) -
         sum(COALESCE(m_l.credit,0) )
         as due_balance
            from account_move_line m_l 
                left join account_move m on(m.id=m_l.move_id)
                left join  account_account ac on(ac.id=m_l.account_id) 
                left join account_payment pay on(pay.id = m.payment_id)
                left join  f_type_details td on (td.id = ac.f_type_id)
        
        LEFT JOIN f_credit_limit_details limit_de ON( limit_de.f_partner_id = m_l.partner_id and limit_de.f_type_id = ac.f_type_id  )
        
            where m.state IN ('posted') 
                and ac.account_type in('asset_receivable','liability_payable')
                and m.company_id = %s
            group by  m_l.partner_id) move on (part.id = move.partner_id)
      
        where part.id = ANY(ARRAY[%s]) 
        group by part.id,part.ref, part.mobile
        """ % (self.to_date,
               self.to_date,
               datetime.today(),
               10,
               self.to_date,
                  30,
               self.env.company.id,
               self.env['res.partner'].browse(self.env.context.get('active_ids')).ids)

    def _general_query(self):
        return """

        select part.id as id ,
        part.ref as ref,
        part.id as partner_id,
        COALESCE(sum( move.balance),0) as balance ,
        COALESCE(sum(move.general_balance),0) as general_balance,
        COALESCE(sum(move.check_returned),0) as check_returned

        from res_partner part
        left join (
            select m_l.partner_id,
            COALESCE(
                sum(
                    case when date(m.date) <= date('%s') then ((m_l.balance )) else 0 
                end), 0) as balance ,
            COALESCE(
                SUM(
                    case when (td.f_is_general = '1') then m_l.balance else 0 
                end),0)as general_balance,
            COALESCE(
                SUM(
                    case when (td.f_is_returened = '1') then m_l.balance else 0 
                end),0)as check_returned
                
            from account_move_line m_l 
                left join account_move m on(m.id=m_l.move_id)
                left join  account_account ac on(ac.id=m_l.account_id) 
                left join account_payment pay on(pay.id = m.payment_id)
                left join  f_type_details td on (td.id = ac.f_type_id)

            where m.state IN ('posted') 
                and ac.account_type in('asset_receivable','liability_payable')
                and m.company_id = %s
            group by  m_l.partner_id) move on (part.id = move.partner_id)

        where part.id = ANY(ARRAY[%s]) 
        group by part.id,part.ref
        """ % (self.to_date,
               self.env.company.id,
               self.env['res.partner'].browse(self.env.context.get('active_ids')).ids)

    def get_deatils(self):
        tools.drop_view_if_exists(self.env.cr, 'f_partner_breif_balance_report')
        self.env.cr.execute("""CREATE or REPLACE VIEW f_partner_breif_balance_report as (%s)""" % (self._query()))

        ids = self.env['f.partner.breif.balance.report'].search([('partner_id', '!=', False)])

        data = {'report_ids_values': ids.ids
                }

        print('data', data)

        return self.env.ref('f_cont_report.f_cont_report').report_action(self, data=data)

    def get_general_details(self):
        tools.drop_view_if_exists(self.env.cr, 'f_partner_general_balance_report')
        self.env.cr.execute("""CREATE or REPLACE VIEW f_partner_general_balance_report as (%s)""" %
                            (self._general_query()))

        ids = self.env['f.partner.general.balance.report'].search([('partner_id', '!=', False)])

        data = {'report_ids_values': ids.ids
                }

        print('data', data)

        return self.env.ref('f_cont_report.f_cont_general_report').report_action(self, data=data)

