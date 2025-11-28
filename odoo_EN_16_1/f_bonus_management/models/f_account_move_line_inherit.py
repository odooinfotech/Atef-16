from odoo import models, fields, api
from odoo.tools import float_compare
from odoo.addons import decimal_precision as dp


class FAccountMoveLineInherit(models.Model):
    _inherit = 'account.move.line'
    #old to be removed
    bonus_qty = fields.Float('Bonus Qty', digits='Product Unit of Measure')
    
    f_bonus_qty = fields.Float('Bonus Qty', digits='Product Unit of Measure')
