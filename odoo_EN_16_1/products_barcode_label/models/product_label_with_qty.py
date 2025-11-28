from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError

import logging
_logger = logging.getLogger(__name__)


class BarcodeProductLabelsLines(models.TransientModel):
    _name = "product.wizard.label.line"
    _description = "Product Label Line"

    product_id = fields.Many2one( 'product.template',string='Product',required=True)
    quantity = fields.Integer('Copies NO.',default=1,required=True)
    wizard_id = fields.Many2one('product.wizard.label', string='Wizard')
    price = fields.Float(string="Sale Price")
    barcode = fields.Char(string="Barcode")
    
    
    @api.model
    def _get_values(self):
        record = []
        for rec in self:
            for qty in range(int(rec.quantity)):
                record.append({
                               'product_id': rec.product_id.name,
                               'barcode': rec.product_id.barcode,
                               'quantity': rec.quantity,
                               'price': rec.product_id.list_price,
                               })
                
        print(record,"rrrrrrrrrrrr")
        return record
    
    
    
class ProductWizardlabel(models.TransientModel):
    _name = 'product.wizard.label'
    _description = "Product Label"

    picking_moves_ids = fields.One2many('product.wizard.label.line', 'wizard_id', string='labels')
    picking_id = fields.Many2one('product.template',string='Product')
    
    @api.model
    def default_get(self, fields):
        res = super(ProductWizardlabel, self).default_get(fields)
        product_picking_moves = []
        pickings = self.env['product.template'].browse(self.env.context.get('active_ids'))
        for picking in pickings:
            if picking:
                print(picking.barcode,"picking.barcode")
                
                product_picking_moves.append((0, 0,
                                                  {'product_id': picking.id, 'barcode': picking.barcode,
                                                    'price': picking.list_price}))
                res.update({'picking_moves_ids': product_picking_moves})
        return res
    
    
    def print_barcode_from_wizard(self):
        move_lines = self.env['product.wizard.label.line'].search([('wizard_id','=',self.id)])
        
        if not move_lines : 
            raise ValidationError( 'All Products Are Printed!')
        else :
            return self.env.ref('products_barcode_label.action_report_label_barcode').report_action(
                move_lines)
