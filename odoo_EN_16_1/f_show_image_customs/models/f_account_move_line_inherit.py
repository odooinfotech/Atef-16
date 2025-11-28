# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class FAccountMoveLineInherit(models.Model):
    _inherit = 'account.move.line'

    f_product_image_128 = fields.Image("Img", related='product_id.image_128')

