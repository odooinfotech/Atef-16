from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class FPurchaseOrderInherit(models.Model):
    _inherit = 'purchase.order'

    f_unit_price_access = fields.Boolean(string='Unit Price Access',
                                         default=lambda self: self.env.user.
                                         has_group('f_purchase_unit_price_access.f_po_account_access'),
                                         compute='_f_compute_unit_price_access')

    def _f_compute_unit_price_access(self):
        for rec in self:
            if self.env.user.has_group('f_purchase_unit_price_access.f_po_account_access'):
                rec.f_unit_price_access = True
            else:
                rec.f_unit_price_access = False

