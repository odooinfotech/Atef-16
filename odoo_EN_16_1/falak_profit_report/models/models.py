# -*- coding: utf-8 -*-

from odoo import models, fields, api, _, tools


class FProductprofit(models.TransientModel):
    _name = 'f.product.profitability'
    _description = "Profit Report "

    from_date = fields.Date("From ", required=True)
    to_date = fields.Date("To", required=True)

    def _get_cogs(self):
        return """
            (coalesce(beginv.beginv_bal,0)  + coalesce(exp.exp_bal,0) - coalesce( endinv.endinv_bal,0)) as cogs,
        """

    def _get_profit(self):
        return """
         coalesce(rev.rev_bal,0) - (coalesce(beginv.beginv_bal,0)  + coalesce(exp.exp_bal,0) - coalesce( endinv.endinv_bal,0)) as profit,
        """

    def _generalselect(self):
        return """
        select prod.product_id as id , prod.product_id as product_id,
             coalesce(beginv.beginv_bal,0)beginv_bal,
        coalesce(exp.exp_bal,0)exp_bal,
        coalesce(rev.rev_bal,0)rev_bal,
        coalesce( endinv.endinv_bal,0)endinv_bal,
        coalesce(rev.rev_qty,0)rev_qty,
        coalesce(exp.exp_qty,0)exp_qty,
        coalesce(beginv.beginv_qty,0)beginv_qty,
        coalesce(endinv.endinv_qty,0)endinv_qty,

        %s
        %s

           comp.id as company_id,
               comp.currency_id as currency_id,
               prod.barcode as barcode

        """ % (self._get_cogs(), self._get_profit())

    def _companyselect(self):
        return """
        select id ,currency_id from res_company where id = %s""" % (self.env.company.id)

    def _productsselect(self):
        return """  
        Select pp.id as product_id , pt.name as product_name, pp.barcode as barcode 

         """

    def _productsfrom(self):
        return """  

        from product_product pp ,product_template pt where pp.product_tmpl_id = pt.id and pt.type = 'product'
         """

    def _revenusesselect(self):
        return """ left join (Select product_id,sum(qty) rev_qty,sum(balance) rev_bal from(Select m.product_id as product_id, 
        CASE WHEN (am.move_type ='out_refund') THEN sum(m.quantity/ u.factor * u2.factor)* -1  ELSE sum(m.quantity/ u.factor * u2.factor)END AS qty,  
                    sum ( m.credit - m.debit ) as balance from account_move am ,account_journal j ,account_move_line m
                    left join product_product pp on m.product_id = pp.id
                    left join product_template pt on pp.product_tmpl_id = pt.id
                    left join uom_uom u on (u.id= m.product_uom_id)  
                    left join uom_uom u2 on (u2.id=pt.uom_id)
                    where m.product_id is not null and  j.id = m.journal_id and j.type = 'sale'  and am.id = m.move_id and am.state='posted' 
                     and m.display_type = 'product'
                      and am.company_id = %s
                    and date(m.date) >= ('%s') and date(m.date )<=('%s')
                    group by m.product_id,am.move_type
                   ) tt group by product_id) rev  on(rev.product_id = prod.product_id)

        """ % (self.env.company.id, self.from_date, self.to_date)

    def _expenesesselect(self):
        return """left join (Select product_id,sum(qty) exp_qty,sum(balance) exp_bal from(Select m.product_id as product_id, 
        sum(CASE WHEN (am.move_type ='in_refund' )THEN (m.quantity/ u.factor * u2.factor)*-1  ELSE m.quantity/ u.factor * u2.factor END) AS qty  ,
                    sum ( m.debit - m.credit ) as balance  from account_move am,account_journal j , account_move_line m
                    left join product_product pp on m.product_id = pp.id
                    left join product_template pt on pp.product_tmpl_id = pt.id
                    left join uom_uom u on (u.id= m.product_uom_id)  
                    left join uom_uom u2 on (u2.id=pt.uom_id)
                    where m.product_id is not null and  j.id = m.journal_id and j.type = 'purchase' and am.id = m.move_id and am.state='posted' 
                     and m.display_type = 'product'
            and am.company_id = %s
                    and date(m.date) >=('%s') and date(m.date) <=('%s')
                    group by m.product_id
                     UNION ALL 
                    select l.product_id ,0 as qty ,sum(l.additional_landed_cost) balance 
                    from stock_valuation_adjustment_lines l ,
                    stock_landed_cost c ,account_journal ac 
                    where l.cost_id = c.id and c.state='done' 
                     and ac.id = c.account_journal_id
                     and ac.company_id = %s
                    and date(c.date) >=('%s') and date(c.date) <=('%s')
                     group by l.product_id) ll group by product_id)exp  on(exp.product_id = prod.product_id)


        """ % (self.env.company.id, self.from_date, self.to_date, self.env.company.id, self.from_date, self.to_date)

    def _begininvselect(self):
        return """ 
        left join  (select l.product_id , sum(l.quantity) beginv_qty , sum(l.value) beginv_bal 
                    from stock_valuation_layer l 
                   where date(l.create_date) <('%s')
                   and l.company_id = %s
                    group by l.product_id) beginv on(beginv.product_id = prod.product_id)
        """ % (self.from_date, self.env.company.id)

    def _endinginvsselect(self):
        return """ 

        left join  ( select l.product_id , sum(l.quantity) endinv_qty , sum(l.value) endinv_bal 
                    from stock_valuation_layer l 
                    where date(l.create_date) <=('%s')
                    and l.company_id = %s 
                    group by l.product_id) endinv on(endinv.product_id = prod.product_id)
        """ % (self.to_date, self.env.company.id)

    # to do in mrp ex module
    def _manfsselect(self):
        # print('222222222222222')
        return """ 
        """

    def _query(self):
        return """
          %s
                FROM
               (%s)comp,
               ( %s
                 %s
               )prod
                 %s
                %s
                 %s
                %s
                %s


       """ % (self._generalselect(), self._companyselect(), self._productsselect(), self._productsfrom(),
              self._revenusesselect(),
              self._expenesesselect(), self._begininvselect(), self._endinginvsselect(), self._manfsselect())

    def get_profit_details(self):
        print("55555555555555555")

        tools.drop_view_if_exists(self.env.cr, 'f_profit_details')
        self.env.cr.execute("""CREATE or REPLACE VIEW f_profit_details as (%s)""" % (self._query()))

        tree_id = self.env.ref('falak_profit_report.view_report_profitabil_tree').id
        form_id = False
        action = {
            'name': _('Profitability Report'),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree',
            'res_model': 'f.profit.details',
        }

        return action

