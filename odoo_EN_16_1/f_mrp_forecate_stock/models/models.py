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
        print('ttttttttttttttttttttttttt')
        res = super()._compute_draft_quantity_count(product_template_ids, product_variant_ids, wh_location_ids)
        res['draft_production_qty'] = {}
        domain = self._product_domain(product_template_ids, product_variant_ids)
        domain += [('state', '=', 'draft')]

        # Pending incoming quantity.
        mo_domain = domain + [('location_dest_id', 'in', wh_location_ids)]
        grouped_mo = self.env['mrp.production'].read_group(mo_domain, ['product_qty:sum'], 'product_id')
        res['draft_production_qty']['in'] = sum(mo['product_qty'] for mo in grouped_mo)

        # Pending outgoing quantity.
        move_domain = domain + [
            ('raw_material_production_id', '!=', False),
            ('location_id', 'in', wh_location_ids),
        ]
        grouped_moves = self.env['stock.move'].read_group(move_domain, ['product_qty:sum'], 'product_id')
        res['draft_production_qty']['out'] = sum(move['product_qty'] for move in grouped_moves)
        res['qty']['in'] += res['draft_production_qty']['in']
        res['qty']['out'] += res['draft_production_qty']['out']

        return res

    def _serialize_docs(self, docs, product_template_ids=False, product_variant_ids=False):
        print('99999999999999999999999')
        res = super()._serialize_docs(docs, product_template_ids, product_variant_ids)
        for i, line in enumerate(docs['lines']):
            if not line['move_out'] or not line['move_out']['raw_material_production_id']:
                continue
            raw_material_production = line['move_out']['raw_material_production_id']
            res['lines'][i]['move_out']['raw_material_production_id'] = \
            raw_material_production.read(fields=['id', 'unreserve_visible', 'reserve_visible', 'priority'])[0]
        return res