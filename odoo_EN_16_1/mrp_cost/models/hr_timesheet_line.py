# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class HrTimesheetLine(models.Model):
    _name = 'hr.timesheet.line'
    _description = "HR TIME MANAGEMENT"
    _rec_name = 'employee_id'

    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    currency_id = fields.Many2one('res.currency', string='Currency')
    start_date = fields.Datetime("Sart Date")
    end_date = fields.Datetime("End Date")
    total_time = fields.Float("Total Work Time", compute="_compute_total_timesheet_cost", default=0.0,store=True)
    work_cost = fields.Monetary('Cost', related="employee_id.hourly_cost")
    total_work_cost = fields.Monetary('Total Cost', compute="_compute_total_timesheet_cost", currency_field="currency_id", default=0.0)
    mrp_production_id = fields.Many2one("mrp.production", string="MRP Production")

    @api.depends('employee_id', 'start_date', 'end_date')
    def _compute_total_timesheet_cost(self):
        for line in self:
            if line.start_date and line.end_date and (line.start_date <= line.end_date):
                start_date = fields.Datetime.from_string(line.start_date)
                end_date = fields.Datetime.from_string(line.end_date)
                delta = end_date - start_date
                total_hours = delta.total_seconds() / 3600
                line.total_time = total_hours
                line.total_work_cost = line.work_cost * total_hours
            else:
                line.total_time = 0.0
                line.total_work_cost = 0.0
