# -*- coding: utf-8 -*-

from odoo import models, fields, api


class F_Res_Partner_Inherit(models.Model):
    _inherit = 'res.partner'
    
    f_vendor_classifications = fields.Many2many('f.po.classification', string="Classifications")
    
    f_vendor_location = fields.Selection([('local', 'Local'),
                                          ('imported', 'Imported')], string='Vendor Location')
    
    f_representative = fields.Many2one('res.partner', string="Representative",
                                       domain="[('category_id.name', '=', 'Internal Agent')]")
    
    f_one_contact_person = fields.One2many('f.vendor.contactperson', 'f_vendor_id', string="Contact Person")
