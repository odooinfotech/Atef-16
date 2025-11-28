from odoo import models, fields, api, _


class FPurchaseOrderLineInherit(models.Model):
    _inherit = 'purchase.order.line'

    f_confirm_date = fields.Datetime(compute='_f_compute_order_id_confirm_date', string='Confirm Date', readonly=True, store=True)

    @api.depends('order_id.date_approve')
    def _f_compute_order_id_confirm_date(self):
        for rec in self:
            rec.f_confirm_date = rec.order_id.date_approve