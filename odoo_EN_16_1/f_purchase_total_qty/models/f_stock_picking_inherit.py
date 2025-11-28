from odoo import api, fields, models, _


class FStockPickingInherit(models.Model):
    _inherit = 'stock.picking'

    f_total_demand_qty = fields.Float(string='Total Demand Qty', compute='_f_compute_total_qty', store=True)
    f_total_done_qty = fields.Float(string='Total Done Qty', compute='_f_compute_total_qty', store=True)

    @api.depends('move_ids_without_package')
    def _f_compute_total_qty(self):
        for rec in self:
            total_demand = 0.0
            total_done = 0.0
            for line in rec.move_ids_without_package:
                if line.product_id.detailed_type == 'product':
                    total_demand += line.product_uom_qty
                    total_done += line.quantity_done
            rec.f_total_demand_qty = total_demand
            rec.f_total_done_qty = total_done