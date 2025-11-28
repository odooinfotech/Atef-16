# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class FSaleOrderLineInherit(models.Model):
    _inherit = 'sale.order.line'

    f_product_image_128 = fields.Image("Img", related='product_id.image_128')

