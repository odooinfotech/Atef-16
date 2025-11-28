from odoo import models, fields, api

class F_Bill_Of_Lading_Type(models.Model):
      _name = 'f.bill.of.lading.type'
      _description = 'Bill Of Lading Types'
      _rec_name = 'f_name'


      f_name = fields.Char(string="Bill Of Lading Type Name")
