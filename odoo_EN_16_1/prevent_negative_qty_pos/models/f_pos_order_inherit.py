from odoo import fields, models, api, _

class FnegqtyfposConfig(models.Model):
    _inherit = 'pos.config'

    pos_deny_order = fields.Boolean(string='Deny POS Order When Product is Out of Stock' ,default=True)
    f_include_rese_pos = fields.Boolean("Include Reserved Qtys of product in Pos orders",default= True)
    f_location = fields.Many2one(related='picking_type_id.default_location_src_id',string='Stock Location')

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    pos_deny_order = fields.Boolean(related='pos_config_id.pos_deny_order',string='Deny POS Order When Product is Out of Stock', default=True,readonly=False)
    f_include_rese_pos = fields.Boolean(related='pos_config_id.f_include_rese_pos',string="Include Reserved Qtys of product in Pos orders", default=True,readonly=False)
    f_location = fields.Many2one(related='pos_config_id.f_location',string='Stock Location')






class FnegativeFstock_quant(models.Model):
    _inherit = 'stock.quant'    
    
    def get_singles_product(self, location,ss,list,f_reserved_qty):
        print(f_reserved_qty,"f_reserved_qty")
        res = []
        x = True
        for k,v in ss.items():
            pro = self.env['product.product'].browse(int(k))
            quants = self.env['stock.quant'].search([('product_id', '=', pro.id),('location_id', '=', location[0])])
            if len(quants) > 1:
                quantity = 0.0
                for quant in quants:
                    if f_reserved_qty:
                        quantity += quant.quantity
                    else:
                        quantity += quant.available_quantity
                        
                if v >0:
                    if v > quantity:
                        x = x and False
                        res.append(pro.display_name)
                        if pro.barcode:
                            res.append(pro.barcode)
                        
                print("qty",pro,quantity)
            else:
                if f_reserved_qty:
                    qty = quants.quantity
                else:
                    qty = quants.available_quantity
                    
                if v >0:
                    if v > qty:
                        x = x and False
                        res.append(pro.display_name)
                        if pro.barcode:
                            res.append(pro.barcode)
                        
        print('eeeeeeeeeee',res)
        return res
                
            

    

        
