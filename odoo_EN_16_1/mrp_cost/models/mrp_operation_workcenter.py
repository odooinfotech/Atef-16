# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class MrpOperationWorkcenter(models.Model):
    _name = 'mrp.operation.workcenter'
    _description = 'MRP Operation Workcenter'

    bom_id = fields.Many2one('mrp.bom', 'Bill of Material', index=True, ondelete='cascade',
                             required=True, help="The Bill of Material this operation is linked to")
    operation_id = fields.Many2one('mrp.routing.workcenter', string='Operation')
    workcenter_id = fields.Many2one('mrp.workcenter', 'Work Center')
    time_cycle = fields.Float('Duration', digits=(16, 2), default=0.0, help="Duration (in minutes)")
    company_id = fields.Many2one('res.company', string='Company', required=True,
                                 default=lambda self: self.env.company)

    #unique combination of opertion_id and workcenter_id
    _sql_constraints = [
        ('operation_workcenter', 'unique(company_id, bom_id, operation_id, workcenter_id)',
         'Operation and Workcenter combinations must be different per company.'),
    ]

    @api.onchange('operation_id')
    def _onchange_operation_id(self):
        """If operation_id not found then the updated the vals."""
        if not self.operation_id:
            self.update({
                'workcenter_id': False,
                'time_cycle':False
            })
            return
        else:
            if self.operation_id:
                self.time_cycle = self.operation_id.time_cycle_manual
