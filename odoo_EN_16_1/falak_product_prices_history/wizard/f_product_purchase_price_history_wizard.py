from odoo import api, fields, models,tools
from datetime import datetime


class F_Product_purchase_Price_History(models.Model):
    _name = "f.product.purchase.price.history.p"
    _description = "product line purchase price history"
    _auto = False

    purchase_order_line_id = fields.Many2one(comodel_name='account.move.line',string='Bill order line')
    order_id = fields.Many2one(comodel_name='account.move',string='Order')
    partner_id = fields.Many2one(comodel_name='res.partner',string='Partner')
    purchase_order_date_order = fields.Date(string='Date')
    product_uom_qty = fields.Float(related="purchase_order_line_id.quantity")
    product_uom = fields.Many2one(related="purchase_order_line_id.product_uom_id")
    price_unit = fields.Float(related="purchase_order_line_id.price_unit")
    currency_id = fields.Many2one(related="purchase_order_line_id.move_id.currency_id")
    tax_id = fields.Many2many(related="purchase_order_line_id.tax_ids")


    def init(self):

        tools.drop_view_if_exists(self._cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as
           select max(a.id) as id from product_product a
           """ % (self._table))

    



