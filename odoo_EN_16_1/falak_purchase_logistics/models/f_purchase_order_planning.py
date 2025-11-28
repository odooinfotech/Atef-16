# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from datetime import timedelta, date
import logging

_logger = logging.getLogger('F_Purchase_Order_Planning')


class F_Purchase_Order_Planning(models.Model):
    _name = 'f.purchase.order.planning'
    _description = 'Purchase Order Planning'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    f_po_id = fields.Many2one('purchase.order', string="Purchase Order", domain="[('f_show_planning','=',True)]",
                              required=True)
    f_po_line_id = fields.Many2one('purchase.order.line', string="PO Line / Description", required=True)

    f_product_description = fields.Text(related="f_po_line_id.name")

    f_internal_ref = fields.Char(related="f_product_name.default_code")

    f_po_receipt_domain = fields.Many2many('stock.picking', compute='_compute_po_receipt_domain')

    f_po_receipt = fields.Many2one('stock.picking', string="PO Receipt")

    @api.depends('f_po_id')
    def _compute_po_receipt_domain(self):
        for record in self:
            if record.f_po_id:
                record.f_po_receipt_domain = [(6, 0, record.f_po_id.picking_ids.ids)]
            else:
                record.f_po_receipt_domain = [(6, 0, [])]

    def name_get(self):
        result = []
        for rec in self:
            po_id = str(rec.f_po_id.name)
            prod = str(rec.f_product_name.name)
            qty = str(rec.f_planned_amount)

            name = po_id + '/' + prod + '/' + qty

            print('name', name)

            result.append((rec.id, name))

        return result

    # filter purchase order line that related to purchase order
    @api.onchange('f_po_id')
    def _onchange_f_po_id(self):

        for cont in self.f_po_id.partner_id.f_one_contact_person:
            if cont.f_primary:
                self.f_vendor_contact_person = cont.f_vendor_name
                self.f_vendor_num = cont.f_vendor_no

        return {'domain': {'f_po_line_id': [('order_id', '=', self.f_po_id.id)]}}

    # filter purchase order that related to purchase order Line
    @api.onchange('f_po_line_id')
    def _onchange_f_po_line_id(self):
        self.f_po_id = self.f_po_line_id.order_id.id
        self.f_planned_amount = self.f_po_line_id.product_qty

    # Related Fields to PO id
    f_vendor_name = fields.Many2one(related='f_po_id.partner_id', string="Vendor Name", store=True)
    f_vendor_num = fields.Char(string="Contact Person Phone")
    f_vendor_contact_person = fields.Char(string="Contact Person Name")
    f_vendor_country = fields.Many2one(related='f_po_id.partner_id.country_id', string="Vendor Country", store=True)

    f_clearance_agent = fields.Many2one(related='f_shipping.f_clearance_representative',
                                        string="Clearance Representative", store=True)
    f_import_agent = fields.Many2one(related='f_shipping.f_import_agent', string="Import Representative", store=True)

    # Related Fields to PO line Id
    f_product_name = fields.Many2one(related='f_po_line_id.product_id', string="Product Name", store=True)
    f_product_price = fields.Float(related='f_po_line_id.price_unit', string="Product Price", store=True)
    f_notes = fields.Char(string="Notes")

    f_state = fields.Selection(
        [('production', 'Production'), ('ready to be shipped', ' Ready To Be Shipped'), ('shipped', 'Shipped'),
         ('on port', 'On Port'), ('arrived at company', 'Arrived At Company'),
         ('balance/documents', ' Balance/ Documents'), ('arrived', 'Arrived'), ('custom clearance', 'Custom Clearance'),
         ('deposit/lc', 'Deposit/ LC')], string="Status_old")
    f_ship_stage = fields.Char(related="f_shipping.f_ship_stage", string="Stage_ld")

    f_shipp_stage = fields.Many2one(related="f_shipping.f_shipp_stage", string="Stage", store=True)

    f_stat = fields.Many2one('f.shipping.stage', string="Status", domain="[('f_owner','=','planning')]", tracking=True)

    # f_package_volume =fields.Float(string="Package Volume",related='f_po_line_id.f_package_volume')
    # f_package_qty = fields.Float(string="Contained QTY",related='f_po_line_id.f_package_qty')
    #
    #
    # f_number_of_packages = fields.Float(string="Number of Packages")
    # f_number_of_packages_calc = fields.Float(string="Number of Packages Computed")
    #
    # f_total_volume =fields.Float(string="Total Volume")
    # f_total_volume_calc = fields.Float(string="Total Volume Computed")
    #
    # f_prod_weight = fields.Float(string="Product Weight",related='f_po_line_id.f_prod_weight')
    #
    # f_total_weight =fields.Float(string="Total Weight")
    # f_total_weight_calc = fields.Float(string="Total Weight Computed")

    f_teken = fields.Boolean(string="Teken")
    f_taken_type = fields.Selection([('talach', 'Talach'),
                                     ('sample_test', 'Sample Test')], string="Taken Type")
    f_bakacha_number = fields.Char(string="Bakacha #")

    f_product_code = fields.Char(compute='f_compute_product_vendor_code', store=True, string="Product Vendor No.")

    @api.depends('f_po_line_id')
    def f_compute_product_vendor_code(self):
        for rec in self:
            for prod in self.f_po_line_id.product_id.seller_ids:
                if prod.partner_id == rec.f_vendor_name:
                    rec.f_product_code = prod.product_code

    def unlink(self):
        for record in self:
            record.f_stat = False
        return super(F_Purchase_Order_Planning, self).unlink()

    # @api.depends('f_planned_amount','f_package_qty')
    # def f_compute_number_of_packages_total_volume(self):
    #     if self.f_package_qty > 0:
    #         self.f_number_of_packages_calc = self.f_planned_amount / self.f_package_qty
    #         self.f_number_of_packages = self.f_planned_amount / self.f_package_qty
    #         self.f_total_volume_calc = self.f_number_of_packages * self.f_package_volume
    #         self.f_total_volume = self.f_number_of_packages * self.f_package_volume
    #         self.f_total_weight_calc = self.f_prod_weight * self.f_planned_amount
    #         self.f_total_weight = self.f_prod_weight * self.f_planned_amount

    # @api.onchange('f_planned_amount','f_package_qty')
    # def f_onchange_f_package_qty(self):
    #     for rec in self:
    #         if rec.f_package_qty > 0:
    #             rec.f_number_of_packages = rec.f_planned_amount / rec.f_package_qty
    #             rec.f_total_volume = rec.f_number_of_packages * rec.f_package_volume
    #         if rec.f_package_qty == 0:
    #             rec.f_number_of_packages = 0
    #             rec.f_total_volume = 0

    # @api.onchange('f_package_qty','f_planned_amount')
    # def f_onchange_f_prod_weight(self):
    #     for rec in self:
    #         if rec.f_package_qty > 0:
    #             rec.f_total_weight_calc = rec.f_prod_weight * rec.f_planned_amount
    #             rec.f_total_weight = rec.f_prod_weight * rec.f_planned_amount

    def f_open_form_view(self):
        # self.f_compute_number_of_packages_total_volume()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Form',
            'res_model': 'f.purchase.order.planning',
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'current',
            'res_id': self.id,
            'context': {'force_detailed_view': True}
        }

    def _get_state(self):
        print('def _get_state(self):')
        for rec in self.filtered(lambda self: self.f_plan_state != 'done'):
            if rec.f_shipp_stage:
                rec.f_plan_state = rec.f_shipp_stage.id
            elif rec.f_stat:
                rec.f_plan_state = rec.f_stat.id
            else:
                rec.f_plan_state = False

    f_shipping = fields.Many2one('f.shipping.details', string="Shipping", tracking=True)
    f_po_line_qty = fields.Float(related="f_po_line_id.product_qty", string="Ordered Qty", store=True)
    f_po_line_rec_qty = fields.Float(related="f_po_line_id.qty_received", string="Received Qty", store=True)
    f_planned_amount = fields.Float(string="Planned  Qty", tracking=True)
    f_shipped_amount = fields.Float(string="Shipped Qty", store=True, tracking=True)

    f_cancelled_qty = fields.Float(string="Cancelled Qty", store=True, tracking=True)

    f_remaining_qty = fields.Float(related='f_po_line_id.f_total_remaining_qty', string="Remaining Qty", store=True, tracking=True)

    f_shipped_amount_price = fields.Float(string="Shipped Qty Price", compute='compute_shipped_amount_price')
    f_planned_amount_price = fields.Float(string="Planned Qty Price", compute='compute_planned_amount_price')

    # Shipping Details Related Fields
    f_shipping_term = fields.Many2one(related='f_po_id.f_payment_terms', string="Payment Terms", store=True)
    f_shipping_time = fields.Char(related="f_shipping.f_shipping_time", string="Shipping Period", store=True)

    f_estimated_shipping_date = fields.Date(string="ETD", store=True, tracking=True)
    f_ready_to_shipping_date = fields.Date(string="RTS", store=True, tracking=True)
    f_delta_shipping_date = fields.Integer(string="Diff", store=True)

    f_real_shipping_date = fields.Date(related="f_shipping.f_real_shipping_date", string="ATD ", store=True)
    f_estimated_port_arrival_date = fields.Date(related="f_shipping.f_estimated_port_arrival_date", string="ETA",
                                                store=True)
    f_real_port_arrival_date = fields.Date(related="f_shipping.f_real_port_arrival_date", string="ATA", store=True)
    f_delta_port_arrival_date = fields.Integer(related="f_shipping.f_delta_port_arrival_date", string="Diff",
                                               store=True)
    f_estimated_company_arrival_date = fields.Date(string="ETAF", store=True, tracking=True)
    f_real_company_arrival_date = fields.Date(related="f_shipping.f_real_company_arrival_date", string="ATAF",
                                              store=True)
    f_delta_company_arrival_date = fields.Integer(related="f_shipping.f_delta_company_arrival_date", string="Diff",
                                                  store=True)
    f_shipping_company = fields.Many2one(related='f_shipping.f_shipping_company', string='Shipping Company', store=True)
    f_shipping_line = fields.Many2one(related="f_shipping.f_shipping_line", string='Shipping Line', store=True)
    f_shipping_company_agent = fields.Many2one(related="f_shipping.f_shipping_company_agent",
                                               string="Shipping Company Agent", store=True)
    f_booking_no = fields.Char(related="f_shipping.f_booking_no", string="Booking Job #", store=True)
    f_freight_cost = fields.Float(related="f_shipping.f_freight_cost", string="Freight Cost", store=True)
    f_free_days_of_demurrage = fields.Char(related="f_shipping.f_free_days_of_demurrage",
                                           string="Free Days of Demurrage", store=True)

    f_bill_of_lading_type = fields.Selection(related="f_shipping.f_bill_of_lading_type", string="B/L Type", store=True)
    f_bill_of_lad_status = fields.Selection(related="f_shipping.f_bill_of_lad_status", string="B/L Status", store=True)
    f_supplier_name = fields.Many2one(related="f_shipping.f_supplier_name", string="Supplier Name", store=True)

    f_port_of_discharge = fields.Many2one(related="f_shipping.f_port_of_discharge", string="Port Of Discharge",
                                          store=True)
    f_port_of_loading = fields.Many2one(related="f_shipping.f_port_of_loading", string="Port Of Loading", store=True)
    f_consignee = fields.Char(related="f_shipping.f_consignee", string="Consignee", store=True)
    f_internal_agent = fields.Many2one(related="f_po_id.f_internal_agent", string="Internal Agent", store=True)
    f_po_date_order = fields.Datetime(related='f_po_id.date_order', string="PO Order Date", store=True)

    f_po_pi_date = fields.Date(related='f_po_id.f_pi_date', string="PI Date", store=True)
    f_po_pi_approval_date = fields.Date(related='f_po_id.f_pi_approval_date', string="PI Approval Date", store=True)

    f_purchase_representative = fields.Many2one(related='f_po_id.user_id', string="Purchase Representative", store=True)

    f_euro1 = fields.Boolean(related='f_po_id.f_euro1', string="Euro1", store=True)

    f_balance_document = fields.Boolean(string="Balance/Document", store=True)
    f_deposit_lc = fields.Boolean(string="Deposit /LC", store=True)
    f_commercial_inv_num = fields.Char(string="Commercial Invoice Number", tracking=True)
    f_commercial_inv_amount = fields.Float(string="Commercial Invoice Amount")

    f_po_classification = fields.Many2one('f.po.classification', string="Classifications",
                                          related='f_po_id.f_po_classification', store=True)

    # @api.depends("f_po_line_qty", "f_po_line_rec_qty", "f_shipped_amount", "f_cancelled_qty")
    # def _compute_remaining_qty(self):
    #     for plan in self:
    #         plan.f_remaining_qty = (plan.f_po_line_qty - plan.f_po_line_rec_qty) - plan.f_shipped_amount - plan.f_cancelled_qty

    def _f_default_classification_access(self):
        f_classification_access = (self.env["ir.config_parameter"].sudo().
                                   get_param('falak_purchase_logistics.f_po_access_based_class'))
        return f_classification_access

    f_classification_access = fields.Boolean(string='Classification Access', default=_f_default_classification_access,
                                             compute='_f_compute_classification_access')

    def _f_compute_classification_access(self):
        self.f_classification_access = (self.env["ir.config_parameter"].sudo().
                                        get_param('falak_purchase_logistics.f_po_access_based_class'))

    @api.onchange('f_estimated_shipping_date', 'f_estimated_port_arrival_date')
    def _check_estimated_dates(self):
        if self.f_estimated_shipping_date and self.f_estimated_port_arrival_date:
            if self.f_estimated_shipping_date > self.f_estimated_port_arrival_date:
                raise UserError("ETD (Estimated time of departure) cannot be after ETA (Estimated time of arrival).")

    # @api.onchange('f_real_shipping_date', 'f_real_port_arrival_date')
    # def _check_real_dates(self):
    # if self.f_real_shipping_date and self.f_real_port_arrival_date:
    # if self.f_real_shipping_date > self.f_real_port_arrival_date:
    # raise UserError("ATD (Actual time of departure) cannot be after ATA (Actual time of arrival).")

    def f_update_plans_shipping(self):
        for plan in self:
            plan.f_stat = plan.f_shipping.f_shipp_stage
            plan.f_estimated_company_arrival_date = plan.f_shipping.f_estimated_company_arrival_date

    @api.onchange('f_estimated_shipping_date', 'f_ready_to_shipping_date')
    def _onchange_dates(self):
        if self.f_estimated_shipping_date and self.f_ready_to_shipping_date:
            delta_days = (self.f_ready_to_shipping_date - self.f_estimated_shipping_date).days
            self.f_delta_shipping_date = delta_days
        else:
            self.f_delta_shipping_date = 0

    @api.onchange('f_estimated_shipping_date')
    def onchange_estimated_shipping_date(self):
        shipping_period = int(self.f_po_id.f_port_of_loading.f_shipping_period or 0)
        clearance_period = 10

        if not isinstance(self.f_estimated_shipping_date, date):
            return

        etaf = self.f_estimated_shipping_date + timedelta(days=shipping_period + clearance_period - 1)

        self.f_estimated_company_arrival_date = etaf

    @api.onchange('f_estimated_port_arrival_date')
    def onchange_estimated_port_arrival_date(self):
        clearance_period = int(self.f_shipping.f_clearance_period or 0)

        if not isinstance(self.f_estimated_port_arrival_date, date):
            return

        etaf = self.f_estimated_port_arrival_date + timedelta(days=clearance_period)

        self.f_estimated_company_arrival_date = etaf

    def f_update_plan_quantities(self):
        for rec in self:
            if not rec.f_po_id or not rec.f_po_line_id:
                continue

            related_plans = self.env['f.purchase.order.planning'].search([
                ('f_po_id', '=', rec.f_po_id.id),
                ('f_po_line_id', '=', rec.f_po_line_id.id),
            ])
            # _logger.info("related_plans: %s", related_plans)

            valid_shipped_plans = related_plans.filtered(
                lambda p: p.f_stat and p.f_stat.f_stage_code not in ['done', 'canceled']
            )
            total_shipped = sum(valid_shipped_plans.mapped('f_shipped_amount'))
            # _logger.info("valid_shipped_plans: %s", valid_shipped_plans)
            # _logger.info("total_shipped: %s", total_shipped)

            total_canceled = sum(related_plans.mapped('f_cancelled_qty'))
            # _logger.info("total_canceled: %s", total_canceled)

            po_line = rec.f_po_line_id
            # _logger.info("po_line: %s", po_line.order_id)

            po_line.write({
                'f_total_shipped_qty': total_shipped,
                'f_total_canceled_qty': total_canceled,
                'f_total_remaining_qty': round(po_line.product_qty - po_line.qty_received - total_shipped - total_canceled, 2),
            })

    @api.onchange('f_shipping')
    def f_onchange_shipping(self):
        for rec in self:
            rec.write({'f_stat': rec.f_shipping.f_shipp_stage,
                       'f_estimated_company_arrival_date': rec.f_shipping.f_estimated_company_arrival_date,
                       'f_real_shipping_date': rec.f_shipping.f_real_shipping_date,
                       'f_real_port_arrival_date': rec.f_shipping.f_real_port_arrival_date,
                       'f_estimated_port_arrival_date': rec.f_shipping.f_estimated_port_arrival_date,
                       'f_real_company_arrival_date': rec.f_shipping.f_real_company_arrival_date,
                       })

    def f_set_quantities(self):
        for plan in self:
            if plan.f_shipped_amount == 0.0:
                plan.write({'f_shipped_amount': plan.f_planned_amount})

    def f_add_plan(self):
        vals = []
        for rec in self:
            vals.append((0, 0, {
                'f_po_id': rec.f_po_id.id,
                'f_po_plan_id': rec.id,
                'f_product_name': rec.f_product_name.id,
                'qty': 0,
                'f_container_details': self.env.context.get('container_id')
            }))
        container = self.env['f.container.details'].sudo().search([('id', '=', self.env.context.get('container_id'))])
        container.update({'f_container_plans': vals})

    @api.onchange('f_shipped_amount')
    def change_shipping_amount(self):
        if self.f_shipped_amount > self.f_po_line_id.product_qty:
            raise ValidationError("Shipped  quantity should not exceed the quantity in the purchase order line!  ")

    @api.onchange('f_planned_amount')
    def _onchange_planned_amount(self):
        for rec in self:
            if not rec.f_po_id or not rec.f_po_line_id:
                continue

            related_plans = self.env['f.purchase.order.planning'].search([
                ('f_po_id', '=', rec.f_po_id.id),
                ('f_po_line_id', '=', rec.f_po_line_id.id),
            ])

            total_planned = sum(related_plans.mapped('f_planned_amount'))

            product_qty = rec.f_po_line_id.product_qty

            if total_planned > product_qty:
                raise ValidationError(
                    f"Total planned quantity ({total_planned}) exceeds ordered quantity ({product_qty}) for this PO line."
                )

    def compute_shipped_amount_price(self):
        for rec in self:
            amount_price = rec.f_product_price * rec.f_shipped_amount
            rec.f_shipped_amount_price = amount_price

    def compute_planned_amount_price(self):
        for rec in self:
            amount_price = rec.f_product_price * rec.f_planned_amount
            rec.f_planned_amount_price = amount_price
