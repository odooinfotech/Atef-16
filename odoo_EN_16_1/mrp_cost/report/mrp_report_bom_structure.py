# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class MrpReportBomStructure(models.AbstractModel):
    _inherit = 'report.mrp.report_bom_structure'
    
    @api.model
    def _get_bom_data(self, bom, warehouse, product=False, line_qty=False, bom_line=False, level=0, parent_bom=False, index=0, product_info=False, ignore_stock=False):
        res = super(MrpReportBomStructure, self)._get_bom_data(bom, warehouse, product, line_qty, bom_line, level, parent_bom, index, product_info, ignore_stock)
        
        if not product_info:
            product_info = {}
        key = product.id
        if key not in product_info:
            product_info[key] = {'consumptions': {'in_stock': 0}}
        
        current_quantity = line_qty
        if bom_line:
            current_quantity = bom_line.product_uom_id._compute_quantity(line_qty, bom.product_uom_id) or 0
            
        print('1 ==> ',current_quantity)
        
        bom_key = bom.id
        if not product_info[key].get(bom_key):
            product_info[key][bom_key] = self.with_context(product_info=product_info, parent_bom=parent_bom)._get_resupply_route_info(warehouse, product, current_quantity, bom)
            
        components = []
        for component_index, line in enumerate(bom.bom_line_ids):
            new_index = f"{index}{component_index}"
            if product and line._skip_bom_line(product):
                continue
            
            line_quantity = (current_quantity / (bom.product_qty or 1.0)) * line.product_qty
            
            if line.child_bom_id:
                component = self.with_context(parent_product_id=product.id)._get_bom_data(line.child_bom_id, warehouse, line.product_id, line_quantity, bom_line=line, level=level + 1, parent_bom=bom,
                                                                                          index=new_index, product_info=product_info, ignore_stock=ignore_stock)
            else:
                component = self.with_context(parent_product_id=product.id)._get_component_data(bom, warehouse, line, line_quantity, level + 1, new_index, product_info, ignore_stock)
            res['bom_cost'] -= component['bom_cost']
            
            line_quantity = 0.0
            bom_prod_qty   = line.bom_id.product_qty
            bom_prod_weight= line.bom_id.weight
            bom_line_qty   = line.product_qty
            
            if line.coefficent_parameters == 'percentage_with_co':
                line_quantity = bom_prod_qty* bom_prod_weight * (line.quantity_ratio_percent / 100) 
                                                                
            
            
            elif line.coefficent_parameters == 'only_co':
                line_quantity = (bom_prod_qty * line.product_qty) / (line.quantity_coefficient or 1)
            
            
            else : 
                line_quantity = bom_line_qty
            
            
            if not line.is_supplementary_product  :
            
                line_quantity = line_quantity +(line_quantity * line.loss_percent) / 100
            
            print('3 ==> ',line_quantity)
            line_quantity = round(line_quantity, 2)
            line_quantity = (current_quantity / (bom.product_qty or 1.0)) * line_quantity
            if line.child_bom_id:
                component = self.with_context(parent_product_id=product.id)._get_bom_data(line.child_bom_id, warehouse, line.product_id, line_quantity, bom_line=line, level=level + 1, parent_bom=bom,
                                                                                          index=new_index, product_info=product_info, ignore_stock=ignore_stock)
            else:
                component = self.with_context(parent_product_id=product.id)._get_component_data(bom, warehouse, line, line_quantity, level + 1, new_index, product_info, ignore_stock)
            components.append(component)
            res['bom_cost'] += component['bom_cost']
        res['components'] = components
        
        
        return res