from odoo import models, fields, api, _


class FStockValuationAdjustmentLinesInherit(models.Model):
    _inherit = 'stock.valuation.adjustment.lines'

    f_landed_date = fields.Date(compute="_f_compute_cost_id_date", string='Date', readonly=True, store=True)

    @api.depends('cost_id.date')
    def _f_compute_cost_id_date(self):
        for rec in self:
            rec.f_landed_date = rec.cost_id.date