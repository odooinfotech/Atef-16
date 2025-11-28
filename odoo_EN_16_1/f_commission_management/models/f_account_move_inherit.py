from odoo import models, fields, api, _


class FAccountMoveInherit(models.Model):
    _inherit = 'account.move'

    f_include_commission = fields.Boolean(string='Include Commission', default=False)
    f_commission_amount = fields.Float(string='Commission Amount')
    f_period_id = fields.Many2one('f.commission.period', string='Period')
    f_sales_person = fields.Many2one('res.users', string='Commission Salesperson')
    f_commission_notes = fields.Text(string='Commission Notes')