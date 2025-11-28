# -*- coding: utf-8 -*-
from odoo import models, fields, api


class FVendorContactPerson(models.Model):
    _name='f.vendor.contactperson'
    _rec_name='f_vendor_name'
    _description = 'Vendor Contact Person Details'

    
    f_vendor_name =fields.Char(string="Name")  
    f_vendor_no =fields.Char(string="Phone")
    f_vendor_id = fields.Many2one('res.partner',string="Vendor")

    f_primary =fields.Boolean(string="Primary")
    f_title =fields.Char(string="Title") 
    f_note =fields.Char(string="Note")

    f_vendor_email = fields.Char(string="Email")


