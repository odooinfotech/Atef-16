from odoo import models, fields, api, _
from datetime import datetime, timedelta


class FCommissionReport(models.Model):
    _name = 'f.commission.report'
    _description = 'Commission Report'

    f_commission_setup_id = fields.Many2one('f.commission.setup', string='Commission Setup')
    f_commission_period = fields.Many2one('f.commission.period', string='Commission Period')
    f_commission_role = fields.Many2one('f.commission.role', string='Commission Role')
    f_commission_type = fields.Selection(related='f_commission_setup_id.f_commission_type', string='Commission Type')
    f_commission_value_type = fields.Selection(related='f_commission_setup_id.f_commission_value_type',
                                               string='Commission Value Type')
    f_commission_value = fields.Float(string='Commission Value')
    f_commission_target = fields.Text(string='Target')
    f_total_amount = fields.Float(string='Total Amount')
    f_commission_amount = fields.Float(string='Commission Amount')
    f_user_id = fields.Many2one('res.users', string='User')
    f_commission_result = fields.Many2one('f.commission.result', string='Commission Result')
    f_notes = fields.Char(string='Notes')

    def f_calculate_commission(self):
        for rec in self:
            if rec.f_commission_setup_id.f_commission_type == 'sales':
                rec.f_calculate_sales(rec.f_commission_setup_id)
            elif rec.f_commission_setup_id.f_commission_type == 'product_based':
                rec.f_calculate_product_based(rec.f_commission_setup_id)
            elif rec.f_commission_setup_id.f_commission_type == 'collection':
                rec.f_calculate_collection(rec.f_commission_setup_id)

    def f_calculate_sales(self, sales_setup):
        sales_person_ids = tuple(
            self.f_commission_role.f_sales_persons.ids) if self.f_commission_role.f_sales_persons.ids else (
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
                            WHERE fcs.id = {sales_setup.id}
                        )
                        AND pt.f_product_family NOT IN (
                            SELECT exc_family.f_product_family_id
                            FROM f_commission_setup fcs
                            JOIN f_commission_setup_product_family_exc_rel exc_family ON exc_family.f_commission_setup_id = fcs.id
                            WHERE fcs.id = {sales_setup.id}
                        )
                        AND pt.fprodidentity NOT IN (
                            SELECT exc_identity.f_prod_identity_id
                            FROM f_commission_setup fcs
                            JOIN f_commission_setup_product_identity_exc_rel exc_identity ON exc_identity.f_commission_setup_id = fcs.id
                            WHERE fcs.id = {sales_setup.id}
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
                f_commission_period p ON p.id = {self.f_commission_period.id}
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
        self.env.cr.execute(query)
        result = self.env.cr.fetchall()

        if result:
            f_total_sales = sum(row[0] for row in result)
            f_net_sales = sum(row[1] for row in result)
            self.f_total_amount = f_net_sales
            if sales_setup.f_commission_value_type == 'amount':
                self.f_commission_target = 'No Target Needed'
                f_commission_amount = sales_setup.f_commission_value
                self.f_commission_value = sales_setup.f_commission_value
                if f_commission_amount > sales_setup.f_upper_limit:
                    f_commission_amount = sales_setup.f_upper_limit
                    self.f_notes = f'The amount due has exceeded the collection limit ({sales_setup.f_upper_limit}).'
                self.f_commission_amount = f_commission_amount
            elif sales_setup.f_commission_value_type == 'perc':
                self.f_commission_target = 'No Target Needed'
                f_commission_amount = (f_net_sales * sales_setup.f_commission_value) / 100
                self.f_commission_value = sales_setup.f_commission_value
                if f_commission_amount > sales_setup.f_upper_limit:
                    f_commission_amount = sales_setup.f_upper_limit
                    self.f_notes = f'The amount due has exceeded the collection limit ({sales_setup.f_upper_limit}).'
                self.f_commission_amount = f_commission_amount
            elif sales_setup.f_commission_value_type == 'perc_tier':
                self.f_commission_target = f'from {sales_setup.f_tier_from} to {sales_setup.f_tier_to}'
                f_commission_amount = self.f_calculate_sales_tier_value_type(sales_setup, 'percentage', f_net_sales)
                if f_commission_amount > sales_setup.f_upper_limit:
                    f_commission_amount = sales_setup.f_upper_limit
                    self.f_notes = f'The amount due has exceeded the collection limit ({sales_setup.f_upper_limit}).'
                self.f_commission_amount = f_commission_amount
            elif sales_setup.f_commission_value_type == 'amount_tier':
                self.f_commission_target = f'from {sales_setup.f_tier_from} to {sales_setup.f_tier_to}'
                f_commission_amount = self.f_calculate_sales_tier_value_type(sales_setup, 'amount', f_net_sales)
                if f_commission_amount > sales_setup.f_upper_limit:
                    f_commission_amount = sales_setup.f_upper_limit
                    self.f_notes = f'The amount due has exceeded the collection limit ({sales_setup.f_upper_limit}).'
                self.f_commission_amount = f_commission_amount
            elif sales_setup.f_commission_value_type == 'perc_target':
                self.f_commission_target = f'above {sales_setup.f_target}'
                f_commission_amount = self.f_calculate_sales_target_value_type(sales_setup, 'percentage', f_net_sales)
                if f_commission_amount > sales_setup.f_upper_limit:
                    f_commission_amount = sales_setup.f_upper_limit
                    self.f_notes = f'The amount due has exceeded the collection limit ({sales_setup.f_upper_limit}).'
                self.f_commission_amount = f_commission_amount
            elif sales_setup.f_commission_value_type == 'amount_target':
                self.f_commission_target = f'above {sales_setup.f_target}'
                f_commission_amount = self.f_calculate_sales_target_value_type(sales_setup, 'amount', f_net_sales)
                if f_commission_amount > sales_setup.f_upper_limit:
                    f_commission_amount = sales_setup.f_upper_limit
                    self.f_notes = f'The amount due has exceeded the collection limit ({sales_setup.f_upper_limit}).'
                self.f_commission_amount = f_commission_amount
        else:
            self.f_commission_target = ""
            self.f_commission_value = 0.0
            self.f_notes = f'There are no sales'
            self.f_commission_amount = 0

    def f_calculate_product_based(self, product_based_setups):
        sales_person_ids = tuple(
            self.f_commission_role.f_sales_persons.ids) if self.f_commission_role.f_sales_persons.ids else (
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
                            WHERE fcs.id = {product_based_setups.id}
                        )
                        OR pt.f_product_family IN (
                            SELECT family.f_product_family_id
                            FROM f_commission_setup fcs
                            JOIN f_commission_setup_product_family_rel family ON family.f_commission_setup_id = fcs.id
                            WHERE fcs.id = {product_based_setups.id}
                        )
                        OR pt.fprodidentity IN (
                            SELECT identity.f_prod_identity_id
                            FROM f_commission_setup fcs
                            JOIN f_commission_setup_product_identity_rel identity ON identity.f_commission_setup_id = fcs.id
                            WHERE fcs.id = {product_based_setups.id}
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
                            WHERE fcs.id = {product_based_setups.id}
                        )
                        OR pt.f_product_family IN (
                            SELECT family.f_product_family_id
                            FROM f_commission_setup fcs
                            JOIN f_commission_setup_product_family_rel family ON family.f_commission_setup_id = fcs.id
                            WHERE fcs.id = {product_based_setups.id}
                        )
                        OR pt.fprodidentity IN (
                            SELECT identity.f_prod_identity_id
                            FROM f_commission_setup fcs
                            JOIN f_commission_setup_product_identity_rel identity ON identity.f_commission_setup_id = fcs.id
                            WHERE fcs.id = {product_based_setups.id}
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
                f_commission_period p ON p.id = {self.f_commission_period.id}
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
        self.env.cr.execute(query)
        result = self.env.cr.fetchall()

        if result:
            f_total_sales = sum(row[0] for row in result)
            f_net_sales = sum(row[1] for row in result)
            f_net_quantity = sum(row[2] for row in result)
            f_net_amount = 0
            if product_based_setups.f_target_type == 'amount':
                self.f_commission_target = f'Target Type: Amount \n'
                f_net_amount = f_net_sales
            elif product_based_setups.f_target_type == 'quantity':
                f_net_amount = f_net_quantity
            self.f_total_amount = f_net_amount
            if product_based_setups.f_commission_value_type == 'amount':
                self.f_commission_target += 'No Target Needed'
                f_commission_amount = product_based_setups.f_commission_value
                self.f_commission_value = product_based_setups.f_commission_value
                if f_commission_amount > product_based_setups.f_upper_limit:
                    f_commission_amount = product_based_setups.f_upper_limit
                    self.f_notes = f'The amount due has exceeded the collection limit ({product_based_setups.f_upper_limit}).'
                self.f_commission_amount = f_commission_amount
            elif product_based_setups.f_commission_value_type == 'perc':
                self.f_commission_target += 'No Target Needed'
                f_commission_amount = (f_net_sales * product_based_setups.f_commission_value) / 100
                self.f_commission_value = product_based_setups.f_commission_value
                if f_commission_amount > product_based_setups.f_upper_limit:
                    f_commission_amount = product_based_setups.f_upper_limit
                    self.f_notes = f'The amount due has exceeded the collection limit ({product_based_setups.f_upper_limit}).'
                self.f_commission_amount = f_commission_amount
            elif product_based_setups.f_commission_value_type == 'perc_tier':
                self.f_commission_target += f'from {product_based_setups.f_tier_from} to {product_based_setups.f_tier_to}'
                f_commission_amount = self.f_calculate_product_based_tier_value_type(product_based_setups, 'percentage',
                                                                                     f_net_sales, f_net_amount)
                if f_commission_amount > product_based_setups.f_upper_limit:
                    f_commission_amount = product_based_setups.f_upper_limit
                    self.f_notes = f'The amount due has exceeded the collection limit ({product_based_setups.f_upper_limit}).'
                self.f_commission_amount = f_commission_amount
            elif product_based_setups.f_commission_value_type == 'amount_tier':
                self.f_commission_target += f'from {product_based_setups.f_tier_from} to {product_based_setups.f_tier_to}'
                f_commission_amount = self.f_calculate_product_based_tier_value_type(product_based_setups, 'amount',
                                                                                     f_net_sales, f_net_amount)
                if f_commission_amount > product_based_setups.f_upper_limit:
                    f_commission_amount = product_based_setups.f_upper_limit
                    self.f_notes = f'The amount due has exceeded the collection limit ({product_based_setups.f_upper_limit}).'
                self.f_commission_amount = f_commission_amount
            elif product_based_setups.f_commission_value_type == 'perc_target':
                self.f_commission_target += f'above {product_based_setups.f_target}'
                f_commission_amount = self.f_calculate_product_based_target_value_type(product_based_setups, 'percentage',
                                                                                       f_net_sales,
                                                                                       f_net_amount)
                if f_commission_amount > product_based_setups.f_upper_limit:
                    f_commission_amount = product_based_setups.f_upper_limit
                    self.f_notes = f'The amount due has exceeded the collection limit ({product_based_setups.f_upper_limit}).'
                self.f_commission_amount = f_commission_amount
            elif product_based_setups.f_commission_value_type == 'amount_target':
                self.f_commission_target += f'above {product_based_setups.f_target}'
                f_commission_amount = self.f_calculate_product_based_target_value_type(product_based_setups, 'amount',
                                                                                       f_net_sales,
                                                                                       f_net_amount)
                if f_commission_amount > product_based_setups.f_upper_limit:
                    f_commission_amount = product_based_setups.f_upper_limit
                    self.f_notes = f'The amount due has exceeded the collection limit ({product_based_setups.f_upper_limit}).'
                self.f_commission_amount = f_commission_amount

        else:
            self.f_commission_target = ""
            self.f_commission_value = 0.0
            self.f_notes = f'There are no sales'
            self.f_commission_amount = 0

    def f_calculate_collection(self, collection_setups):
        collection_domain = self.f_get_collection_domain(collection_setups, self.f_commission_role)
        total_collections = self.env['account.payment'].read_group(
            domain=collection_domain,
            fields=['amount_total_signed', 'invoice_user_id'],
            groupby=['invoice_user_id'], lazy=False)
        total_collections_amount = sum(row['amount_total_signed'] for row in total_collections)
        return_check_domain = self.f_get_return_domain(collection_setups, self.f_commission_role)
        return_check = self.env['account.payment'].read_group(
            domain=return_check_domain,
            fields=['amount_total_signed', 'invoice_user_id'],
            groupby=['invoice_user_id'], lazy=False)
        total_return_check_amount = sum(row['amount_total_signed'] for row in return_check)
        check_to_cash_amount = self.f_get_check_to_cash_amount(collection_setups, self.f_commission_role)
        exclude_check = self.f_get_exclude_check_amount(collection_setups, self.f_commission_role)
        total_amount = total_collections_amount
        if collection_setups.f_collection_type.f_include_returned_checks or collection_setups.f_collection_type.f_payment_type == 'all':
            total_amount -= total_return_check_amount
        total_amount += check_to_cash_amount
        total_amount -= exclude_check
        self.f_total_amount = total_amount
        if collection_setups.f_commission_value_type == 'amount':
            self.f_commission_target = 'No Target Needed'
            if collection_setups.f_is_bad_debt:
                f_commission_amount = self.f_calculate_bad_debt_commission(collection_setups, self.f_commission_role, total_amount, False)
            else:
                self.f_commission_value = collection_setups.f_commission_value
                f_commission_amount = collection_setups.f_commission_value
            if f_commission_amount > collection_setups.f_upper_limit:
                f_commission_amount = collection_setups.f_upper_limit
                self.f_notes = f'The amount due has exceeded the collection limit ({collection_setups.f_upper_limit}).'
            self.f_commission_amount = f_commission_amount
        elif collection_setups.f_commission_value_type == 'perc':
            self.f_commission_target = 'No Target Needed'
            if collection_setups.f_is_bad_debt:
                f_commission_amount = self.f_calculate_bad_debt_commission(collection_setups, self.f_commission_role, total_amount, False)
            else:
                self.f_commission_value = collection_setups.f_commission_value
                f_commission_amount = (total_amount * collection_setups.f_commission_value) / 100
            if f_commission_amount > collection_setups.f_upper_limit:
                f_commission_amount = collection_setups.f_upper_limit
                self.f_notes = f'The amount due has exceeded the collection limit ({collection_setups.f_upper_limit}).'
            self.f_commission_amount = f_commission_amount
        elif collection_setups.f_commission_value_type == 'perc_tier':
            self.f_commission_target = f'from {collection_setups.f_tier_from} to {collection_setups.f_tier_to}'
            if collection_setups.f_is_bad_debt:
                f_commission_amount = self.f_calculate_bad_debt_commission(collection_setups, self.f_commission_role, total_amount, 'tier')
            else:
                f_commission_amount = self.f_calculate_sales_tier_value_type(collection_setups, 'percentage', total_amount)
            if f_commission_amount > collection_setups.f_upper_limit:
                f_commission_amount = collection_setups.f_upper_limit
                self.f_notes = f'The amount due has exceeded the collection limit ({collection_setups.f_upper_limit}).'
            self.f_commission_amount = f_commission_amount
        elif collection_setups.f_commission_value_type == 'amount_tier':
            self.f_commission_target = f'from {collection_setups.f_tier_from} to {collection_setups.f_tier_to}'
            if collection_setups.f_is_bad_debt:
                f_commission_amount = self.f_calculate_bad_debt_commission(collection_setups, self.f_commission_role, total_amount, 'tier')
            else:
                f_commission_amount = self.f_calculate_sales_tier_value_type(collection_setups, 'amount', total_amount)
            if f_commission_amount > collection_setups.f_upper_limit:
                f_commission_amount = collection_setups.f_upper_limit
                self.f_notes = f'The amount due has exceeded the collection limit ({collection_setups.f_upper_limit}).'
            self.f_commission_amount = f_commission_amount
        elif collection_setups.f_commission_value_type == 'perc_target':
            self.f_commission_target = f'above {collection_setups.f_target}'
            if collection_setups.f_is_bad_debt:
                f_commission_amount = self.f_calculate_bad_debt_commission(collection_setups, self.f_commission_role, total_amount, 'target')
            else:
                f_commission_amount = self.f_calculate_sales_target_value_type(collection_setups, 'percentage', total_amount)
            if f_commission_amount > collection_setups.f_upper_limit:
                f_commission_amount = collection_setups.f_upper_limit
                self.f_notes = f'The amount due has exceeded the collection limit ({collection_setups.f_upper_limit}).'
            self.f_commission_amount = f_commission_amount
        elif collection_setups.f_commission_value_type == 'amount_target':
            self.f_commission_target = f'above {collection_setups.f_target}'
            if collection_setups.f_is_bad_debt:
                f_commission_amount = self.f_calculate_bad_debt_commission(collection_setups, self.f_commission_role, total_amount, 'target')
            else:
                f_commission_amount = self.f_calculate_sales_target_value_type(collection_setups, 'amount', total_amount)
            if f_commission_amount > collection_setups.f_upper_limit:
                f_commission_amount = collection_setups.f_upper_limit
                self.f_notes = f'The amount due has exceeded the collection limit ({collection_setups.f_upper_limit}).'
            self.f_commission_amount = f_commission_amount

    def f_calculate_sales_tier_value_type(self, setup, type, total_amount):
        if setup.f_tier_from < total_amount <= setup.f_tier_to:
            if type == 'percentage':
                self.f_commission_value = setup.f_commission_value
                return (total_amount * setup.f_commission_value) / 100
            elif type == 'amount':
                self.f_commission_value = setup.f_commission_value
                return setup.f_commission_value
        if total_amount > setup.f_tier_to and setup.f_limit_to_target:
            if type == 'percentage':
                self.f_commission_value = setup.f_commission_value
                return (setup.f_tier_to * setup.f_commission_value) / 100
            elif type == 'amount':
                self.f_commission_value = setup.f_commission_value
                return setup.f_commission_value
        return 0

    def f_calculate_sales_target_value_type(self, setup, type, total_amount):
        entry_point = setup.f_target * setup.f_entry_point
        if total_amount >= entry_point:
            if type == 'percentage':
                self.f_commission_value = setup.f_commission_value
                if setup.f_limit_to_target:
                    return (setup.f_target * setup.f_commission_value) / 100
                return (total_amount * setup.f_commission_value) / 100
            elif type == 'amount':
                self.f_commission_value = setup.f_commission_value
                if setup.f_limit_to_target:
                    return setup.f_commission_value
                percent = setup.f_commission_value / setup.f_target
                return percent * total_amount
        return 0

    def f_calculate_product_based_tier_value_type(self, setup, type, net_sales, net_amount):
        if setup.f_tier_from < net_amount <= setup.f_tier_to:
            if type == 'percentage':
                self.f_commission_value = setup.f_commission_value
                return (net_sales * setup.f_commission_value) / 100
            elif type == 'amount':
                self.f_commission_value = setup.f_commission_value
                return setup.f_commission_value
        if net_amount > setup.f_tier_to and setup.f_limit_to_target:
            if type == 'percentage':
                self.f_commission_value = setup.f_commission_value
                if setup.f_target_type == 'amount':
                    return (setup.f_tier_to * setup.f_commission_value) / 100
                elif setup.f_target_type == 'quantity':
                    tier_perc = setup.f_tier_to / net_amount
                    tier_amount = tier_perc * net_sales
                    return (tier_amount * setup.f_commission_value) / 100
            elif type == 'amount':
                self.f_commission_value = setup.f_commission_value
                return setup.f_commission_value
        return 0

    def f_calculate_product_based_target_value_type(self, setup, type, net_sales, net_amount):
        entry_point = setup.f_target * setup.f_entry_point
        if net_amount >= entry_point:
            if type == 'percentage':
                self.f_commission_value = setup.f_commission_value
                if setup.f_limit_to_target:
                    if setup.f_target_type == 'amount':
                        return (setup.f_target * setup.f_commission_value) / 100
                    elif setup.f_target_type == 'quantity':
                        target_perc = setup.f_target / net_amount
                        target_amount = target_perc * net_sales
                        return (target_amount * setup.f_commission_value) / 100
                return (net_sales * setup.f_commission_value) / 100
            elif type == 'amount':
                self.f_commission_value = setup.f_commission_value
                if setup.f_limit_to_target:
                    return setup.f_commission_value
                percent = setup.f_commission_value / setup.f_target
                return percent * net_sales
        return 0

    def f_get_collection_domain(self, setup, role):
        domain = [
            ('invoice_user_id', 'in', role.f_sales_persons.ids),
            ('date', '>=', self.f_commission_period.f_from),
            ('date', '<=', self.f_commission_period.f_to),
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
            ('return_date', '>=', self.f_commission_period.f_from),
            ('return_date', '<=', self.f_commission_period.f_to),
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
            ('date', '>=', self.f_commission_period.f_from),
            ('date', '<=', self.f_commission_period.f_to),
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
            ('date', '>=', self.f_commission_period.f_from),
            ('date', '<=', self.f_commission_period.f_to),
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
        bad_debt_date = self.f_commission_period.f_to - timedelta(days=setup.f_bad_debt_matrix.f_bad_debt)
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

        self.f_commission_value = f_commission_percent
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