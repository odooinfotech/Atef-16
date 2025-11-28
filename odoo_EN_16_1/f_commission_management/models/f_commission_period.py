from odoo import models, fields, api, _


class FCommissionPeriod(models.Model):
    _name = 'f.commission.period'
    _description = 'Commission Period'
    _rec_name = 'f_name'

    f_name = fields.Char(string='Name', required=True)
    f_from = fields.Date(string='From')
    f_to = fields.Date(string='To')
    f_closed = fields.Boolean(string='Closed')
    f_recurring = fields.Selection([('monthly', 'Monthly'), ('quarterly', 'Quarterly'), ('yearly', 'Yearly')], string='Recurring')
