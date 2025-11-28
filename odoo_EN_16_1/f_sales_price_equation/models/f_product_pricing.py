# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from pygments.lexer import default


class FProductPricing(models.Model):
    _name = 'f.product.pricing'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Product Pricing Model'
    _rec_name = 'f_name'

    f_name = fields.Char(string='Name', required=True, index=True, copy=False, default='New')
    active = fields.Boolean(string='Active', default=True)
    f_pricing_type = fields.Many2many('f.pricing.type', string='Purchase Type')
    f_internal_po = fields.Boolean(string='Is internal PO?', compute='_f_compute_purchase_type', store=True)
    f_external_po = fields.Boolean(string='Is external PO?', compute='_f_compute_purchase_type', store=True)
    f_purchase_ids = fields.Many2many('purchase.order', string='Purchase Orders')
    f_landed_ids = fields.Many2many('stock.landed.cost', string='Landed Cost', domain="[('state', '=', 'done')]")
    f_pricing_equation_int = fields.Many2one('f.pricing.equation', string='Pricing Equation Int.')
    f_pricing_equation_ext = fields.Many2one('f.pricing.equation', string='Pricing Equation Ext.')
    f_status = fields.Selection([('draft', 'Draft'),('ready', 'Ready'),('done', 'Done')], string='Status', default='draft')
    f_purchase_pricing_lines = fields.One2many('f.purchase.pricing.line', 'f_pricing_id', string='Purchase Pricing Lines')
    f_landed_pricing_lines = fields.One2many('f.landed.pricing.line', 'f_pricing_id', string='Landed Pricing Lines')
    f_last_landed_before = fields.Date(string='Last Landed Before', default=fields.Date.today())
    f_last_purchase_before = fields.Datetime(string='Last Purchase Before', default=fields.Datetime.now())

    def _f_get_shortcut(self):
        return _("N/C: New Cost\nU/N/C: Unit New Cost\nU/L/C: Unit Latest Cost\nDef.: Deference\nDef. X P.E: Deference X Price Equation\nC/P: Current Price\nN/P: New Price\nPO/P: Purchase Price\nU/PO/P: Unit Purchase Price\nU/L/P: Unit Latest Price")

    f_shortcut = fields.Text(string='Shortcuts', default=lambda self: self._f_get_shortcut())
    f_warning_message_ext = fields.Text(string="Waring Message", compute='_compute_warning_message_ext', store=True)
    f_warning_message_int = fields.Text(string="Waring Message", compute='_compute_warning_message_int', store=True)

    @api.depends('f_purchase_pricing_lines')
    def _compute_warning_message_int(self):
        for rec in self:
            rec.f_warning_message_int = False
            for line in rec.f_purchase_pricing_lines:
                if not line.f_last_po:
                    rec.f_warning_message_int = "Some lines don't have Latest Purchase!"

    @api.depends('f_landed_pricing_lines')
    def _compute_warning_message_ext(self):
        for rec in self:
            rec.f_warning_message_ext = False
            for line in rec.f_landed_pricing_lines:
                if not line.f_last_landed:
                    rec.f_warning_message_ext = "Some lines don't have Latest Landed!"

    @api.depends('f_pricing_type')
    def _f_compute_purchase_type(self):
        for rec in self:
            rec.f_external_po = False
            rec.f_internal_po = False
            for type in rec.f_pricing_type:
                if type.f_name == 'Internal Purchase':
                    rec.f_internal_po = True
                if type.f_name == 'External Purchase':
                    rec.f_external_po = True


    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('f_name', 'New') == 'New':
                seq_date = None
                vals['f_name'] = self.env['ir.sequence'].next_by_code('f.product.pricing',
                                                                      sequence_date=seq_date) or '/'
        return super(FProductPricing, self).create(vals_list)

    @api.model
    def archive(self):
        self.ensure_one()
        self.active = False

    def f_confirm_pricing(self):
        self.ensure_one()
        for line in self.f_landed_pricing_lines:
            line.f_product_id.list_price = line.f_new_price
        for line in self.f_purchase_pricing_lines:
            line.f_product_id.list_price = line.f_new_price
        self.f_status = 'done'

    def f_compute_landed_prices(self):
        self.ensure_one()
        for line in self.f_landed_pricing_lines:
            line.f_unit_new_cost = line.f_new_cost / line.f_quantity
            line.f_deference = line.f_unit_new_cost - line.f_unit_old_cost
            line.f_def_with_vat = line.f_deference * self.f_pricing_equation_ext.f_factor
            line.f_new_price = line.f_current_price + line.f_def_with_vat

    def f_compute_po_prices(self):
        self.ensure_one()
        for line in self.f_purchase_pricing_lines:
            line.f_unit_po_price = line.f_po_price / line.f_quantity
            line.f_deference = line.f_unit_po_price - line.f_unit_latest_price
            line.f_def_with_vat = line.f_deference * self.f_pricing_equation_int.f_factor
            line.f_new_price = line.f_current_price + line.f_def_with_vat

    def f_compute_prices(self):
        self.ensure_one()
        if self.f_external_po:
            self.f_compute_landed_prices()
        if self.f_internal_po:
            self.f_compute_po_prices()

    def f_get_landed_product(self):
        self.ensure_one()
        self.write({
            'f_landed_pricing_lines': [(6, 0, [])]
        })
        for landed in self.f_landed_ids:
            landed_lines = self.env['stock.valuation.adjustment.lines'].read_group(
                domain=[('cost_id', '=', landed.id)],
                fields=['product_id', 'quantity', 'final_cost'], groupby=['product_id'])
            for line in landed_lines:
                new_cost = line['final_cost'] / line['quantity']
                product = self.env['product.product'].search([('id', '=', line['product_id'][0])])
                vals = {
                    'f_product_id': product.product_tmpl_id.id,
                    'f_pricing_id': self.id,
                    'f_quantity': line['quantity'],
                    'f_new_cost': line['final_cost'],
                    'f_unit_new_cost': new_cost,
                    'f_current_price': product.list_price
                }
                last_line = self.env['stock.valuation.adjustment.lines'].search([('product_id', '=', product.id),
                                                                                 ('cost_id.date', '<', self.f_last_landed_before),
                                                                                 ('cost_id', '!=', landed.id),
                                                                                 ('cost_id.state', '=', 'done')],
                                                                                order='f_landed_date desc', limit=1)
                if last_line:
                    last_landed = last_line.cost_id
                    vals['f_last_landed'] = last_landed.id
                    vals['f_source'] = last_landed.name
                    last_landed_lines = self.env['stock.valuation.adjustment.lines'].read_group(
                        domain=[('cost_id', '=', last_landed.id), ('product_id', '=', product.id)],
                        fields=['product_id', 'quantity', 'final_cost'], groupby=['product_id'])
                    if last_landed_lines:
                        last_cost = last_landed_lines[0]['final_cost'] / last_landed_lines[0]['quantity']
                        deference = new_cost - last_cost
                        f_def_with_vat = deference * self.f_pricing_equation_ext.f_factor
                        vals['f_unit_old_cost'] = last_cost
                        vals['f_deference'] = deference
                        vals['f_def_with_vat'] = f_def_with_vat
                        vals['f_new_price'] = product.list_price + f_def_with_vat
                else:
                    last_line = self.env['purchase.order.line'].search([('product_id', '=', product.id),
                                                                        ('order_id.date_approve', '<',
                                                                         self.f_last_purchase_before),
                                                                        ('order_id.state', 'in', ('done', 'purchase'))],
                                                                       order='f_confirm_date desc', limit=1)
                    if last_line:
                        last_po = last_line.order_id
                        vals['f_source'] = last_po.name
                        last_po_lines = self.env['purchase.order.line'].read_group(
                            domain=[('order_id', '=', last_po.id), ('product_id', '=', product.id)],
                            fields=['product_id', 'product_qty', 'price_subtotal'], groupby=['product_id'])
                        if last_po_lines:
                            last_price = last_po_lines[0]['price_subtotal'] / last_po_lines[0]['product_qty']
                            deference = new_cost - last_price
                            f_def_with_vat = deference * self.f_pricing_equation_ext.f_factor
                            vals['f_unit_old_cost'] = last_price
                            vals['f_deference'] = deference
                            vals['f_def_with_vat'] = f_def_with_vat
                            vals['f_new_price'] = product.list_price + f_def_with_vat

                self.env['f.landed.pricing.line'].create(vals)

    def f_get_po_product(self):
        self.ensure_one()
        self.write({
            'f_purchase_pricing_lines': [(6, 0, [])]
        })
        for purchase in self.f_purchase_ids:
            po_lines = self.env['purchase.order.line'].read_group(
                domain=[('order_id', '=', purchase.id)],
                fields=['product_id', 'product_qty', 'price_subtotal'], groupby=['product_id'])
            for line in po_lines:
                new_price = line['price_subtotal'] / line['product_qty']
                product = self.env['product.product'].search([('id', '=', line['product_id'][0])])
                vals = {
                    'f_product_id': product.product_tmpl_id.id,
                    'f_po_order_id': purchase.id,
                    'f_partner_id': purchase.partner_id.id,
                    'f_pricing_id': self.id,
                    'f_quantity': line['product_qty'],
                    'f_po_price': line['price_subtotal'],
                    'f_unit_po_price': new_price,
                    'f_current_price': product.list_price
                }
                last_line = self.env['purchase.order.line'].search([('product_id', '=', product.id),
                                                                    ('order_id.date_approve', '<', self.f_last_purchase_before),
                                                                    ('order_id', '!=', purchase.id),
                                                                    ('order_id.state', 'in', ('done','purchase'))],
                                                                   order='f_confirm_date desc', limit=1)
                if last_line:
                    last_po = last_line.order_id
                    vals['f_last_po'] = last_po.id
                    last_po_lines = self.env['purchase.order.line'].read_group(
                        domain=[('order_id', '=', last_po.id), ('product_id', '=', product.id)],
                        fields=['product_id', 'product_qty', 'price_subtotal'], groupby=['product_id'])
                    if last_po_lines:
                        last_price = last_po_lines[0]['price_subtotal'] / last_po_lines[0]['product_qty']
                        deference = new_price - last_price
                        f_def_with_vat = deference * self.f_pricing_equation_int.f_factor
                        vals['f_unit_latest_price'] = last_price
                        vals['f_deference'] = deference
                        vals['f_def_with_vat'] = f_def_with_vat
                        vals['f_new_price'] = product.list_price + f_def_with_vat

                self.env['f.purchase.pricing.line'].create(vals)

    def f_get_products(self):
        self.ensure_one()
        if self.f_external_po:
            self.f_get_landed_product()
        if self.f_internal_po:
            self.f_get_po_product()
        if self.f_external_po and self.f_landed_pricing_lines and self.f_internal_po and self.f_purchase_pricing_lines:
            self.f_status = 'ready'
        elif self.f_external_po and self.f_landed_pricing_lines:
            self.f_status = 'ready'
        elif self.f_internal_po and self.f_purchase_pricing_lines:
            self.f_status = 'ready'
