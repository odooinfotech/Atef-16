# -*- coding: utf-8 -*-
from odoo import models, fields, api


class FProductPackagingInherit(models.Model):
    _inherit = 'product.packaging'

    f_delivery_packaging = fields.Boolean(string='Delivery Packaging', default=False)
