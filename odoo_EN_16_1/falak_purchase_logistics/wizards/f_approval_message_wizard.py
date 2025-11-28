from odoo import models, fields, api, _


class FApprovalMessageWizard(models.TransientModel):
    _name = 'f.approval.message.wizard'
    _description = 'Approval Message Wizard'

    f_purchase_order_id = fields.Many2one('purchase.order', string='Purchase Order')
    f_approval_type = fields.Selection([('manage', 'Manage'),('finance', 'Finance')], string='Approval Type', default='manage')
    f_message = fields.Char(string='Message')

    def f_reject_purchase(self):
        self.ensure_one()
        if self.f_purchase_order_id:
            if self.f_approval_type == 'manage':
                self.f_purchase_order_id.f_approval_state = 'rejected_mgr'
                if self.env.user.lang.startswith('ar_'):
                    self.f_purchase_order_id.mgr_approval_message = "تم الرفض الاداري على الطلبية!"
                else:
                    self.f_purchase_order_id.mgr_approval_message = "Order Manage Approval Rejected!"
                self.f_purchase_order_id.state = 'draft'
                self.f_purchase_order_id.f_manage_approve = self.env.user.id
                self.f_purchase_order_id.f_manage_approve_date = fields.Datetime.now()
                self.f_purchase_order_id.f_manage_approval_note = self.f_message
            else:
                self.f_purchase_order_id.f_approval_state = 'rejected_fin'
                if self.env.user.lang.startswith('ar_'):
                    self.f_purchase_order_id.fin_approval_message = "تم الرفض المالي على الطلبية!"
                else:
                    self.f_purchase_order_id.fin_approval_message = "Order Financial Approval Rejected!"
                if self.f_purchase_order_id.f_po_classification:
                    converted_amount = self.f_purchase_order_id.currency_id._convert(
                        self.f_purchase_order_id.amount_total, self.env.company.currency_id,
                        self.env.company, fields.Date.today())
                    approval = (self.env['f.classification.approval'].sudo().
                                search([('f_class_id', '=', self.f_purchase_order_id.f_po_classification.id),
                                        ('f_min_amount', '<', converted_amount)], order='f_min_amount desc', limit=1))
                    if approval:
                        if approval.f_manage_approvals and approval.f_financial_approvals:
                            self.f_purchase_order_id.state = 'ready'
                            if self.env.user.lang.startswith('ar_'):
                                self.f_purchase_order_id.mgr_approval_message = "هذه الطلبية بحاجة لموافقة ادارية!"
                            else:
                                self.f_purchase_order_id.mgr_approval_message = "This Order Need Management Approvals!"
                            self.f_purchase_order_id.f_finance_approve = self.env.user.id
                            self.f_purchase_order_id.f_finance_approve_date = fields.Datetime.now()
                            self.f_purchase_order_id.f_finance_approval_note = self.f_message
                        elif approval.f_financial_approvals:
                            self.f_purchase_order_id.state = 'draft'
                            self.f_purchase_order_id.f_manage_approve = self.env.user.id
                            self.f_purchase_order_id.f_manage_approve_date = fields.Datetime.now()
                            self.f_purchase_order_id.f_manage_approval_note = self.f_message
        self.unlink()
        return {'type': 'ir.actions.act_window_close'}
