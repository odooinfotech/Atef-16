# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields,_
from odoo.exceptions import ValidationError


class MrpBom(models.Model):
    """MRP BOM OverHeads"""
    _inherit = 'mrp.bom'

    cost_visible = fields.Boolean('Employee Cost Visibility', default=False)
    overhead_line_ids = fields.One2many('mrp.bom.overhead', 'bom_id', 'Overhead Lines', copy=True)
    total_cost_over_head_percent = fields.Float("Over Head '%' over Total Cost",tracking=True)
    operation_workcenter_ids = fields.One2many('mrp.operation.workcenter', 'bom_id','Operation Workcenter', copy=True)
    weight = fields.Float(related='product_tmpl_id.weight', string='Weight', digits='Stock Weight')
    product_qty = fields.Float(tracking=True)

    f_default_bom = fields.Boolean(string="Default Bill Of Material",tracking=True)
    f_warning_message = fields.Text(string="Warning Message")


    def write(self,vals):
        if 'total_quantity_ratio_percent' in vals and vals['total_quantity_ratio_percent'] > 100:
            print('vals', vals['total_quantity_ratio_percent'])
            raise ValidationError(_("The total of the component quantity ratio is greater than 100. Please check it!"))

        res = super(MrpBom,self).write(vals)
        return res

    @api.onchange('bom_line_ids')
    def _f_onchange_bom_line_ids(self):
        for rec in self:
            quantity_ratio_percent = sum(rec.bom_line_ids.filtered(lambda l: l.coefficent_parameters == 'percentage_with_co').mapped('quantity_ratio_percent'))
            if quantity_ratio_percent != 100:
                rec.f_warning_message = 'The total quantity ratio percent for BOM lines must equal 100.'
            else:
                rec.f_warning_message = False



class MrpBomLine(models.Model):
    """MRP BOM OverHeads Loss Percent"""
    _inherit = 'mrp.bom.line'

    loss_percent = fields.Float('Loss %', help="BOM Componenets Loss %")
    is_supplementary_product = fields.Boolean('Is Supplementary Product?', default=False)
    quantity_ratio_percent = fields.Float("Quantity Ratio (%)")
    quantity_coefficient = fields.Integer("Quantity Coefficient")
    coefficent_parameters = fields.Selection([('percentage_with_co', '% with Co.'),('only_co', 'Only Co.')], string="Coefficent", default=False)

    # @api.onchange('coefficent_parameters', 'quantity_ratio_percent', 'quantity_coefficient')
    # def _onchange_coefficent_parameters(self):
    #     print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>cooo')
    #     if self.coefficent_parameters == 'percentage_with_co':
    #         self.product_qty = self.bom_id.weight * ((self.quantity_ratio_percent / 100) / (self.quantity_coefficient or 1))
    #     elif self.coefficent_parameters == 'only_co':
    #         self.product_qty = self.bom_id.product_qty / (self.quantity_coefficient or 1)
    #
    #

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            product = self.env['product.product'].sudo().search([('id', '=', vals['product_id'])])
            if 'quantity_ratio_percent' in vals and 'coefficent_parameters' in vals and vals['quantity_ratio_percent'] > 0.0 and vals['coefficent_parameters'] != 'percentage_with_co':
                raise ValidationError(_("%s %s has Quantity Ratio (%%) and the Coefficient is not %% with Co., please check it!") % (product.default_code, product.name))
            if 'quantity_coefficient' in vals and 'coefficent_parameters' in vals and vals['quantity_coefficient'] > 0.0 and vals['coefficent_parameters'] != 'only_co':
                raise ValidationError(_("%s %s has Quantity Coefficient and the Coefficient is not Only Co., please check it!") % (product.default_code, product.name))
            if 'product_qty' in vals and 'coefficent_parameters' in vals and vals['product_qty'] > 0.0 and vals['coefficent_parameters'] != False and vals['quantity_coefficient'] == 0.0 and vals['quantity_ratio_percent'] == 0.0:
                raise ValidationError(_("%s %s has not Quantity Coefficient or Quantity Ratio (%%) and the Coefficient is not False, please check it!") % (product.default_code, product.name))


            bom = self.env['mrp.bom'].sudo().search([('id','=',vals['bom_id'])])
            product = self.env['product.product'].sudo().search([('id','=',vals['product_id'])])
            bom.message_post(
                body=_("""<span style='font-weight: bold; font-size: 16px;'>&#8226;</span>
                                    A new component (%s) has been added """) % (product.name),
                message_type="notification"

            )
        res = super(MrpBomLine, self).create(vals_list)
        return res

    def unlink(self):
        self.bom_id.message_post(
            body=_("""<span style='font-weight: bold; font-size: 16px;'>&#8226;</span>
                                            Component (%s) deleted """) % (self.product_id.name),
            message_type="notification"

        )
        res = super(MrpBomLine, self).unlink()
        return res


    def write(self, vals):
        product = self.product_id
        if 'product_id' in vals:
            product = self.env['product.product'].sudo().search([('id', '=', vals['product_id'])])

        if any(field_name in vals for field_name in ['coefficent_parameters', 'product_qty', 'quantity_ratio_percent', 'quantity_coefficient']):

            new_values = {field: vals.get(field, self[field]) for field in ['coefficent_parameters', 'product_qty', 'quantity_ratio_percent', 'quantity_coefficient']}

            if new_values['quantity_ratio_percent'] > 0.0 and new_values['coefficent_parameters'] != 'percentage_with_co':
                raise ValidationError(_("%s %s has Quantity Ratio (%%) and the Coefficient is not %% with Co., please check it!") % (product.default_code,product.name))
            if new_values['quantity_coefficient'] > 0.0 and new_values['coefficent_parameters'] != 'only_co':
                raise ValidationError(_("%s %s has Quantity Coefficient and the Coefficient is not Only Co., please check it!") % (product.default_code, product.name))
            if new_values['product_qty'] > 0.0 and new_values['quantity_ratio_percent'] == 0.0 and new_values['quantity_coefficient'] == 0.0 and new_values['coefficent_parameters'] != False:
                raise ValidationError(_("%s %s has not Quantity Coefficient or Quantity Ratio (%%) and the Coefficient is not False, please check it!") % (product.default_code, product.name))


        if 'product_id' in vals:
            product = self.env['product.product'].sudo().search([('id', '=', vals['product_id'])])
        else:
            product = self.product_id
        if 'product_qty' in vals and vals['product_qty'] != self.product_qty:
            self.bom_id.message_post(
                body=_("""<span style='font-weight: bold; font-size: 16px;'>&#8226;</span>
                        The %s product quantity has been changed from
                        <span style='color: blue;'>%s</span>
                        to 
                        <span style='color: blue;'>%s</span>
                        """) % (product.name,self.product_qty,vals['product_qty']),
                message_type="notification"

            )

        if 'loss_percent' in vals and vals['loss_percent'] != self.loss_percent:
            self.bom_id.message_post(
                body=_("""<span style='font-weight: bold; font-size: 16px;'>&#8226;</span>
                        The %s product loss has been changed from
                        <span style='color: blue;'>%s</span>
                        to 
                        <span style='color: blue;'>%s</span>
                        """) % (product.name,self.loss_percent,vals['loss_percent']),
                message_type="notification"

            )

        if 'quantity_ratio_percent' in vals and vals['quantity_ratio_percent'] != self.quantity_ratio_percent:
            self.bom_id.message_post(
                body=_("""<span style='font-weight: bold; font-size: 16px;'>&#8226;</span>
                        The %s product quantity ratio has been changed from
                        <span style='color: blue;'>%s</span>
                        to 
                        <span style='color: blue;'>%s</span>
                        """) % (product.name,self.quantity_ratio_percent,vals['quantity_ratio_percent']),
                message_type="notification"

            )

        if 'quantity_coefficient' in vals and vals['quantity_coefficient'] != self.quantity_coefficient:
            self.bom_id.message_post(
                body=_("""<span style='font-weight: bold; font-size: 16px;'>&#8226;</span>
                        The %s product quantity coefficient has been changed from
                        <span style='color: blue;'>%s</span>
                        to 
                        <span style='color: blue;'>%s</span>
                        """) % (product.name,self.quantity_coefficient,vals['quantity_coefficient']),
                message_type="notification"

            )

        if 'coefficent_parameters' in vals and vals['coefficent_parameters'] != self.coefficent_parameters:
            self.bom_id.message_post(
                body=_("""<span style='font-weight: bold; font-size: 16px;'>&#8226;</span>
                        The %s product coefficient parameters has been changed from
                        <span style='color: blue;'>%s</span>
                        to 
                        <span style='color: blue;'>%s</span>
                        """) % (product.name,self.coefficent_parameters,vals['coefficent_parameters']),
                message_type="notification"

            )



        res = super(MrpBomLine, self).write(vals)
        return res

