# -*- coding: utf-8 -*-
from odoo import models, fields, api


class FProductTemplateInherit(models.Model):
    _inherit = 'product.template'

    f_class_id = fields.Many2one('f.po.classification', string='PO Classification')

    def _f_default_classification_access(self):
        f_classification_access = (self.env["ir.config_parameter"].sudo().
                                   get_param('falak_purchase_logistics.f_po_access_based_class'))
        return f_classification_access

    f_classification_access = fields.Boolean(string='Classification Access', default=_f_default_classification_access,
                                             compute='_f_compute_classification_access')

    def _f_compute_classification_access(self):
        self.f_classification_access = (self.env["ir.config_parameter"].sudo().
                                        get_param('falak_purchase_logistics.f_po_access_based_class'))
