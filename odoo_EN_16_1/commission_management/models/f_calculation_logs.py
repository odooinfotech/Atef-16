from odoo import models, fields, api, _


class FCalculationLogs(models.Model):
    _name = 'f.calculation.logs'
    _description = 'Calculation Logs'
    _rec_name = 'f_commission_setup'

    f_commission_setup = fields.Many2one('f.commission.management', string='Setup')
    f_description = fields.Text(string='Description')
    f_date = fields.Datetime(string='Date & Time')
    f_user = fields.Many2one('res.users', string='Writer')
    f_sale_person = fields.Many2one('res.users', string='Sales Person')