# -*- coding: utf-8 -*-
from odoo import models, fields, api


class FProductProductInherit(models.Model):
    _inherit = 'product.product'

    f_length = fields.Float(string='Length')
    f_width = fields.Float(string='Width')
    f_height = fields.Float(string='Height')
    f_length_uom = fields.Many2one('uom.uom', string='Length UOM',
                                   domain=lambda self: self._get_length_domain(),
                                   default=lambda self: self._get_length_default())
    f_width_uom = fields.Many2one('uom.uom', string='Width UOM',
                                  domain=lambda self: self._get_length_domain(),
                                  default=lambda self: self._get_length_default())
    f_height_uom = fields.Many2one('uom.uom', string='Height UOM',
                                   domain=lambda self: self._get_length_domain(),
                                   default=lambda self: self._get_length_default())

    def _get_length_domain(self):
        category_id = self.env['uom.category'].sudo().search([('name', '=', 'Length / Distance')])
        domain = [
            ('category_id', '=', category_id.id)]
        return domain

    def _get_length_default(self):
        uom = self.env['uom.uom'].sudo().search([('name', '=', 'cm')])
        return uom.id

    @api.onchange('f_length', 'f_width', 'f_height', 'f_length_uom', 'f_width_uom', 'f_height_uom', 'volume_uom_name')
    def _f_onchange_length_width_height(self):
        ref_length = self.f_reference_length(self.f_length, self.f_length_uom)
        ref_width = self.f_reference_length(self.f_width, self.f_width_uom)
        ref_height = self.f_reference_length(self.f_height, self.f_height_uom)
        volume = ref_length * ref_width * ref_height
        if self.volume_uom_name == 'm³':
            self.volume = volume
            print("new Volume in m³")
            print(self.volume)
        elif self.volume_uom_name == 'ft³':
            volume_uom = self.env['uom.uom'].sudo().search([('name', '=', self.volume_uom_name)])
            old_uom = self.env['uom.uom'].sudo().search([('name', '=', 'm³')])
            ref_volume = volume * old_uom.ratio
            new_volume = ref_volume / volume_uom.ratio
            self.volume = new_volume
            print("new Volume in ft³")

    def f_reference_length(self, quantity, uom):
        ref_uom = self.env['uom.uom'].sudo().search([
            ('uom_type', '=', 'reference'),
            ('category_id', '=', uom.category_id.id)])
        new_quantity = quantity
        if uom.id != ref_uom.id and uom.uom_type == 'bigger':
            new_quantity = quantity * uom.ratio
        elif uom.id != ref_uom.id and uom.uom_type == 'smaller':
            new_quantity = quantity / uom.ratio

        return new_quantity
