from odoo import models, fields, api


class F_PO_Classification(models.Model):
    _name = 'f.po.classification'
    _description = 'Purchase Order Classifications'
    _rec_name = 'f_name'

    f_name = fields.Char(string="Classification Name")
    # f_po_approval = fields.Many2many('res.users', string="PO Approval")
    # f_financial_po_approval = fields.Many2many('res.users',
    #                                            'f_financial_users_relation',
    #                                            'f_class_id',
    #                                            'f_user_id',
    #                                            string="Financial PO Approval")
