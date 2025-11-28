# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare, float_is_zero, float_round
import logging
_logger = logging.getLogger(__name__)

class FStockPickingInherit(models.Model):
    _inherit = 'stock.picking'

    def f_print_packages(self):
        packages_id = self.move_line_ids.mapped('result_package_id')
        packages = self.env['stock.quant.package'].sudo().search([('id', 'in', packages_id.ids),
                                                                  ('f_printed', '=', False)])
        if packages:
            packages.write({'f_printed': True})
            print("///////////////////////// 123", packages)
            return (self.env.ref('f_packages_management.f_action_package_label_barcode').
                    report_action(packages))

    def _f_package_move_lines(self, batch_pack=False):
        picking_move_lines = self.move_line_ids
        # in theory, the following values in the "if" statement after this should always be the same
        # (i.e. for batch transfers), but customizations may bypass it and cause unexpected behavior
        # so we avoid allowing those situations
        if len(self.picking_type_id) > 1:
            raise UserError(_("You cannot pack products into the same package when they are from different transfers with different operation types."))
        if len(set(self.mapped("immediate_transfer"))) > 1:
            raise UserError(_("You cannot pack products into the same package when they are from both immediate and planned transfers."))
        if (
            not self.picking_type_id.show_reserved
            and any(not p.immediate_transfer for p in self)
            and not self.env.context.get('barcode_view')
        ):
            picking_move_lines = self.move_line_nosuggest_ids

        move_line_ids = picking_move_lines.filtered(lambda ml: float_compare(ml.qty_done, 0.0,
                                                    precision_rounding=ml.product_uom_id.rounding) > 0
                                                    and not ml.result_package_id
                                                    )
        if not move_line_ids:
            move_line_ids = picking_move_lines.filtered(lambda ml: float_compare(ml.reserved_uom_qty, 0.0,
                                                                                 precision_rounding=ml.product_uom_id.rounding) > 0 and float_compare(
                ml.qty_done, 0.0,
                precision_rounding=ml.product_uom_id.rounding) == 0)
        return move_line_ids

    def _f_pre_put_in_pack_hook(self, move_line_ids):
        return self._f_check_destinations(move_line_ids)

    def _f_check_destinations(self, move_line_ids):
        if len(move_line_ids.mapped('location_dest_id')) > 1:
            view_id = self.env.ref('f_packages_management.f_stock_package_destination_form_view').id
            wiz = self.env['f.stock.package.destination'].create({
                'f_picking_id': self.id,
                'f_location_dest_id': move_line_ids[0].location_dest_id.id,
            })
            return {
                'name': _('Choose destination location'),
                'view_mode': 'form',
                'res_model': 'f.stock.package.destination',
                'view_id': view_id,
                'views': [(view_id, 'form')],
                'type': 'ir.actions.act_window',
                'res_id': wiz.id,
                'target': 'new'
            }
        else:
            return {}

    def _f_put_in_pack(self, move_line_ids, create_package_level=True):
        package = False
        package_ids = []
        packages = []
        for pick in self:
            move_lines_to_pack = self.env['stock.move.line']

            precision_digits = self.env['decimal.precision'].precision_get('Product Unit of Measure')
            if float_is_zero(move_line_ids[0].qty_done, precision_digits=precision_digits):
                for line in move_line_ids:
                    line.qty_done = line.reserved_uom_qty

            for ml in move_line_ids:
                if float_compare(ml.qty_done, ml.reserved_uom_qty, precision_rounding=ml.product_uom_id.rounding) >= 0:
                    if ml.move_id.product_packaging_id.f_delivery_packaging:
                        done = ml.qty_done
                        pack_qty = ml.move_id.product_packaging_id.qty
                        packages_to_create = []

                        while done > 0:
                            if done > pack_qty:
                                new_move_line = ml.copy(default={'reserved_uom_qty': 0, 'qty_done': pack_qty})
                                packages_to_create.append({'new_move_line': new_move_line, 'qty': pack_qty})
                                done = float_round(done - pack_qty, precision_rounding=ml.product_uom_id.rounding,
                                                   rounding_method='HALF-UP')
                                ml.write({'reserved_uom_qty': done, 'qty_done': done})
                                new_move_line.write({'reserved_uom_qty': pack_qty})
                            elif done == pack_qty:
                                packages_to_create.append({'new_move_line': ml, 'qty': pack_qty})
                                done = 0
                            else:
                                move_lines_to_pack |= ml
                                done = 0

                        _logger.info(_("///////////////////////////// packages_to_create: %s") % packages_to_create)
                        package_ids = self.env['stock.quant.package'].create([{'f_product_id': p['new_move_line'].move_id.product_id.id} for p in packages_to_create])
                        _logger.info(_("///////////////////////////// package_ids: %s") % package_ids)
                        packages += package_ids
                        for i, pack in enumerate(package_ids):
                            pack_type = packages_to_create[i]['new_move_line'].move_id.product_packaging_id.package_type_id
                            if len(pack_type) == 1:
                                pack.package_type_id = pack_type
                            packages_to_create[i]['new_move_line'].write({'result_package_id': pack.id})
                            new_move_line_dest_location = packages_to_create[i]['new_move_line']._get_default_dest_location()
                            packages_to_create[i]['new_move_line'].location_dest_id = new_move_line_dest_location._get_putaway_strategy(
                                product=packages_to_create[i]['new_move_line'].product_id,
                                quantity=packages_to_create[i]['new_move_line'].reserved_uom_qty,
                                package=pack)
                            if create_package_level:
                                package_level = self.env['stock.package_level'].create({
                                    'package_id': pack.id,
                                    'picking_id': pick.id,
                                    'location_id': False,
                                    'location_dest_id': packages_to_create[i]['new_move_line'].mapped('location_dest_id').id,
                                    'move_line_ids': [(6, 0, packages_to_create[i]['new_move_line'].ids)],
                                    'company_id': pick.company_id.id,
                                })

                    else:
                        move_lines_to_pack |= ml
                else:
                    quantity_left_todo = float_round(
                        ml.reserved_uom_qty - ml.qty_done,
                        precision_rounding=ml.product_uom_id.rounding,
                        rounding_method='HALF-UP')
                    done_to_keep = ml.qty_done
                    new_move_line = ml.copy(
                        default={'reserved_uom_qty': 0, 'qty_done': ml.qty_done})
                    vals = {'reserved_uom_qty': quantity_left_todo, 'qty_done': 0.0}
                    if pick.picking_type_id.code == 'incoming':
                        if ml.lot_id:
                            vals['lot_id'] = False
                        if ml.lot_name:
                            vals['lot_name'] = False
                    ml.write(vals)
                    new_move_line.write({'reserved_uom_qty': done_to_keep})
                    if new_move_line.move_id.product_packaging_id.f_delivery_packaging:
                        done = new_move_line.qty_done
                        pack_qty = new_move_line.move_id.product_packaging_id.qty
                        packages_to_create = []

                        while done > 0:
                            if done > pack_qty:
                                new_move_line_new = new_move_line.copy(
                                    default={'reserved_uom_qty': 0, 'qty_done': pack_qty})
                                packages_to_create.append({'new_move_line_new': new_move_line_new, 'qty': pack_qty})
                                done = float_round(done - pack_qty,
                                                   precision_rounding=new_move_line.product_uom_id.rounding,
                                                   rounding_method='HALF-UP')
                                new_move_line.write({'reserved_uom_qty': done, 'qty_done': done})
                                new_move_line_new.write({'reserved_uom_qty': pack_qty})
                            elif done == pack_qty:
                                packages_to_create.append({'new_move_line_new': new_move_line, 'qty': pack_qty})
                                done = 0
                            else:
                                move_lines_to_pack |= new_move_line
                                done = 0

                        package_ids = self.env['stock.quant.package'].create([{'f_product_id': p['new_move_line'].move_id.product_id.id} for p in packages_to_create])
                        packages += package_ids
                        for i, pack in enumerate(package_ids):
                            pack_type = packages_to_create[i][
                                'new_move_line_new'].move_id.product_packaging_id.package_type_id
                            if len(pack_type) == 1:
                                pack.package_type_id = pack_type
                            packages_to_create[i]['new_move_line_new'].write({'result_package_id': pack.id})
                            new_move_line_dest_location = packages_to_create[i]['new_move_line_new']._get_default_dest_location()
                            packages_to_create[i][
                                'new_move_line_new'].location_dest_id = new_move_line_dest_location._get_putaway_strategy(
                                product=packages_to_create[i]['new_move_line_new'].product_id,
                                quantity=packages_to_create[i]['new_move_line_new'].reserved_uom_qty,
                                package=pack)
                            if create_package_level:
                                package_level = self.env['stock.package_level'].create({
                                    'package_id': pack.id,
                                    'picking_id': pick.id,
                                    'location_id': False,
                                    'location_dest_id': packages_to_create[i]['new_move_line_new'].mapped('location_dest_id').id,
                                    'move_line_ids': [(6, 0, packages_to_create[i]['new_move_line_new'].ids)],
                                    'company_id': pick.company_id.id,
                                })

                    else:
                        move_lines_to_pack |= new_move_line
            if len(move_lines_to_pack) > 0:
                package = self.env['stock.quant.package'].create({})
            if package and not package.package_type_id:
                package_type = move_lines_to_pack.move_id.product_packaging_id.package_type_id
                if len(package_type) == 1:
                    package.package_type_id = package_type
            if len(move_lines_to_pack) == 1:
                default_dest_location = move_lines_to_pack._get_default_dest_location()
                move_lines_to_pack.location_dest_id = default_dest_location._get_putaway_strategy(
                    product=move_lines_to_pack.product_id,
                    quantity=move_lines_to_pack.reserved_uom_qty,
                    package=package)
            if len(move_lines_to_pack) > 0:
                move_lines_to_pack.write({
                    'result_package_id': package.id,
                })
                if create_package_level:
                    package_level = self.env['stock.package_level'].create({
                        'package_id': package.id,
                        'picking_id': pick.id,
                        'location_id': False,
                        'location_dest_id': move_lines_to_pack.mapped('location_dest_id').id,
                        'move_line_ids': [(6, 0, move_lines_to_pack.ids)],
                        'company_id': pick.company_id.id,
                    })
        if package:
            package_ids += package
            packages += package
        return packages

    def f_action_put_in_pack(self):
        self.ensure_one()
        if self.state not in ('done', 'cancel'):
            move_line_ids = self._f_package_move_lines()
            if move_line_ids:
                res = self._f_pre_put_in_pack_hook(move_line_ids)
                if not res:
                    res = self._f_put_in_pack(move_line_ids)
                return res
            else:
                raise UserError(_("Please add 'Done' quantities to the picking to create a new pack."))

