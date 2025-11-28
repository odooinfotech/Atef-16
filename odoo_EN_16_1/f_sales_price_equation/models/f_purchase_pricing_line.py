# -*- coding: utf-8 -*-

from odoo import models, fields, api

class FProductPricingLine(models.Model):
    _name = 'f.purchase.pricing.line'
    _description = 'Purchase Pricing Line Model'
    _rec_name = 'f_product_id'

    f_product_id = fields.Many2one('product.template', string='Product')
    f_po_order_id = fields.Many2one('purchase.order', string='Purchase Order')
    f_partner_id = fields.Many2one('res.partner', string='Vendor')
    f_product_ref = fields.Char(string='Internal Reference', related='f_product_id.default_code')
    f_pricing_id = fields.Many2one('f.product.pricing', string='Product Pricing')
    f_quantity = fields.Float(string='Quantity')
    f_po_price = fields.Float(string='PO/P')
    f_unit_po_price = fields.Float(string='U/PO/P')
    f_unit_latest_price = fields.Float(string='U/L/P')
    f_last_po = fields.Many2one('purchase.order', string='Latest PO')
    f_deference = fields.Float(string='Def.')
    f_def_with_vat = fields.Float(string='Def. X P.E')
    f_current_price = fields.Float(string='C/P')
    f_new_price = fields.Float(string='N/P')

    @api.onchange('f_last_po')
    def _f_onchange_last_po(self):
        for rec in self:
            last_po_lines = self.env['purchase.order.line'].read_group(
                domain=[('order_id', '=', rec.f_last_po.id),
                        ('product_id', '=', rec.f_product_id.product_variant_id.id)],
                fields=['product_id', 'product_qty', 'price_subtotal'], groupby=['product_id'])
            if last_po_lines:
                last_price = last_po_lines[0]['price_subtotal'] / last_po_lines[0]['product_qty']
                rec.f_unit_latest_price = last_price
                deference = rec.f_unit_po_price - last_price
                rec.f_deference = deference
                f_def_with_vat = deference * rec.f_pricing_id.f_pricing_equation_int.f_factor
                rec.f_def_with_vat = f_def_with_vat
                rec.f_new_price = rec.f_current_price + f_def_with_vat
            else:
                rec.f_unit_latest_price = 0.0
                rec.f_deference = 0.0
                rec.f_def_with_vat = 0.0
                rec.f_new_price = 0.0

    @api.onchange('f_product_id')
    def _f_onchange_product_id(self):
        for rec in self:
            rec.f_current_price = rec.f_product_id.list_price
