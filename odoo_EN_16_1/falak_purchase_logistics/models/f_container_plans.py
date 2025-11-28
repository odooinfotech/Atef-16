from odoo import models, fields, api

class F_Container_Plans(models.Model):
    _name = 'f.container.plans'
    _description = 'Container Plans'
    

    f_po_id = fields.Many2one('purchase.order', string="Purchase Order")
    
    f_po_plan_id = fields.Many2one('f.purchase.order.planning', string="PO Planning")
    
    f_product_name = fields.Many2one('product.product',string="Product Name")

    f_product_desc = fields.Text(related="f_po_plan_id.f_product_description")

    f_intarnal_referance = fields.Char(related="f_po_plan_id.f_internal_ref",store=True)
    
    f_commercial_invoice_number = fields.Char(related="f_po_plan_id.f_commercial_inv_num")
    
    qty = fields.Float(string="Quantity")
        
    f_container_details = fields.Many2one('f.container.details', string="Container Details")
    
    
