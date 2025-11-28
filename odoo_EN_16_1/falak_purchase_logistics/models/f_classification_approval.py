from odoo import models, fields, api


class F_Financial_Users_Rel(models.Model):
    _name = 'f.financial.users.rel'
    _description = 'Financial Approve Relation'
    _table = 'f_financial_users_relation'
    _rec_name = 'f_class_id'

    f_approval = fields.Many2one('f.classification.approval', string='Approval')
    f_class_id = fields.Many2one('f.po.classification', string="Classification", related='f_approval.f_class_id')
    f_user_id = fields.Many2one('res.users', string="Users")


class FClassificationApproval(models.Model):
    _name = 'f.classification.approval'
    _description = 'Purchase Order Classifications Approvals'
    _rec_name = 'f_class_id'

    f_class_id = fields.Many2one('f.po.classification', string="Classification")
    f_min_amount = fields.Float(string='Min Amount')
    f_currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    f_manage_approvals = fields.Many2many('res.users', string='Manage Approvals')
    f_financial_approvals = fields.Many2many('res.users',
                                             'f_financial_users_relation',
                                             'f_approval',
                                             'f_user_id',
                                             string='Financial Approvals')
