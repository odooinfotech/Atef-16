# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import logging
_logger = logging.getLogger(__name__)


class FStockPickingInherit(models.Model):
    _inherit = 'stock.picking'

    def f_reference_uom(self, quantity, uom):
        new_quantity = quantity
        if uom:
            ref_uom = self.env['uom.uom'].sudo().search([
                ('uom_type', '=', 'reference'),
                ('category_id', '=', uom.category_id.id)])

            if uom.id != ref_uom.id and uom.uom_type == 'bigger':
                new_quantity = quantity * uom.ratio
            elif uom.id != ref_uom.id and uom.uom_type == 'smaller':
                new_quantity = quantity / uom.ratio

        return new_quantity

    def f_new_uom(self, quantity, uom):
        new_quantity = quantity
        if uom:
            ref_uom = self.env['uom.uom'].sudo().search([
                ('uom_type', '=', 'reference'),
                ('category_id', '=', uom.category_id.id)])
            if uom.id != ref_uom.id and uom.uom_type == 'bigger':
                new_quantity = quantity / uom.ratio
            elif uom.id != ref_uom.id and uom.uom_type == 'smaller':
                new_quantity = quantity * uom.ratio
        return new_quantity

    def f_products_locations(self):
        self.ensure_one()
        vals = []
        locations_suggestions = []
        for move in self.move_ids_without_package:
            product_volume = move.reserved_availability * move.product_id.volume
            product_uom = self.env['uom.uom'].sudo().search([('name', '=', move.product_id.volume_uom_name)])
            ref_product_volume = self.f_reference_uom(product_volume, product_uom)

            quants = self.env['stock.quant'].read_group(
                domain=[
                    ('product_id', '=', move.product_id.id),
                    ('location_id', 'child_of', move.product_id.f_parent_location.id)
                ],
                fields=['product_id', 'location_id'],
                groupby=['location_id']
            )
            print("////////////////////////////////////// quants: ", quants)
            location_to_suggest = []
            total_volume = ref_product_volume
            print("////////////////////////////////////// total_volume: ", total_volume)
            total_qty = move.reserved_availability
            locations = False
            if quants:
                print("there is a quantity for product ", move.product_id.name)
                quant_locations = []
                for quant in quants:
                    location = self.env['stock.location'].browse([quant['location_id'][0]])
                    quant_locations.append(location.id)

                locations = self.env['stock.location'].sudo().search([
                    ('id', 'in', quant_locations),
                    ('child_ids', '=', False)
                ])
                locations._f_compute_remaining_volume()

                sorted_locations = sorted(locations, key=lambda loc: loc.f_remaining_volume, reverse=True)
                print("there is a location ", sorted_locations, " for product ", move.product_id.name)
                one_location = False
                for loc in sorted_locations:

                    ref_location_volume = self.f_reference_uom(loc.f_remaining_volume, loc.f_volume_uom)
                    suggested_volume = 0.0
                    for ls in locations_suggestions:
                        if ls.get('location').id == loc.id:
                            _logger.info(_("////////////////////////////// ls.get('qty'): %s") % ls.get('qty'))
                            volume = ls.get('qty') * ls.get('product').volume
                            uom = self.env['uom.uom'].sudo().search([('name', '=', ls.get('product').volume_uom_name)])
                            ref_volume = self.f_reference_uom(volume, uom)
                            _logger.info(_("////////////////////////////// ref_volume: %s") % ref_volume)
                            suggested_volume += ref_volume
                    ref_location_volume = ref_location_volume - suggested_volume
                    if ref_location_volume >= ref_product_volume:
                        print("////////////////////////////////////// total_volume == ref_product_volume: ", total_volume)
                        location_to_suggest.clear()
                        total_volume = ref_product_volume
                        total_qty = move.reserved_availability
                        data = {
                            'location': loc,
                            'qty': total_qty
                        }
                        location_to_suggest.append(data)
                        total_volume = 0.0
                        total_qty = 0.0
                        one_location = True
                    elif ref_location_volume == 0.0 and total_volume > 0.000000 and not one_location:
                        print("////////////////////////////////////// total_volume: ", total_volume)
                        ref_unit_product_volume = self.f_reference_uom(move.product_id.volume, product_uom)
                        qty_quotient, qty_remainder = divmod(ref_location_volume, ref_unit_product_volume)
                        ref_used_volume = qty_quotient * ref_unit_product_volume

                        if qty_quotient > total_qty:
                            qty_quotient = total_qty
                            ref_used_volume = qty_quotient * ref_unit_product_volume
                        total_volume = total_volume - ref_used_volume
                        total_qty = total_qty - qty_quotient
                        print("////////////////////////////////////// remain prod total qty: ", total_qty)

                        if qty_quotient > 0.0:
                            data = {
                                'location': loc,
                                'qty': qty_quotient
                            }
                            location_to_suggest.append(data)
                    print("total_qty after quant Loc", total_qty)

            if len(location_to_suggest) == 0 or total_qty > 0:
                print("len(location_to_suggest)", len(location_to_suggest))
                print("total_qty after quant", total_qty)
                print("there is no quantity for product ", move.product_id.name)
                if locations:
                    parent_locations = self.env['stock.location'].sudo().search([
                        ('id', 'child_of', move.product_id.f_parent_location.id),
                        ('id', 'not in', locations.ids),
                        ('child_ids', '=', False)])
                else:
                    parent_locations = self.env['stock.location'].sudo().search([
                        ('id', 'child_of', move.product_id.f_parent_location.id),
                        ('child_ids', '=', False)])
                parent_locations._f_compute_remaining_volume()
                location_to_suggest_two = []
                sorted_locations = sorted(parent_locations, key=lambda loc: loc.f_remaining_volume, reverse=True)
                print("there is a location ", sorted_locations, " for product ", move.product_id.name)
                one_location = False
                for parent_location in sorted_locations:
                    ref_location_volume = self.f_reference_uom(parent_location.f_remaining_volume, parent_location.f_volume_uom)
                    suggested_volume = 0.0
                    for ls in locations_suggestions:
                        if ls.get('location').id == parent_location.id:
                            _logger.info(_("////////////////////////////// ls.get('qty'): %s") % ls.get('qty'))
                            volume = ls.get('qty') * ls.get('product').volume
                            uom = self.env['uom.uom'].sudo().search([('name', '=', ls.get('product').volume_uom_name)])
                            ref_volume = self.f_reference_uom(volume, uom)
                            _logger.info(_("////////////////////////////// ref_volume: %s") % ref_volume)
                            suggested_volume += ref_volume
                    _logger.info(_("////////////////////////////// product: %s, location: %s, suggested_volume: %s") % (move.product_id.default_code, parent_location.name, suggested_volume))
                    ref_location_volume = ref_location_volume - suggested_volume
                    _logger.info(_("////////////////////////////// ref_location_volume: %s") % ref_location_volume)
                    if ref_location_volume >= total_volume:
                        print('//////////////////////////////// total_volume', total_volume)
                        print('//////////////////////////////// ref_location_volume', ref_location_volume)
                        location_to_suggest_two.clear()
                        data = {
                            'location': parent_location,
                            'qty': total_qty
                        }
                        location_to_suggest_two.append(data)
                        one_location = True
                    elif ref_location_volume == 0.0 and total_volume > 0.00000 and not one_location:
                        ref_unit_product_volume = self.f_reference_uom(move.product_id.volume, product_uom)
                        qty_quotient, qty_remainder = divmod(ref_location_volume, ref_unit_product_volume)
                        ref_used_volume = qty_quotient * ref_unit_product_volume

                        if qty_quotient > total_qty:
                            qty_quotient = total_qty
                            ref_used_volume = qty_quotient * ref_unit_product_volume
                        total_volume = total_volume - ref_used_volume
                        total_qty = total_qty - qty_quotient

                        if qty_quotient > 0.0:
                            data = {
                                'location': parent_location,
                                'qty': qty_quotient
                            }
                            location_to_suggest_two.append(data)

                for ltst in location_to_suggest_two:
                    location_to_suggest.append(ltst)

            for lts in location_to_suggest:
                value = {
                    'location': lts.get('location'),
                    'qty': lts.get('qty'),
                    'product': move.product_id
                }
                locations_suggestions.append(value)
                print("lts name ", lts.get('location').name)
                volume = lts.get('qty') * move.product_id.volume
                ref_volume = self.f_reference_uom(volume, product_uom)
                new_volume = self.f_new_uom(ref_volume, lts.get('location').f_volume_uom)
                _logger.info(_("//////////////////////////////// final new_volume: %s, location: %s") % (new_volume, lts.get('location').name))
                val = {
                    'f_picking_id': self.id,
                    'f_move_id': move.id,
                    'f_product_id': move.product_id.id,
                    'f_product_uom_qty': lts.get('qty'),
                    'f_product_packaging': move.product_packaging_id.id,
                    'f_dest_location': lts.get('location').id,
                    'f_product_volume': new_volume,
                    'f_location_available_volume': lts.get('location').f_remaining_volume

                }
                print(val)
                vals.append(val)
        print(vals)
        self.env.cr.execute("DELETE FROM f_location_suggestion where f_picking_id = %s;" % self.id)
        self.env.cr.commit()
        self.env['f.location.suggestion'].create(vals)

        res = {
            'type': 'ir.actions.act_window',
            'name': 'Location Suggestion',
            'target': 'new',
            'view_mode': 'tree',
            'res_model': 'f.location.suggestion',
            'view_id': self.env.ref('f_locations_dimensions.f_location_suggestion_tree_view').id,
            'domain': [('f_picking_id', '=', self.id)]
        }
        return res
