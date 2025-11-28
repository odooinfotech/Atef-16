from odoo import models, fields, api,_


class FResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    f_bad_debt = fields.Boolean('Bad Debt',default=False)