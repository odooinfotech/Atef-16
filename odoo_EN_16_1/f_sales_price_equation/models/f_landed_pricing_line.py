from odoo import models, fields, api, _


class FLandedPricingLine(models.Model):
    _name = 'f.landed.pricing.line'
    _description = 'Landed Pricing Line'
    _rec_name = 'f_product_id'

    f_product_id = fields.Many2one('product.template', string='Product')
    f_product_ref = fields.Char(string='Internal Reference', related='f_product_id.default_code')
    f_pricing_id = fields.Many2one('f.product.pricing', string='Product Pricing')
    f_quantity = fields.Float(string='Quantity')
    f_new_cost = fields.Float(string='N/C')
    f_unit_new_cost = fields.Float(string='U/N/C')
    f_unit_old_cost = fields.Float(string='U/L/C')
    f_last_landed = fields.Many2one('stock.landed.cost', string='Latest Landed')
    f_deference = fields.Float(string='Def.')
    f_def_with_vat = fields.Float(string='Def. X P.E')
    f_current_price = fields.Float(string='C/P')
    f_new_price = fields.Float(string='N/P')
    f_source = fields.Char(string='Source')

    @api.onchange('f_last_landed')
    def _f_onchange_last_landed(self):
        for rec in self:
            last_landed_lines = self.env['stock.valuation.adjustment.lines'].read_group(
                domain=[('cost_id', '=', rec.f_last_landed.id), ('product_id', '=', rec.f_product_id.product_variant_id.id)],
                fields=['product_id', 'quantity', 'final_cost'], groupby=['product_id'])
            if last_landed_lines:
                last_cost = last_landed_lines[0]['final_cost'] / last_landed_lines[0]['quantity']
                rec.f_unit_old_cost = last_cost
                deference = rec.f_unit_new_cost - last_cost
                rec.f_deference = deference
                f_def_with_vat = deference * rec.f_pricing_id.f_pricing_equation_ext.f_factor
                rec.f_def_with_vat = f_def_with_vat
                rec.f_new_price = rec.f_current_price + f_def_with_vat
            else:
                rec.f_unit_old_cost = 0.0
                rec.f_deference = 0.0
                rec.f_def_with_vat = 0.0
                rec.f_new_price = 0.0


    @api.onchange('f_product_id')
    def _f_onchange_product_id(self):
        for rec in self:
            rec.f_current_price = rec.f_product_id.list_price
