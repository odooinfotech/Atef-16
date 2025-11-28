from odoo import models, fields, api, _


class FCommissionResult(models.Model):
    _name = 'f.commission.result'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Commission Result'
    _rec_name = 'f_commission_role_id'

    f_commission_role_id = fields.Many2one('f.commission.role', string='Commission Role')
    f_role_responsible_id = fields.Many2one(related='f_commission_role_id.f_responsible', string='Responsible', store=True)
    f_commission_setup_id = fields.Many2one('f.commission.setup', string='Setup')
    f_commission_calculation_id = fields.Many2one('f.commission.calculation', string='Commission Calculation')
    f_commission_period_id = fields.Many2one('f.commission.period', string='Commission Period')
    f_commission_amount = fields.Float(string='Commission Amount')
    f_total_amount = fields.Float(string='Total Amount')
    f_commission_percent = fields.Float(string='Commission Percent')
    f_commission_target = fields.Char(string='Target')
