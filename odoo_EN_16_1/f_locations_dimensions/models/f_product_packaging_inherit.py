# -*- coding: utf-8 -*-
from odoo import models, fields, api


class FProductPackagingInherit(models.Model):
    _inherit = 'product.packaging'

    f_length = fields.Float(string='Length')
    f_width = fields.Float(string='Width')
    f_height = fields.Float(string='Height')
    f_volume = fields.Float(string='Volume', digits='Volume')
    f_length_uom = fields.Many2one('uom.uom', string='Length UOM',
                                   domain=lambda self: self._get_length_domain(),
                                   default=lambda self: self._get_length_default())
    f_width_uom = fields.Many2one('uom.uom', string='Width UOM',
                                  domain=lambda self: self._get_length_domain(),
                                  default=lambda self: self._get_length_default())
    f_height_uom = fields.Many2one('uom.uom', string='Height UOM',
                                   domain=lambda self: self._get_length_domain(),
                                   default=lambda self: self._get_length_default())
    f_volume_uom = fields.Many2one('uom.uom', string='Volume UOM',
                                   domain=lambda self: self._get_volume_domain(),
                                   default=lambda self: self._get_volume_default())

    def _get_length_domain(self):
        category_id = self.env['uom.category'].sudo().search([('name', '=', 'Length / Distance')])
        domain = [
            ('category_id', '=', category_id.id)]
        return domain

    def _get_volume_domain(self):
        category_id = self.env['uom.category'].sudo().search([('name', '=', 'Volume')])
        domain = [
            ('category_id', '=', category_id.id)]
        return domain

    def _get_length_default(self):
        uom = self.env['uom.uom'].sudo().search([('name', '=', 'cm')])
        return uom.id

    def _get_volume_default(self):
        uom = self.env['uom.uom'].sudo().search([('name', '=', 'm³')])
        return uom.id

    @api.onchange('f_length', 'f_width', 'f_height', 'f_length_uom', 'f_width_uom', 'f_height_uom', 'f_volume_uom')
    def _f_onchange_dimensions(self):
        for rec in self:
            ref_length = rec.f_reference_uom(rec.f_length, rec.f_length_uom)
            ref_width = rec.f_reference_uom(rec.f_width, rec.f_width_uom)
            ref_height = rec.f_reference_uom(rec.f_height, rec.f_height_uom)
            old_volume = ref_length * ref_width * ref_height
            old_uom = self.env['uom.uom'].sudo().search([('name', '=', 'm³')])
            ref_volume = rec.f_reference_uom(old_volume, old_uom)
            new_uom = rec.f_volume_uom
            volume = rec.f_new_uom(ref_volume, new_uom)
            rec.write({'f_volume': volume})

    # def write(self, vals):
    #     f_length = self.f_length
    #     f_width = self.f_width
    #     f_height = self.f_height
    #     f_length_uom = self.f_length_uom
    #     f_width_uom = self.f_width_uom
    #     f_height_uom = self.f_height_uom
    #     if 'f_length' in vals:
    #         f_length = vals['f_length']
    #     if 'f_width' in vals:
    #         f_width = vals['f_width']
    #     if 'f_height' in vals:
    #         f_height = vals['f_height']
    #     if 'f_length_uom' in vals:
    #         f_length_uom = new_uom = self.env['uom.uom'].sudo().search([('id', '=', vals['f_length_uom'])])
    #     if 'f_width_uom' in vals:
    #         f_width_uom = new_uom = self.env['uom.uom'].sudo().search([('id', '=', vals['f_width_uom'])])
    #     if 'f_height_uom' in vals:
    #         f_height_uom = new_uom = self.env['uom.uom'].sudo().search([('id', '=', vals['f_height_uom'])])
    #     ref_length = self.f_reference_uom(f_length, f_length_uom)
    #     ref_width = self.f_reference_uom(f_width, f_width_uom)
    #     ref_height = self.f_reference_uom(f_height, f_height_uom)
    #     old_volume = ref_length * ref_width * ref_height
    #     old_uom = self.env['uom.uom'].sudo().search([('name', '=', 'm³')])
    #     ref_volume = self.f_reference_uom(old_volume, old_uom)
    #     new_uom = self.f_volume_uom
    #     if 'f_volume_uom' in vals:
    #         new_uom = self.env['uom.uom'].sudo().search([('id', '=', vals['f_volume_uom'])])
    #     volume = self.f_new_uom(ref_volume, new_uom)
    #     vals['f_volume'] = volume
    #     print(vals['f_volume'])
    #     return super(FProductPackagingInherit, self).write(vals)

    def f_reference_uom(self, quantity, uom):
        ref_uom = self.env['uom.uom'].sudo().search([
            ('uom_type', '=', 'reference'),
            ('category_id', '=', uom.category_id.id)])
        new_quantity = quantity
        if uom.id != ref_uom.id and uom.uom_type == 'bigger':
            new_quantity = quantity * uom.ratio
        elif uom.id != ref_uom.id and uom.uom_type == 'smaller':
            new_quantity = quantity / uom.ratio

        return new_quantity

    def f_new_uom(self, quantity, uom):
        ref_uom = self.env['uom.uom'].sudo().search([
            ('uom_type', '=', 'reference'),
            ('category_id', '=', uom.category_id.id)])
        new_quantity = quantity
        if uom.id != ref_uom.id and uom.uom_type == 'bigger':
            new_quantity = quantity / uom.ratio
        elif uom.id != ref_uom.id and uom.uom_type == 'smaller':
            new_quantity = quantity * uom.ratio

        return new_quantity


