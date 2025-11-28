from odoo import models, fields, api


class FAccountInvReportInherit(models.Model):
    _inherit = "account.invoice.report"
    #old to be removed
    #bonus_qty = fields.Float('Bonus Qty')
    #total_qty = fields.Float("Total Qty")
    
    
    f_bonus_qty = fields.Float('Bonus Qty')
    f_total_qty = fields.Float("Total Qty")
    
    def _select(self):
        return super(FAccountInvReportInherit, self)._select() + """
            ,case
            when move.move_type = 'out_invoice' then line.f_bonus_qty
            when move.move_type != 'out_invoice' then - line.f_bonus_qty
        end as f_bonus_qty
        , case
            when move.move_type = 'out_invoice' then line.f_bonus_qty + line.quantity 
            when move.move_type != 'out_invoice' then -1*(line.f_bonus_qty + line.quantity )
        end as f_total_qty
        
        """
