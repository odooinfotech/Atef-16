# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class FTransferInherit(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        if self.env['ir.config_parameter'].sudo().get_param('prevent_sell_negative_qty.f_prevent_transfer'):
            for picking in self:
                groups = {}
                for move in picking.move_ids_without_package:
                    dic_name = move.product_id.id
                    if move.product_id.type == 'product':
                        if not groups.get(dic_name):
                            groups[dic_name] = {
                                'product': move.product_id.id,
                                'qty': move.product_uom_qty,
                            }
                        else:
                            groups[dic_name]['qty'] += move.product_uom_qty

                wh_location_ids = [loc['id'] for loc in self.env['stock.location'].search_read(
                    [('id', 'child_of', picking.location_id.id)], ['id'])]

                for product_id, values in groups.items():
                    product = self.env['product.product'].browse(product_id)
                    stock_qty = self.env['stock.quant'].search([
                        ('product_id', '=', product.id),
                        ('location_id', 'in', wh_location_ids)
                    ])
                    quantity = sum(quant.quantity for quant in stock_qty)

                    if values['qty'] != 0:
                        if (quantity < values['qty'] and
                                not self.env.user.has_group('prevent_sell_negative_qty.f_bypass_minus_transactions') and
                                picking.location_id.usage == 'internal'):
                            raise UserError(_(
                                'Can NOT Transfer product \n [%s]-[%s] \n Because the demand Qty is greater than the Available qty in stock... \n Please Contact Your Manager ')
                                            % (product.barcode, product.display_name))

        return super(FTransferInherit, self).button_validate()
