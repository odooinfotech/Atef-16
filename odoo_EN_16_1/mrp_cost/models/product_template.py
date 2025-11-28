# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from unicodedata import digit

from odoo import fields, models, _
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger('Compute MRP Cost')


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_overhead = fields.Boolean('Is Overhead?', tracking=True)
    f_default_bom = fields.Many2one('mrp.bom', string='Default BOM')

    def _f_get_comp_values(self):
        record = []
        bom = self.env['mrp.bom'].sudo().search([('f_default_bom', '=', True), ('id', 'in', self.bom_ids.ids)], limit=1)
        if bom:
            for component in bom.bom_line_ids:
                line_quantity = 0.0
                if component.coefficent_parameters == 'percentage_with_co':
                    line_quantity = bom.product_qty * bom.weight * (component.quantity_ratio_percent / 100)

                elif component.coefficent_parameters == 'only_co':
                    line_quantity = (bom.product_qty * component.product_qty) / (component.quantity_coefficient or 1)

                else:
                    line_quantity = component.product_qty

                if not component.is_supplementary_product:
                    line_quantity = line_quantity + (line_quantity * component.loss_percent) / 100

                print("line qty: ", line_quantity)
                _logger.info("line qty: %s", line_quantity)
                line_quantity = self.f_convert_uom_product(line_quantity, 1, bom.product_qty, bom.product_uom_id)

                line_quantity = round(line_quantity, 6)
                print("Converted Line QTY", line_quantity)
                print("Product Name", component.product_id.name)
                print("standard_price", component.product_id.standard_price)
                line_cost = line_quantity * component.product_id.standard_price
                line_cost = round(line_cost, 4)

                record.append({
                    'component': component.product_id,
                    'line_quantity': line_quantity,
                    'line_uom': component.product_uom_id.name,
                    'standard_price': component.product_id.standard_price,
                    'loss_percent': component.loss_percent,
                    'coefficent_parameters': component.coefficent_parameters,
                    'quantity_ratio_percent': component.quantity_ratio_percent,
                    'quantity_coefficient': component.quantity_coefficient,
                    'line_cost': line_cost,
                })

        return record

    def _f_get_op_values(self):
        record = []
        bom = self.env['mrp.bom'].sudo().search([('f_default_bom', '=', True), ('id', 'in', self.bom_ids.ids)], limit=1)
        if bom:
            for operation_line in bom.operation_ids:
                work_center = operation_line.workcenter_id
                operation_cost = 0.0
                if work_center.default_capacity >= 1:
                    duration = operation_line.time_cycle
                    print("duration: ", duration)
                    _logger.info("duration: %s", duration)
                    hour_duration = duration / 60
                    second_duration = duration * 60
                    hour_cost = work_center.costs_hour
                    operation_cost = hour_duration * hour_cost
                    operation_cost = round(operation_cost, 4)
                    record.append({
                        'work_center': work_center.name,
                        'operation_line': operation_line,
                        'second_duration': second_duration,
                        'hour_cost': hour_cost,
                        'operation_cost': operation_cost,
                    })
                elif work_center.default_capacity < 1:
                    quantity = 1 / work_center.default_capacity
                    duration = operation_line.time_cycle * quantity
                    print("duration: ", duration)
                    _logger.info("duration: %s", duration)
                    hour_duration = duration / 60
                    hour_cost = work_center.costs_hour
                    operation_cost = hour_duration * hour_cost
                    operation_cost = round(operation_cost, 4)
                    record.append({
                        'work_center': work_center.name,
                        'operation_line': operation_line,
                        'hour_duration': hour_duration,
                        'hour_cost': hour_cost,
                        'operation_cost': operation_cost,
                    })



        return record

    def _f_get_overhead_values(self):
        record = []
        bom = self.env['mrp.bom'].sudo().search([('f_default_bom', '=', True), ('id', 'in', self.bom_ids.ids)], limit=1)
        if bom:
            unit_total_cost = self._f_get_cost_without_overhead()
            for line in bom.overhead_line_ids:
                if line.overhead_parameters == "amount_div_by_duration":
                    duration = sum(bom.operation_ids.mapped('time_cycle'))

                    print('5 duration ==> ', duration)
                    duration_cost = ((duration / 60.0) * line.overhead_cost)
                    duration_cost = round(duration_cost, 4)

                    record.append({
                        'product': line.product_id,
                        'overhead_parameters': 'Amount/ Duration (per hours)',
                        'cost': line.overhead_cost,
                        'total_cost': duration_cost,
                    })

                # Calculation of 'Percent (%)'
                if line.overhead_parameters == "percent":
                    percent_cost = (line.overhead_cost * unit_total_cost) / 100
                    percent_cost = round(percent_cost, 4)
                    record.append({
                        'product': line.product_id,
                        'overhead_parameters': 'Percent(%)',
                        'cost': line.overhead_cost,
                        'total_cost': percent_cost,
                    })
                # Calculation of 'Amount/ Final QTY'
                if line.overhead_parameters == "amount_div_by_final_qty":
                    final_cost = line.overhead_cost
                    record.append({
                        'product': line.product_id,
                        'overhead_parameters': 'Amount/ Final QTY',
                        'cost': line.overhead_cost,
                        'total_cost': final_cost,
                    })

        return record

    def _f_get_cost_without_overhead(self):
        unit_total_cost = 0.0
        bom = self.env['mrp.bom'].sudo().search([('f_default_bom', '=', True), ('id', 'in', self.bom_ids.ids)], limit=1)
        if bom:
            unit_total_component_cost = self.compute_bom_components_cost(bom)
            unit_total_component_cost = round(unit_total_component_cost, 4)
            operations_cost = self.compute_bom_operations_cost(bom)
            operations_cost = round(operations_cost, 4)
            unit_total_cost = unit_total_component_cost + operations_cost


        return unit_total_cost

    def _f_get_overhead_total(self):
        overhead = 0.0
        bom = self.env['mrp.bom'].sudo().search([('f_default_bom', '=', True), ('id', 'in', self.bom_ids.ids)], limit=1)
        if bom:
            overhead = bom.total_cost_over_head_percent
        return overhead
    def _f_get_cost_with_overhead(self):
        total_cost_with_overhead = 0.0
        bom = self.env['mrp.bom'].sudo().search([('f_default_bom', '=', True), ('id', 'in', self.bom_ids.ids)], limit=1)
        if bom:
            unit_total_component_cost = self.compute_bom_components_cost(bom)
            unit_total_component_cost = round(unit_total_component_cost, 4)
            operations_cost = self.compute_bom_operations_cost(bom)
            operations_cost = round(operations_cost, 4)
            unit_total_cost = unit_total_component_cost + operations_cost
            overhead_cost = self.compute_bom_overhead_cost(bom,unit_total_cost)
            total_cost_with_overhead = unit_total_cost + overhead_cost
            total_cost_with_overhead = total_cost_with_overhead + (
                        total_cost_with_overhead * (bom.total_cost_over_head_percent / 100))
        return total_cost_with_overhead
    

    def button_bom_weight(self):
        return self.mapped('product_variant_id').button_bom_weight()

    def compute_bom_set(self):
        for rec in self:
            bom = self.env['mrp.bom'].sudo().search([('f_default_bom','=',True),('id','in',rec.bom_ids.ids)],limit=1)
            if bom:
                rec.f_bom_set = True
            else:
                rec.f_bom_set = False

    def compute_bom_cost(self):

        records = self.sudo().search([('id','in',self.ids)])
        if not records:
            records = self.sudo().search([('bom_ids','!=',False)])
        for rec in records:
            _logger.info("start compute_bom_cost  %s", rec.id)
            bom = self.env['mrp.bom'].sudo().search([('f_default_bom','=',True),('id','in',rec.bom_ids.ids)],limit=1)
            if bom:
                rec.f_default_bom = bom.id
                unit_total_component_cost = rec.compute_bom_components_cost(bom)
                unit_total_component_cost = round(unit_total_component_cost, 4)

                print('2 unit_total_component_cost ==> ',unit_total_component_cost)
                _logger.info("2 unit_total_component_cost ==> %s", unit_total_component_cost)
                
                
                operations_cost = rec.compute_bom_operations_cost(bom)
                operations_cost = round(operations_cost, 4)
                
                    
                print('3 operations_cost ==> ',operations_cost)
                _logger.info("3 operations_cost ==> %s", operations_cost)
                
                unit_total_cost = unit_total_component_cost + operations_cost
                unit_total_cost = round(unit_total_cost, 4)
                print('4 unit_total_cost ==> ',unit_total_cost)
                _logger.info("4 unit_total_cost ==> %s", unit_total_cost)
                
                overhead_cost = rec.compute_bom_overhead_cost(bom,unit_total_cost)
                overhead_cost = round(overhead_cost, 4)
                    
                total_cost_with_overhead = unit_total_cost + overhead_cost
                total_cost_with_overhead = round(total_cost_with_overhead, 4)
                total_cost_with_overhead = total_cost_with_overhead + (total_cost_with_overhead * (bom.total_cost_over_head_percent / 100))
                total_cost_with_overhead = round(total_cost_with_overhead, 4)
                print(total_cost_with_overhead)
                _logger.info("5 total_cost_with_overhead ==> %s", total_cost_with_overhead)
                
                rec.f_bom_cost = total_cost_with_overhead
                
            else:
                rec.f_bom_cost = 0.0
                
                
    def f_convert_uom_product(self,line_quantity,new_product_qty,old_product_qty,old_uom):
        new_line_quantity = line_quantity / old_product_qty
        if self.uom_id.id != old_uom.id and old_uom.uom_type == 'bigger' and self.uom_id.uom_type == 'reference':
            new_line_quantity = new_line_quantity / old_uom.ratio
        elif self.uom_id.id != old_uom.id and old_uom.uom_type == 'reference' and self.uom_id.uom_type == 'bigger':
            new_line_quantity = new_line_quantity * old_uom.ratio
        elif self.uom_id.id != old_uom.id  and old_uom.uom_type == 'smaller' and self.uom_id.uom_type == 'reference':
            new_line_quantity = new_line_quantity * old_uom.ratio
        elif self.uom_id.id != old_uom.id and old_uom.uom_type == 'reference' and self.uom_id.uom_type == 'smaller':
            new_line_quantity = new_line_quantity / old_uom.ratio
        elif self.uom_id.id != old_uom.id and old_uom.uom_type == 'bigger' and self.uom_id.uom_type != 'reference':
            referance_qty = new_line_quantity / old_uom.ratio
            if self.uom_id.uom_type == 'bigger':
                new_line_quantity = referance_qty * self.uom_id.ratio
            elif self.uom_id.uom_type == 'smaller':
                new_line_quantity = referance_qty / self.uom_id.ratio
        elif self.uom_id.id != old_uom.id and old_uom.uom_type == 'smaller' and self.uom_id.uom_type != 'reference':
            referance_qty = new_line_quantity * old_uom.ratio
            if self.uom_id.uom_type == 'bigger':
                new_line_quantity = referance_qty * self.uom_id.ratio
            elif self.uom_id.uom_type == 'smaller':
                new_line_quantity = referance_qty / self.uom_id.ratio

            
        new_line_quantity = new_line_quantity * new_product_qty
        return new_line_quantity
    
    def compute_bom_components_cost(self,bom):
        unit_total_component_cost = 0.0
        for component in bom.bom_line_ids:
            line_quantity = 0.0
            if component.coefficent_parameters == 'percentage_with_co':
                line_quantity = bom.product_qty * bom.weight * (component.quantity_ratio_percent / 100)
                                                                
            elif component.coefficent_parameters == 'only_co':
                line_quantity = (bom.product_qty * component.product_qty) / (component.quantity_coefficient or 1)
            
            else : 
                line_quantity = component.product_qty
            
            if not component.is_supplementary_product:
                line_quantity = line_quantity +(line_quantity * component.loss_percent) / 100
                
            print("line qty: ",line_quantity)
            _logger.info("line qty: %s", line_quantity)
            line_quantity = self.f_convert_uom_product(line_quantity,1,bom.product_qty,bom.product_uom_id)

            line_quantity = round(line_quantity, 6)
            print("Converted Line QTY" ,line_quantity)
            print("Product Name", component.product_id.name)
            print("standard_price", component.product_id.standard_price)
            line_cost = line_quantity * component.product_id.standard_price
            line_cost = round(line_cost, 4)
            unit_total_component_cost += line_cost
        
        return unit_total_component_cost
    
    def compute_bom_operations_cost(self,bom):
        operations_cost = 0.0
        for operation_line in bom.operation_ids:
            work_center = operation_line.workcenter_id
            operation_cost = 0.0
            if work_center.default_capacity >= 1:
                duration = operation_line.time_cycle
                print("duration: ", duration)
                _logger.info("duration: %s", duration)
                hour_duration = duration / 60
                hour_cost = work_center.costs_hour
                operation_cost = hour_duration * hour_cost
                operation_cost = round(operation_cost,4)
                operations_cost += operation_cost
            elif work_center.default_capacity < 1:
                quantity = 1 / work_center.default_capacity
                duration = operation_line.time_cycle * quantity
                print("duration: ", duration)
                _logger.info("duration: %s", duration)
                hour_duration = duration / 60
                hour_cost = work_center.costs_hour
                operation_cost = hour_duration * hour_cost
                operation_cost = round(operation_cost,4)
                operations_cost += operation_cost
                
        return operations_cost
    
    def compute_bom_overhead_cost(self,bom,unit_total_cost):
        duration_cost = 0.0
        percent_cost = 0.0
        final_cost = 0.0 
        for line in bom.overhead_line_ids:
            if line.overhead_parameters == "amount_div_by_duration":
                duration = sum(bom.operation_ids.mapped('time_cycle'))

                print('5 duration ==> ',duration)
                duration_cost = duration_cost + ((duration / 60.0) * line.overhead_cost)
                duration_cost = round(duration_cost, 4)

                    
            #Calculation of 'Percent (%)'
            if line.overhead_parameters == "percent":
                percent_cost = percent_cost + (line.overhead_cost * unit_total_cost) / 100
                percent_cost = round(percent_cost, 4)
            #Calculation of 'Amount/ Final QTY'
            if line.overhead_parameters == "amount_div_by_final_qty":
                final_cost = final_cost + line.overhead_cost
        print('6 duration_cost ==> ',duration_cost)  
        print('7 percent_cost ==> ',percent_cost)  
        print('8 final_cost ==> ',final_cost)  
        
        overhead_cost = duration_cost + percent_cost + final_cost
        return overhead_cost
        
        
    f_bom_cost = fields.Float("BOM Expected Cost", digits='Product Price')
    f_bom_set = fields.Boolean("BOM is set",compute='compute_bom_set', default=False,copy=False)

    def f_action_cost_analysis(self):
        bom = self.env['mrp.bom'].sudo().search([('f_default_bom', '=', True), ('id', 'in', self.bom_ids.ids)], limit=1)
        if bom:
            self.f_default_bom = bom.id
            return self.env.ref('mrp_cost.f_action_cost_analysis_product_template').report_action(self, config=False)
        raise ValidationError(_("There is no default BOM!!"))