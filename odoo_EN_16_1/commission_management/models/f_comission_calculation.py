from odoo import models, fields, api,_
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import logging

_logger = logging.getLogger(__name__)


class FCommissionCalculation(models.Model):
    _name = 'f.commission.calculation'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "f_comm_calc_name"

    f_comm_state = fields.Selection(
        [('draft', 'Draft'), ('cancel', 'Cancelled'), ('done', 'Done'), ('confirm', 'Confirmed')], default='draft',
        tracking=True, string='State')
    f_comm_calc_name = fields.Char('Name', required=True, tracking=True)
    f_cal_period = fields.Many2one(comodel_name='f.comisson.period', string='Period',
                                   domain="[('f_colsed', '=', False)]", tracking=True)
    f_commission_calculated_at = fields.Datetime(string='Calculated At', readonly=True, tracking=True)
    f_sales_persons = fields.Many2many('res.users', string='Sales Person', tracking=True)
    f_comments = fields.Html(string='Calculation Comments', tracking=True)

    def confirm_calculate(self):

        self.f_comm_state = 'confirm'

    def cancel_calculate(self):
        _logger.info('-------------------------------------------------------------------------')
        _logger.info('Commission Calculation -> Cancelled')
        comm_setups = self.env['f.commission.management'].search([('f_comm_calc_id', '=', self.id)])
        for comm in comm_setups:
            comm.f_is_calculated = False
            comm.f_commission_amount = 0
            comm.f_comment = ' '
            comm.f_calculated_by = False
            comm.f_comm_calc_id = False

        self.f_comm_state = 'cancel'
        self.f_comments = ' '

    def reset_to_draft(self):
        _logger.info('-------------------------------------------------------------------------')
        _logger.info('Commission Calculation -> Reset To Draft')
        comm_setups = self.env['f.commission.management'].search([('f_comm_calc_id', '=', self.id)])
        for comm in comm_setups:
            comm.f_is_calculated = False
            comm.f_commission_amount = 0
            comm.f_comment = ' '
            comm.f_calculated_by = False
            comm.f_comm_calc_id = False

        self.f_comm_state = 'draft'
        self.f_comments = ' '

    def _calc_comm(self, spset, sp_total_balance, sp_total_qty, type, log):
        _logger.info(_('*****start comm value calc for  Sales Person : %s for Type %s '), spset.f_sales_person.name,
                     type)
        f_commission_amount = 0
        f_comment = ' '
        if type == 'sales':
            entry_point = spset.f_entry_point * spset.f_target
            _logger.info(_('Entry Point for Sales Person : %s '), entry_point)
            f_comment = f_comment + '\n Entry Point for Sales Person = ' + str(entry_point)
            log.f_description = log.f_description + f'Entry Point: {entry_point} \n'
            if (sp_total_balance >= entry_point):

                if (spset.f_comm_value_type == 'camount'):
                    f_commission_amount = (sp_total_balance * spset.f_comm_value) / spset.f_target

                elif (spset.f_comm_value_type == 'cpercentage'):
                    f_commission_amount = (spset.f_comm_value / 100) * sp_total_balance
                _logger.info(_('commission amount for Sales Person : %s  wit commission type  %s  = %s'),
                             spset.f_sales_person.name, spset.f_comm_value_type, f_commission_amount)
                f_comment = f_comment + '\n commission amount for commission type' + spset.f_comm_value_type + ' = ' + str(
                    f_commission_amount)
                log.f_description = log.f_description + f'commission amount = {f_commission_amount}\n'
            else:
                f_commission_amount = 0.0
                f_comment = f_comment + '\n The sales person does not reach the entry point...'
                _logger.info(_('Sales Person : %s  not reach the entry point %s '), spset.f_sales_person.name,
                             entry_point)
                log.f_description = log.f_description + f'commission amount = {f_commission_amount}\n'

        else:
            if spset.f_target_type == 'amount':

                if (sp_total_balance >= spset.f_target):

                    if (spset.f_comm_value_type == 'camount'):
                        f_commission_amount = spset.f_comm_value

                    elif (spset.f_comm_value_type == 'cpercentage'):
                        f_commission_amount = spset.f_comm_value * sp_total_balance * 0.01
                    _logger.info(_('commission amount for Sales Person : %s  wit commission type  %s  = %s'),
                                 spset.f_sales_person.name, spset.f_comm_value_type, f_commission_amount)
                    f_comment = f_comment + '\n Commission amount for commission type' + spset.f_comm_value_type + ' = ' + str(
                        f_commission_amount)
                    log.f_description = log.f_description + f'commission amount = {f_commission_amount}\n'
                else:

                    f_commission_amount = 0.0
                    f_comment = f_comment + '\n The sales person does not reach the Target...'
                    _logger.info(_('Sales Person : %s  not reach the Target %s '), spset.f_sales_person.name,
                                 spset.f_target)
                    log.f_description = log.f_description + f'commission amount = {f_commission_amount}\n'


            elif spset.f_target_type == 'quantity':

                if (sp_total_qty >= spset.f_target):

                    if (spset.f_comm_value_type == 'camount'):
                        f_commission_amount = spset.f_comm_value

                    elif (spset.f_comm_value_type == 'cpercentage'):
                        f_commission_amount = spset.f_comm_value * sp_total_balance * 0.01
                    _logger.info(_('commission amount for Sales Person : %s  wit commission type  %s  = %s'),
                                 spset.f_sales_person.name, spset.f_comm_value_type, f_commission_amount)
                    f_comment = f_comment + '\n   Commission amount for  commission type ' + spset.f_comm_value_type + ' =' + str(
                        f_commission_amount)
                    log.f_description = log.f_description + f'commission amount = {f_commission_amount}\n'
                else:
                    f_commission_amount = 0.0
                    f_comment = f_comment + '\n The sales person does not reach the Target...'
                    _logger.info(_('Sales Person : %s  not reach the Target %s '), spset.f_sales_person.name,
                                 spset.f_target)
                    log.f_description = log.f_description + f'commission amount = {f_commission_amount}\n'

        #To Change it to set status not here at the end of the function
        self._set_comm_results(spset, True, f_commission_amount, f_comment, log)

    def _set_comm_results(self, spset, f_is_calculated, f_commission_amount, f_comment, log=False):
        for stp in spset:
            _logger.info(_('Set Commission Calculation  Result for %s with Values Comm_amount = %s comment = %s'),
                         spset.f_description, f_commission_amount, f_comment)
            stp.f_is_calculated = f_is_calculated
            stp.f_commission_amount = f_commission_amount
            stp.f_comment = f_comment
            stp.f_calculated_by = self.create_uid
            stp.f_comm_calc_id = self.id
            stp.f_commission_calculated_at = datetime.now()

    def _get_total_coll_comm(self, type, dbt_prc, total_collection, log):
        _logger.info(_('Start comm calc for collection  in function ->_get_total_coll_comm'))
        coll_rules = self.env['f.comm.collection.rules'].search([('f_customer_type', '=', type)])
        total_comm = 0
        comm_perc = 0

        #dbt_prc = dbt_prc / 100
        for col in coll_rules:

            if col.f_operator == 'between' and dbt_prc >= col.f_debit_from and dbt_prc <= col.f_debit_to:
                comm_perc = col.f_collection_com
            elif col.f_operator == 'less' and dbt_prc < col.f_debit_from:
                comm_perc = col.f_collection_com
            elif col.f_operator == 'great' and dbt_prc > col.f_debit_to:
                comm_perc = col.f_collection_com
            if not comm_perc:
                comm_perc = 0

        _logger.info(_('Commission Percentage based on the setup = %s'), comm_perc)
        log.f_description = log.f_description + f'Commission Percentage = {comm_perc}\n'
        total_comm = (total_collection / 1.16) * (comm_perc / 100)
        _logger.info(_('Total Commission Amount  = %s'), total_comm)

        return total_comm

    def calculate_commission(self):
        _logger.info('************* Start Commission Calculation **********************')
        _logger.info(_('************* for Sales Persons : %s'), self.f_sales_persons)

        f_comments = ' '
        self.f_comments = ' '
        if self.f_sales_persons:
            domain = [('f_period', '=', self.f_cal_period.id), ('f_sales_person', 'in', self.f_sales_persons.ids),
                      ('f_is_calculated', '=', False)]

        else:
            domain = [('f_period', '=', self.f_cal_period.id), ('f_is_calculated', '=', False)]

        whole_sale_setups = self.env['f.commission.management'].search(domain + [('f_commission_type', '=', 'sales')])
        product_based_setups = self.env['f.commission.management'].search(
            domain + [('f_commission_type', '=', 'product_based')])
        pidentity_based_setups = self.env['f.commission.management'].search(
            domain + [('f_commission_type', '=', 'product_based'), ('f_product_family', '=', False),
                      ('f_product', '=', False), ('f_product_identity', '!=', False)])
        family_based_setups = self.env['f.commission.management'].search(
            domain + [('f_commission_type', '=', 'product_based'), ('f_product_family', '!=', False),
                      ('f_product', '=', False)])
        collection_setups = self.env['f.commission.management'].search(
            [('f_period', '=', self.f_cal_period.id), ('f_is_calculated', '=', False),
             ('f_commission_type', '=', 'collection')])

        #****************************************************Sales Based *************************************************
        if whole_sale_setups:
            _logger.info(_('***** Start Calculation For sales setups: %s'), whole_sale_setups)
            sales_person_ids = tuple(self.f_sales_persons.ids) if self.f_sales_persons.ids else (-1,)
            if len(sales_person_ids) == 1:
                sales_person_condition = f"= {sales_person_ids[0]}"
            else:
                sales_person_condition = f"IN {sales_person_ids}"

            query = (f"""
                select f_sales_person,count(f_description)
                from f_commission_management
                where 
                    f_sales_person {sales_person_condition}
                    and f_period = %s
                    and (f_is_calculated = false or f_is_calculated is null)
                    and f_commission_type = 'sales'
                group by f_sales_person
            """ % (self.f_cal_period.id))
            self.env.cr.execute(query)
            result = self.env.cr.fetchall()

            has_count_greater_than_one = any(count > 1 for _, count in result)

            if has_count_greater_than_one:
                print("There is at least one salesperson with greater than 1 setups.")
                _logger.info(_('There is at least one salesperson with greater than 1 setups.'))
                for spset in whole_sale_setups:
                    vals = {
                        'f_commission_setup': spset.id,
                        'f_description': "There is at least one salesperson with greater than 1 setups.\n",
                        'f_date': fields.Datetime.now(),
                        'f_user': self.env.user.id,
                        'f_sale_person': spset.f_sales_person.id
                    }
                    log = self.env['f.calculation.logs'].create(vals)
            else:
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
                                    WHERE fcm.f_sales_person = am.f_sale_person
                                    AND fcm.f_period = %s
                                    AND (fcm.f_is_calculated = false or fcm.f_is_calculated is null)
                                    AND fcm.f_commission_type = 'sales'
                                )
                                AND am.f_prod_family_id NOT IN (
                                    SELECT exc_family.f_product_family_id
                                    FROM f_commission_management fcm
                                    JOIN f_commission_management_product_family_exc_rel exc_family ON exc_family.f_commission_management_id = fcm.id
                                    WHERE fcm.f_sales_person = am.f_sale_person
                                    AND fcm.f_period = %s
                                    AND (fcm.f_is_calculated = false or fcm.f_is_calculated is null)
                                    AND fcm.f_commission_type = 'sales'
                                )
                                AND am.f_prod_identity_id NOT IN (
                                    SELECT exc_identity.f_prod_identity_id
                                    FROM f_commission_management fcm
                                    JOIN f_commission_management_product_identity_exc_rel exc_identity ON exc_identity.f_commission_management_id = fcm.id
                                    WHERE fcm.f_sales_person = am.f_sale_person
                                    AND fcm.f_period = %s
                                    AND (fcm.f_is_calculated = false or fcm.f_is_calculated is null)
                                    AND fcm.f_commission_type = 'sales'
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
                        am.f_sale_person {sales_person_condition}
                        AND m.invoice_date BETWEEN p.f_from AND p.f_to
                        AND m.state = 'posted'
                        AND m.move_type IN ('out_invoice','out_refund')
                        AND am.display_type = 'product'
                    GROUP BY
                        am.f_sale_person
                    ORDER BY
                        am.f_sale_person

                """ % (
                self.f_cal_period.id, self.f_cal_period.id, self.f_cal_period.id, self.f_cal_period.id))
                print("/////////////////////////// query: ", query)
                self.env.cr.execute(query)
                result = self.env.cr.fetchall()

                print("/////////////////////////// query result: ", result)
                for res in result:
                    for spset in whole_sale_setups:
                        if spset.f_sales_person.id == res[0]:
                            if spset.f_comm_value_type == 'camount':
                                f_comm_value_type = 'Amount'
                            else:
                                f_comm_value_type = 'Percentage'
                            vals = {
                                'f_commission_setup': spset.id,
                                'f_description': f"Commission Type: Sales, Commission Value Type: {f_comm_value_type}\n",
                                'f_date': fields.Datetime.now(),
                                'f_user': self.env.user.id,
                                'f_sale_person': spset.f_sales_person.id
                            }
                            log = self.env['f.calculation.logs'].create(vals)
                            _logger.info(_('*****Total Sales For Sales Person : %s = %s'), spset.f_sales_person.name,
                                         res[2])
                            log.f_description = log.f_description + f'Total Sales = {res[2]}\n'
                            self._calc_comm(spset, res[2], 0, 'sales', log)
                            # f_comments = f_comments + '\n No Sales For this Sales Persons in this Period'

        # ****************************************************Product Based *************************************************
        if product_based_setups:
            # Change it to product not product template
            _logger.info(_('***** Start Calculation For Product Based setups: %s'), product_based_setups)
            sales_person_ids = tuple(self.f_sales_persons.ids) if self.f_sales_persons.ids else (-1,)
            if len(sales_person_ids) == 1:
                sales_person_condition = f"= {sales_person_ids[0]}"
            else:
                sales_person_condition = f"IN {sales_person_ids}"
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
                                WHERE fcm.f_sales_person = am.f_sale_person
                                AND fcm.f_period = %s
                                AND (fcm.f_is_calculated = false or fcm.f_is_calculated is null)
                                AND fcm.f_commission_type = 'product_based'
                            )
                            OR am.f_prod_family_id IN (
                                SELECT family.f_product_family_id
                                FROM f_commission_management fcm
                                JOIN f_commission_management_product_family_rel family ON family.f_commission_management_id = fcm.id
                                WHERE fcm.f_sales_person = am.f_sale_person
                                AND fcm.f_period = %s
                                AND (fcm.f_is_calculated = false or fcm.f_is_calculated is null)
                                AND fcm.f_commission_type = 'product_based'
                            )
                            OR am.f_prod_identity_id IN (
                                SELECT identity.f_prod_identity_id
                                FROM f_commission_management fcm
                                JOIN f_commission_management_product_identity_rel identity ON identity.f_commission_management_id = fcm.id
                                WHERE fcm.f_sales_person = am.f_sale_person
                                AND fcm.f_period = %s
                                AND (fcm.f_is_calculated = false or fcm.f_is_calculated is null)
                                AND fcm.f_commission_type = 'product_based'
                            ) 

                            THEN case when am.price_subtotal != 0 then ((am.balance*-1)/am.price_subtotal)*am.price_total else 0 end
                            ELSE 0
                        END
                    ) AS total_price_with_inclusions,
                    SUM(
                        CASE
                            WHEN am.f_product_tmpl IN (
                                SELECT prod.product_template_id
                                FROM f_commission_management fcm
                                JOIN f_commission_management_product_rel prod ON prod.f_commission_management_id = fcm.id
                                WHERE fcm.f_sales_person = am.f_sale_person
                                AND fcm.f_period = %s
                                AND (fcm.f_is_calculated = false or fcm.f_is_calculated is null)
                                AND fcm.f_commission_type = 'product_based'
                            )
                            OR am.f_prod_family_id IN (
                                SELECT family.f_product_family_id
                                FROM f_commission_management fcm
                                JOIN f_commission_management_product_family_rel family ON family.f_commission_management_id = fcm.id
                                WHERE fcm.f_sales_person = am.f_sale_person
                                AND fcm.f_period = %s
                                AND (fcm.f_is_calculated = false or fcm.f_is_calculated is null)
                                AND fcm.f_commission_type = 'product_based'
                            )
                            OR am.f_prod_identity_id IN (
                                SELECT identity.f_prod_identity_id
                                FROM f_commission_management fcm
                                JOIN f_commission_management_product_identity_rel identity ON identity.f_commission_management_id = fcm.id
                                WHERE fcm.f_sales_person = am.f_sale_person
                                AND fcm.f_period = %s
                                AND (fcm.f_is_calculated = false or fcm.f_is_calculated is null)
                                AND fcm.f_commission_type = 'product_based'
                            ) 

                            THEN am.quantity
                            ELSE 0
                        END
                    ) AS quantity
                FROM
                    account_move_line am
                JOIN
                    account_move m ON am.move_id = m.id
                JOIN
                    f_comisson_period p ON p.id = %s
                WHERE
                    am.f_sale_person {sales_person_condition}
                    AND m.invoice_date BETWEEN p.f_from AND p.f_to
                    AND m.state = 'posted'
                    AND m.move_type IN ('out_invoice','out_refund')
                    AND am.display_type = 'product'
                GROUP BY
                    am.f_sale_person
                ORDER BY
                    am.f_sale_person

            """ % (self.f_cal_period.id, self.f_cal_period.id, self.f_cal_period.id, self.f_cal_period.id, self.f_cal_period.id, self.f_cal_period.id, self.f_cal_period.id))
            print("/////////////////////////// query: ", query)
            self.env.cr.execute(query)
            result = self.env.cr.fetchall()

            for res in result:
                for spset in product_based_setups:
                    if spset.f_sales_person.id == res[0]:
                        if spset.f_comm_value_type == 'camount':
                            f_comm_value_type = 'Amount'
                        else:
                            f_comm_value_type = 'Percentage'
                        vals = {
                            'f_commission_setup': spset.id,
                            'f_description': f"Commission Type: Product Based, Commission Value Type: {f_comm_value_type}, Target Type: {spset.f_target_type}\n",
                            'f_date': fields.Datetime.now(),
                            'f_user': self.env.user.id,
                            'f_sale_person': spset.f_sales_person.id
                        }
                        log = self.env['f.calculation.logs'].create(vals)
                        _logger.info(_('*****Total Sales For Sales Person : %s = %s'), spset.f_sales_person.name,
                                     res[2])
                        log.f_description = log.f_description + f'Total Sales = {res[2]}\n'
                        log.f_description = log.f_description + f'Total QTYs = {res[3]}\n'
                        self._calc_comm(spset, res[2], res[3], 'product_based', log)

            self.f_comments = self.f_comments + '\n Product  Based Calculation Process Done...'

        #****************************************************Product Family Based *************************************************
        # if family_based_setups:
        #     _logger.info(_('***** Start Calculation For Product Family Based setups: %s'), product_based_setups)
        #     sp_sales = self.env['account.move.line'].read_group(
        #         domain=[('f_sale_person', 'in', family_based_setups.f_sales_person.ids),
        #                 ('move_id.invoice_date', '>=', self.f_cal_period.f_from),
        #                 ('move_id.invoice_date', '<=', self.f_cal_period.f_to),
        #                 ('move_id.state', '=', 'posted'),
        #                 ('move_id.move_type', 'in', ('out_invoice', 'out_refund')),
        #                 ('f_prod_family_id', 'in', family_based_setups.f_product_family.ids),
        #                 ],
        #         fields=['f_sale_person', 'f_prod_family_id', 'balance', 'quantity'],
        #         groupby=['f_sale_person', 'f_prod_family_id'], lazy=False)
        #
        #     _logger.info(_('***** Product Family Based Sales: %s'), sp_sales)
        #     if sp_sales:
        #         for sp in sp_sales:
        #             sp_total_balance = sp['balance'] * -1
        #             sp_total_qty = sp['quantity']
        #             for spset in family_based_setups:
        #                 vals = {
        #                     'f_commission_setup': spset.id,
        #                     'f_description': f"start comm value calc for  Sales Person : {spset.f_sales_person.name} for setup {spset.f_description}\n",
        #                     'f_date': fields.Datetime.now(),
        #                     'f_user': self.env.user.id,
        #                     'f_sale_person': spset.f_sales_person.id
        #                 }
        #                 log = self.env['f.calculation.logs'].create(vals)
        #                 if spset.f_sales_person.id == sp['f_sale_person'][0] and sp['f_prod_family_id'][
        #                     0] in spset.f_product_family.ids:
        #                     _logger.info(
        #                         _('Total Sales from product Families %s For Sales Person : %s = %s'),
        #                         ', '.join(family.fprodfamily_name for family in spset.f_product_family),
        #                         sp['f_sale_person'][0],
        #                         sp_total_balance
        #                     )
        #                     log.f_description = log.f_description + f"Total Sales from product Families {', '.join(family.fprodfamily_name for family in spset.f_product_family)} For Sales Person : {sp['f_sale_person'][0]} = {sp_total_balance}\n"
        #                     #f_comments = f_comments + '\n Total Sales from  product Family '+spset.f_product_family.fprodfamily_name+' = ' +  str(sp_total_balance)
        #                     self._calc_comm(spset, sp_total_balance, sp_total_qty, 'family_based', log)
        #                 elif not spset.f_is_calculated:
        #                     self._set_comm_results(spset, True, 0, 'No Sales For this Setup..')
        #                     _logger.info(
        #                         _('No Sales from product Families: %s For this For Sales Person : %s'),
        #                         ', '.join(family.fprodfamily_name for family in spset.f_product_family),
        #                         spset.f_sales_person.id
        #                     )
        #                     log.f_description = log.f_description + f"No Sales from product Families: {', '.join(family.fprodfamily_name for family in spset.f_product_family)} For this For Sales Person : {spset.f_sales_person.id}\n"
        #                     #f_comments = f_comments + '\n No Sales from  product Family '+spset.f_product_family.fprodfamily_name
        #
        #     else:
        #         self._set_comm_results(family_based_setups, True, 0, 'No Sales For this Setup..')
        #         _logger.info(_('No Sales for product Family: %s For this For Sales Persons : %s for Period %s'),
        #                      family_based_setups.f_product_family.ids, family_based_setups.f_sales_person.ids,
        #                      self.f_cal_period.f_name)
        #
        #     self.f_comments = self.f_comments + '\n Family Based Calculation Process Done...'
        #
        # #****************************************************Product Identity Based *************************************************
        # if pidentity_based_setups:
        #     _logger.info(_('***** Start Calculation For Product Identity Based setups: %s'), pidentity_based_setups)
        #     sp_sales = self.env['account.move.line'].read_group(
        #         domain=[('f_sale_person', 'in', pidentity_based_setups.f_sales_person.ids),
        #                 ('move_id.invoice_date', '>=', self.f_cal_period.f_from),
        #                 ('move_id.invoice_date', '<=', self.f_cal_period.f_to),
        #                 ('move_id.state', '=', 'posted'),
        #                 ('move_id.move_type', 'in', ('out_invoice', 'out_refund')),
        #                 ('f_prod_identity_id', 'in', pidentity_based_setups.f_product_identity.ids),
        #                 ],
        #         fields=['f_sale_person', 'f_prod_identity_id', 'balance', 'quantity'],
        #         groupby=['f_sale_person', 'f_prod_identity_id'], lazy=False)
        #
        #     _logger.info(_('***** Product Identity Based Sales: %s'), sp_sales)
        #     if sp_sales:
        #         for sp in sp_sales:
        #             sp_total_balance = sp['balance'] * -1
        #             sp_total_qty = sp['quantity']
        #             for spset in pidentity_based_setups:
        #                 vals = {
        #                     'f_commission_setup': spset.id,
        #                     'f_description': f"start comm value calc for  Sales Person : {spset.f_sales_person.name} for setup {spset.f_description}\n",
        #                     'f_date': fields.Datetime.now(),
        #                     'f_user': self.env.user.id,
        #                     'f_sale_person': spset.f_sales_person.id
        #                 }
        #                 log = self.env['f.calculation.logs'].create(vals)
        #                 if spset.f_sales_person.id == sp['f_sale_person'][0] and sp['f_prod_identity_id'][
        #                     0] in spset.f_product_identity.ids:
        #                     _logger.info(
        #                         _('Total Sales from product Identities %s For Sales Person : %s = %s with qty = %s'),
        #                         ', '.join(identity.fprodidentity_name for identity in spset.f_product_identity),
        #                         sp['f_sale_person'][0],
        #                         sp_total_balance,
        #                         sp_total_qty
        #                     )
        #                     log.f_description = log.f_description + f"Total Sales from product Identities {', '.join(identity.fprodidentity_name for identity in spset.f_product_identity)} For Sales Person : {sp['f_sale_person'][0]} = {sp_total_balance} with qty = {sp_total_qty}\n"
        #                     #f_comments = f_comments + '\n Total Sales from  product Identity ' + spset.f_product_identity.fprodidentity_name +' = '+ sp_total_balance +' Qty =  '+str(sp_total_qty)
        #                     self._calc_comm(spset, sp_total_balance, sp_total_qty, 'identity_based', log)
        #                 elif not spset.f_is_calculated:
        #                     self._set_comm_results(spset, True, 0, 'No Sales For this Setup..')
        #                     _logger.info(
        #                         _('No Sales from product Identities: %s For this For Sales Person : %s'),
        #                         ', '.join(identity.fprodidentity_name for identity in spset.f_product_identity),
        #                         spset.f_sales_person.id
        #                     )
        #                     log.f_description = log.f_description + f"No Sales from product Identities: {', '.join(identity.fprodidentity_name for identity in spset.f_product_identity)} For this For Sales Person : {spset.f_sales_person.id}\n"
        #                     #f_comments = f_comments + '\n No Sales from product Identity'+spset.f_product_identity.fprodidentity_name
        #     else:
        #         self._set_comm_results(pidentity_based_setups, True, 0, 'No Sales For this Setup..')
        #         _logger.info(_('No Sales for product Identity : %s For this For Sales Persons : %s for Period %s'),
        #                      pidentity_based_setups.f_product_identity.ids, pidentity_based_setups.f_sales_person.ids,
        #                      self.f_cal_period.f_name)
        #
        #     self.f_comments = self.f_comments + '\n Product Identity Based Calculation Process Done...'

        #****************************************************Collection Based ************************************************* 
        if collection_setups:

            _logger.info(_('***** Start Calculation For Collection Based setups: %s'), collection_setups)
            #Get All Payments for the Sales Persons in this Period
            sp_collections = self.env['account.payment'].read_group(
                domain=[('invoice_user_id', 'in', collection_setups.f_sales_person.ids),
                        ('date', '>=', self.f_cal_period.f_from),
                        ('date', '<=', self.f_cal_period.f_to),
                        ('state', '=', 'posted'),
                        ('payment_type', '=', 'inbound'),
                        ('f_cust_type', 'in', ('whole', 'retail')),
                        ],
                fields=['f_cust_type', 'amount_total_signed', 'invoice_user_id'],
                groupby=['invoice_user_id', 'f_cust_type'], lazy=False)

            _logger.info(_('Payments in this Period: %s'), sp_collections)

            #Get The returned Checks to deduct them from the total payments 
            sp_ret_checks = self.env['account.payment'].read_group(domain=
                                                                   ['&', '&', '&', '&', '&', '&', '&',
                                                                    ('return_date', '>=', self.f_cal_period.f_from),
                                                                    ('return_date', '<=', self.f_cal_period.f_to),
                                                                    ('invoice_user_id', 'in',
                                                                     collection_setups.f_sales_person.ids),
                                                                    ('state', '=', 'posted'),
                                                                    ('payment_type', '=', 'inbound'),
                                                                    ('f_cust_type', 'in', ('whole', 'retail')),
                                                                    ('check_state', '=', 'returned'),

                                                                    '|', '&',
                                                                    ('bounce_date', '>=', self.f_cal_period.f_from),
                                                                    ('bounce_date', '<=', self.f_cal_period.f_to),

                                                                    ('bounce_date', '=', False),
                                                                    ],
                                                                   fields=['f_cust_type', 'amount_total_signed',
                                                                           'invoice_user_id'],
                                                                   groupby=['invoice_user_id', 'f_cust_type'],
                                                                   lazy=False)
            _logger.info(_('Returned Checks this Period: %s'), sp_ret_checks)

            #Get The bounced Checks to deduct them from the total payments 
            sp_bounced_checks = self.env['account.payment'].read_group(
                domain=[('invoice_user_id', 'in', collection_setups.f_sales_person.ids),
                        ('bounce_date', '>=', self.f_cal_period.f_from),
                        ('bounce_date', '<=', self.f_cal_period.f_to),
                        ('state', '=', 'posted'),
                        ('payment_type', '=', 'inbound'),
                        ('f_cust_type', 'in', ('whole', 'retail')),
                        ('check_state', '=', 'bounced'),
                        ],
                fields=['f_cust_type', 'amount_total_signed', 'invoice_user_id'],
                groupby=['invoice_user_id', 'f_cust_type'], lazy=False)

            _logger.info(_('Bounced Checks this Period: %s'), sp_bounced_checks)

            #             #get aged debit from account_move_linemore than 60 days whole , retail
            #             sp_debts = self.env['account.move.line'].read_group(domain = [('f_sale_person', 'in', collection_setups.f_sales_person.ids),
            #                                                                           ('date', '<=', self.f_cal_period.f_to - relativedelta(days = 61)),
            #                                                                           ('move_id.state', '=', 'posted'),
            #                                                                           ('account_id.internal_type','=','receivable'),
            #                                                                           ('f_cust_type','in',('whole','retail')),
            #                                                                           # ('move_id.move_type','in',('out_invoice','out_refund')),
            #                                                                           ('f_bad_debt','=',False),
            #                                                                           ],
            #                                                                 fields=['debit','f_sale_person','partner_id'],
            #                                                                 groupby=['f_sale_person','partner_id'],lazy=False)
            #
            #
            #             _logger.info(_('Total Aged debit %s'),sp_debts )
            #             sp_credits = self.env['account.move.line'].read_group(domain = [('f_sale_person', 'in', collection_setups.f_sales_person.ids),
            #
            #                                                                           ('date', '>=', self.f_cal_period.f_to - relativedelta(days = 61)),
            #                                                                           ('move_id.state', '=', 'posted'),
            #                                                                           ('account_id.internal_type','=','receivable'),
            #                                                                           ('f_cust_type','in',('whole','retail')),
            #                                                                            #('move_id.move_type','in',('out_invoice','out_refund')),
            #                                                                          ],
            #                                                                 fields  = ['credit','f_sale_person','partner_id'],
            #                                                                 groupby = ['f_sale_person','partner_id'],lazy=False)
            #
            #
            #             _logger.info(_('Total Aged Credit %s'),sp_credits )
            # #
            #
            #             partner_balance = 0
            #             balance = 0
            #             sp_aged_balance = []
            #
            #             for db in sp_debts:
            #                 for cr in sp_credits:
            #                     if db['f_sale_person'][0] == cr['f_sale_person'][0]:
            #
            #                         sp_aged_balance.append({'f_sale_person': db['f_sale_person'][0],'balance':0})
            #                         if db['partner_id'][0] == cr['partner_id'][0]:
            #
            #                             balance = cr['credit'] - db['debit']
            #                             if balance >0 :
            #                                 partner_balance += balance
            #                             else :
            #                                 balance =0
            #                             sp_aged_balance[db['f_sale_person'][0]] = partner_balance
            #
            #
            #             _logger.info(_('Total Sales person balance  %s '),sp_aged_balance )
            #

            #Calculate the Percentage for the debit vs collection 
            for sp in collection_setups:
                f_commission_amount = 0
                sp.f_total_whole_sp_colletion = 0
                sp.f_total_retail_sp_colletion = 0
                sp.f_total_sp_db = 0
                sp.f_total_sp_cr = 0

                for col in sp_collections:
                    if col['invoice_user_id'][0] == sp.f_sales_person.id:
                        vals = {
                            'f_commission_setup': sp.id,
                            'f_description': "Commission Type: Collection\n",
                            'f_date': fields.Datetime.now(),
                            'f_user': self.env.user.id,
                            'f_sale_person': sp.f_sales_person.id
                        }
                        log = self.env['f.calculation.logs'].create(vals)
                        f_comment_coll = ' '
                        _logger.info(_('Start Calculation For Sales Person  %s'), sp.f_sales_person.name)
                        f_comment_coll = f_comment_coll + 'Start Calculation'

                        if col['f_cust_type'] == 'whole':

                            sp.f_total_whole_sp_colletion = col['amount_total_signed']
                            _logger.info(_('Total Whole Sales Collection For Sales Person  %s = %s'),
                                         sp.f_sales_person.name, sp.f_total_whole_sp_colletion)
                            f_comment_coll = f_comment_coll + '\n Whole Sales Col  ' + str(
                                sp.f_total_whole_sp_colletion)
                            log.f_description = log.f_description + f"Whole Sales = {sp.f_total_whole_sp_colletion}\n"
                            for retcheck in sp_ret_checks:
                                if retcheck['invoice_user_id'][0] == sp.f_sales_person.id and retcheck[
                                    'f_cust_type'] == 'whole':
                                    sp.f_total_whole_sp_colletion = sp.f_total_whole_sp_colletion - retcheck[
                                        'amount_total_signed']
                                    _logger.info(_('Total Whole Sales Returned Check For Sales Person  %s = %s'),
                                                 sp.f_sales_person.name, retcheck['amount_total_signed'])
                                    log.f_description = log.f_description + f"Total Whole Sales Returned Check = {retcheck['amount_total_signed']}\n"
                                    f_comment_coll = f_comment_coll + '\n Whole Sales Ret Checks   ' + str(
                                        retcheck['amount_total_signed'])
                            for bocheck in sp_bounced_checks:
                                if bocheck['invoice_user_id'][0] == sp.f_sales_person.id and retcheck[
                                    'f_cust_type'] == 'whole':
                                    sp.f_total_whole_sp_colletion = sp.f_total_whole_sp_colletion - bocheck[
                                        'amount_total_signed']
                                    _logger.info(_('Total Whole Sales Bounced Check For Sales Person  %s = %s'),
                                                 sp.f_sales_person.name, bocheck['amount_total_signed'])
                                    f_comment_coll = f_comment_coll + '\n Whole Sales BNC Checks ' + str(
                                        bocheck['amount_total_signed'])
                                    log.f_description = log.f_description + f"Total Whole Sales Bounced Check = {bocheck['amount_total_signed']}\n"
                            _logger.info(_('Total Whole Sales Collections For Sales Person  %s = %s'),
                                         sp.f_sales_person.name, sp.f_total_whole_sp_colletion)
                            f_comment_coll = f_comment_coll + '\nNet Whole Sales Coll = ' + str(
                                sp.f_total_whole_sp_colletion)
                            log.f_description = log.f_description + f"Total Whole Sales = {sp.f_total_whole_sp_colletion}\n"

                        if col['f_cust_type'] == 'retail':
                            sp.f_total_retail_sp_colletion = col['amount_total_signed']
                            _logger.info(_('Total Retail Collection For Sales Person  %s = %s'), sp.f_sales_person.name,
                                         sp.f_total_retail_sp_colletion)
                            f_comment_coll = f_comment_coll + '\n Retail Coll ' + str(sp.f_total_retail_sp_colletion)
                            log.f_description = log.f_description + f"Retail Sales = {sp.f_total_retail_sp_colletion}\n"
                            for retcheck in sp_ret_checks:
                                if retcheck['invoice_user_id'][0] == sp.f_sales_person.id and retcheck[
                                    'f_cust_type'] == 'retail':
                                    sp.f_total_retail_sp_colletion = sp.f_total_retail_sp_colletion - retcheck[
                                        'amount_total_signed']
                                    _logger.info(_('Total Retail Returned Check For Sales Person  %s = %s'),
                                                 sp.f_sales_person.name, retcheck['amount_total_signed'])
                                    f_comment_coll = f_comment_coll + '\n Retail Ret Checks =' + str(
                                        retcheck['amount_total_signed'])
                                    log.f_description = log.f_description + f"Total Retail Returned Check = {retcheck['amount_total_signed']}\n"
                            for bocheck in sp_bounced_checks:
                                if bocheck['invoice_user_id'][0] == sp.f_sales_person.id and retcheck[
                                    'f_cust_type'] == 'retail':
                                    sp.f_total_retail_sp_colletion = sp.f_total_retail_sp_colletion - bocheck[
                                        'amount_total_signed']
                                    _logger.info(_('Total Retail Bounced Check For Sales Person  %s = %s'),
                                                 sp.f_sales_person.name, bocheck['amount_total_signed'])
                                    f_comment_coll = f_comment_coll + '\n Retail BNC Checks =' + str(
                                        bocheck['amount_total_signed'])
                                    log.f_description = log.f_description + f"Total Retail Bounced Check = {bocheck['amount_total_signed']}\n"
                            _logger.info(_('Total Retail Collections For Sales Person  %s = %s'),
                                         sp.f_sales_person.name, sp.f_total_retail_sp_colletion)
                            f_comment_coll = f_comment_coll + '\n Net Retail Col = ' + str(
                                sp.f_total_retail_sp_colletion)
                            log.f_description = log.f_description + f"Total Retail Sales = {sp.f_total_retail_sp_colletion}\n"
                        sp.f_comment = f_comment_coll
                _logger.info(_('Start Calculating the Old Debit Percentage For Sales Person  %s '),
                             sp.f_sales_person.name)
                f_comments = f_comments + sp.f_comment
                f_comments = f_comments + '\n Old Debit %'

                #
                #                 for db in sp_debts:
                #                     if db['f_sale_person'][0] == sp.f_sales_person.id :
                #                         sp.f_total_sp_db = db['debit']
                #                         _logger.info(_('Total Debits > 60 days   %s '),db['debit'] )
                #
                #
                #
                #                 for cr in sp_credits:
                #                     if cr['f_sale_person'][0] == sp.f_sales_person.id :
                #                         sp.f_total_sp_cr = cr['credit']
                #                         _logger.info(_('Total Credits =  %s'),cr['credit'] )

                #                 for spb in sp_aged_balance:
                #                     if spb['f_sale_person'] == sp.f_sales_person.id :
                #                         sp.f_total_sp_cr = spb['balance']
                #                         _logger.info(_('Total balance =  %s'),spb['balance'] )
                #
                #

                self.env.cr.execute("""
                    select user_id, sum(xbalance)as total_balance from (
                        select user_id , partner_id, xbalance
                        from (
                            select am.invoice_user_id as user_id, p.id as partner_id,
                            sum(
                                CASE WHEN am.move_type = 'out_invoice' and am.invoice_date_due <  DATE('%s') THEN COALESCE(aml.debit,0) 
                                WHEN am.move_type != 'out_invoice' and am.date <  DATE('%s') THEN COALESCE(aml.debit,0)
                                ELSE 0 
                            END) - 
                            sum(
                                CASE WHEN am.move_type = 'out_invoice' and am.invoice_date_due <  DATE('%s') THEN COALESCE(aml.credit,0) 
                                WHEN am.move_type != 'out_invoice' and am.date <  DATE('%s') THEN COALESCE(aml.credit,0)
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
                            AND AML.f_cust_type in ('whole','retail')
                            AND p.id = aml.partner_id
                            and (p.f_bad_debt = False or p.f_bad_debt is NULL)
                            group by am.invoice_user_id,p.id
                        ) s1 
                    ) s2 
                    where xbalance>0
                    and user_id =%s
                    group by user_id
                               
                """ % (
                self.f_cal_period.f_from, self.f_cal_period.f_from, self.f_cal_period.f_from, self.f_cal_period.f_from,
                sp.f_sales_person.id))

                balance = 0
                result = self.env.cr.fetchone()
                if result:
                    balance = result[1] or 0

                _logger.info(_('Total Balance = %s %s'), balance, result)
                log.f_description = log.f_description + f"Total Balance = {balance}\n"

                f_comments = f_comments + '\n Total Balance = ' + str(balance)

                sp.f_compute_exclude_amount()
                sp.f_compute_include_amount()

                f_whole_excluded_amount = sp.f_whole_excluded_amount
                f_retail_excluded_amount = sp.f_retail_excluded_amount
                f_whole_included_amount = sp.f_whole_included_amount
                f_retail_included_amount = sp.f_retail_included_amount

                if f_whole_excluded_amount < 0:
                    f_whole_excluded_amount = 0
                if f_retail_excluded_amount < 0:
                    f_retail_excluded_amount = 0

                if f_whole_included_amount < 0:
                    f_whole_included_amount = 0
                if f_retail_included_amount < 0:
                    f_retail_included_amount = 0

                total_collection = sp.f_total_whole_sp_colletion + sp.f_total_retail_sp_colletion
                _logger.info(_('Total Collection for Sales Person in this Period  = %s before exclude & include'),
                             total_collection)
                log.f_description = log.f_description + f"Total Sales = {total_collection}\n"
                excluded_collection = f_whole_excluded_amount + f_retail_excluded_amount
                _logger.info(_('Total excluded Collection for Sales Person in this Period  = %s'), excluded_collection)
                log.f_description = log.f_description + f"Excluded Sales = {excluded_collection}\n"
                included_collection = f_whole_included_amount + f_retail_included_amount
                _logger.info(_('Total included Collection for Sales Person in this Period  = %s'), included_collection)
                log.f_description = log.f_description + f"Included Sales = {included_collection}\n"
                total_collection = total_collection - excluded_collection + included_collection
                _logger.info(_('Total Collection for Sales Person in this Period  = %s'), total_collection)
                log.f_description = log.f_description + f"Net Sales = {total_collection}\n"
                f_comments = f_comments + '\n Total Coll = ' + str(total_collection)
                if (total_collection) > 0:
                    if balance <= 0:
                        dbt_prc = 100
                    else:
                        dbt_prc = (total_collection / balance) * 100

                    _logger.info(_('Debit Percentage  = %s'), dbt_prc)
                    f_comments = f_comments + '\n\r Debit % = ' + str(dbt_prc)
                    log.f_description = log.f_description + f"Debit Percentage  = {dbt_prc}%\n"
                    whole_total = self._get_total_coll_comm('whole', dbt_prc,
                                                            sp.f_total_whole_sp_colletion - f_whole_excluded_amount + f_whole_included_amount,
                                                            log)
                    _logger.info(_('Total whole sale commission  = %s'), whole_total)
                    f_comments = f_comments + '\n\r whole sale comm   = ' + str(whole_total)
                    log.f_description = log.f_description + f"Whole sale commission  = {whole_total}\n"
                    retail_total = self._get_total_coll_comm('retail', dbt_prc,
                                                             sp.f_total_retail_sp_colletion - f_retail_excluded_amount + f_retail_included_amount,
                                                             log)
                    _logger.info(_('Total retail sale commission  = %s'), retail_total)
                    f_comments = f_comments + '\n\r  Retail comm   = ' + str(retail_total)
                    log.f_description = log.f_description + f"Retail sale commission  = {retail_total}\n"
                    f_commission_amount += whole_total + retail_total
                    _logger.info(_('Total  commission  = %s'), f_commission_amount)
                    f_comments = f_comments + '\n\r Total commission   = ' + str(f_commission_amount)
                    log.f_description = log.f_description + f"Total Commission = {f_commission_amount}\n"

                    self._set_comm_results(sp, True, f_commission_amount, 'Calculated' + f_comments, log)

                else:

                    _logger.info(_('Total Collection Less than or = 0'))
                    log.f_description = log.f_description + f"Debit Percentage  = 0%\n"
                    log.f_description = log.f_description + f"Whole sale commission  = 0\n"
                    log.f_description = log.f_description + f"Retail sale commission  = 0\n"
                    log.f_description = log.f_description + f"Total Commission = 0\n"
                    self._set_comm_results(sp, True, 0, 'Total Collection Less than or = 0', log)
            self.f_comments = self.f_comments + '\n Collection Calculation Process Done...'

        self.f_comm_state = 'done'
