from odoo import models, fields, api


class FPurchaseOrderInherit(models.Model):
    _inherit = 'purchase.order'

    def f_update_prices_based_on_disc(self):
        for line in self.order_line:
            if line.f_full_price and line.f_discount:
                price_after_disc = line.f_full_price * (line.f_discount / 100)
                line.price_unit = line.f_full_price - price_after_disc
            else:
                pass


class FPurchaseOrderLineInherit(models.Model):
    _inherit = 'purchase.order.line'

    f_full_price = fields.Float(string="Full Price", store=True)
    f_discount = fields.Float(string="Disc%", store=True)