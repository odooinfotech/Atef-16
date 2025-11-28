# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_scan_by_lot = fields.Boolean('Scan By Lots')


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def _get_fields_stock_barcode(self):
        """ Inject the field 'is_scan_by_lot' in the initial state of the barcode view.
        """
        fields = super(ProductProduct, self)._get_fields_stock_barcode()
        fields.append('is_scan_by_lot')
        return fields
