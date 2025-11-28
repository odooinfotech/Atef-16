# -*- coding: utf-8 -*-
from odoo import models, fields, api



class FBarcodeManual(models.TransientModel):
    _name = 'f.barcode.manual'
    _description = 'Barcode Manual'

    
    


    def f_generate_manual_barcode(self):
        if self.env['ir.config_parameter'].sudo().get_param('falak_product_barcode.f_barcode_setting'):
            for record in self.env['product.product'].browse(self._context.get('active_id')):
                    if  record.barcode:
                        continue
                
                    seq_number = self.env['ir.sequence'].next_by_code('f.barcode.seq')
                    seq_number = int(seq_number) + 199000000000
                    barcode_generate = self.env['barcode.nomenclature'].sanitize_ean("%s" % int(seq_number))
                    record.write({'barcode':barcode_generate})
                
              
                
            return True
        

class FProductAutoBarcode(models.TransientModel):
    _name = 'f.barcode.auto'
    _description = 'Barcode Auto'

    


    def f_generate_auto_barcode(self):
        if self.env['ir.config_parameter'].sudo().get_param('falak_product_barcode.f_barcode_setting'):
            for record in self.env['product.product'].browse(self._context.get('active_ids')):
                if  record.barcode:
                    continue
                
                
                
                seq_number = self.env['ir.sequence'].next_by_code('f.barcode.seq')
                seq_number = int(seq_number) + 199000000000
                barcode_generate = self.env['barcode.nomenclature'].sanitize_ean("%s" % int(seq_number))
                record.write({'barcode':barcode_generate})
                
         
            return True

