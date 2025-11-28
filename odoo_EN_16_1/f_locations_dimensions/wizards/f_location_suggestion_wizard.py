from odoo import models, fields, api, _


class FLocationSuggestionWizard(models.TransientModel):
    _name = "f.location.suggestion"
    _description = 'Location Suggestion Wizard'

    f_picking_id = fields.Many2one('stock.picking', string='Receipt')
    f_move_id = fields.Many2one('stock.move', string='Move')
    f_product_id = fields.Many2one('product.product', string='Product')
    f_default_code = fields.Char(string='Internal Reference', related="f_product_id.default_code")
    f_parent_location = fields.Many2one('stock.location', string='Parent Location',
                                        related="f_product_id.f_parent_location")
    f_product_uom_qty = fields.Float(string='Demand')
    f_product_packaging = fields.Many2one('product.packaging', string='Packaging',
                                          domain="[('product_id', '=', f_product_id)]")
    f_dest_location = fields.Many2one('stock.location', string='Destination Location',
                                      domain="[('id', 'child_of', f_parent_location), ('child_ids', '=', False)]")
    f_product_volume = fields.Float(string='Product Volume', readonly=True, digits='Volume')
    f_location_available_volume = fields.Float(string='Available Volume', related='f_dest_location.f_remaining_volume')
    f_confirmed = fields.Boolean(string='Confirmed', default=False)
    f_product_locations = fields.Char(string="Product Locations", compute='_f_compute_product_locations', store=True)

    @api.depends('f_product_id')
    def _f_compute_product_locations(self):
        for rec in self:
            cur_company_id = self.env.user.company_id[0].id
            if cur_company_id:
                quant_ids = self.env['stock.quant'].sudo().search(
                    [('product_id', '=', rec.f_product_id.id), ('location_id.usage', '=', 'internal'),
                     ('company_id', '=', cur_company_id)], order='location_id')
            else:
                quant_ids = self.env['stock.quant'].sudo().search(
                    [('product_id', '=', rec.f_product_id.id), ('location_id.usage', '=', 'internal')],
                    order='location_id')

            quant_ids.sorted(key=lambda a: (a.location_id.name))
            t_warehouses = {}

            for quant in quant_ids:
                if quant.location_id.name:
                    if quant.location_id.name not in t_warehouses:
                        t_warehouses.update({quant.location_id.name: 0})
                        print(t_warehouses)

                    t_warehouses[quant.location_id.name] += (quant.quantity)

                    print(t_warehouses)

            warehouse_quantity_text = '['
            ks = t_warehouses.keys()
            ks = sorted(ks)
            for i in ks:
                if t_warehouses[i] != 0:
                    warehouse_quantity_text = warehouse_quantity_text + ' ** ' + i + ': ' + str(t_warehouses[i])

            warehouse_quantity_text = warehouse_quantity_text + ']'
            rec.f_product_locations = warehouse_quantity_text

    @api.onchange('f_product_uom_qty', 'f_product_id')
    def _f_onchange_product_qty(self):
        for rec in self:
            product_volume = rec.f_product_uom_qty * rec.f_product_id.volume
            product_uom = self.env['uom.uom'].sudo().search([('name', '=', rec.f_product_id.volume_uom_name)])
            ref_product_volume = rec.f_reference_uom(product_volume, product_uom)
            new_product_volume = rec.f_new_uom(ref_product_volume, rec.f_dest_location.f_volume_uom)
            rec.f_product_volume = new_product_volume

    def f_reference_uom(self, quantity, uom):
        ref_uom = self.env['uom.uom'].sudo().search([
            ('uom_type', '=', 'reference'),
            ('category_id', '=', uom.category_id.id)])
        new_quantity = quantity
        if uom.id != ref_uom.id and uom.uom_type == 'bigger':
            new_quantity = quantity * uom.ratio
        elif uom.id != ref_uom.id and uom.uom_type == 'smaller':
            new_quantity = quantity / uom.ratio

        return new_quantity

    def f_new_uom(self, quantity, uom):
        ref_uom = self.env['uom.uom'].sudo().search([
            ('uom_type', '=', 'reference'),
            ('category_id', '=', uom.category_id.id)])
        new_quantity = quantity
        if uom.id != ref_uom.id and uom.uom_type == 'bigger':
            new_quantity = quantity / uom.ratio
        elif uom.id != ref_uom.id and uom.uom_type == 'smaller':
            new_quantity = quantity * uom.ratio

        return new_quantity

    def f_confirm_location_suggestion(self):
        lines = self[0].f_picking_id.move_line_ids_without_package
        for line in lines:
            suggestion = self.filtered_domain([('f_confirmed', '=', False), ('f_product_id', '=', line.product_id.id)])
            if suggestion:
                vals = {
                    'location_dest_id': suggestion[0].f_dest_location.id,
                    'qty_done': suggestion[0].f_product_uom_qty,
                    'reserved_uom_qty': suggestion[0].f_product_uom_qty
                }
                print('////////////////////////////// / // / update')
                line.write(vals)
                print('////////////////////////////// / // / updated')
                suggestion[0].write({'f_confirmed': True})
            else:
                line.unlink()

        for sug in self:
            if sug.f_confirmed == False:
                vals = {
                    'picking_id': sug.f_picking_id.id,
                    'move_id': sug.f_move_id.id,
                    'product_id': sug.f_product_id.id,
                    'location_dest_id': sug.f_dest_location.id,
                    'qty_done': sug.f_product_uom_qty,
                    'reserved_uom_qty': sug.f_product_uom_qty
                }
                print('////////////////////////////// / // / create')
                self.env['stock.move.line'].create(vals)
                print('////////////////////////////// / // / created')
                sug.write({'f_confirmed': True})

        return {'type': 'ir.actions.act_window_close'}

