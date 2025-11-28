from odoo import models, fields, api, _
from datetime import datetime, timedelta
import logging

_logger = logging.getLogger(__name__)

class FCommissionCalculation(models.Model):
    _name = 'f.commission.calculation'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Commission Calculation'
    _rec_name = "f_name"

    f_state = fields.Selection(
        [('draft', 'Draft'), ('cancel', 'Cancelled'), ('done', 'Done'), ('confirm', 'Confirmed')], default='draft',
        tracking=True, string='State', copy=False)
    f_name = fields.Char('Name', required=True, tracking=True)
    f_period = fields.Many2one(comodel_name='f.commission.period', string='Period',
                                   domain="[('f_closed', '=', False)]", required=True, tracking=True)
    f_calculated_at = fields.Datetime(string='Calculated At', readonly=True, tracking=True)
    f_commission_role_ids = fields.Many2many('f.commission.role', string='Role', required=True, tracking=True)
    f_comments = fields.Html(string='Calculation Comments', tracking=True)

    f_collection_adjustment_id = fields.One2many('f.collections.adjustment', 'f_commission_calculation_id',
                                             string='Collection Adjustment')

    def f_compute_exclude_amount(self):
        for role in self.f_commission_role_ids:
            adjustment = self.env['f.collections.adjustment'].search([('f_commission_calculation_id', '=', self.id), ('f_commission_role_id', '=', role.id), ('f_adjustment_type', '=', 'exclude'), ('f_type', '=', 'auto')])
            sp_collections = self.env['account.payment'].read_group(
                domain=[('invoice_user_id', 'in', role.f_sales_persons.ids),
                        ('date', '>=', self.f_period.f_from),
                        ('date', '<=', self.f_period.f_to),
                        ('state', '=', 'posted'),
                        ('payment_type', '=', 'inbound'),
                        ('f_commission_exclude', '=', True),
                        ],
                fields=['amount_total_signed', 'state'],
                groupby=['state'], lazy=False)
            if sp_collections and not adjustment:
                vals = {
                    'f_commission_calculation_id': self.id,
                    'f_commission_role_id': role.id,
                    'f_adjustment_type': 'exclude',
                    'f_type': 'auto',
                    'f_amount': sp_collections[0]['amount_total_signed']
                }
                self.env['f.collections.adjustment'].create(vals)
            elif sp_collections and adjustment:
                adjustment.f_amount = sp_collections[0]['amount_total_signed']
            elif not sp_collections and adjustment:
                adjustment.unlink()


    def f_compute_include_amount(self):
        for role in self.f_commission_role_ids:
            adjustment = self.env['f.collections.adjustment'].search(
                [('f_commission_calculation_id', '=', self.id), ('f_commission_role_id', '=', role.id),
                 ('f_adjustment_type', '=', 'include'), ('f_type', '=', 'auto')])
            sp_collections = self.env['account.move'].read_group(
                domain=[('f_sales_person', '=', role.f_sales_persons.ids),
                        ('f_period_id', '=', self.f_period.id),
                        ('state', '=', 'posted'),
                        ('f_include_commission', '=', True),
                        ],
                fields=['f_commission_amount', 'state'],
                groupby=['state'], lazy=False)

            if sp_collections and not adjustment:
                vals = {
                    'f_commission_calculation_id': self.id,
                    'f_commission_role_id': role.id,
                    'f_adjustment_type': 'include',
                    'f_type': 'auto',
                    'f_amount': sp_collections[0]['f_commission_amount']
                }
                self.env['f.collections.adjustment'].create(vals)
            elif sp_collections and adjustment:
                adjustment.f_amount = sp_collections[0]['f_commission_amount']
            elif not sp_collections and adjustment:
                adjustment.unlink()

    def f_confirm_calculate(self):
        self.f_state = 'confirm'

    def f_cancel_calculate(self):
        _logger.info('-------------------------------------------------------------------------')
        _logger.info('Commission Calculation -> Cancelled')
        comm_setups = self.env['f.commission.setup'].search([('f_comm_calc_id', '=', self.id)])
        for comm in comm_setups:
            comm.f_is_calculated = False
            comm.f_comment = ' '
            comm.f_calculated_by = False
            comm.f_comm_calc_id = False

        self.env['f.commission.result'].search([('f_commission_calculation_id', '=', self.id)]).unlink()
        self.f_state = 'cancel'
        self.f_comments = ' '

    def f_reset_to_draft(self):
        _logger.info('-------------------------------------------------------------------------')
        _logger.info('Commission Calculation -> Reset To Draft')
        comm_setups = self.env['f.commission.setup'].search([('f_comm_calc_id', '=', self.id)])
        for comm in comm_setups:
            comm.f_is_calculated = False
            comm.f_comment = ' '
            comm.f_calculated_by = False
            comm.f_comm_calc_id = False

        self.f_state = 'draft'
        self.f_comments = ' '

    def f_calculate_commission(self):
        domain = [('f_commission_role_ids', 'in', self.f_commission_role_ids.ids)]
        if self.f_period.f_recurring:
            domain += ['|', ('f_commission_period_id', '=', self.f_period.id), ('f_recurring', '=', self.f_period.f_recurring)]
        else:
            domain += [('f_is_calculated', '=', False), ('f_commission_period_id', '=', self.f_period.id)]
        sale_setups = self.env['f.commission.setup'].search(domain + [('f_commission_type', '=', 'sales')])
        product_based_setups = self.env['f.commission.setup'].search(domain + [('f_commission_type', '=', 'product_based')])
        collection_setups = self.env['f.commission.setup'].search(domain + [('f_commission_type', '=', 'collection')])
        self.f_calculate_sales(sale_setups)
        self.f_calculate_product_based(product_based_setups)
        self.f_calculate_collection(collection_setups)
        self.f_state = 'done'

    def f_calculate_sales(self, sales_setup):
        for setup in sales_setup:
            for role in setup.f_commission_role_ids:
                sales_person_ids = tuple(
                    role.f_sales_persons.ids) if role.f_sales_persons.ids else (
                -1,)
                if len(sales_person_ids) == 1:
                    sales_person_condition = f"= {sales_person_ids[0]}"
                else:
                    sales_person_condition = f"IN {sales_person_ids}"
                query = (f"""
                    SELECT
                        SUM(case when am.price_subtotal != 0 then ((am.balance*-1)/am.price_subtotal)*am.price_total else 0 end) AS total_price,
                        SUM(
                            CASE
                                WHEN pt.id NOT IN (
                                    SELECT exc_prod.product_template_id
                                    FROM f_commission_setup fcs
                                    JOIN f_commission_setup_product_exc_rel exc_prod ON exc_prod.f_commission_setup_id = fcs.id
                                    WHERE fcs.id = {setup.id}
                                )
                                AND pt.f_product_family NOT IN (
                                    SELECT exc_family.f_product_family_id
                                    FROM f_commission_setup fcs
                                    JOIN f_commission_setup_product_family_exc_rel exc_family ON exc_family.f_commission_setup_id = fcs.id
                                    WHERE fcs.id = {setup.id}
                                )
                                AND pt.fprodidentity NOT IN (
                                    SELECT exc_identity.f_prod_identity_id
                                    FROM f_commission_setup fcs
                                    JOIN f_commission_setup_product_identity_exc_rel exc_identity ON exc_identity.f_commission_setup_id = fcs.id
                                    WHERE fcs.id = {setup.id}
                                ) 
        
                                THEN case when am.price_subtotal != 0 then ((am.balance*-1)/am.price_subtotal)*am.price_total else 0 end
                                ELSE 0
                            END
                        ) AS total_price_without_exclusions,
                        m.invoice_user_id as sales_person
                    FROM
                        account_move_line am
                    JOIN
                        account_move m ON am.move_id = m.id
                    JOIN
                        f_commission_period p ON p.id = {self.f_period.id}
                    JOIN 
                        product_product pp ON pp.id = am.product_id
                    JOIN 
                        product_template pt ON pt.id = pp.product_tmpl_id
                    WHERE
                        m.invoice_user_id {sales_person_condition}
                        AND m.invoice_date BETWEEN p.f_from AND p.f_to
                        AND m.state = 'posted'
                        AND m.move_type IN ('out_invoice','out_refund')
                        AND am.display_type = 'product'
                    GROUP BY m.invoice_user_id
        
                """ )
                print("/////////////////////////// query: ", query)
                self.env.cr.execute(query)
                result = self.env.cr.fetchall()

                print("/////////////////////////// query result: ", result)
                if result:
                    f_total_sales = sum(row[0] for row in result)
                    f_net_sales = sum(row[1] for row in result)
                    if setup.f_commission_value_type == 'amount':
                        f_commission_amount = setup.f_commission_value
                        if f_commission_amount > setup.f_upper_limit:
                            f_commission_amount = setup.f_upper_limit
                        vals = {
                            'f_commission_role_id': role.id,
                            'f_commission_setup_id': setup.id,
                            'f_commission_calculation_id': self.id,
                            'f_commission_period_id': self.f_period.id,
                            'f_commission_amount': f_commission_amount,
                            'f_total_amount': f_net_sales,
                            'f_commission_target': 'No Target',
                            'f_commission_percent': setup.f_commission_value
                        }
                        self.env['f.commission.result'].sudo().create(vals)
                    elif setup.f_commission_value_type == 'perc':
                        f_commission_amount = (f_net_sales * setup.f_commission_value) / 100
                        if f_commission_amount > setup.f_upper_limit:
                            f_commission_amount = setup.f_upper_limit
                        vals = {
                            'f_commission_role_id': role.id,
                            'f_commission_setup_id': setup.id,
                            'f_commission_calculation_id': self.id,
                            'f_commission_period_id': self.f_period.id,
                            'f_commission_amount': f_commission_amount,
                            'f_total_amount': f_net_sales,
                            'f_commission_target': 'No Target',
                            'f_commission_percent': setup.f_commission_value
                        }
                        self.env['f.commission.result'].sudo().create(vals)
                    elif setup.f_commission_value_type == 'perc_tier':
                        f_commission_amount = self.f_calculate_sales_tier_value_type(setup, 'percentage', f_net_sales)
                        if f_commission_amount > setup.f_upper_limit:
                            f_commission_amount = setup.f_upper_limit
                        vals = {
                            'f_commission_role_id': role.id,
                            'f_commission_setup_id': setup.id,
                            'f_commission_calculation_id': self.id,
                            'f_commission_period_id': self.f_period.id,
                            'f_commission_amount': f_commission_amount,
                            'f_total_amount': f_net_sales,
                            'f_commission_target': f'from {setup.f_tier_from} to {setup.f_tier_to}',
                            'f_commission_percent': setup.f_commission_value
                        }
                        self.env['f.commission.result'].sudo().create(vals)
                    elif setup.f_commission_value_type == 'amount_tier':
                        f_commission_amount = self.f_calculate_sales_tier_value_type(setup, 'amount', f_net_sales)
                        if f_commission_amount > setup.f_upper_limit:
                            f_commission_amount = setup.f_upper_limit
                        vals = {
                            'f_commission_role_id': role.id,
                            'f_commission_setup_id': setup.id,
                            'f_commission_calculation_id': self.id,
                            'f_commission_period_id': self.f_period.id,
                            'f_commission_amount': f_commission_amount,
                            'f_total_amount': f_net_sales,
                            'f_commission_target': f'from {setup.f_tier_from} to {setup.f_tier_to}',
                            'f_commission_percent': setup.f_commission_value
                        }
                        self.env['f.commission.result'].sudo().create(vals)
                    elif setup.f_commission_value_type == 'perc_target':
                        f_commission_amount = self.f_calculate_sales_target_value_type(setup, 'percentage', f_net_sales)
                        if f_commission_amount > setup.f_upper_limit:
                            f_commission_amount = setup.f_upper_limit
                        vals = {
                            'f_commission_role_id': role.id,
                            'f_commission_setup_id': setup.id,
                            'f_commission_calculation_id': self.id,
                            'f_commission_period_id': self.f_period.id,
                            'f_commission_amount': f_commission_amount,
                            'f_total_amount': f_net_sales,
                            'f_commission_target': f'above {setup.f_target}',
                            'f_commission_percent': setup.f_commission_value
                        }
                        self.env['f.commission.result'].sudo().create(vals)
                    elif setup.f_commission_value_type == 'amount_target':
                        f_commission_amount = self.f_calculate_sales_target_value_type(setup, 'amount', f_net_sales)
                        if f_commission_amount > setup.f_upper_limit:
                            f_commission_amount = setup.f_upper_limit
                        vals = {
                            'f_commission_role_id': role.id,
                            'f_commission_setup_id': setup.id,
                            'f_commission_calculation_id': self.id,
                            'f_commission_period_id': self.f_period.id,
                            'f_commission_amount': f_commission_amount,
                            'f_total_amount': f_net_sales,
                            'f_commission_target': f'above {setup.f_target}',
                            'f_commission_percent': setup.f_commission_value
                        }
                        self.env['f.commission.result'].sudo().create(vals)
                else:
                    vals = {
                        'f_commission_role_id': role.id,
                        'f_commission_setup_id': setup.id,
                        'f_commission_calculation_id': self.id,
                        'f_commission_period_id': self.f_period.id,
                        'f_commission_amount': 0,
                        'f_total_amount': 0,
                        'f_commission_target': "",
                        'f_commission_percent': 0
                    }
                    self.env['f.commission.result'].sudo().create(vals)
            setup.f_is_calculated = True
            setup.f_comm_calc_id = self.id

    def f_calculate_product_based(self, product_based_setups):
        for setup in product_based_setups:
            for role in setup.f_commission_role_ids:
                sales_person_ids = tuple(
                    role.f_sales_persons.ids) if role.f_sales_persons.ids else (
                    -1,)
                if len(sales_person_ids) == 1:
                    sales_person_condition = f"= {sales_person_ids[0]}"
                else:
                    sales_person_condition = f"IN {sales_person_ids}"
                query = (f"""
                    SELECT
                        SUM(case when am.price_subtotal != 0 then ((am.balance*-1)/am.price_subtotal)*am.price_total else 0 end) AS total_price,
                        SUM(
                            CASE
                                WHEN pt.id IN (
                                    SELECT prod.product_template_id
                                    FROM f_commission_setup fcs
                                    JOIN f_commission_setup_product_rel prod ON prod.f_commission_setup_id = fcs.id
                                    WHERE fcs.id = {setup.id}
                                )
                                OR pt.f_product_family IN (
                                    SELECT family.f_product_family_id
                                    FROM f_commission_setup fcs
                                    JOIN f_commission_setup_product_family_rel family ON family.f_commission_setup_id = fcs.id
                                    WHERE fcs.id = {setup.id}
                                )
                                OR pt.fprodidentity IN (
                                    SELECT identity.f_prod_identity_id
                                    FROM f_commission_setup fcs
                                    JOIN f_commission_setup_product_identity_rel identity ON identity.f_commission_setup_id = fcs.id
                                    WHERE fcs.id = {setup.id}
                                ) 
    
                                THEN case when am.price_subtotal != 0 then ((am.balance*-1)/am.price_subtotal)*am.price_total else 0 end
                                ELSE 0
                            END
                        ) AS total_price_with_inclusions,
                        SUM(
                            CASE
                                WHEN pt.id IN (
                                    SELECT prod.product_template_id
                                    FROM f_commission_setup fcs
                                    JOIN f_commission_setup_product_rel prod ON prod.f_commission_setup_id = fcs.id
                                    WHERE fcs.id = {setup.id}
                                )
                                OR pt.f_product_family IN (
                                    SELECT family.f_product_family_id
                                    FROM f_commission_setup fcs
                                    JOIN f_commission_setup_product_family_rel family ON family.f_commission_setup_id = fcs.id
                                    WHERE fcs.id = {setup.id}
                                )
                                OR pt.fprodidentity IN (
                                    SELECT identity.f_prod_identity_id
                                    FROM f_commission_setup fcs
                                    JOIN f_commission_setup_product_identity_rel identity ON identity.f_commission_setup_id = fcs.id
                                    WHERE fcs.id = {setup.id}
                                ) 
    
                                THEN am.quantity
                                ELSE 0
                            END
                        ) AS quantity,
                        m.invoice_user_id as sales_person
                    FROM
                        account_move_line am
                    JOIN
                        account_move m ON am.move_id = m.id
                    JOIN
                        f_commission_period p ON p.id = {self.f_period.id}
                    JOIN 
                        product_product pp ON pp.id = am.product_id
                    JOIN 
                        product_template pt ON pt.id = pp.product_tmpl_id
                    WHERE
                        m.invoice_user_id {sales_person_condition}
                        AND m.invoice_date BETWEEN p.f_from AND p.f_to
                        AND m.state = 'posted'
                        AND m.move_type IN ('out_invoice','out_refund')
                        AND am.display_type = 'product'
                    GROUP BY m.invoice_user_id

                """)
                print("/////////////////////////// query: ", query)
                self.env.cr.execute(query)
                result = self.env.cr.fetchall()

                print("/////////////////////////// query result: ", result)
                if result:
                    f_total_sales = sum(row[0] for row in result)
                    f_net_sales = sum(row[1] for row in result)
                    f_net_quantity = sum(row[2] for row in result)
                    f_net_amount = 0
                    if setup.f_target_type == 'amount':
                        f_net_amount = f_net_sales
                    elif setup.f_target_type == 'quantity':
                        f_net_amount = f_net_quantity
                    if setup.f_commission_value_type == 'amount':
                        f_commission_amount = setup.f_commission_value
                        if f_commission_amount > setup.f_upper_limit:
                            f_commission_amount = setup.f_upper_limit
                        vals = {
                            'f_commission_role_id': role.id,
                            'f_commission_setup_id': setup.id,
                            'f_commission_calculation_id': self.id,
                            'f_commission_period_id': self.f_period.id,
                            'f_commission_amount': f_commission_amount,
                            'f_total_amount': f_net_amount,
                            'f_commission_target': f'no target',
                            'f_commission_percent': setup.f_commission_value
                        }
                        self.env['f.commission.result'].sudo().create(vals)
                    elif setup.f_commission_value_type == 'perc':
                        f_commission_amount = (f_net_sales * setup.f_commission_value) / 100
                        if f_commission_amount > setup.f_upper_limit:
                            f_commission_amount = setup.f_upper_limit
                        vals = {
                            'f_commission_role_id': role.id,
                            'f_commission_setup_id': setup.id,
                            'f_commission_calculation_id': self.id,
                            'f_commission_period_id': self.f_period.id,
                            'f_commission_amount': f_commission_amount,
                            'f_total_amount': f_net_amount,
                            'f_commission_target': f'no target',
                            'f_commission_percent': setup.f_commission_value
                        }
                        self.env['f.commission.result'].sudo().create(vals)
                    elif setup.f_commission_value_type == 'perc_tier':
                        f_commission_amount = self.f_calculate_product_based_tier_value_type(setup, 'percentage', f_net_sales, f_net_amount)
                        if f_commission_amount > setup.f_upper_limit:
                            f_commission_amount = setup.f_upper_limit
                        vals = {
                            'f_commission_role_id': role.id,
                            'f_commission_setup_id': setup.id,
                            'f_commission_calculation_id': self.id,
                            'f_commission_period_id': self.f_period.id,
                            'f_commission_amount': f_commission_amount,
                            'f_total_amount': f_net_amount,
                            'f_commission_target': f'from {setup.f_tier_from} to {setup.f_tier_to}',
                            'f_commission_percent': setup.f_commission_value
                        }
                        self.env['f.commission.result'].sudo().create(vals)
                    elif setup.f_commission_value_type == 'amount_tier':
                        f_commission_amount = self.f_calculate_product_based_tier_value_type(setup, 'amount', f_net_sales, f_net_amount)
                        if f_commission_amount > setup.f_upper_limit:
                            f_commission_amount = setup.f_upper_limit
                        vals = {
                            'f_commission_role_id': role.id,
                            'f_commission_setup_id': setup.id,
                            'f_commission_calculation_id': self.id,
                            'f_commission_period_id': self.f_period.id,
                            'f_commission_amount': f_commission_amount,
                            'f_total_amount': f_net_amount,
                            'f_commission_target': f'from {setup.f_tier_from} to {setup.f_tier_to}',
                            'f_commission_percent': setup.f_commission_value
                        }
                        self.env['f.commission.result'].sudo().create(vals)
                    elif setup.f_commission_value_type == 'perc_target':
                        f_commission_amount = self.f_calculate_product_based_target_value_type(setup, 'percentage', f_net_sales, f_net_amount)
                        if f_commission_amount > setup.f_upper_limit:
                            f_commission_amount = setup.f_upper_limit
                        vals = {
                            'f_commission_role_id': role.id,
                            'f_commission_setup_id': setup.id,
                            'f_commission_calculation_id': self.id,
                            'f_commission_period_id': self.f_period.id,
                            'f_commission_amount': f_commission_amount,
                            'f_total_amount': f_net_amount,
                            'f_commission_target': f'above {setup.f_target}',
                            'f_commission_percent': setup.f_commission_value
                        }
                        self.env['f.commission.result'].sudo().create(vals)
                    elif setup.f_commission_value_type == 'amount_target':
                        f_commission_amount = self.f_calculate_product_based_target_value_type(setup, 'amount', f_net_sales, f_net_amount)
                        if f_commission_amount > setup.f_upper_limit:
                            f_commission_amount = setup.f_upper_limit
                        vals = {
                            'f_commission_role_id': role.id,
                            'f_commission_setup_id': setup.id,
                            'f_commission_calculation_id': self.id,
                            'f_commission_period_id': self.f_period.id,
                            'f_commission_amount': f_commission_amount,
                            'f_total_amount': f_net_amount,
                            'f_commission_target': f'above {setup.f_target}',
                            'f_commission_percent': setup.f_commission_value
                        }
                        self.env['f.commission.result'].sudo().create(vals)

                else:
                    vals = {
                        'f_commission_role_id': role.id,
                        'f_commission_setup_id': setup.id,
                        'f_commission_calculation_id': self.id,
                        'f_commission_period_id': self.f_period.id,
                        'f_commission_amount': 0,
                        'f_total_amount': 0,
                        'f_commission_target': "",
                        'f_commission_percent': 0
                    }
                    self.env['f.commission.result'].sudo().create(vals)
            setup.f_is_calculated = True
            setup.f_comm_calc_id = self.id

    def f_calculate_collection(self, collection_setups):
        for setup in collection_setups:
            _logger.info(
                _("/////////////////////////////// setup: %s") % setup.f_description)
            for role in setup.f_commission_role_ids:
                _logger.info(
                    _("/////////////////////////////// setup: %s") % role.f_name)
                collection_domain = self.f_get_collection_domain(setup, role)
                total_collections = self.env['account.payment'].read_group(
                    domain=collection_domain,
                    fields=['amount_total_signed', 'invoice_user_id'],
                    groupby=['invoice_user_id'], lazy=False)
                total_collections_amount = sum(row['amount_total_signed'] for row in total_collections)
                _logger.info(_("/////////////////////////////// total_collections_amount: %s") % total_collections_amount)
                return_check_domain = self.f_get_return_domain(setup, role)
                return_check = self.env['account.payment'].read_group(
                    domain=return_check_domain,
                    fields=['amount_total_signed', 'invoice_user_id'],
                    groupby=['invoice_user_id'], lazy=False)
                total_return_check_amount = sum(row['amount_total_signed'] for row in return_check)
                _logger.info(
                    _("/////////////////////////////// total_return_check_amount: %s") % total_return_check_amount)
                check_to_cash_amount = self.f_get_check_to_cash_amount(setup, role)
                _logger.info(
                    _("/////////////////////////////// check_to_cash_amount: %s") % check_to_cash_amount)
                exclude_check = self.f_get_exclude_check_amount(setup, role)
                _logger.info(
                    _("/////////////////////////////// exclude_check: %s") % exclude_check)
                total_amount = total_collections_amount
                if setup.f_collection_type.f_include_returned_checks or setup.f_collection_type.f_payment_type == 'all':
                    total_amount -= total_return_check_amount
                total_amount += check_to_cash_amount
                total_amount -= exclude_check
                f_excluded_amount = self.env['f.collections.adjustment'].read_group(
                    domain=[('f_commission_setup_id', '=', setup.id),
                            ('f_commission_calculation_id', '=', self.id),
                            ('f_commission_role_id', '=', role.id),
                            ('f_adjustment_type', '=', 'exclude'),
                            ],
                    fields=['f_amount', 'f_adjustment_type'],
                    groupby=['f_adjustment_type'], lazy=False)

                f_include_amount = self.env['f.collections.adjustment'].read_group(
                    domain=[('f_commission_setup_id', '=', setup.id),
                            ('f_commission_calculation_id', '=', self.id),
                            ('f_commission_role_id', '=', role.id),
                            ('f_adjustment_type', '=', 'include'),
                            ],
                    fields=['f_amount', 'f_adjustment_type'],
                    groupby=['f_adjustment_type'], lazy=False)
                if f_include_amount:
                    total_amount += f_include_amount[0]['f_amount']
                if f_excluded_amount:
                    total_amount -= f_excluded_amount[0]['f_amount']
                _logger.info(
                    _("/////////////////////////////// total_amount: %s") % total_amount)
                if setup.f_commission_value_type == 'amount':
                    if setup.f_is_bad_debt:
                        f_commission_amount = self.f_calculate_bad_debt_commission(setup, role, total_amount, False)
                    else:
                        f_commission_amount = setup.f_commission_value
                    if f_commission_amount > setup.f_upper_limit:
                        f_commission_amount = setup.f_upper_limit
                    vals = {
                        'f_commission_role_id': role.id,
                        'f_commission_setup_id': setup.id,
                        'f_commission_calculation_id': self.id,
                        'f_commission_period_id': self.f_period.id,
                        'f_commission_amount': f_commission_amount,
                        'f_total_amount': total_amount,
                        'f_commission_target': f'no target',
                        'f_commission_percent': setup.f_commission_value
                    }
                    self.env['f.commission.result'].sudo().create(vals)
                elif setup.f_commission_value_type == 'perc':
                    if setup.f_is_bad_debt:
                        f_commission_amount = self.f_calculate_bad_debt_commission(setup, role, total_amount, False)
                    else:
                        f_commission_amount = (total_amount * setup.f_commission_value) / 100
                    if f_commission_amount > setup.f_upper_limit:
                        f_commission_amount = setup.f_upper_limit
                    vals = {
                        'f_commission_role_id': role.id,
                        'f_commission_setup_id': setup.id,
                        'f_commission_calculation_id': self.id,
                        'f_commission_period_id': self.f_period.id,
                        'f_commission_amount': f_commission_amount,
                        'f_total_amount': total_amount,
                        'f_commission_target': f'no target',
                        'f_commission_percent': setup.f_commission_value
                    }
                    self.env['f.commission.result'].sudo().create(vals)
                elif setup.f_commission_value_type == 'perc_tier':
                    if setup.f_is_bad_debt:
                        f_commission_amount = self.f_calculate_bad_debt_commission(setup, role, total_amount, 'tier')
                    else:
                        f_commission_amount = self.f_calculate_sales_tier_value_type(setup, 'percentage', total_amount)
                    if f_commission_amount > setup.f_upper_limit:
                        f_commission_amount = setup.f_upper_limit
                    vals = {
                        'f_commission_role_id': role.id,
                        'f_commission_setup_id': setup.id,
                        'f_commission_calculation_id': self.id,
                        'f_commission_period_id': self.f_period.id,
                        'f_commission_amount': f_commission_amount,
                        'f_total_amount': total_amount,
                        'f_commission_target': f'from {setup.f_tier_from} to {setup.f_tier_to}',
                        'f_commission_percent': setup.f_commission_value
                    }
                    self.env['f.commission.result'].sudo().create(vals)
                elif setup.f_commission_value_type == 'amount_tier':
                    if setup.f_is_bad_debt:
                        f_commission_amount = self.f_calculate_bad_debt_commission(setup, role, total_amount, 'tier')
                    else:
                        f_commission_amount = self.f_calculate_sales_tier_value_type(setup, 'amount', total_amount)
                    if f_commission_amount > setup.f_upper_limit:
                        f_commission_amount = setup.f_upper_limit
                    vals = {
                        'f_commission_role_id': role.id,
                        'f_commission_setup_id': setup.id,
                        'f_commission_calculation_id': self.id,
                        'f_commission_period_id': self.f_period.id,
                        'f_commission_amount': f_commission_amount,
                        'f_total_amount': total_amount,
                        'f_commission_target': f'from {setup.f_tier_from} to {setup.f_tier_to}',
                        'f_commission_percent': setup.f_commission_value
                    }
                    self.env['f.commission.result'].sudo().create(vals)
                elif setup.f_commission_value_type == 'perc_target':
                    if setup.f_is_bad_debt:
                        f_commission_amount = self.f_calculate_bad_debt_commission(setup, role, total_amount, 'target')
                    else:
                        f_commission_amount = self.f_calculate_sales_target_value_type(setup, 'percentage', total_amount)
                    if f_commission_amount > setup.f_upper_limit:
                        f_commission_amount = setup.f_upper_limit
                    vals = {
                        'f_commission_role_id': role.id,
                        'f_commission_setup_id': setup.id,
                        'f_commission_calculation_id': self.id,
                        'f_commission_period_id': self.f_period.id,
                        'f_commission_amount': f_commission_amount,
                        'f_total_amount': total_amount,
                        'f_commission_target': f'above {setup.f_target}',
                        'f_commission_percent': setup.f_commission_value
                    }
                    self.env['f.commission.result'].sudo().create(vals)
                elif setup.f_commission_value_type == 'amount_target':
                    if setup.f_is_bad_debt:
                        f_commission_amount = self.f_calculate_bad_debt_commission(setup, role, total_amount, 'target')
                    else:
                        f_commission_amount = self.f_calculate_sales_target_value_type(setup, 'amount', total_amount)
                    if f_commission_amount > setup.f_upper_limit:
                        f_commission_amount = setup.f_upper_limit
                    vals = {
                        'f_commission_role_id': role.id,
                        'f_commission_setup_id': setup.id,
                        'f_commission_calculation_id': self.id,
                        'f_commission_period_id': self.f_period.id,
                        'f_commission_amount': f_commission_amount,
                        'f_total_amount': total_amount,
                        'f_commission_target': f'above {setup.f_target}',
                        'f_commission_percent': setup.f_commission_value
                    }
                    self.env['f.commission.result'].sudo().create(vals)
            setup.f_is_calculated = True
            setup.f_comm_calc_id = self.id

    def f_calculate_sales_tier_value_type(self, setup, type, total_amount):
        if setup.f_tier_from < total_amount <= setup.f_tier_to:
            if type == 'percentage':
                return (total_amount * setup.f_commission_value) / 100
            elif type == 'amount':
                return setup.f_commission_value
        if total_amount > setup.f_tier_to and setup.f_limit_to_target:
            if type == 'percentage':
                return (setup.f_tier_to * setup.f_commission_value) / 100
            elif type == 'amount':
                return setup.f_commission_value
        return 0

    def f_calculate_sales_target_value_type(self, setup, type, total_amount):
        entry_point = setup.f_target * setup.f_entry_point
        if total_amount >= entry_point:
            if type == 'percentage':
                if setup.f_limit_to_target:
                    return (setup.f_target * setup.f_commission_value) / 100
                return (total_amount * setup.f_commission_value) / 100
            elif type == 'amount':
                if setup.f_limit_to_target:
                    return setup.f_commission_value
                percent = setup.f_commission_value / setup.f_target
                return percent * total_amount
        return 0

    def f_calculate_product_based_tier_value_type(self, setup, type, net_sales, net_amount):
        if setup.f_tier_from < net_amount <= setup.f_tier_to:
            if type == 'percentage':
                return (net_sales * setup.f_commission_value) / 100
            elif type == 'amount':
                return setup.f_commission_value
        if net_amount > setup.f_tier_to and setup.f_limit_to_target:
            if type == 'percentage':
                if setup.f_target_type == 'amount':
                    return (setup.f_tier_to * setup.f_commission_value) / 100
                elif setup.f_target_type == 'quantity':
                    tier_perc = setup.f_tier_to / net_amount
                    tier_amount = tier_perc * net_sales
                    return (tier_amount * setup.f_commission_value) / 100
            elif type == 'amount':
                return setup.f_commission_value
        return 0

    def f_calculate_product_based_target_value_type(self, setup, type, net_sales, net_amount):
        entry_point = setup.f_target * setup.f_entry_point
        if net_amount >= entry_point:
            if type == 'percentage':
                if setup.f_limit_to_target:
                    if setup.f_target_type == 'amount':
                        return (setup.f_target * setup.f_commission_value) / 100
                    elif setup.f_target_type == 'quantity':
                        target_perc = setup.f_target / net_amount
                        target_amount = target_perc * net_sales
                        return (target_amount * setup.f_commission_value) / 100
                return (net_sales * setup.f_commission_value) / 100
            elif type == 'amount':
                if setup.f_limit_to_target:
                    return setup.f_commission_value
                percent = setup.f_commission_value / setup.f_target
                return percent * net_sales
        return 0

    def f_calculate_collection_target_value_type(self, setup, type, total_amount, bad_debt):
        entry_point = setup.f_target * setup.f_entry_point
        if total_amount >= entry_point:
            if type == 'percentage':
                if setup.f_limit_to_target:
                    return (setup.f_target * setup.f_commission_value) / 100
                return (total_amount * setup.f_commission_value) / 100
            elif type == 'amount':
                if setup.f_limit_to_target:
                    return setup.f_commission_value
                percent = setup.f_commission_value / setup.f_target
                return percent * total_amount
        return 0

    def f_get_collection_domain(self, setup, role):
        domain = [
            ('invoice_user_id', 'in', role.f_sales_persons.ids),
            ('date', '>=', self.f_period.f_from),
            ('date', '<=', self.f_period.f_to),
            ('state', '=', 'posted'),
            ('payment_type', '=', 'inbound'),
        ]
        if setup.f_collection_type.f_payment_type == 'all':
            return domain

        domain = domain + [('journal_id', 'in', setup.f_collection_type.f_journals.ids), ('destination_account_id', 'in', setup.f_collection_type.f_destination_account.ids)]

        return domain

    def f_get_return_domain(self, setup, role):
        domain = [
            '&', '&', '&', '&', '&',
            ('return_date', '>=', self.f_period.f_from),
            ('return_date', '<=', self.f_period.f_to),
            ('invoice_user_id', 'in', role.f_sales_persons.ids),
            ('state', '=', 'posted'),
            ('payment_type', '=', 'inbound'),
            ('check_state', '=', 'returned')
        ]

        return domain

    def f_get_check_to_cash_amount(self, setup, role):
        total_bounce_check_amount = 0
        domain = [
            ('invoice_user_id', 'in', role.f_sales_persons.ids),
            ('date', '>=', self.f_period.f_from),
            ('date', '<=', self.f_period.f_to),
            ('state', '=', 'posted'),
            ('payment_type', '=', 'inbound'),
        ]
        if setup.f_collection_type.f_payment_type == 'custom':
            domain = domain + [('journal_id', 'not in', setup.f_collection_type.f_journals.ids), ('destination_account_id', 'in', setup.f_collection_type.f_destination_account.ids)]

            check_to_cash = self.env['account.payment'].with_context(lang='en_US').read_group(
                domain=domain,
                fields=['amount_total_signed', 'date', 'due_date', 'invoice_user_id'],
                groupby=['invoice_user_id', 'date:day', 'due_date:day'], lazy=False)
            print(check_to_cash)
            for row in check_to_cash:
                date = datetime.strptime(row['date:day'], "%d %b %Y") if row['date:day'] else None
                due_date = datetime.strptime(row['due_date:day'], "%d %b %Y") if row['due_date:day'] else None
                if date and due_date:
                    limit_days = (due_date - date).days
                    if setup.f_collection_type.f_check_to_cash_limit_from <= limit_days < setup.f_collection_type.f_check_to_cash_limit_to:
                        total_bounce_check_amount += row['amount_total_signed']
        return total_bounce_check_amount

    def f_get_exclude_check_amount(self, setup, role):
        total_exclude_check_amount = 0
        domain = [
            ('invoice_user_id', 'in', role.f_sales_persons.ids),
            ('date', '>=', self.f_period.f_from),
            ('date', '<=', self.f_period.f_to),
            ('state', '=', 'posted'),
            ('payment_type', '=', 'inbound'),
        ]
        if setup.f_collection_type.f_payment_type == 'custom':
            domain = domain + [('journal_id', 'in', setup.f_collection_type.f_journals.ids), ('destination_account_id', 'in', setup.f_collection_type.f_destination_account.ids)]

            cash_exclude = self.env['account.payment'].with_context(lang='en_US').read_group(
                domain=domain,
                fields=['amount_total_signed', 'date', 'due_date', 'invoice_user_id'],
                groupby=['invoice_user_id', 'date:day', 'due_date:day'], lazy=False)
            for row in cash_exclude:
                date = datetime.strptime(row['date:day'], "%d %b %Y") if row['date:day'] else None
                due_date = datetime.strptime(row['due_date:day'], "%d %b %Y") if row['due_date:day'] else None
                if date and due_date:
                    limit_days = (due_date - date).days
                    if setup.f_collection_type.f_check_exclude_from <= limit_days < setup.f_collection_type.f_check_exclude_to:
                        total_exclude_check_amount += row['amount_total_signed']
        return total_exclude_check_amount

    def f_calculate_bad_debt_commission(self, setup, role, total_amount, type):
        sales_person_ids = tuple(
            role.f_sales_persons.ids) if role.f_sales_persons.ids else (
            -1,)
        if len(sales_person_ids) == 1:
            sales_person_condition = f"= {sales_person_ids[0]}"
        else:
            sales_person_condition = f"IN {sales_person_ids}"
        bad_debt_date = self.f_period.f_to - timedelta(days=setup.f_bad_debt_matrix.f_bad_debt)
        self.env.cr.execute(f"""
            select user_id, sum(xbalance)as total_balance from (
                select user_id , partner_id, xbalance
                from (
                    select am.invoice_user_id as user_id, p.id as partner_id,
                    sum(
                        CASE WHEN am.move_type = 'out_invoice' and am.invoice_date_due <  DATE('{bad_debt_date}') THEN COALESCE(aml.debit,0) 
                        WHEN am.move_type != 'out_invoice' and am.date <  DATE('{bad_debt_date}') THEN COALESCE(aml.debit,0)
                        ELSE 0 
                    END) - 
                    sum(
                        CASE WHEN am.move_type = 'out_invoice' and am.invoice_date_due <  DATE('{bad_debt_date}') THEN COALESCE(aml.credit,0) 
                        WHEN am.move_type != 'out_invoice' and am.date <  DATE('{bad_debt_date}') THEN COALESCE(aml.credit,0)
                        ELSE 0 
                    END) as xbalance
                    from account_move_line aml,
                        account_move am , 
                        account_account ac, 
                        res_partner p
                    where aml.move_id = am.id
                        AND am.state = 'posted'
                        AND  ac.id = aml.account_id
                        and ac.account_type in ('liability_payable','asset_receivable')
                        AND p.id = aml.partner_id
                        and (p.f_bad_debt = False or p.f_bad_debt is NULL)
                    group by am.invoice_user_id,p.id
                ) s1 
            ) s2 
            where xbalance>0
                and user_id {sales_person_condition}
                group by user_id

        """)

        balance = 0
        result = self.env.cr.fetchall()
        if result:
            balance = sum(row[0] for row in result) or 0
        f_commission_percent = 0
        for line in setup.f_bad_debt_matrix.f_matrix_line:
            if line.f_operator == 'between' and balance >= line.f_from_value and balance <= line.f_to_value:
                f_commission_percent = line.f_commission_percent
            elif line.f_operator == 'less' and balance < line.f_to_value:
                f_commission_percent = line.f_commission_percent
            elif line.f_operator == 'great' and balance > line.f_from_value:
                f_commission_percent = line.f_commission_percent

        if type == 'target':
            entry_point = setup.f_target * setup.f_entry_point
            if total_amount >= entry_point:
                if type == 'percentage':
                    if setup.f_limit_to_target:
                        return setup.f_target * f_commission_percent
                    return total_amount * f_commission_percent
        elif type == 'tier':
            if setup.f_tier_from < total_amount <= setup.f_tier_to:
                return total_amount * f_commission_percent
            if total_amount > setup.f_tier_to and setup.f_limit_to_target:
                return setup.f_tier_to * f_commission_percent
            if setup.f_tier_from > total_amount:
                return 0
        else:
            return total_amount * f_commission_percent

    def f_get_commission_result(self):
        results = self.env['f.commission.result'].sudo().search([('f_commission_calculation_id', '=', self.id)])
        action = self.env['ir.actions.actions']._for_xml_id('f_commission_management.f_commission_result_action')
        if len(results) > 1:
            action['domain'] = [('id', 'in', results.ids)]
        elif len(results) == 1:
            form_view = [(self.env.ref('f_commission_management.f_commission_result_form_view').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state, view) for state, view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = results.id
        else:
            action = {'type': 'ir.actions.act_window_close'}

        context = {}
        if len(self) == 1:
            context.update({
                'default_f_commission_calculation_id': self.id,
            })
        action['context'] = context
        return action