#         self.env.cr.execute("""
#         CREATE OR REPLACE VIEW f_profit_details AS (
#
#                 %s
#                 FROM
#                (%s)comp,
#                ( %s
#                  %s
#                )prod
#                  %s
#                 %s
#                  %s
#                 %s
#
#
#          )
#
#          """ % ( self._generalselect(), self._companyselect(), self._productsselect(), self._productsfrom(), self._revenusesselect(), self._expenesesselect(), self._begininvselect(), self._endinginvsselect())
#         )


#     def get_profit_details(self):
#         print("55555555555555555")
#
#         tools.drop_view_if_exists(self.env.cr, 'f_profit_details')
#
#
#
#         self.env.cr.execute("""
#         CREATE OR REPLACE VIEW f_profit_details AS (
#
#             select prod.product_id as id , prod.product_id as product_id,
#              coalesce(beginv.beginv_bal,0)beginv_bal,
#         coalesce(exp.exp_bal,0)exp_bal,
#         coalesce(rev.rev_bal,0)rev_bal,
#         coalesce( endinv.endinv_bal,0)endinv_bal,
#         coalesce(rev.rev_qty,0)rev_qty,
#         coalesce(exp.exp_qty,0)exp_qty,
#         coalesce(beginv.beginv_qty,0)beginv_qty,
#         coalesce(endinv.endinv_qty,0)endinv_qty,
#
#               (coalesce(beginv.beginv_bal,0)  + coalesce(exp.exp_bal,0) - coalesce( endinv.endinv_bal,0)) as cogs,
#               coalesce(rev.rev_bal,0) - (coalesce(beginv.beginv_bal,0)  + coalesce(exp.exp_bal,0) - coalesce( endinv.endinv_bal,0)) as profit,
#               comp.id as company_id,
#                comp.currency_id as currency_id,
#                prod.barcode as barcode
#
#                 from
#
#                     (select id ,currency_id from res_company where id = %s ) comp,
#                     (Select pp.id as product_id , pt.name as product_name, pp.barcode as barcode   from product_product pp ,product_template pt where pp.product_tmpl_id = pt.id and pt.type = 'product') prod
#                     left join  (
#                 Select product_id,sum(qty) rev_qty,sum(balance) rev_bal
#                     from(
#                     Select m.product_id as product_id, CASE WHEN (am.move_type ='out_refund') THEN sum(m.quantity)* -1  ELSE sum(m.quantity)END AS qty,
#                     sum ( m.credit - m.debit ) as balance from account_move_line m,account_move am ,account_journal j
#                     where product_id is not null and  j.id = m.journal_id and j.type = 'sale'  and am.id = m.move_id and am.state='posted'
#                     and m.date >=(%s) and m.date <=(%s)
#                     group by m.product_id,am.move_type
#                      UNION ALL
#                     Select l.product_id as product_id,  sum(l.qty) as qty,
#                     sum(l.price_subtotal) as balance  from pos_order_line l , pos_order o ,
#                      pos_session s
#                      where
#                      l.order_id = o.id and  s.id = o.session_id
#                      and date(o.date_order) >=(%s) and date( o.date_order )<=(%s)
#                     Group by l.product_id) tt group by product_id) rev  on(rev.product_id = prod.product_id)
#                     left join   (Select product_id,sum(qty) exp_qty,sum(balance) exp_bal
#                     from(Select m.product_id as product_id, sum(CASE WHEN (am.move_type ='in_refund' )THEN (m.quantity)*-1  ELSE m.quantity END) AS qty  ,
#                     sum ( m.debit - m.credit ) as balance  from account_move_line m,account_move am,account_journal j
#                     where product_id is not null and  j.id = m.journal_id and j.type = 'purchase' and am.id = m.move_id and am.state='posted'
#                     and m.date >=(%s) and m.date <=(%s)
#                     group by m.product_id
#                      UNION ALL
#                     select l.product_id ,0 as qty ,sum(l.additional_landed_cost) balance
#                     from stock_valuation_adjustment_lines l ,
#                     stock_landed_cost c
#                     where l.cost_id = c.id and c.state='done'
#                     and c.date >=(%s) and c.date <=(%s)
#                      group by l.product_id) ll group by product_id)exp  on(exp.product_id = prod.product_id)
#                     left join  (select l.product_id , sum(l.quantity) beginv_qty , sum(l.value) beginv_bal
#                     from stock_valuation_layer l
#                    where date(l.create_date) <(%s)
#                     group by l.product_id) beginv on(beginv.product_id = prod.product_id)
#                     left join  ( select l.product_id , sum(l.quantity) endinv_qty , sum(l.value) endinv_bal
#                     from stock_valuation_layer l
#                     where date(l.create_date) <=(%s)
#                     group by l.product_id) endinv on(endinv.product_id = prod.product_id)
#
#
#
#
#
#          )
#
#         """,(self.env.company.id,self.from_date,self.to_date,self.from_date,self.to_date,self.from_date,self.to_date,self.from_date,self.to_date,self.from_date,self.to_date))
#
#
#
#
#
#         tree_id = self.env.ref('falak_profit_report.view_report_profitabil_tree').id
#         form_id = False
#         action = {
#             'name':_('Profitability Report'),
#             'type': 'ir.actions.act_window',
#             'view_mode': 'tree',
#             'res_model': 'f.profit.details',
#             }
#
#         return action
#








