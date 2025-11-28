# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models
from odoo.tools import  float_round


class MrpCostStructure(models.AbstractModel):
    """Added the Employee Timesheet and Overhead Costs structure tables"""
    _inherit = 'report.mrp_account_enterprise.mrp_cost_structure'

    def get_lines(self, productions):
        """Calculated the  overhead costs and employee timesheet
        table structure related values."""
        res = super(MrpCostStructure, self).get_lines(productions)
        for record in res:
            total_operation_cost = sum((row[3]* row[4]) for row in record.get('operations'))
            mrp_production_ids = productions.filtered(\
                                                lambda r: r.product_id == record.get('product'))
            overheads_list = []
            timesheet_line_records = []
            emp_timesheet_total_cost = 0.0
            emp_timesheet_grand_total_time = 0.0
            total_cost_overheads = 0.0
            total_overhead_cost_percent = 0.0
            total_cost_share_percent = 0
            for production in mrp_production_ids:
                byproduct_moves = production.move_byproduct_ids.filtered(lambda m: m.state != 'cancel' and m.cost_share > 0)
                total_cost_share_percent += sum(rec.cost_share for rec in byproduct_moves)
                emp_timesheet_total_cost += production.total_cost
                emp_timesheet_grand_total_time += production.effective_hours
                total_overhead_cost_percent += production.total_cost_over_head_percent
                if production and production.bom_id and production.mrp_bom_overhead_ids:
                    for line in production.mrp_bom_overhead_ids:
                        data_overhead_recs = {"product_id": line.product_id, \
                                              "overhead_parameters": line.overhead_parameters}
                        #Calculation of 'Amount/ Duration'
                        if line.overhead_parameters == "amount_div_by_duration":
                            data_overhead_recs['overhead_cost'] = \
                                    self.env.company.currency_id.round(( \
                                        (line.production_id.production_real_duration / 60.0) * \
                                         line.overhead_cost))
                            total_cost_overheads += data_overhead_recs['overhead_cost']
                            overheads_list.append(data_overhead_recs)
                        #Calculation of 'Percent (%)'
                        if line.overhead_parameters == "percent":
                            data_overhead_recs['overhead_cost'] = (line.overhead_cost * \
                                            record.get('total_cost')) / 100
                            total_cost_overheads += data_overhead_recs['overhead_cost']
                            overheads_list.append(data_overhead_recs)
                        #Calculation of 'Amount/ Final QTY'
                        if line.overhead_parameters == "amount_div_by_final_qty":
                            data_overhead_recs['overhead_cost'] = \
                               record.get('mo_qty') * line.overhead_cost
                            total_cost_overheads += data_overhead_recs['overhead_cost']
                            overheads_list.append(data_overhead_recs)

                #Employee timesheet line records
                for employee in production.timesheet_ids:
                    timesheet_line_records.append(employee)

                record['timesheet_line_records'] = timesheet_line_records
                record['emp_timesheet_total_cost'] = float_round(emp_timesheet_total_cost, 2)
                record['emp_timesheet_grand_total_time'] = emp_timesheet_grand_total_time
                record['overheads_data'] = overheads_list
                record['total_overhead_cost'] = float_round(sum(rec.get('overhead_cost') \
                                                    for rec in overheads_list), 2)
                record['total_all_costs'] = float_round(record['emp_timesheet_total_cost'] + \
                                            record['total_overhead_cost'] +\
                                            record.get('total_cost') , 2) #+ total_operation_cost
                record['total_overhead_cost_percent'] = float_round(total_overhead_cost_percent, 2)
                record['overhead_percent_total_cost'] = float_round((record['total_all_costs'] * \
                                                        total_overhead_cost_percent) / \
                                                        (100 * record.get('mocount')), 2)
                record['total_all_cost_per_unit'] = (record['total_all_costs'] +\
                                                     record['overhead_percent_total_cost']) / record.get('mocount')
                #Products Cost share total percent
                #currently client not request to by product functionality so commented the below code.
                ##record['total_cost_share_percent'] = total_cost_share_percent
        return res
