from odoo import _, api, fields, models
import re


class FInheritpicking(models.Model):
    _inherit = ['stock.picking']

    product_barcode_scan = fields.Char(string='Barcode')

    @api.model
    def on_barcode_scanned(self, picking_id, barcode):
        picking = self.browse(picking_id)
        product = self.env['product.product'].search(
            ['|', ('barcode', '=', barcode), ('default_code', '=', barcode)], limit=1)


        if not product:
            return {
                'warning': {
                    'title': _('User Error'),
                    'message': _('This barcode %s is not related to any product.') % barcode,
                }
            }

        move_lines = picking.move_ids.filtered(
            lambda r: r.product_id == product)




        if move_lines:
            for line in move_lines:
                line.write({
                    'quantity_done' : line.quantity_done +1

                })
        else:
            move = self.env['stock.move'].create({
                'name': product.name,
                'product_id': product.id,
                'product_uom_qty': 1,
                'location_id': picking.location_id.id,
                'location_dest_id': picking.location_dest_id.id,
                'product_uom': product.uom_id.id,
                'picking_id': picking.id,
                'state': 'assigned',
            })
            move._action_assign()


            # return {
            #     'warning': {
            #         'title': _('Successfully Added'),
            #         'message': _('%s - %s/%s.') % (
            #             product.name,
            #             sum(move.quantity_done for move in move_lines),
            #             sum(move.product_uom_qty for move in move_lines),
            #         )
            #     }
            # }


    @api.onchange('product_barcode_scan')
    def onchange_product_barcode_scan(self):
        barcode = self.product_barcode_scan
        self.product_barcode_scan = ''
        if barcode:
            pick_data = self.env['stock.picking'].search([('name','=',self.name)],limit=1)
            return self.on_barcode_scanned(pick_data.id, barcode)
