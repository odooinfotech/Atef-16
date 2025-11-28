# -*- coding: utf-8 -*-
from odoo import fields, models, api, _, tools


class Fxlspartneragingde(models.TransientModel):
    _name = 'f.loc.qtycost.wizard'
    _description = "Location qtys - cost  Wizard"

    from_date = fields.Date("From Date")
    to_date = fields.Date("To Date")
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company.id)

    location_id = fields.Many2one('stock.location', string="Location",
                                  domain=lambda self: [('company_id', '=', self.env.company.id)])

    def _select_final(self):
        return """

        select 

        prod.product_id as product_id,
        qtys.qty_from as qty_from_loc,
       ( case when (qty_main.onhand_quantity_from != 0 ) then (costs.cost_from/(qty_main.onhand_quantity_from ))   else 0 end  )* qtys.qty_from   as cost_from_loc,
        prod.product_cost * qtys.qty_from  as cost_stan_from_loc,
        qtys.qty_to as qty_to_loc,
        ( case when (qty_main.onhand_quantity_to != 0 ) then (costs.cost_to/(qty_main.onhand_quantity_to))   else 0 end  )* qtys.qty_to   as cost_to_loc, 
        prod.product_cost * qtys.qty_to as cost_stan_to_loc,
        prod.id as id,
        %s as company_id,
        case when qtys.qty_from = 0 and qtys.qty_to  = 0 then 1 else 0 end as is_zero_qtys 
        """ % (self.env.company.id)

    def _products_select(self):
        return """

        select 
        pp.id  as product_id ,
           pp.id  as id , 
        pr.value_float as product_cost
       from product_product pp
         LEFT JOIN product_template pt on (pt.id = pp.product_tmpl_id)
        LEFT JOIN ir_property pr ON (pr.company_id= %s and  pr.name = \'standard_price\' and res_id = \'product.product,\' || pp.id)

        where pt.active = 't'
        and pt.type = 'product'




        """ % (self.env.company.id)

    def _qtysselect(self):
        return """

       SELECT 
       sl.product_id as product_id,
       sum((case when  date(sl.date) <= date('%s') and source.id <> %s and dest.id = %s  then  (sl.qty_done/ u.factor * u2.factor) else 0 end )   - (case when  date(sl.date) <= date('%s') and source.id = %s and dest.id <> %s  then  (sl.qty_done/ u.factor * u2.factor) else 0 end ) ) as qty_from ,
sum((case when  date(sl.date) <= date('%s') and source.id <> %s and dest.id = %s  then  (sl.qty_done/ u.factor * u2.factor) else 0 end )   - (case when  date(sl.date) <= date('%s') and source.id = %s and dest.id <> %s  then  (sl.qty_done/ u.factor * u2.factor) else 0 end ) ) as qty_to




         from stock_move_line sl 
            left join stock_move sm on (sm.id = sl.move_id)
            left join stock_location source on (source.id = sl.location_id)
            left join stock_location dest on (dest.id = sl.location_dest_id)
            left join product_product pp on (sl.product_id = pp.id)
            left join product_template pt on (pt.id = pp.product_tmpl_id)
            left join uom_uom u on (u.id= sl.product_uom_id)  
        left join uom_uom u2 on (u2.id=pt.uom_id)


        where 

          sl.state = 'done' 
          and date(sl.date) <= date('%s') 
         and (source.id = %s or dest.id  = %s)
         and sl.company_id = %s

                    group by  sl.product_id

        """ % (self.from_date, self.location_id.id, self.location_id.id, self.from_date, self.location_id.id,
               self.location_id.id,
               self.to_date, self.location_id.id, self.location_id.id, self.to_date, self.location_id.id,
               self.location_id.id,
               self.to_date,
               self.location_id.id, self.location_id.id,
               self.env.company.id)

    def main_qty(self):
        return """
         select 
                    sl.product_id as  product_id,

                     sum((case when  date(sl.date) <= date('%s')  and source.usage != 'internal' and dest.usage = 'internal'  then  (sl.qty_done/ u.factor * u2.factor) else 0 end ) 
                     - (case when  date(sl.date) <= date('%s')  and source.usage = 'internal' and dest.usage != 'internal'   then  (sl.qty_done/ u.factor * u2.factor) else 0 end ) ) as onhand_quantity_from ,

       sum((case when  date(sl.date) <= date('%s')  and source.usage != 'internal' and dest.usage = 'internal'  then  (sl.qty_done/ u.factor * u2.factor) else 0 end ) 
                     - (case when  date(sl.date) <= date('%s')  and source.usage = 'internal' and dest.usage != 'internal'   then  (sl.qty_done/ u.factor * u2.factor) else 0 end ) ) as onhand_quantity_to  

                    from stock_move_line sl 
            left join stock_move sm on (sm.id = sl.move_id)
            left join stock_location source on (source.id = sl.location_id)
            left join stock_location dest on (dest.id = sl.location_dest_id)
            left join product_product pp on (sl.product_id = pp.id)
            left join product_template pt on (pt.id = pp.product_tmpl_id)
            left join uom_uom u on (u.id= sl.product_uom_id)  
        left join uom_uom u2 on (u2.id=pt.uom_id)
                where 

          sl.state = 'done' 
          and date(sl.date) <= date('%s') 

         and sl.company_id = %s


                    group by  sl.product_id



        """ % (self.from_date, self.from_date, self.to_date, self.to_date, self.to_date, self.env.company.id)

    def _valcost_select(self):
        return """
             SELECT 
         sl.product_id as product_id,
       sum(case when  date(sl.create_date) <= date('%s')  then  (sl.value) else 0 end   ) as cost_from ,
            sum(case when  date(sl.create_date) <= date('%s')  then  (sl.value) else 0 end   ) as cost_to 


         from stock_valuation_layer sl 

            left join product_product pp on (sl.product_id = pp.id)
            left join product_template pt on (pt.id = pp.product_tmpl_id)



        where 
   sl.company_id = %s
    and  date(sl.create_date) <= date('%s') 

    group by  sl.product_id



        """ % (self.from_date, self.to_date, self.env.company.id, self.to_date)

    def f_get_cost_details(self):
        self.env.cr.execute("""
                CREATE OR REPLACE VIEW f_loc_qty_cost_details AS (


                %s
                from

                (%s) prod

                left join 
                (%s)qtys on (qtys.product_id = prod.product_id)

                 left join 
                (%s )costs on (costs.product_id = prod.product_id)

                left join
                (%s) qty_main on (qty_main.product_id = prod.product_id)

                          ) """ % (
        self._select_final(), self._products_select(), self._qtysselect(), self._valcost_select(), self.main_qty()))

        action = {
            'name': _('Location qtys - cost report '),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree',
            'res_model': 'f.loc.qty.cost.details',
        }

        return action

