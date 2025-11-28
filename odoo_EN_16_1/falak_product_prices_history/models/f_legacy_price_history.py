from odoo import api, fields, models


class FLegacyPriceHistory(models.Model):
    _name = "f.legacy.price.history.lines"
    _description = "Legacy price history"


    product_id = fields.Many2one('product.product', string="Product")
    f_legacy_order_date = fields.Datetime(string='Date')
    f_source =  fields.Char('Source')
    partner_id = fields.Many2one('res.partner', string='Partner' )
    f_legacy_order_id = fields.Char('Legacy Order Id')
    f_price = fields.Float( string='Price' )
    f_currency_id = fields.Many2one('res.currency', string='Currency')
    f_qty = fields.Float(string='Qty')
    f_discount = fields.Float( string  = 'Discount')

