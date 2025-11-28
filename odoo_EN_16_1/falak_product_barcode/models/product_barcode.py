# -*- coding: utf-8 -*-
from odoo import models, api,fields, _
from odoo.exceptions import UserError, ValidationError


# class FPOSCATE(models.Model):
#     _inherit = "pos.category"
# 
#     f_barcode_prefix= fields.Char('Barcode Prefix')
    
    
#     @api.onchange('f_barcode_prefix')
#     def get_changes(self):
#             
#             print(self.f_barcode_prefix)
#             if self.f_barcode_prefix:
#             
#                 if (len(self.f_barcode_prefix) > 5) or (len(self.f_barcode_prefix)  < 5 ):
#                     raise UserError(_(
#                                             'Barcode prefix must be 5 digits'
#                                         ))
                    

class Fproductproduct(models.Model):
    _inherit = "product.product"

    f_barcode_general_setting= fields.Boolean('Check Barcode Setting')
    
    
    
    
    @api.model
    def default_get(self,field_lst):
        res = super(Fproductproduct, self).default_get(field_lst)
        if self.env['ir.config_parameter'].sudo().get_param('falak_product_barcode.f_barcode_setting'):
            res['f_barcode_general_setting'] = True
        return res



    @api.model
    def create(self, vals):
        res = super(Fproductproduct, self).create(vals)
        
        if res:
            if not vals.get('barcode') and self.env['ir.config_parameter'].sudo().get_param('falak_product_barcode.f_barcode_setting'):
                    seq_number = self.env['ir.sequence'].next_by_code('f.barcode.seq')
                    seq_number = int(seq_number) + 199000000000
                    barcode_generate = self.env['barcode.nomenclature'].sanitize_ean("%s" % int(seq_number))
                    
                    res.write({'barcode' : barcode_generate})
                
                    
             

        return res

