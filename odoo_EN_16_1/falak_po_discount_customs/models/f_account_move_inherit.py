from odoo import models, fields, api


class FAccountMoveLineInherit(models.Model):
    _inherit = 'account.move.line'

    f_po_line_full_price = fields.Float(related='purchase_line_id.f_full_price', string="PO Full Price", store=True)

    f_po_line_discount = fields.Float(related='purchase_line_id.f_discount', string="PO Disc%", store=True)
