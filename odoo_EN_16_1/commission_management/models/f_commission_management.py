from odoo import models, fields, api,_




class FCommissionManagement(models.Model):
    _name ='f.commission.management'
    _inherit = ['mail.thread','mail.activity.mixin']
    _rec_name = "f_description"
    #Basic Fields 
    
    f_commission_type = fields.Selection([('sales','Sales'),('product_based','Product Based'),('collection','Collection')], default = 'sales', required = True, string = 'Commission Type',copy = True, tracking=True)
    f_description = fields.Char(string = "Description",copy = True,tracking=True)
    f_period = fields.Many2one(comodel_name ='f.comisson.period', string = 'Period',domain="[('f_colsed', '=', False)]", required = True,copy = True,tracking=True)
    f_sales_person = fields.Many2one('res.users', 'Sales Person', required = True,copy = True,tracking=True)
    f_target_type = fields.Selection([('quantity','Quantity'),('amount','Amount')],default = 'amount',required = True,string = 'Target Type',tracking=True)
    f_target = fields.Float(string = 'Target',tracking=True)
    f_entry_point = fields.Float(string ='Entry Point',tracking=True)
    f_comm_value_type = fields.Selection([('camount','Amount'),('cpercentage','%')],default = 'camount', required = True, string = 'Commission Value Type',tracking=True)
    f_comm_value = fields.Float(string ='Commission Value',tracking=True)
    # f_comm_value_percent = fields.Float(string ='Commission Value')
    
        
    # product Based  commission fields
    f_product = fields.Many2many(comodel_name ='product.template', relation='f_commission_management_product_rel', string = 'Product Name',tracking=True)
    f_product_exc = fields.Many2many(comodel_name ='product.template', relation='f_commission_management_product_exc_rel', string = 'Exclude Products',tracking=True)
    f_product_family = fields.Many2many(comodel_name = 'f.product.family', relation='f_commission_management_product_family_rel', string = 'Product Family',tracking=True)
    f_product_family_exc = fields.Many2many(comodel_name = 'f.product.family', relation='f_commission_management_product_family_exc_rel', string = 'Exclude Families',tracking=True)
    f_product_identity = fields.Many2many(comodel_name ='f.prod.identity', relation='f_commission_management_product_identity_rel', string = 'Product Identity',tracking=True)
    f_product_identity_exc = fields.Many2many(comodel_name ='f.prod.identity', relation='f_commission_management_product_identity_exc_rel', string = 'Exclude Identities',tracking=True)

    #Commission Calculation results 
    f_is_calculated = fields.Boolean(string = 'Calculated',copy = False,tracking=True, store=True)
    f_commission_amount = fields.Float(string = "Commission Amount",copy = False,tracking=True)
    f_calculated_by = fields.Integer(string = "Calculated By",copy = False,tracking=True)
    f_commission_calculated_at =  fields.Datetime(string='Calculated At', readonly=True,tracking=True)
    f_comment= fields.Char(string = 'Comment',copy = False,tracking=True)
    f_comm_calc_id =fields.Many2one(comodel_name='f.commission.calculation',string = 'Calculation Id',copy = False,tracking=True)
    
    
    #calculation temp fields 
    f_total_whole_sp_colletion = fields.Float()
    f_total_retail_sp_colletion = fields.Float()
    f_total_sp_db = fields.Float()
    f_total_sp_cr = fields.Float()

    #calculation progress fields
    f_total_sales = fields.Float(string='Total Sales', store=True)
    f_net_sales = fields.Float(string='Net Sales', store=True)
    f_sales_perc = fields.Float(string='Sales%', store=True)

    #exclude payments & include stock move fields
    f_whole_excluded_amount = fields.Float(string='Exclude Whole Amount', default=-1)
    f_retail_excluded_amount = fields.Float(string='Exclude Retail Amount', default=-1)
    f_whole_included_amount = fields.Float(string='Include Whole Amount', default=-1)
    f_retail_included_amount = fields.Float(string='Include Retail Amount', default=-1)

    def f_compute_exclude_amount(self):
        sp_collections = self.env['account.payment'].read_group(
            domain=[('invoice_user_id', '=', self.f_sales_person.id),
                    ('date', '>=', self.f_period.f_from),
                    ('date', '<=', self.f_period.f_to),
                    ('state', '=', 'posted'),
                    ('payment_type', '=', 'inbound'),
                    ('f_cust_type', 'in', ('whole', 'retail')),
                    ('f_commission_exclude', '=', True),
                    ],
            fields=['f_cust_type', 'amount_total_signed', 'invoice_user_id'],
            groupby=['f_cust_type'], lazy=False)

        for col in sp_collections:
            if col['f_cust_type'] == 'whole' and self.f_whole_excluded_amount < 0:
                self.f_whole_excluded_amount = col['amount_total_signed']
            if col['f_cust_type'] == 'retail' and self.f_retail_excluded_amount < 0:
                self.f_retail_excluded_amount = col['amount_total_signed']

    def f_compute_include_amount(self):
        sp_collections = self.env['account.move'].read_group(
            domain=[('f_sales_person', '=', self.f_sales_person.id),
                    ('f_period_id', '=', self.f_period.id),
                    ('state', '=', 'posted'),
                    ('f_cust_type', 'in', ('whole', 'retail')),
                    ('f_include_commission', '=', True),
                    ],
            fields=['f_cust_type', 'f_commission_amount'],
            groupby=['f_cust_type'], lazy=False)

        for col in sp_collections:
            if col['f_cust_type'] == 'whole' and self.f_whole_included_amount < 0:
                self.f_whole_included_amount = col['f_commission_amount']
            if col['f_cust_type'] == 'retail' and self.f_retail_included_amount < 0:
                self.f_retail_included_amount = col['f_commission_amount']


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
                if record.f_commission_type == 'sales':
                    query = (f"""
                        SELECT
                            am.f_sale_person AS sales_person,
                            SUM(case when am.price_subtotal != 0 then ((am.balance*-1)/am.price_subtotal)*am.price_total else 0 end) AS total_price,
                            SUM(
                                CASE
                                    WHEN am.f_product_tmpl NOT IN (
                                        SELECT exc_prod.product_template_id
                                        FROM f_commission_management fcm
                                        JOIN f_commission_management_product_exc_rel exc_prod ON exc_prod.f_commission_management_id = fcm.id
                                        WHERE fcm.id = %s
                                    )
                                    AND am.f_prod_family_id NOT IN (
                                        SELECT exc_family.f_product_family_id
                                        FROM f_commission_management fcm
                                        JOIN f_commission_management_product_family_exc_rel exc_family ON exc_family.f_commission_management_id = fcm.id
                                        WHERE fcm.id = %s
                                    )
                                    AND am.f_prod_identity_id NOT IN (
                                        SELECT exc_identity.f_prod_identity_id
                                        FROM f_commission_management fcm
                                        JOIN f_commission_management_product_identity_exc_rel exc_identity ON exc_identity.f_commission_management_id = fcm.id
                                        WHERE fcm.id = %s
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
                            f_comisson_period p ON p.id = %s
                        WHERE
                            am.f_sale_person = %s
                            AND m.invoice_date BETWEEN p.f_from AND p.f_to
                            AND m.state = 'posted'
                            AND m.move_type IN ('out_invoice','out_refund')
                            AND am.display_type = 'product'
                        GROUP BY
                            am.f_sale_person
                        ORDER BY
                            am.f_sale_person

                    """ % (record.id,record.id,record.id,record.f_period.id,record.f_sales_person.id))
                    print("/////////////////////////// query: ", query)
                    self.env.cr.execute(query)
                    result = self.env.cr.fetchall()

                    record.f_total_sales = result[0][1]
                    record.f_net_sales = result[0][2]
                    if record.f_target > 0:
                        record.f_sales_perc = (result[0][2] / record.f_target) * 100
                        print("Target Perc", record.f_sales_perc)

                elif record.f_commission_type == 'product_based':
                    query = (f"""
                        SELECT
                            am.f_sale_person AS sales_person,
                            SUM(case when am.price_subtotal != 0 then ((am.balance*-1)/am.price_subtotal)*am.price_total else 0 end) AS total_price,
                            SUM(
                                CASE
                                    WHEN am.f_product_tmpl IN (
                                        SELECT prod.product_template_id
                                        FROM f_commission_management fcm
                                        JOIN f_commission_management_product_rel prod ON prod.f_commission_management_id = fcm.id
                                        WHERE fcm.id = %s
                                    )
                                    OR am.f_prod_family_id IN (
                                        SELECT family.f_product_family_id
                                        FROM f_commission_management fcm
                                        JOIN f_commission_management_product_family_rel family ON family.f_commission_management_id = fcm.id
                                        WHERE fcm.id = %s
                                    )
                                    OR am.f_prod_identity_id IN (
                                        SELECT identity.f_prod_identity_id
                                        FROM f_commission_management fcm
                                        JOIN f_commission_management_product_identity_rel identity ON identity.f_commission_management_id = fcm.id
                                        WHERE fcm.id = %s
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
                            f_comisson_period p ON p.id = %s
                        WHERE
                            am.f_sale_person = %s
                            AND m.invoice_date BETWEEN p.f_from AND p.f_to
                            AND m.state = 'posted'
                            AND m.move_type IN ('out_invoice','out_refund')
                            AND am.display_type = 'product'
                        GROUP BY
                            am.f_sale_person
                        ORDER BY
                            am.f_sale_person

                    """ % (record.id,record.id,record.id,record.f_period.id, record.f_sales_person.id))
                    print("/////////////////////////// query: ", query)
                    self.env.cr.execute(query)
                    result = self.env.cr.fetchall()
                    record.f_total_sales = result[0][1]
                    record.f_net_sales = result[0][2]
                    if record.f_target > 0:
                        record.f_sales_perc = (result[0][2] / record.f_target) * 100
                        print("Target Perc", record.f_sales_perc)
    
    @api.onchange('f_is_calculated')
    def calc_on_change(self):
        # add warning that the the values will be empty 
        if self.f_is_calculated == False :
            
            self.f_commission_amount = 0
            self.f_calculated_by=False
            self.f_comment = ' '
            self.f_comm_calc_id = False
            self.f_comm_calc_id.f_comments = False 
    
        

    