from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError


class fCustomerTarget(models.Model):
    _name = "f.cust.target"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "f_name"
    _description = 'Customer Target'

    active = fields.Boolean(string='Active', default=True, copy=True)
    f_name = fields.Char(string="Name", required=True, copy=False)
    f_customer = fields.Many2one("res.partner", string="Customer Name", required=True, tracking=True, copy=False)
    f_from_date = fields.Date(string="From Date", required=True, tracking=True, copy=True)
    f_to_date = fields.Date(string="To Date", required=True, tracking=True, copy=True)
    f_target_type = fields.Selection([('rental', 'Rental'), ('sales', 'Sales')], default='sales', string="Target Type",
                                     required=True, tracking=True, copy=True)
    f_target_amount = fields.Monetary(string="Target Amount", required=True, tracking=True,
                                   currency_field='company_currency', copy=True)
    f_commision_value_type = fields.Selection([('percent', '%'), ('fixed', 'Fixed')], default='fixed',
                                              string="Commission Type", tracking=True, copy=True)
    f_commision_value = fields.Monetary(string="Amount", required=True, tracking=True, currency_field='company_currency',
                                     copy=True)
    f_commision_value_calculated = fields.Monetary(string="Calculated Amount", readonly=True, tracking=True,
                                                currency_field='company_currency', copy=True)
    f_is_calculated = fields.Boolean(string="Calculated", readonly=True, tracking=True, copy=False)
    f_user = fields.Char(string="Calculated By", default=lambda self: self.env.user.name, readonly=True, tracking=True,
                         copy=False)
    f_status = fields.Selection([('draft', 'Draft'), ('inprogress', 'In Progress'), ('cancelled', 'Cancelled'),
                                 ('calculated', 'Calculated'), ('confirmed', 'Confirmed')], default='draft',
                                readonly=True, tracking=True, copy=False)
    f_comment = fields.Text(string="Status", readonly=True, tracking=True, copy=False)
    f_calculated_date = fields.Date(string="Calculated Date", readonly=True, tracking=True, copy=False)
    company_currency_symbol = fields.Char(string='Company Currency', related="company_id.currency_id.symbol",
                                          readonly=True, copy=True)
    company_currency = fields.Many2one('res.currency', string='Company Currency', related="company_id.currency_id",
                                       readonly=True, copy=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, readonly=True,
                                 default=lambda self: self.env.company, copy=True)
    f_excluded_prods = fields.Many2many('product.product', string='Excluded Products', copy=True)
    f_excluded_families = fields.Many2many('f.product.family', string='Excluded Families', copy=True)
    f_excluded_identities = fields.Many2many('f.prod.identity', string='Excluded Identities', copy=True)
    f_total_sales = fields.Float(string='Total Sales', store=True)
    f_net_sales = fields.Float(string='Net Sales', store=True)
    f_sales_perc = fields.Float(string='Sales%', store=True)

    def get_total_sales(self):
        records = self
        if not records:
            records = self.env['f.cust.target'].sudo().search([])

        print("Target Records", records)
        for record in records:
            record.f_total_sales = 0
            record.f_net_sales = 0
            record.f_sales_perc = 0
            if record.f_status in ('draft', 'inprogress') and record.active:
                sales_bills = self.env['account.move.line'].read_group(
                    domain=['&', '&', '&', '&', '&',
                            ('partner_id', '=', record.f_customer.id),
                            ('move_id.invoice_date', '>=', record.f_from_date),
                            ('move_id.invoice_date', '<=', record.f_to_date),
                            ('move_id.state', '=', 'posted'),
                            ('move_id.move_type', 'in', ('out_invoice', 'out_refund')),
                            ('display_type', '=', 'product'), ],
                    fields=['partner_id', 'balance', 'price_total', 'price_subtotal'], groupby=['partner_id'])

                sales_bills_net = self.env['account.move.line'].read_group(
                    domain=['&', '&', '&', '&', '&', '&',
                            ('partner_id', '=', record.f_customer.id),
                            ('move_id.invoice_date', '>=', record.f_from_date),
                            ('move_id.invoice_date', '<=', record.f_to_date),
                            ('move_id.state', '=', 'posted'),
                            ('move_id.move_type', 'in', ('out_invoice', 'out_refund')),
                            ('display_type', '=', 'product'),
                            '&', '|',
                            ('product_id', 'not in', record.f_excluded_prods.ids),
                            ('product_id', '=', False),
                            '&', '|',
                            ('f_prod_family_id', 'not in', record.f_excluded_families.ids),
                            ('f_prod_family_id', '=', False),
                            '|',
                            ('f_prod_identity_id', 'not in', record.f_excluded_identities.ids),
                            ('f_prod_identity_id', '=', False), ],
                    fields=['partner_id', 'balance', 'price_total', 'price_subtotal'], groupby=['partner_id'])

                if sales_bills:
                    com_cur_round_prec = self.company_id.currency_id.decimal_places
                    sales = round(((sales_bills[0]['balance'] * -1) / sales_bills[0]['price_subtotal']) *
                                  sales_bills[0]['price_total'], com_cur_round_prec)
                    record.f_total_sales = sales
                    print("Target Sale", record.f_total_sales)

                if sales_bills_net:
                    com_cur_round_prec = self.company_id.currency_id.decimal_places
                    sales = round(((sales_bills_net[0]['balance'] * -1) / sales_bills_net[0]['price_subtotal']) *
                                  sales_bills_net[0]['price_total'], com_cur_round_prec)
                    record.f_net_sales = sales
                    if record.f_target_amount > 0:
                        record.f_sales_perc = (sales / record.f_target_amount) * 100
                        print("Target Perc", record.f_sales_perc)

    @api.onchange('f_to_date')
    def _f_onchange_to_date(self):
        print("111111")
        if self.f_from_date and self.f_to_date <= self.f_from_date:
            raise UserError('Period End Date should be greater than Start Date! ')

    # this function for change domain of Commission type based on target type
    @api.onchange('f_target_type')
    def _f_onchange_target_type(self):
        print("111111222")
        self.f_commision_value_type = False
        if self.f_target_type == 'sales':
            self.f_commision_value_type = "percent"
        elif self.f_target_type == 'rental':
            self.f_commision_value_type = "fixed"

    # this function for calculate the amount of bonus if hitting the target
    def f_calculate(self):
        for record in self:

            if record.f_status == 'inprogress':
                comm_amount = 0
                record.f_commision_value_calculated = 0
                record.f_is_calculated = False
                sales_bills = self.env['account.move.line'].read_group(
                    domain=['&', '&', '&', '&', '&', '&',
                            ('partner_id', '=', record.f_customer.id),
                            ('move_id.invoice_date', '>=', record.f_from_date),
                            ('move_id.invoice_date', '<=', record.f_to_date),
                            ('move_id.state', '=', 'posted'),
                            ('move_id.move_type', 'in', ('out_invoice', 'out_refund')),
                            ('display_type', '=', 'product'),
                            '&', '|',
                            ('product_id', 'not in', record.f_excluded_prods.ids),
                            ('product_id', '=', False),
                            '&', '|',
                            ('f_prod_family_id', 'not in', record.f_excluded_families.ids),
                            ('f_prod_family_id', '=', False),
                            '|',
                            ('f_prod_identity_id', 'not in', record.f_excluded_identities.ids),
                            ('f_prod_identity_id', '=', False), ],
                    fields=['partner_id', 'balance', 'price_total', 'price_subtotal'], groupby=['partner_id'])
                print('sales_bills', sales_bills)
                if sales_bills:
                    com_cur_round_prec = self.company_id.currency_id.decimal_places
                    print(com_cur_round_prec)
                    sales = round(((sales_bills[0]['balance'] * -1) / sales_bills[0]['price_subtotal']) *
                                  sales_bills[0]['price_total'], com_cur_round_prec)
                    print('sales', sales)
                    if sales >= record.f_target_amount:
                        print('record.f_commision_value_type', record.f_commision_value_type)
                        if record.f_commision_value_type == "percent":
                            comm_amount = sales * (record.f_commision_value / 100)
                        elif record.f_commision_value_type == "fixed":
                            comm_amount = record.f_commision_value
                        comment = "Calculation is Done For Partner : " + record.f_customer.name
                    else:
                        comment = "Partner " + record.f_customer.name + " Did NOT reach the target"
                else:
                    comment = "Partner " + record.f_customer.name + " Did NOT reach the target"
                record.f_commision_value_calculated = comm_amount
                record.f_calculated_date = datetime.now()
                record.f_user = self.env.user
                record.f_is_calculated = True
                record.f_status = "calculated"
                record.f_comment = comment

    # this function for Cancel button
    def f_cancel(self):
        self.f_status = "cancelled"
        self.f_is_calculated = False
        self.f_user = False
        self.f_comment = " "
        self.f_calculated_date = False

    # this function for Cancel button
    def f_start(self):
        self.f_status = "inprogress"

    # this function for Draft button
    def f_reset_to_draft(self):
        self.f_status = "draft"
        self.f_is_calculated = False
        self.f_user = False
        self.f_comment = " "
        self.f_calculated_date = False
        self.f_commision_value_calculated = 0

    def f_confirm(self):
        self.f_status = "confirmed"
