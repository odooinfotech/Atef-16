from odoo import api,fields, models,_
from functools import lru_cache

class fAccountMoveLineInherit(models.Model):
    _inherit = 'account.move.line'

    f_manual_currency_rate = fields.Float('Force Currency Rate')


    @api.depends('currency_id', 'company_id', 'move_id.date', 'f_manual_currency_rate')
    def _compute_currency_rate(self):
        @lru_cache()
        def get_rate(from_currency, to_currency, company, date):
            return self.env['res.currency']._get_conversion_rate(
                from_currency=from_currency,
                to_currency=to_currency,
                company=company,
                date=date,
            )
        for line in self:
            if line.f_manual_currency_rate > 0:
                line.currency_rate = line.f_manual_currency_rate
                amount =  line.amount_currency / line.f_manual_currency_rate
                line.debit = amount if amount < 0.0 else 0.0
                line.credit = -amount if amount > 0.0 else 0.0

            else :
                line.currency_rate = get_rate(
                    from_currency=line.company_currency_id,
                    to_currency=line.currency_id,
                    company=line.company_id,
                    date=line.move_id.invoice_date or line.move_id.date or fields.Date.context_today(line),
                )
