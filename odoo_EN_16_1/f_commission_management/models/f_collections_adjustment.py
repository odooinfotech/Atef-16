from odoo import models, fields, api, _


class FCollectionsAdjustment(models.Model):
    _name = 'f.collections.adjustment'
    _description = 'Collections Adjustment'

    f_commission_setup_id = fields.Many2one('f.commission.setup', string='Commission Setup')
    f_commission_calculation_id = fields.Many2one('f.commission.calculation', string='Commission Calculation')
    f_commission_role_id = fields.Many2one('f.commission.role', string='Role')
    f_adjustment_type = fields.Selection([('include', 'Include'), ('exclude', 'Exclude')], default='include', string='Adjustment Type')
    f_type = fields.Selection([('manual', 'Manual'), ('auto', 'Auto')], default='manual', string='Type')
    f_amount = fields.Float(string='Amount')
