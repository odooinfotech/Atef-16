# -*- coding: utf-8 -*-

from odoo import models, fields, api


class F_Purchase_Order_Inherit(models.Model):
    _inherit ='purchase.order'
    
    #f_one_lc_details =fields.One2many('f.lc.management','f_purchase_id',string="Lc Details")

    #PI Details 
    f_pi_number =fields.Char(string="PI Reference")
    f_pi_amount =fields.Float(string="PI Value (Total Amount)")
    f_pi_date =fields.Date(string="PI Issue Date",help="Date When Vendor Sent PI ")
    f_pi_attachment =fields.Binary(string='PI Attachment')
    f_pi_confirmed_attach =fields.Binary(string='Confirmed PI')
    file_name_pi = fields.Char(string='PI File ')
    file_name_confirmed_pi = fields.Char(string='Confirmed PI File')
    
    
    
    
    
    f_delivery_date =fields.Date(string="Expected Delivery Date")
    f_volume_cbm =fields.Float(string="Volume CBM")
    f_weight =fields.Float(string="Weight Kg")
    f_offer_validity =fields.Date(string="Offer Validity")
    f_pi_approval_date = fields.Date(string="Approval Date",help="When should Approve PI ")
    
   
