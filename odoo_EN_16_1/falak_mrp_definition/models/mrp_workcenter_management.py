# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class MrpWorkcenterManagement(models.Model):
    _name = 'mrp.workcenter.management'
    _description = 'MRP Work Center Management'

    name = fields.Char("Work Center Management")
