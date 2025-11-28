from odoo import models, fields, api, _


class FCommissionGroupsSetup(models.Model):
    _name = 'f.commission.groups.setup'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Commission Groups Setup'
    _rec_name = "f_description"

    f_commission_type = fields.Selection(
        [('sales', 'Sales'), ('product_based', 'Product Based'), ('collection', 'Collection')], default='sales',
        required=True, string='Commission Type', copy=True, tracking=True)
    f_description = fields.Char(string="Description", copy=True, tracking=True)
    f_period = fields.Many2one(comodel_name='f.comisson.period', string='Period', domain="[('f_colsed', '=', False)]",
                               required=True, copy=True, tracking=True)
    f_sales_person = fields.Many2many('res.users', string='Sales Persons', required=True, copy=True, tracking=True)
    f_target_type = fields.Selection([('quantity', 'Quantity'), ('amount', 'Amount')], default='amount', required=True,
                                     string='Target Type', tracking=True)
    f_target = fields.Float(string='Target', tracking=True)
    f_entry_point = fields.Float(string='Entry Point', tracking=True)
    f_comm_value_type = fields.Selection([('camount', 'Amount'), ('cpercentage', '%')], default='camount',
                                         required=True, string='Commission Value Type', tracking=True)
    f_comm_value = fields.Float(string='Commission Value', tracking=True)
    # f_comm_value_percent = fields.Float(string ='Commission Value')

    # product Based  commission fields
    f_product = fields.Many2many(comodel_name='product.template', relation='f_commission_management_product_rel_groups',
                                 string='Product Name', tracking=True)
    f_product_exc = fields.Many2many(comodel_name='product.template',
                                     relation='f_commission_management_product_exc_rel_groups', string='Exclude Products',
                                     tracking=True)
    f_product_family = fields.Many2many(comodel_name='f.product.family',
                                        relation='f_commission_management_product_family_rel_groups', string='Product Family',
                                        tracking=True)
    f_product_family_exc = fields.Many2many(comodel_name='f.product.family',
                                            relation='f_commission_management_product_family_exc_rel_groups',
                                            string='Exclude Families', tracking=True)
    f_product_identity = fields.Many2many(comodel_name='f.prod.identity',
                                          relation='f_commission_management_product_identity_rel_groups',
                                          string='Product Identity', tracking=True)
    f_product_identity_exc = fields.Many2many(comodel_name='f.prod.identity',
                                              relation='f_commission_management_product_identity_exc_rel_groups',
                                              string='Exclude Identities', tracking=True)
    f_status = fields.Selection(
        [('draft', 'Draft'), ('posted', 'Posted')], default='draft', copy=False,
        string='Status', tracking=True)

    def f_post_commission_group(self):
        for rec in self:
            setups = rec.env['f.commission.management'].sudo().search([('f_commission_type', '=', rec.f_commission_type),
                                                                       ('f_sales_person', 'in', rec.f_sales_person.ids),
                                                                       ('f_is_calculated', '=', False)])
            setups.unlink()
            for sp in rec.f_sales_person:
                vals = {
                    'f_commission_type': rec.f_commission_type,
                    'f_description': rec.f_description + " - " + sp.name,
                    'f_period': rec.f_period.id,
                    'f_sales_person': sp.id,
                    'f_target_type': rec.f_target_type,
                    'f_target': rec.f_target,
                    'f_entry_point': rec.f_entry_point,
                    'f_comm_value_type': rec.f_comm_value_type,
                    'f_comm_value': rec.f_comm_value,
                    'f_product': rec.f_product.ids,
                    'f_product_exc': rec.f_product_exc.ids,
                    'f_product_family': rec.f_product_family.ids,
                    'f_product_family_exc': rec.f_product_family_exc.ids,
                    'f_product_identity': rec.f_product_identity.ids,
                    'f_product_identity_exc': rec.f_product_identity_exc
                }
                rec.env['f.commission.management'].create(vals)
            rec.f_status = 'posted'
