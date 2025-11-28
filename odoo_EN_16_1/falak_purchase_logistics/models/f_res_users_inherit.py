# -*- coding: utf-8 -*-
from odoo import models, fields, api


class FResUsersInherit(models.Model):
    _inherit = 'res.users'

    f_class_ids = fields.Many2many('f.po.classification', string='PO Classification')

    @api.onchange('f_class_ids')
    def _f_onchange_classifications(self):
        rule = self.env.ref('falak_purchase_logistics.f_classifications_access_purchase_order')
        rule.write({'active': not rule.active})
        rule.write({'active': not rule.active})

    def _f_default_classification_access(self):
        f_classification_access = (self.env["ir.config_parameter"].sudo().
                                   get_param('falak_purchase_logistics.f_po_access_based_class'))
        return f_classification_access

    f_classification_access = fields.Boolean(string='Classification Access', default=_f_default_classification_access,
                                             compute='_f_compute_classification_access')

    def _f_compute_classification_access(self):
        self.f_classification_access = (self.env["ir.config_parameter"].sudo().
                                        get_param('falak_purchase_logistics.f_po_access_based_class'))
