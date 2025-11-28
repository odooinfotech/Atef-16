# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import SUPERUSER_ID,_
from collections import defaultdict
import copy
from odoo import api, models
from odoo.tools import float_compare, float_is_zero, format_date, float_round
from odoo.tools.float_utils import float_is_zero, float_repr


class ReplenishmentReport(models.AbstractModel):
    _inherit = 'report.stock.report_product_product_replenishment'


    def _compute_draft_quantity_count(self, product_template_ids, product_variant_ids, wh_location_ids):
        in_domain, out_domain = self._move_draft_domain(product_template_ids, product_variant_ids, wh_location_ids)
        incoming_moves = self.env['stock.move']._read_group(in_domain, ['product_qty:sum'], 'product_id')
        outgoing_moves = self.env['stock.move']._read_group(out_domain, ['product_qty:sum'], 'product_id')
        in_sum = sum(move['product_qty'] for move in incoming_moves)
        out_sum = sum(move['product_qty'] for move in outgoing_moves)

        # po start
        domain_po = [('state', 'in', ['draft', 'sent', 'to approve'])]
        domain_po += self._product_purchase_domain(product_template_ids, product_variant_ids)
        warehouse_id = self.env.context.get('warehouse', False)
        if warehouse_id:
            domain_po += [('order_id.picking_type_id.warehouse_id', '=', warehouse_id)]
        po_lines = self.env['purchase.order.line'].sudo().search(domain_po)
        in_sum_po = sum(po_lines.mapped('product_uom_qty'))
     


        


        
        #po end 

        # sales start 
        domain_sales = self._product_sale_domain(product_template_ids, product_variant_ids)
        so_lines = self.env['sale.order.line'].sudo().search(domain_sales)
        out_sum_sale = 0
        if so_lines:
            product_uom = so_lines[0].product_id.uom_id
            quantities = so_lines.mapped(lambda line: line.product_uom._compute_quantity(line.product_uom_qty, product_uom))
            out_sum_sale = sum(quantities)
    



        


        

        # sales end 

        #stock_account start 

        if not self.user_has_groups('stock.group_stock_manager'):
            return  {
            'draft_picking_qty': {
                'in': in_sum,
                'out': out_sum
            },
            'qty': {
                'in': in_sum+in_sum_po,
                'out': out_sum+out_sum_sale
            },


            'draft_purchase_qty':in_sum_po,
             'draft_purchase_orders':po_lines.mapped("order_id").sorted(key=lambda po: po.name),
            'draft_purchase_orders_matched':self.env.context.get('purchase_line_to_match_id') in po_lines.ids,


            'draft_sale_qty':out_sum_sale,
             'draft_sale_orders':so_lines.mapped("order_id").sorted(key=lambda so: so.name),
            'draft_sale_orders_matched':self.env.context.get('sale_line_to_match_id') in so_lines.ids,
            
           
          
        }


            
        domain = self._product_domain(product_template_ids, product_variant_ids)
        company = self.env['stock.location'].browse(wh_location_ids[0]).company_id
        svl = self.env['stock.valuation.layer'].search(domain + [('company_id', '=', company.id)])
        domain_quants = [
            ('company_id', '=', company.id),
            ('location_id', 'in', wh_location_ids)
        ]
        if product_template_ids:
            domain_quants += [('product_id.product_tmpl_id', 'in', product_template_ids)]
        else:
            domain_quants += [('product_id', 'in', product_variant_ids)]
        quants = self.env['stock.quant'].search(domain_quants)
        currency = svl.currency_id or self.env.company.currency_id
        total_quantity = sum(svl.mapped('quantity'))
        # Because we can have negative quantities, `total_quantity` may be equal to zero even if the warehouse's `quantity` is positive.
        if svl and not float_is_zero(total_quantity, precision_rounding=svl.product_id.uom_id.rounding):
            value = sum(svl.mapped('value')) * (sum(quants.mapped('quantity')) / total_quantity)
        else:
            value = 0
        value = float_repr(value, precision_digits=currency.decimal_places)
        if currency.position == 'after':
            value = '%s %s' % (value, currency.symbol)
        else:
            value = '%s %s' % (currency.symbol, value)
        return {
            'draft_picking_qty': {
                'in': in_sum,
                'out': out_sum
            },
            'qty': {
                'in': in_sum+in_sum_po,
                'out': out_sum+out_sum_sale
            },


            'draft_purchase_qty':in_sum_po,
             'draft_purchase_orders':po_lines.mapped("order_id").sorted(key=lambda po: po.name),
            'draft_purchase_orders_matched':self.env.context.get('purchase_line_to_match_id') in po_lines.ids,


            'draft_sale_qty':out_sum_sale,
             'draft_sale_orders':so_lines.mapped("order_id").sorted(key=lambda so: so.name),
            'draft_sale_orders_matched':self.env.context.get('sale_line_to_match_id') in so_lines.ids,
            'value':value
            
           
          
        }

        # account finish
        


        
        


    

    def _serialize_docs(self, docs, product_template_ids=False, product_variant_ids=False):
        print('origin foraceeeeeeeeeeeeeeee')
        """
        Since conversion from report to owl client_action, adapt/override this method to make records available from js code.
        """
        res = copy.copy(docs)
        if product_template_ids:
            res['product_templates'] = docs['product_templates'].read(fields=['id', 'display_name'])
            product_variants = []
            for pv in docs['product_variants']:
                product_variants.append({
                        'id' : pv.id,
                        'combination_name' : pv.product_template_attribute_value_ids._get_combination_name(),
                    })
            res['product_variants'] = product_variants
        elif product_variant_ids:
            res['product_variants'] = docs['product_variants'].read(fields=['id', 'display_name'])
        


        
        
        res['lines'] = []
        for index, line in enumerate(docs['lines']):
            res['lines'].append({
                'index': index,
                'document_in' : {
                    '_name' : line['document_in']._name,
                    'id' : line['document_in']['id'],
                    'name' : line['document_in']['name'],
                } if line['document_in'] else False,
                'document_out' : {
                    '_name' : line['document_out']._name,
                    'id' : line['document_out']['id'],
                    'name' : line['document_out']['name'],
                } if line['document_out'] else False,
                'uom_id' : line['uom_id'].read()[0],
                'move_out' : line['move_out'].read(self._fields_for_serialized_moves())[0] if line['move_out'] else False,
                'move_in' : line['move_in'].read(self._fields_for_serialized_moves())[0] if line['move_in'] else False,
                'product': line['product'],
                'replenishment_filled': line['replenishment_filled'],
                'receipt_date': line['receipt_date'],
                'delivery_date': line['delivery_date'],
                'is_late': line['is_late'],
                'quantity': line['quantity'],
                'reservation': line['reservation'],
                'is_matched': line['is_matched'],
            })
            if line['move_out'] and line['move_out']['picking_id']:
                res['lines'][-1]['move_out'].update({
                    'picking_id' : line['move_out']['picking_id'].read(fields=['id', 'priority'])[0],
                    })

        #start custom sale - forcaste

        res['draft_sale_orders'] = docs['draft_sale_orders'].read(fields=['id', 'name'])

        
        for i in range(len(docs['lines'])):
            if not docs['lines'][i]['move_out'] or not docs['lines'][i]['move_out']['picking_id'] or not \
            docs['lines'][i]['move_out']['picking_id']['sale_id']:
                continue
            picking = docs['lines'][i]['move_out']['picking_id']
            res['lines'][i]['move_out'].update({
                'picking_id': {
                    'id': picking.sudo().id,
                    'priority': picking.sudo().priority,
                     'sale_id': {
                         'id': picking.sudo().sale_id.sudo().id,
                         'amount_untaxed': picking.sudo().sale_id.sudo().amount_untaxed,
                         'currency_id': picking.sudo().sale_id.sudo().currency_id.read(fields=['id', 'name'])[0],
                         'partner_id': picking.sudo().sale_id.sudo().partner_id.sudo().read(fields=['id', 'name'])[0],
                     }
                }
            })


        # finish custom

        # start custom po - forcaste
        res['draft_purchase_orders'] = docs['draft_purchase_orders'].read(fields=['id', 'name'])
        # finish po forcaste

        return res


