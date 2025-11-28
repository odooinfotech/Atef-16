# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api
from odoo.tools import float_round


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    cost_visible = fields.Boolean(related="bom_id.cost_visible")
    effective_hours = fields.Float("Hours Spent", compute='_compute_effective_hours_cost')
    total_cost = fields.Float("Total cost", compute='_compute_effective_hours_cost')
    mrp_bom_overhead_ids = fields.One2many('mrp.bom.overhead', 'production_id', 'MRP BOM Overheads')
    timesheet_ids = fields.One2many('hr.timesheet.line', 'mrp_production_id',
                                    'Associated Timesheets', readonly=False,
                                    states={'done': [('readonly', True)]})
    total_cost_over_head_percent = fields.Float("Over Head '%' over Total Cost", readonly=True,
                                                states={'draft': [('readonly', False)],
                                                        'confirmed': [('readonly', False)]})
    resource_calendar_id = fields.Many2one('resource.calendar', string="Working Hours")
    workcenter_id = fields.Many2one('mrp.workcenter', 'Work Center', readonly=True,
                                    states={'draft': [('readonly', False)]}, check_company=True,
                                    help="""Allow users to pass specific workcenter and
                                    replace Related BOM work center from the header automatically
                                    """)

    def action_confirm(self):
        """Set the BOM overhead records on the click of 'Confirm' button
            and also MRP: Plan Production Orders"""
        res = super(MrpProduction, self).action_confirm()
        for order in self.filtered(lambda order: order.bom_id):
            for record in order.bom_id.overhead_line_ids:
                record.sudo().copy({"production_id":  order.id or order._origin})
        return res

    @api.depends('timesheet_ids.total_time', 'timesheet_ids.total_work_cost')
    def _compute_effective_hours_cost(self):
        for task in self:
            task.effective_hours = sum(task.timesheet_ids.mapped('total_time'))
            task.total_cost = float_round(sum(task.timesheet_ids.mapped('total_work_cost')), 2)

    @api.onchange('bom_id')
    def _onchange_bom_id(self):
        #res = super(MrpProduction, self)._onchange_bom_id()
        if self.bom_id:
            self.total_cost_over_head_percent = self.bom_id.total_cost_over_head_percent


    def _get_moves_raw_values(self):
        """By default calculated the product uom quantity including
        the loss percent quantity, on selection BOM product."""
        result = super(MrpProduction, self)._get_moves_raw_values()
        mrp_bom_line_obj = self.env['mrp.bom.line']
        for record in result:
            mrp_bom_line_obj = mrp_bom_line_obj.browse(record.get('bom_line_id'))
            
            mo_product_qty = self.product_qty
            bom_prod_weight= mrp_bom_line_obj.bom_id.weight
            bom_prod_qty   = mrp_bom_line_obj.bom_id.product_qty
            bom_line_qty   = mrp_bom_line_obj.product_qty
            
            product_line_qty = 0.0
            
            if mrp_bom_line_obj and mrp_bom_line_obj.coefficent_parameters == 'percentage_with_co':
                product_line_qty = bom_prod_qty* bom_prod_weight * ((mrp_bom_line_obj.quantity_ratio_percent / 100) #/ (mrp_bom_line_obj.quantity_coefficient or 1)#
                                                                )
                
            
            elif mrp_bom_line_obj and mrp_bom_line_obj.coefficent_parameters == 'only_co':
                product_line_qty = (bom_prod_qty * bom_line_qty) / (mrp_bom_line_obj.quantity_coefficient or 1)



                
            else : 
                product_line_qty = bom_line_qty
            
            
            if mrp_bom_line_obj and not mrp_bom_line_obj.is_supplementary_product:
                
                product_line_qty = product_line_qty +(product_line_qty * mrp_bom_line_obj.loss_percent) / 100
                
            
            
            product_line_qty = product_line_qty/bom_prod_qty
            if self.product_uom_id.id != mrp_bom_line_obj.bom_id.product_uom_id.id  and mrp_bom_line_obj.bom_id.product_uom_id.uom_type == 'bigger' and self.product_uom_id.uom_type == 'reference':
                product_line_qty = product_line_qty / mrp_bom_line_obj.bom_id.product_uom_id.ratio
            elif self.product_uom_id.id != mrp_bom_line_obj.bom_id.product_uom_id.id and mrp_bom_line_obj.bom_id.product_uom_id.uom_type == 'reference' and self.product_uom_id.uom_type == 'bigger':
                product_line_qty = product_line_qty * mrp_bom_line_obj.bom_id.product_uom_id.ratio
            elif self.product_uom_id.id != mrp_bom_line_obj.bom_id.product_uom_id.id  and mrp_bom_line_obj.bom_id.product_uom_id.uom_type == 'smaller' and self.product_uom_id.uom_type == 'reference':
                product_line_qty = product_line_qty * mrp_bom_line_obj.bom_id.product_uom_id.ratio
            elif self.product_uom_id.id != mrp_bom_line_obj.bom_id.product_uom_id.id and mrp_bom_line_obj.bom_id.product_uom_id.uom_type == 'reference' and self.product_uom_id.uom_type == 'smaller':
                product_line_qty = product_line_qty / mrp_bom_line_obj.bom_id.product_uom_id.ratio
            
            product_line_qty = product_line_qty * mo_product_qty
            record.update({"product_uom_qty":product_line_qty})
            
            
            
        return result

    def _cal_price(self, consumed_moves):
        """Set a price unit on the finished move according to `consumed_moves`.
        """
        res = super(MrpProduction, self)._cal_price(consumed_moves)
        work_center_cost = 0
        total_operation_cost = 0
        total_cost_overheads = 0
        finished_move = self.move_finished_ids.filtered(
            lambda x: x.product_id == self.product_id and x.state not in ('done', 'cancel') and x.quantity_done > 0)
        if finished_move:
            finished_move.ensure_one()
            for work_order in self.workorder_ids:
                time_lines = work_order.time_ids.filtered(
                    lambda x: x.date_end and not x.cost_already_recorded)
                duration = sum(time_lines.mapped('duration'))
                time_lines.write({'cost_already_recorded': True})
                work_center_cost += (duration / 60.0) * \
                    work_order.workcenter_id.costs_hour
                total_operation_cost += (work_order.duration / 60) * \
                                         work_order.workcenter_id.costs_hour

            qty_done = finished_move.product_uom._compute_quantity(
                finished_move.quantity_done, finished_move.product_id.uom_id)
            extra_cost = self.extra_cost * qty_done
            total_cost = (sum(-m.stock_valuation_layer_ids.value for m in consumed_moves.sudo()) + work_center_cost + extra_cost)
            total_operation_cost = total_operation_cost
            for line in self.mrp_bom_overhead_ids:
                if line.overhead_parameters == "amount_div_by_duration":
                    total_cost_overheads += self.env.company.currency_id.round(( \
                                            (line.production_id.production_real_duration / 60.0) * \
                                            line.overhead_cost))
                if line.overhead_parameters == "percent":
                    total_cost_overheads += (line.overhead_cost * (total_cost+total_operation_cost))/ 100
                if line.overhead_parameters == "amount_div_by_final_qty":
                    total_cost_overheads += qty_done * line.overhead_cost
            total_cost_of_employee = self.total_cost
            total_all_costs = total_cost + total_operation_cost + total_cost_of_employee + total_cost_overheads
            total_cost_of_over_head_percent = (total_all_costs * self.total_cost_over_head_percent) / 100
            total_cost = float_round((total_all_costs + total_cost_of_over_head_percent), 2)
            byproduct_moves = self.move_byproduct_ids.filtered(lambda m: m.state not in ('done', 'cancel') and m.quantity_done > 0)
            byproduct_cost_share = 0
            for byproduct in byproduct_moves:
                if byproduct.cost_share == 0:
                    continue
                byproduct_cost_share += byproduct.cost_share
                if byproduct.product_id.cost_method in ('fifo', 'average'):
                    byproduct.price_unit = total_cost * byproduct.cost_share / 100 / byproduct.product_uom._compute_quantity(byproduct.quantity_done, byproduct.product_id.uom_id)
            if finished_move.product_id.cost_method in ('fifo', 'average'):
                finished_move.price_unit = total_cost * float_round(1 - byproduct_cost_share / 100, precision_rounding=0.0001) / qty_done
        return res

    def _create_workorder(self):
        """
        To create the work order and allow the same operation to be done
        on a multi Work Center with different durations.
        """
        res = super(MrpProduction, self)._create_workorder()
        for production in self:
            if not production.bom_id or not production.product_id:
                continue
            workorders_values = []
            product_qty = production.product_uom_id._compute_quantity(production.product_qty, production.bom_id.product_uom_id)
            exploded_boms, dummy = production.bom_id.explode(production.product_id, product_qty / production.bom_id.product_qty, picking_type=production.bom_id.picking_type_id)
            for bom, bom_data in exploded_boms:
                if not (bom.operation_workcenter_ids and (not bom_data['parent_line'] or bom_data['parent_line'].bom_id.operation_workcenter_ids != bom.operation_workcenter_ids)):
                    continue
                for operation in bom.operation_workcenter_ids:
                    if operation.operation_id._skip_operation_line(bom_data['product']):
                        continue
                    workorders_values += [{
                        'name': operation.operation_id.name,
                        'production_id': production.id,
                        'workcenter_id': operation.workcenter_id.id,
                        'product_uom_id': production.product_uom_id.id,
                        'operation_id': operation.operation_id.id,
                        'duration_expected': operation.time_cycle,
                        'state': 'pending',
                    }]
            production.workorder_ids = [(5, 0)] + [(0, 0, value) for value in workorders_values]
        return res

    @api.onchange('workcenter_id')
    def _onchange_workcenter_id(self):
        """Allow users to pass specific work center and replace Related BOM work centers from the header.
        Duration will be affected.
        """
        bom_operation_duration = []
        if self.workcenter_id:
            if self.bom_id and self.bom_id.operation_workcenter_ids:
                bom_operation_duration.extend(\
                    [record.time_cycle for record in self.bom_id.operation_workcenter_ids.filtered(\
                        lambda r: r.workcenter_id == self.workcenter_id and r.time_cycle > 0)])
            for workorder in self.workorder_ids:
                if workorder._origin and workorder._origin.production_bom_id:
                    workorder._origin.workcenter_id = self.workcenter_id.id or False
                    if bom_operation_duration:
                        workorder._origin.duration_expected = min(bom_operation_duration)
                    else:
                        workorder._origin.duration_expected = 0