class MrpRoutingWorkCenter(models.Model):
    _inherit = 'mrp.routing.workcenter'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            bom = self.env['mrp.bom'].sudo().search([('id', '=', vals['bom_id'])])
            bom.message_post(
                body=_("""<span style='font-weight: bold; font-size: 16px;'>&#8226;</span>
                                                A new operation (%s) has been added """) % (vals['name']),
                message_type="notification"

            )

        res = super(MrpRoutingWorkCenter, self).create(vals_list)
        return res

    def unlink(self):
        self.bom_id.message_post(
            body=_("""<span style='font-weight: bold; font-size: 16px;'>&#8226;</span>
                                            Operation (%s) deleted """) % (self.name),
            message_type="notification"

        )
        res = super(MrpRoutingWorkCenter, self).unlink()
        return res

    def write(self, vals):
        if 'name' in vals:
            name = vals['name']
        else:
            for rec in self:
                name = rec.name
        if 'time_cycle_manual' in vals and vals['time_cycle_manual'] != self.time_cycle_manual:
            self.bom_id.message_post(
                body=_("""<span style='font-weight: bold; font-size: 16px;'>&#8226;</span>
                        The %s operation default duration has been changed from
                        <span style='color: blue;'>%s</span>
                        to 
                        <span style='color: blue;'>%s</span>
                        """) % (name,self.time_cycle_manual,vals['time_cycle_manual']),
                message_type="notification"

            )

        if 'employee_ratio' in vals and vals['employee_ratio'] != self.employee_ratio:
            self.bom_id.message_post(
                body=_("""<span style='font-weight: bold; font-size: 16px;'>&#8226;</span>
                        The %s operation Employee Capacity has been changed from
                        <span style='color: blue;'>%s</span>
                        to 
                        <span style='color: blue;'>%s</span>
                        """) % (name,self.employee_ratio,vals['employee_ratio']),
                message_type="notification"

            )

        res = super(MrpRoutingWorkCenter, self).write(vals)
        return res



    def action_archive(self):
        self.bom_id.message_post(
            body=_("""<span style='font-weight: bold; font-size: 16px;'>&#8226;</span>
                                                    Operation (%s) archived """) % (self.name),
            message_type="notification"

        )
        res = super(MrpRoutingWorkCenter, self).action_archive()
        return res

    def action_unarchive(self):
        self.bom_id.message_post(
            body=_("""<span style='font-weight: bold; font-size: 16px;'>&#8226;</span>
                                                            Operation (%s) unarchived """) % (self.name),
            message_type="notification"

        )
        res = super(MrpRoutingWorkCenter, self).action_unarchive()
        return res