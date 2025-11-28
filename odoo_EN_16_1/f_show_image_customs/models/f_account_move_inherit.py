# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class FAccountMoveInherit(models.Model):
    _inherit = 'account.move'

    f_show_image = fields.Boolean('Show Product Image')
