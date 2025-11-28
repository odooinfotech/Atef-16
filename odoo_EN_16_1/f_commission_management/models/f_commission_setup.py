from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class FCommissionSetup(models.Model):
    _name = 'f.commission.setup'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Commission Setup'
    _rec_name = 'f_description'

    # Base Fields
    f_description = fields.Char(string='Description')
    f_commission_type = fields.Selection(
        [('sales', 'Sales'), ('product_based', 'Product Based'), ('collection', 'Collection')], default='sales',
        required=True, string='Commission Type', copy=True, tracking=True)
    f_commission_period_id = fields.Many2one('f.commission.period', string='Period', tracking=True)
    f_commission_role_ids = fields.Many2many('f.commission.role', string='Role', required=True, tracking=True)
    f_commission_value_type = fields.Selection(
        [('amount', 'Amount'), ('perc', '%'), ('perc_tier', '% / Tier'), ('perc_target', '% / Target'),
         ('amount_tier', 'Amount / Tier'), ('amount_target', 'Amount / Target')], default='amount', required=True,
        string='Commission Value Type', tracking=True)
    f_commission_value = fields.Float(string='Commission Value', tracking=True)
    f_is_calculated = fields.Boolean(string='Calculated', copy=False, tracking=True, store=True)
    f_calculated_by = fields.Integer(string="Calculated By", copy=False, tracking=True)
    f_commission_calculated_at = fields.Datetime(string='Calculated At', readonly=True, tracking=True)
    f_comment = fields.Char(string='Comment', copy=False, tracking=True)
    f_comm_calc_id = fields.Many2one(comodel_name='f.commission.calculation', string='Last Calculation', copy=False,
                                     tracking=True)
    f_is_recurring = fields.Boolean(string='Recurring', default=False)
    f_recurring = fields.Selection([('monthly', 'Monthly'), ('quarterly', 'Quarterly'), ('yearly', 'Yearly')],
                                   string='Recurring Type')
    f_pricelist = fields.Many2many('product.pricelist', string='Pricelist')
    f_limit_to_target = fields.Boolean(string='Limit To Target', default=False)
    f_upper_limit = fields.Float(string='Upper Limit')


    # Target Fields
    f_target_type = fields.Selection([('quantity', 'Quantity'), ('amount', 'Amount')], default='amount', required=True, string='Target Type', tracking=True)
    f_target = fields.Float(string='Target', tracking=True)
    f_entry_point = fields.Float(string='Entry Point', tracking=True)

    # Tier Fields
    f_tier_from = fields.Float(string='Tier From')
    f_tier_to = fields.Float(string='Tier To')

    # Product Based Fields
    f_product = fields.Many2many(comodel_name='product.template', relation='f_commission_setup_product_rel', string='Product Name', tracking=True)
    f_product_family = fields.Many2many(comodel_name='f.product.family', relation='f_commission_setup_product_family_rel', string='Product Family', tracking=True)
    f_product_identity = fields.Many2many(comodel_name='f.prod.identity', relation='f_commission_setup_product_identity_rel', string='Product Identity', tracking=True)

    # Sales Fields
    f_product_family_exc = fields.Many2many(comodel_name='f.product.family', relation='f_commission_setup_product_family_exc_rel', string='Exclude Families', tracking=True)
    f_product_exc = fields.Many2many(comodel_name='product.template', relation='f_commission_setup_product_exc_rel', string='Exclude Products', tracking=True)
    f_product_identity_exc = fields.Many2many(comodel_name='f.prod.identity', relation='f_commission_setup_product_identity_exc_rel', string='Exclude Identities', tracking=True)

    # Sales & Product Based Fields
    f_sales_period_id = fields.Many2one('f.commission.period', string='Period', tracking=True)
    f_total_sales = fields.Float(string='Total Sales', store=True)
    f_net_sales = fields.Float(string='Net Sales', store=True)
    f_sales_perc = fields.Float(string='Sales%', store=True)

    # Collection Fields
    f_total_sp_collection = fields.Float()
    f_total_sp_db = fields.Float()
    f_total_sp_cr = fields.Float()
    f_collection_type = fields.Many2one('f.collection.type', string='Collection Type')
    f_is_bad_debt = fields.Boolean(string='Bad Debt', default=False)
    f_bad_debt_matrix = fields.Many2one('f.aged.balance.matrix', string='Bad Debt Matrix')
    f_excluded_amount = fields.Float(string='Exclude Amount', default=0)
    f_included_amount = fields.Float(string='Include Amount', default=0)
    f_collection_adjustment_id = fields.One2many('f.collections.adjustment', 'f_commission_setup_id', string='Collection Adjustment')

    def f_get_setup_adjustment(self):
        return {
                'name': 'Setup Adjustment',
                'view_mode': 'tree',
                'res_model': 'f.collections.adjustment',
                'type': 'ir.actions.act_window',
                'view_type': 'tree',
                'view_id': self.env.ref('f_commission_management.f_collections_adjustment_tree_view').id,
                'domain': [('f_commission_setup_id', '=', self.id)],
                'target': 'current',
            }


    def get_total_sales(self):
        records = self
        if not records:
            records = self.env['f.commission.management'].sudo().search([])

        print("Commission Records", records)
        for record in records:
            record.f_total_sales = 0
            record.f_net_sales = 0
            record.f_sales_perc = 0
            if not record.f_is_calculated:
                if not record.f_sales_period_id:
                    raise ValidationError(_("Please Select Period For Sales"))
                if record.f_commission_type == 'sales':
                    sales_person_ids = tuple(record.f_commission_role_ids.f_sales_persons.ids) if record.f_commission_role_ids.f_sales_persons.ids else (-1,)
                    if len(sales_person_ids) == 1:
                        sales_person_condition = f"= {sales_person_ids[0]}"
                    else:
                        sales_person_condition = f"IN {sales_person_ids}"
                    query = (f"""
                        SELECT
                            m.invoice_user_id AS sales_person,
                            SUM(case when am.price_subtotal != 0 then ((am.balance*-1)/am.price_subtotal)*am.price_total else 0 end) AS total_price,
                            SUM(
                                CASE
                                    WHEN pt.id NOT IN (
                                        SELECT exc_prod.product_template_id
                                        FROM f_commission_setup fcs
                                        JOIN f_commission_setup_product_exc_rel exc_prod ON exc_prod.f_commission_setup_id = fcs.id
                                        WHERE fcs.id = %s
                                    )
                                    AND pt.f_product_family NOT IN (
                                        SELECT exc_family.f_product_family_id
                                        FROM f_commission_setup fcs
                                        JOIN f_commission_setup_product_family_exc_rel exc_family ON exc_family.f_commission_setup_id = fcs.id
                                        WHERE fcs.id = %s
                                    )
                                    AND pt.fprodidentity NOT IN (
                                        SELECT exc_identity.f_prod_identity_id
                                        FROM f_commission_setup fcs
                                        JOIN f_commission_setup_product_identity_exc_rel exc_identity ON exc_identity.f_commission_setup_id = fcs.id
                                        WHERE fcs.id = %s
                                    ) 

                                    THEN case when am.price_subtotal != 0 then ((am.balance*-1)/am.price_subtotal)*am.price_total else 0 end
                                    ELSE 0
                                END
                            ) AS total_price_without_exclusions
                        FROM
                            account_move_line am
                        JOIN
                            account_move m ON am.move_id = m.id
                        JOIN
                            f_commission_period p ON p.id = %s
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
                        GROUP BY
                            m.invoice_user_id
                        ORDER BY
                            m.invoice_user_id

                    """ % (record.id, record.id, record.id, record.f_sales_period_id.id))
                    print("/////////////////////////// query: ", query)
                    self.env.cr.execute(query)
                    result = self.env.cr.fetchall()
                    if result:
                        record.f_total_sales = sum(row[1] for row in result)
                        record.f_net_sales = sum(row[2] for row in result)
                        if record.f_target > 0:
                            record.f_sales_perc = (record.f_net_sales / record.f_target) * 100
                            print("Target Perc", record.f_sales_perc)

                elif record.f_commission_type == 'product_based':
                    sales_person_ids = tuple(
                        record.f_commission_role_ids.f_sales_persons.ids) if record.f_commission_role_ids.f_sales_persons.ids else (
                    -1,)
                    if len(sales_person_ids) == 1:
                        sales_person_condition = f"= {sales_person_ids[0]}"
                    else:
                        sales_person_condition = f"IN {sales_person_ids}"
                    query = (f"""
                        SELECT
                            m.invoice_user_id AS sales_person,
                            SUM(case when am.price_subtotal != 0 then ((am.balance*-1)/am.price_subtotal)*am.price_total else 0 end) AS total_price,
                            SUM(
                                CASE
                                    WHEN pt.id IN (
                                        SELECT prod.product_template_id
                                        FROM f_commission_setup fcs
                                        JOIN f_commission_setup_product_rel prod ON prod.f_commission_setup_id = fcs.id
                                        WHERE fcs.id = %s
                                    )
                                    OR pt.f_product_family IN (
                                        SELECT family.f_product_family_id
                                        FROM f_commission_setup fcs
                                        JOIN f_commission_setup_product_family_rel family ON family.f_commission_setup_id = fcs.id
                                        WHERE fcs.id = %s
                                    )
                                    OR pt.fprodidentity IN (
                                        SELECT identity.f_prod_identity_id
                                        FROM f_commission_setup fcs
                                        JOIN f_commission_setup_product_identity_rel identity ON identity.f_commission_setup_id = fcs.id
                                        WHERE fcs.id = %s
                                    ) 

                                    THEN case when am.price_subtotal != 0 then ((am.balance*-1)/am.price_subtotal)*am.price_total else 0 end
                                    ELSE 0
                                END
                            ) AS total_price_with_inclusions
                        FROM
                            account_move_line am
                        JOIN
                            account_move m ON am.move_id = m.id
                        JOIN
                            f_commission_period p ON p.id = %s
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
                        GROUP BY
                            m.invoice_user_id
                        ORDER BY
                            m.invoice_user_id

                    """ % (record.id, record.id, record.id, record.f_sales_period_id.id))
                    print("/////////////////////////// query: ", query)
                    self.env.cr.execute(query)
                    result = self.env.cr.fetchall()
                    if result:
                        record.f_total_sales = sum(row[1] for row in result)
                        record.f_net_sales = sum(row[2] for row in result)
                        if record.f_target > 0:
                            record.f_sales_perc = (record.f_net_sales / record.f_target) * 100
                            print("Target Perc", record.f_sales_perc)

    @api.onchange('f_is_calculated')
    def calc_on_change(self):
        # add warning that the the values will be empty
        if self.f_is_calculated == False:
            self.f_calculated_by = False
            self.f_comment = ' '
            self.f_comm_calc_id = False
            self.f_comm_calc_id.f_comments = False