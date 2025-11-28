from odoo import models, fields, api, _


class FCollectionType(models.Model):
    _name = 'f.collection.type'
    _description = 'Collection Type'
    _rec_name = 'f_name'

    f_name = fields.Char(string='Name')
    f_payment_type = fields.Selection([('all', 'All'), ('custom', 'Custom')], string='Payment Type', default='all')
    f_journals = fields.Many2many('account.journal', string='Journals')
    f_destination_account = fields.Many2many('account.account', string='Destination Account', domain="[('account_type', 'in', ('asset_receivable', 'liability_payable')), ('deprecated','=',False)]")
    f_check_to_cash_limit_from = fields.Integer(string='Check To Cash Limit From (Days)')
    f_check_to_cash_limit_to = fields.Integer(string='Check To Cash Limit To (Days)')
    f_check_exclude_from = fields.Integer(string='Check Exclude From (Days)')
    f_check_exclude_to = fields.Integer(string='Check Exclude To (Days)')
    f_include_returned_checks = fields.Boolean(string='Include Returned Checks')
