# -*- coding: utf-8 -*-
from odoo import models, fields, api

class F_Account_Incoterm_Inherit(models.Model):
    _inherit ='account.incoterms'


    f_incoterm_location_type = fields.Selection([('loading', 'Loading'),('discharge', 'Discharge'),
                                                ('blank','Blank')],string="Incoterm Location Type")
    def name_get(self):
           result = []
           if self:
               for rec in self:
                    incoterm_code = rec.code
                    incoterm_name = rec.name
                                   
                    name =  incoterm_code + '   ' +  ' - ' + '  ' +  incoterm_name             
                    result.append((rec.id, name))
               return result
           return super(F_Account_Incoterm_Inherit,self).name_get()
