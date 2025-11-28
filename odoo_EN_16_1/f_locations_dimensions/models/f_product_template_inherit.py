# -*- coding: utf-8 -*-
from odoo import models, fields, api


class FProductTemplateInherit(models.Model):
    _inherit = 'product.template'

    f_parent_location = fields.Many2one('stock.location', string='Parent Location')

    # f_length = fields.Float(string='Length', compute='_f_compute_length', inverse='_f_set_length')
    # f_width = fields.Float(string='Width', compute='_f_compute_width', inverse='_f_set_width')
    # f_height = fields.Float(string='Height', compute='_f_compute_height', inverse='_f_set_height')
    # f_length_uom = fields.Many2one('uom.uom', string='Length UOM',
    #                                domain=lambda self: self._get_length_domain(),
    #                                default=lambda self: self._get_length_default(),
    #                                compute='_f_compute_length_uom', inverse='_f_set_length_uom')
    # f_width_uom = fields.Many2one('uom.uom', string='Width UOM',
    #                               domain=lambda self: self._get_length_domain(),
    #                               default=lambda self: self._get_length_default(),
    #                               compute='_f_compute_width_uom', inverse='_f_set_width_uom')
    # f_height_uom = fields.Many2one('uom.uom', string='Height UOM',
    #                                domain=lambda self: self._get_length_domain(),
    #                                default=lambda self: self._get_length_default(),
    #                                compute='_f_compute_height_uom', inverse='_f_set_height_uom')

    # def _get_length_domain(self):
    #     category_id = self.env['uom.category'].sudo().search([('name', '=', 'Length / Distance')])
    #     domain = [
    #         ('category_id', '=', category_id.id)]
    #     return domain
    #
    # def _get_length_default(self):
    #     uom = self.env['uom.uom'].sudo().search([('name', '=', 'cm')])
    #     return uom.id

    # @api.onchange('f_length', 'f_width', 'f_height', 'f_length_uom', 'f_width_uom', 'f_height_uom', 'volume_uom_name')
    # def _f_onchange_length_width_height(self):
    #     ref_length = self.f_reference_length(self.f_length, self.f_length_uom)
    #     ref_width = self.f_reference_length(self.f_width, self.f_width_uom)
    #     ref_height = self.f_reference_length(self.f_height, self.f_height_uom)
    #     volume = ref_length * ref_width * ref_height
    #     if self.volume_uom_name == 'm³':
    #         self.volume = volume
    #         print("new Volume in m³")
    #         print(self.volume)
    #     elif self.volume_uom_name == 'ft³':
    #         volume_uom = self.env['uom.uom'].sudo().search([('name', '=', self.volume_uom_name)])
    #         old_uom = self.env['uom.uom'].sudo().search([('name', '=', 'm³')])
    #         ref_volume = volume * old_uom.ratio
    #         new_volume = ref_volume / volume_uom.ratio
    #         self.volume = new_volume
    #         print("new Volume in ft³")

    # def f_reference_length(self, quantity, uom):
    #     ref_uom = self.env['uom.uom'].sudo().search([
    #         ('uom_type', '=', 'reference'),
    #         ('category_id', '=', uom.category_id.id)])
    #     new_quantity = quantity
    #     if uom.id != ref_uom.id and uom.uom_type == 'bigger':
    #         new_quantity = quantity * uom.ratio
    #     elif uom.id != ref_uom.id and uom.uom_type == 'smaller':
    #         new_quantity = quantity / uom.ratio
    #
    #     return new_quantity

    # @api.depends('product_variant_ids', 'product_variant_ids.f_length')
    # def _f_compute_length(self):
    #     unique_variants = self.filtered(lambda template: len(template.product_variant_ids) == 1)
    #     for template in unique_variants:
    #         template.f_length = template.product_variant_ids.f_length
    #     for template in (self - unique_variants):
    #         template.f_length = 0.0
    #
    # @api.depends('product_variant_ids', 'product_variant_ids.f_width')
    # def _f_compute_width(self):
    #     unique_variants = self.filtered(lambda template: len(template.product_variant_ids) == 1)
    #     for template in unique_variants:
    #         template.f_width = template.product_variant_ids.f_width
    #     for template in (self - unique_variants):
    #         template.f_width = 0.0
    #
    # @api.depends('product_variant_ids', 'product_variant_ids.f_height')
    # def _f_compute_height(self):
    #     unique_variants = self.filtered(lambda template: len(template.product_variant_ids) == 1)
    #     for template in unique_variants:
    #         template.f_height = template.product_variant_ids.f_height
    #     for template in (self - unique_variants):
    #         template.f_height = 0.0
    #
    # @api.depends('product_variant_ids', 'product_variant_ids.f_length_uom')
    # def _f_compute_length_uom(self):
    #     unique_variants = self.filtered(lambda template: len(template.product_variant_ids) == 1)
    #     for template in unique_variants:
    #         template.f_length_uom = template.product_variant_ids.f_length_uom.id
    #     for template in (self - unique_variants):
    #         template.f_length_uom = False
    #
    # @api.depends('product_variant_ids', 'product_variant_ids.f_width_uom')
    # def _f_compute_width_uom(self):
    #     unique_variants = self.filtered(lambda template: len(template.product_variant_ids) == 1)
    #     for template in unique_variants:
    #         template.f_width_uom = template.product_variant_ids.f_width_uom.id
    #     for template in (self - unique_variants):
    #         template.f_width_uom = False
    #
    # @api.depends('product_variant_ids', 'product_variant_ids.f_height_uom')
    # def _f_compute_height_uom(self):
    #     unique_variants = self.filtered(lambda template: len(template.product_variant_ids) == 1)
    #     for template in unique_variants:
    #         template.f_height_uom = template.product_variant_ids.f_height_uom.id
    #     for template in (self - unique_variants):
    #         template.f_height_uom = False
    #
    # def _f_set_length(self):
    #     for template in self:
    #         if len(template.product_variant_ids) == 1:
    #             template.product_variant_ids.f_length = template.f_length
    #
    # def _f_set_width(self):
    #     for template in self:
    #         if len(template.product_variant_ids) == 1:
    #             template.product_variant_ids.f_width = template.f_width
    #
    # def _f_set_height(self):
    #     for template in self:
    #         if len(template.product_variant_ids) == 1:
    #             template.product_variant_ids.f_height = template.f_height
    #
    # def _f_set_length_uom(self):
    #     for template in self:
    #         if len(template.product_variant_ids) == 1:
    #             template.product_variant_ids.f_length_uom = template.f_length_uom.id
    #
    # def _f_set_width_uom(self):
    #     for template in self:
    #         if len(template.product_variant_ids) == 1:
    #             template.product_variant_ids.f_width_uom = template.f_width_uom.id
    #
    # def _f_set_height_uom(self):
    #     for template in self:
    #         if len(template.product_variant_ids) == 1:
    #             template.product_variant_ids.f_height_uom = template.f_height_uom.id
