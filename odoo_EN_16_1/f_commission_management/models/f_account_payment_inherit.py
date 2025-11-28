from odoo import models, fields, api


class FAccountPaymentInherit(models.Model):
    _inherit = 'account.payment'

    f_commission_exclude = fields.Boolean(string='Exclude Commission', default=False)
    f_commission_note = fields.Text(string='Notes')
