from odoo import api, fields, models, _


class FPurchaseOrderInherit(models.Model):
    _inherit = 'purchase.order'

    f_total_qty = fields.Float(string='Total Qty', compute='_f_compute_total_qty', store=True)

    @api.depends('order_line')
    def _f_compute_total_qty(self):
        for rec in self:
            total = 0.0
            for line in rec.order_line:
                if line.product_id.detailed_type == 'product':
                    total += line.product_qty
            rec.f_total_qty = total
