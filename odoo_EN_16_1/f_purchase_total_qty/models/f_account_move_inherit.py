from odoo import api, fields, models, _


class FAccountMoveInherit(models.Model):
    _inherit = 'account.move'

    f_total_qty = fields.Float(string='Total Qty', compute='_f_compute_total_qty', store=True)

    @api.depends('invoice_line_ids')
    def _f_compute_total_qty(self):
        for rec in self:
            total = 0.0
            for line in rec.invoice_line_ids:
                if line.product_id.detailed_type == 'product':
                    total += line.quantity
            rec.f_total_qty = total