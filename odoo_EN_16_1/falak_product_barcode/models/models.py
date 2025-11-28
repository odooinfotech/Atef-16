# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class FConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    f_barcode_setting = fields.Boolean("Generate Product Barcode (EAN13)")
   


    def get_values(self):
        res = super(FConfigSettings, self).get_values()
        f_barcode_setting = self.env['ir.config_parameter'].sudo().get_param('falak_product_barcode.f_barcode_setting')
        res.update(
            f_barcode_setting = f_barcode_setting,
        )
        return res

    def set_values(self):
        super(FConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('falak_product_barcode.f_barcode_setting', self.f_barcode_setting)
        

