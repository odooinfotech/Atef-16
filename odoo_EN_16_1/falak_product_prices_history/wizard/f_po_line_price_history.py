from odoo import api, fields, models,tools


class F_Purchase_Order_Line_Price_History(models.Model):
    _name = "f.purchase.order.line.price.history.po"
    _description = "Purchase order line price history line"
    _auto = False

    f_purchase_order_line_id = fields.Many2one(
        comodel_name="purchase.order.line",
        string="Purchase Order Line",
    )
    
    purchase_order_line_id = fields.Many2one(
        comodel_name='account.move.line',
        string='Bill order line',
    )
    order_id = fields.Many2one(
        related="purchase_order_line_id.move_id",
    )
    partner_id = fields.Many2one(
        related="purchase_order_line_id.partner_id"
    )
    purchase_order_date_order = fields.Date(
        related="purchase_order_line_id.move_id.invoice_date"
    )
    product_uom_qty = fields.Float(
        related="purchase_order_line_id.quantity",
    )
    
    product_uom = fields.Many2one(
        related="purchase_order_line_id.product_uom_id",
    )
    
    
    price_unit = fields.Float(
        related="purchase_order_line_id.price_unit",
    )
    currency_id = fields.Many2one(
        related="purchase_order_line_id.move_id.currency_id",)

    tax_id = fields.Many2many(
        related="purchase_order_line_id.tax_ids",)
    
    def f_set_price(self):
        print("dwsedf")
        purchase_order_line = self.env['purchase.order.line'].search([('id','=',self.f_purchase_order_line_id.id)])
        print(purchase_order_line)
        if purchase_order_line:
            purchase_order_line.price_unit = self.price_unit
    def init(self):

        tools.drop_view_if_exists(self._cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as
           select max(a.id) as id from product_product a
           """ % (self._table))
