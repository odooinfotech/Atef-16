# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)


class F_Purchase_Order_Inherit(models.Model):
    _inherit = 'purchase.order'

    state = fields.Selection(selection_add=[
        ('sent',),
        ('ready', 'Manage Approval'),
        ('manage_approved', 'Finance Approval'),
        ('approved', 'Approved'),
        ('purchase',)], default='draft')

    f_approval_state = fields.Selection([
        ('draft', 'Draft'),
        ('pending_mgr', 'Pending MGR'),
        ('rejected_mgr', 'Rejected MGR'),
        ('approved_mgr', 'Approved MGR'),
        ('pending_fin', 'Pending FIN'),
        ('rejected_fin', 'Rejected FIN'),
        ('fully_approved', 'Fully Approved'),
        ('po_confirmed', 'PO Confirmed'),
        ('cancelled', 'Cancelled')], default='draft', string='Approval Status')

    @api.onchange('incoterm_id', 'f_port_of_loading', 'f_port_of_discharge')
    def f_fill_incoterm_location(self):
        for rec in self:
            if rec.incoterm_id.f_incoterm_location_type == 'loading':
                rec.incoterm_location = rec.f_port_of_loading.f_port_name
            if rec.incoterm_id.f_incoterm_location_type == 'discharge':
                rec.incoterm_location = rec.f_port_of_discharge.f_port_name
            if rec.incoterm_id.f_incoterm_location_type == 'blank':
                rec.incoterm_location = ' '
            if not rec.incoterm_id.f_incoterm_location_type:
                rec.incoterm_location = ' '

    def button_confirm(self):
        res = super(F_Purchase_Order_Inherit, self).button_confirm()
        for order in self:
            order.f_approval_state = 'po_confirmed'
            if order.state in ['approved']:
                order._add_supplier_to_product()
                # Deal with double validation process
                if order._approval_allowed():
                    order.button_approve()
                else:
                    order.write({'state': 'to approve'})
                if order.partner_id not in order.message_partner_ids:
                    order.message_subscribe([order.partner_id.id])
            if order.f_show_planning:
                order.f_purchase_order_action()

        return res

    def button_cancel(self):
        res = super(F_Purchase_Order_Inherit, self).button_cancel()
        for order in self:
            order.f_approval_state = 'cancelled'
            self.mgr_approval_message = ""
            self.fin_approval_message = ""

        return res

    def button_draft(self):
        res = super(F_Purchase_Order_Inherit, self).button_draft()
        for order in self:
            order.f_approval_state = 'draft'
            self.mgr_approval_message = ""
            self.fin_approval_message = ""
        return res

    # def button_approve_status(self):
    #     if self.f_need_financial_app and self.state == 'draft':
    #         self.state = 'fa'
    #     else:
    #         self.state = 'approved'

    # def button_lc_status(self):
    #     self.state = 'lc'

    @api.onchange('partner_id')
    def _f_onchange_partner_id_class(self):
        param = (self.env["ir.config_parameter"].sudo().
                 get_param('falak_purchase_logistics.f_po_access_based_class'))
        domain = []
        if param:
            if self.partner_id:
                f_po_classification = self.partner_id.f_vendor_classifications[:1]
                if f_po_classification:
                    self.f_po_classification = f_po_classification[0]
                _logger.info(
                    _("/////////////////////////////// Partner Class: %s") % self.partner_id.f_vendor_classifications)
                domain = domain + [('id', 'in', self.env.user.f_class_ids.ids),
                                   ('id', 'in', self.partner_id.f_vendor_classifications.ids)]
                return {'domain': {'f_po_classification': domain}}
            else:
                domain = domain + [('id', 'in', self.env.user.f_class_ids.ids)]
                return {'domain': {'f_po_classification': domain}}
        else:
            return {'domain': {'f_po_classification': domain}}

    @api.onchange('partner_id')
    def f_onchange_partner_id(self):
        if self.partner_id:
            if self.partner_id.f_vendor_location == 'imported':
                self.f_show_planning = True
            else:
                self.f_show_planning = False

            self.f_internal_agent = self.partner_id.f_representative.id

    # Other Information Tab
    f_payment_terms = fields.Many2one('f.payment.terms', string='Payment Terms')
    f_note = fields.Char(string="Note")
    f_internal_agent = fields.Many2one('res.partner', string="Internal Agent",
                                       domain="[('category_id.name', '=', 'Internal Agent')]")
    f_show_planning = fields.Boolean(string="PO Planning")
    f_po_classification = fields.Many2one('f.po.classification', string="Classifications",
                                          domain=lambda self: self._f_order_compute_classification_access_domain())
    # f_po_approval = fields.Many2many('res.users', string="PO Approval")
    # f_need_financial_app = fields.Boolean(string="Need Fainancial Approval")
    # f_allow_po_approve = fields.Many2many(related='f_po_classification.f_po_approval', string="PO Approvers")
    # f_allow_financial_po = fields.Many2many(related='f_po_classification.f_financial_po_approval',
    #                                         string="PO Financial Approvers")
    # f_user_po_flag = fields.Boolean(string="user po flag", compute="user_can_approve")
    f_notes = fields.Html(string="Notes")

    # summary_field
    f_total_prods = fields.Float(string="Total Products", compute="compute_total_products", store=True)
    f_total_quantities = fields.Float(string="Total Quantities", compute="compute_total_qty", store=True)

    # f_total_volumes = fields.Float(string="Total Volumes", compute="compute_total_volumes", store=True)
    # f_total_weights = fields.Float(string="Total Weights", compute="compute_total_weights", store=True)

    # other_info
    f_port_of_loading = fields.Many2one('f.purchase.ports', string="Port Of Loading",
                                        domain="[('f_port_type', 'in', ('loading','both'))]")
    f_port_of_discharge = fields.Many2one('f.purchase.ports', string="Port Of Discharge",
                                          domain="[('f_port_type', 'in', ('discharge','both'))]")
    f_packing = fields.Char(string="Packing")
    f_commercial_inv_num = fields.Char(string="Commercial Invoice Number")
    f_commercial_inv_amount = fields.Float(string="Commercial Invoice Amount")
    f_commercial_inv_attach = fields.Binary(string='Commercial Invoice')
    f_packing_list = fields.Binary(string='Packing List')
    file_name_packinglist = fields.Char(string='Packing List File')
    file_name_comm_inv = fields.Char(string='Commercial Invoice File')
    f_require_euro = fields.Selection([('yes', 'Yes'), ('no', 'No')], default='no', string="Require Euro1 ?")
    f_euro1 = fields.Boolean(string="Euro1")

    validation_message = fields.Text(string="Validation Message", compute='_compute_validation_message', store=True)
    mgr_approval_message = fields.Text(string="MGR Approval Message", store=True)
    fin_approval_message = fields.Text(string="FIN Approval Message", store=True)
    approval_message = fields.Text(string="legacy  Approval Message", store=True)
    f_is_manager = fields.Boolean(string='Is Manager', compute='_f_compute_is_manager')
    f_is_finance = fields.Boolean(string='Is Finance', compute='_f_compute_is_manager')

    f_manage_approve = fields.Many2one('res.users', string="Manage Approval By", tracking=True)
    f_finance_approve = fields.Many2one('res.users', string="Finance Approval By", tracking=True)

    f_manage_approve_date = fields.Datetime(string="Manage Approval On", tracking=True)
    f_finance_approve_date = fields.Datetime(string="Finance Approval On", tracking=True)

    f_manage_approval_note = fields.Char(string='Manage Approval Notes')
    f_finance_approval_note = fields.Char(string='Finance Approval Notes')

    f_planning_ids = fields.One2many('f.purchase.order.planning', 'f_po_id', string='Planning Lines')

    def _f_compute_is_manager(self):
        for rec in self:
            if rec.f_po_classification:
                converted_amount = rec.currency_id._convert(rec.amount_total, rec.env.company.currency_id,
                                                             rec.env.company, fields.Date.today())
                approval = (rec.env['f.classification.approval'].sudo().
                            search([('f_class_id', '=', rec.f_po_classification.id),
                                    ('f_min_amount', '<', converted_amount)], order='f_min_amount desc', limit=1))
                if approval:
                    if approval.f_manage_approvals and rec.env.user.id in approval.f_manage_approvals.ids:
                        rec.f_is_manager = True
                    else:
                        rec.f_is_manager = False
                    if approval.f_financial_approvals and rec.env.user.id in approval.f_financial_approvals.ids:
                        rec.f_is_finance = True
                    else:
                        rec.f_is_finance = False
                else:
                    rec.f_is_manager = False
                    rec.f_is_finance = False
            else:
                rec.f_is_manager = False
                rec.f_is_finance = False

    def f_button_ready(self):
        self.mgr_approval_message = ""
        self.fin_approval_message = ""
        if self.f_po_classification:
            converted_amount = self.currency_id._convert(self.amount_total, self.env.company.currency_id,
                                                         self.env.company, fields.Date.today())
            print(converted_amount)
            approval = (self.env['f.classification.approval'].sudo().
                        search([('f_class_id', '=', self.f_po_classification.id),
                                ('f_min_amount', '<', converted_amount)], order='f_min_amount desc', limit=1))
            if approval:
                if approval.f_manage_approvals:
                    self.state = 'ready'
                    self.f_approval_state = 'pending_mgr'
                    if self.env.user.lang.startswith('ar_'):
                        self.mgr_approval_message = "هذه الطلبية بحاجة لموافقة ادارية!"
                    else:
                        self.mgr_approval_message = "This Order Need Management Approvals!"
                elif approval.f_financial_approvals:
                    self.state = 'manage_approved'
                    self.f_approval_state = 'pending_fin'
                    if self.env.user.lang.startswith('ar_'):
                        self.fin_approval_message = "هذه الطلبية بحاجة لموافقة مالية!"
                    else:
                        self.fin_approval_message = "This Order Need Financial Approvals!"
                    self.f_manage_approve = self.env.user
                    self.f_manage_approve_date = fields.Datetime.now()
                else:
                    self.state = 'approved'
                    self.f_approval_state = 'fully_approved'
                    if self.env.user.lang.startswith('ar_'):
                        self.fin_approval_message = "تمت الموافقة على الطلبية!"
                    else:
                        self.fin_approval_message = "Order Accepted!"
                    self.f_manage_approve = self.env.user
                    self.f_manage_approve_date = fields.Datetime.now()
                    self.f_finance_approve = self.env.user
                    self.f_finance_approve_date = fields.Datetime.now()
                    message_body = 'Order '+self.name+' is approved'
                    con_act = self.env['mail.activity.type'].sudo().search([('name', '=', 'To Do')])
                    self.env['mail.activity'].sudo().create({
                        'activity_type_id': con_act.id,
                        'summary': 'Purchase Approval',
                        'date_deadline': fields.Date.today(),
                        'user_id': self.user_id.id,
                        'res_model_id': self.env['ir.model'].sudo().search([('model', '=', 'purchase.order')]).id,
                        'res_id': self.id,
                        'note': message_body,
                    })
            else:
                self.state = 'approved'
                self.f_approval_state = 'fully_approved'
                self.f_manage_approve = self.env.user
                self.f_manage_approve_date = fields.Datetime.now()
                self.f_finance_approve = self.env.user
                self.f_finance_approve_date = fields.Datetime.now()
                message_body = 'Order ' + self.name + ' is approved'
                con_act = self.env['mail.activity.type'].sudo().search([('name', '=', 'To Do')])
                self.env['mail.activity'].sudo().create({
                    'activity_type_id': con_act.id,
                    'summary': 'Purchase Approval',
                    'date_deadline': fields.Date.today(),
                    'user_id': self.user_id.id,
                    'res_model_id': self.env['ir.model'].sudo().search([('model', '=', 'purchase.order')]).id,
                    'res_id': self.id,
                    'note': message_body,
                })
        else:
            self.state = 'approved'
            self.f_approval_state = 'fully_approved'
            self.f_manage_approve = self.env.user
            self.f_manage_approve_date = fields.Datetime.now()
            self.f_finance_approve = self.env.user
            self.f_finance_approve_date = fields.Datetime.now()
            message_body = 'Order ' + self.name + ' is approved'
            con_act = self.env['mail.activity.type'].sudo().search([('name', '=', 'To Do')])
            self.env['mail.activity'].sudo().create({
                'activity_type_id': con_act.id,
                'summary': 'Purchase Approval',
                'date_deadline': fields.Date.today(),
                'user_id': self.user_id.id,
                'res_model_id': self.env['ir.model'].sudo().search([('model', '=', 'purchase.order')]).id,
                'res_id': self.id,
                'note': message_body,
            })

    def f_button_manage_approve(self):
        self.mgr_approval_message = ""
        self.fin_approval_message = ""
        if self.f_po_classification:
            converted_amount = self.currency_id._convert(self.amount_total, self.env.company.currency_id,
                                                         self.env.company, fields.Date.today())
            approval = (self.env['f.classification.approval'].sudo().
                        search([('f_class_id', '=', self.f_po_classification.id),
                                ('f_min_amount', '<', converted_amount)], order='f_min_amount desc', limit=1))
            if approval:
                if approval.f_financial_approvals:
                    self.state = 'manage_approved'
                    self.f_approval_state = 'approved_mgr'
                    if self.env.user.lang.startswith('ar_'):
                        self.mgr_approval_message = "تمت الموافقة الادارية على الطلبية!"
                        self.fin_approval_message = "هذه الطلبية بحاجة لموافقة مالية!"
                    else:
                        self.mgr_approval_message = "Order Manage Approval Accepted!"
                        self.fin_approval_message = "This Order Need Financial Approvals!"
                else:
                    self.state = 'approved'
                    self.f_approval_state = 'fully_approved'
                    if self.env.user.lang.startswith('ar_'):
                        self.fin_approval_message = "تمت الموافقة على الطلبية!"
                    else:
                        self.fin_approval_message = "Order Accepted!"
                    self.f_finance_approve = self.env.user
                    self.f_finance_approve_date = fields.Datetime.now()
                    message_body = 'Order ' + self.name + ' is approved'
                    con_act = self.env['mail.activity.type'].sudo().search([('name', '=', 'To Do')])
                    self.env['mail.activity'].sudo().create({
                        'activity_type_id': con_act.id,
                        'summary': 'Purchase Approval',
                        'date_deadline': fields.Date.today(),
                        'user_id': self.user_id.id,
                        'res_model_id': self.env['ir.model'].sudo().search([('model', '=', 'purchase.order')]).id,
                        'res_id': self.id,
                        'note': message_body,
                    })
            else:
                self.state = 'approved'
                self.f_approval_state = 'fully_approved'
                self.f_finance_approve = self.env.user
                self.f_finance_approve_date = fields.Datetime.now()
                message_body = 'Order ' + self.name + ' is approved'
                con_act = self.env['mail.activity.type'].sudo().search([('name', '=', 'To Do')])
                self.env['mail.activity'].sudo().create({
                    'activity_type_id': con_act.id,
                    'summary': 'Purchase Approval',
                    'date_deadline': fields.Date.today(),
                    'user_id': self.user_id.id,
                    'res_model_id': self.env['ir.model'].sudo().search([('model', '=', 'purchase.order')]).id,
                    'res_id': self.id,
                    'note': message_body,
                })
        else:
            self.state = 'approved'
            self.f_approval_state = 'fully_approved'
            self.f_finance_approve = self.env.user
            self.f_finance_approve_date = fields.Datetime.now()
            message_body = 'Order ' + self.name + ' is approved'
            con_act = self.env['mail.activity.type'].sudo().search([('name', '=', 'To Do')])
            self.env['mail.activity'].sudo().create({
                'activity_type_id': con_act.id,
                'summary': 'Purchase Approval',
                'date_deadline': fields.Date.today(),
                'user_id': self.user_id.id,
                'res_model_id': self.env['ir.model'].sudo().search([('model', '=', 'purchase.order')]).id,
                'res_id': self.id,
                'note': message_body,
            })
        self.f_manage_approve = self.env.user
        self.f_manage_approve_date = fields.Datetime.now()

    def f_button_manage_reject(self):
        return {
            'name': 'Approval Message',
            'view_mode': 'form',
            'res_model': 'f.approval.message.wizard',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'target': 'new',
            'context': {
                'default_f_purchase_order_id': self.id,
                'default_f_approval_type': 'manage',
            }
        }

    def f_button_finance_approve(self):
        self.mgr_approval_message = ""
        self.fin_approval_message = ""
        self.state = 'approved'
        self.f_approval_state = 'fully_approved'
        if self.env.user.lang.startswith('ar_'):
            self.fin_approval_message = "تمت الموافقة على الطلبية!"
        else:
            self.fin_approval_message = "Order Accepted!"
        self.f_finance_approve = self.env.user
        self.f_finance_approve_date = fields.Datetime.now()
        message_body = 'Order ' + self.name + ' is approved'
        con_act = self.env['mail.activity.type'].sudo().search([('name', '=', 'To Do')])
        self.env['mail.activity'].sudo().create({
            'activity_type_id': con_act.id,
            'summary': 'Purchase Approval',
            'date_deadline': fields.Date.today(),
            'user_id': self.user_id.id,
            'res_model_id': self.env['ir.model'].sudo().search([('model', '=', 'purchase.order')]).id,
            'res_id': self.id,
            'note': message_body,
        })

    def f_button_finance_reject(self):
        return {
            'name': 'Approval Message',
            'view_mode': 'form',
            'res_model': 'f.approval.message.wizard',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'target': 'new',
            'context': {
                'default_f_purchase_order_id': self.id,
                'default_f_approval_type': 'finance',
            }
        }

    def _f_default_vendor_domain(self):
        param = self.env["ir.config_parameter"].sudo().get_param('falak_purchase_logistics.f_po_access_based_class')

        if param:
            user_classifications = self.env.user.f_class_ids.ids
            if not user_classifications:
                return self.env['res.partner'].search([])
            else:

                partners = self.env['res.partner'].search([
                    ('f_vendor_classifications', 'in', user_classifications)
                ])
                return partners
        else:
            return self.env['res.partner'].search([])

    f_vendor_domain = fields.Many2many('res.partner', string='Vendor Domain', default=_f_default_vendor_domain,
                                       compute='_f_compute_vendor_domain')

    def _f_compute_vendor_domain(self):
        param = self.env["ir.config_parameter"].sudo().get_param('falak_purchase_logistics.f_po_access_based_class')
        for record in self:
            if param:
                user_classifications = self.env.user.f_class_ids.ids
                if not user_classifications:
                    record.f_vendor_domain = self.env['res.partner'].search([])
                else:
                    partners = self.env['res.partner'].search([
                        ('f_vendor_classifications', 'in', user_classifications)
                    ])
                    record.f_vendor_domain = partners
            else:
                record.f_vendor_domain = self.env['res.partner'].search([])

    def _f_default_classification_access(self):
        f_classification_access = (self.env["ir.config_parameter"].sudo().
                                   get_param('falak_purchase_logistics.f_po_access_based_class'))
        return f_classification_access

    f_classification_access = fields.Boolean(string='Classification Access', default=_f_default_classification_access,
                                             compute='_f_compute_classification_access')

    def _f_compute_classification_access(self):
        self.f_classification_access = (self.env["ir.config_parameter"].sudo().
                                        get_param('falak_purchase_logistics.f_po_access_based_class'))

    def _f_order_compute_classification_access_domain(self):
        param = (self.env["ir.config_parameter"].sudo().
                 get_param('falak_purchase_logistics.f_po_access_based_class'))
        domain = []
        if param:
            domain = domain + [('id', 'in', self.env.user.f_class_ids.ids),
                               ('id', 'in', self.partner_id.f_vendor_classifications.ids)]

        return domain

    # @api.depends('f_po_classification', 'order_line', 'f_approval_state')
    # def _compute_approval_message(self):
    #     for rec in self:
    #         if rec.f_po_classification:
    #             rec.mgr_approval_message = ""
    #             rec.fin_approval_message = ""
    #             if rec.f_approval_state == 'rejected_mgr':
    #                 if rec.env.user.lang.startswith('ar_'):
    #                     rec.mgr_approval_message = "هذه الطلبية بحاجة لموافقة ادارية!"
    #                 else:
    #                     rec.mgr_approval_message = "This Order Need Management Approvals!"
    #             elif rec.f_approval_state == 'pending_mgr':
    #                 if rec.env.user.lang.startswith('ar_'):
    #                     rec.mgr_approval_message = "هذه الطلبية بحاجة لموافقة ادارية!"
    #                 else:
    #                     rec.mgr_approval_message = "This Order Need Management Approvals!"
    #
    #             converted_amount = rec.currency_id._convert(rec.amount_total, rec.env.company.currency_id,
    #                                                         rec.env.company, fields.Date.today())
    #             approval = (rec.env['f.classification.approval'].sudo().
    #                         search([('f_class_id', '=', rec.f_po_classification.id),
    #                                 ('f_min_amount', '<', converted_amount)], order='f_min_amount desc', limit=1))
    #             if approval:
    #                 if approval.f_manage_approvals and approval.f_financial_approvals:
    #                     if rec.state == 'ready':
    #                         if rec.env.user.lang.startswith('ar_'):
    #                             rec.approval_message = "هذه الطلبية بحاجة لموافقة مالية وادارية!"
    #                         else:
    #                             rec.approval_message = "This Order Need Management And Financial Approvals!"
    #                     if rec.state == 'manage_approved':
    #                         if rec.env.user.lang.startswith('ar_'):
    #                             rec.approval_message = "هذه الطلبية بحاجة لموافقة مالية!"
    #                         else:
    #                             rec.approval_message = "This Order Need Financial Approvals!"
    #                     if rec.state == 'approved':
    #                         if rec.env.user.lang.startswith('ar_'):
    #                             rec.approval_message = "تمت الموافقة على الطلبية!"
    #                         else:
    #                             rec.approval_message = "Order Accepted!"
    #                 elif approval.f_manage_approvals:
    #                     if rec.state == 'ready':
    #                         if rec.env.user.lang.startswith('ar_'):
    #                             rec.approval_message = "هذه الطلبية بحاجة لموافقة ادارية!"
    #                         else:
    #                             rec.approval_message = "This Order Need Management Approvals!"
    #                     if rec.state == 'approved':
    #                         if rec.env.user.lang.startswith('ar_'):
    #                             rec.approval_message = "تمت الموافقة على الطلبية!"
    #                         else:
    #                             rec.approval_message = "Order Accepted!"
    #                 elif approval.f_financial_approvals:
    #                     if rec.state == 'manage_approved':
    #                         if rec.env.user.lang.startswith('ar_'):
    #                             rec.approval_message = "هذه الطلبية بحاجة لموافقة مالية"
    #                         else:
    #                             rec.approval_message = "This Order Need Financial Approvals!"
    #                     if rec.state == 'approved':
    #                         if rec.env.user.lang.startswith('ar_'):
    #                             rec.approval_message = "تمت الموافقة على الطلبية!"
    #                         else:
    #                             rec.approval_message = "Order Accepted!"

    @api.depends('order_line')
    def _compute_validation_message(self):
        for line in self.order_line:
            planned = self.env['f.purchase.order.planning'].search([('f_po_line_id', '=', line.id)])
            if not planned:
                line.order_id.validation_message = "Some lines are not planned !"
            else:
                line.order_id.validation_message = False

    def f_cancel_po(self):
        canceled_stage = self.env['f.shipping.stage'].search(
            [('f_owner', '=', 'planning'), ('f_stage_code', '=', 'CANCELED')], limit=1)
        planning_records = self.env['f.purchase.order.planning'].search([('f_po_id', 'in', self.ids)])
        if planning_records and self.state == 'cancel':
            planning_records.write({'f_stat': canceled_stage.id})

    def f_delete_po(self):
        planning_records = self.env['f.purchase.order.planning'].search([('f_po_id', 'in', self.ids)])
        if planning_records:
            planning_records.unlink()

    @api.depends('order_line')
    def compute_total_products(self):
        for rec in self:
            count = 0
            for line in rec.order_line.filtered(lambda s: s.product_id.detailed_type == 'product'):
                count += 1
            rec.f_total_prods = count

    @api.depends('order_line')
    def compute_total_qty(self):
        for rec in self:
            rec.f_total_quantities = 0
            for line in rec.order_line.filtered(lambda s: s.product_id.detailed_type == 'product'):
                rec.f_total_quantities += line.product_qty

    # @api.depends('order_line')
    # def compute_total_volumes(self):
    #     for rec in self:
    #         rec.f_total_volumes = 0
    #         for line in rec.order_line:
    #             rec.f_total_volumes += line.f_total_volume
    #
    # @api.depends('order_line')
    # def compute_total_weights(self):
    #     for rec in self:
    #         rec.f_total_weights = 0
    #         for line in rec.order_line:
    #             rec.f_total_weights += line.f_total_weight

    # def user_can_approve(self):
    #     print('calc', self.env.uid, self.f_allow_po_approve.ids)
    #     if self.env.uid in self.f_allow_po_approve.ids or (
    #             self.env.uid in self.f_allow_financial_po.ids and self.f_need_financial_app):
    #         self.f_user_po_flag = True
    #     else:
    #         self.f_user_po_flag = False
    #     print('calc', self.f_user_po_flag)

    # to check if there is planning related to po, if not created planning for all products in lines
    def f_purchase_order_action(self):
        contact_name = ""
        contact_phone = ""
        for cont in self.partner_id.f_one_contact_person:
            if cont.f_primary:
                contact_name = cont.f_vendor_name
                contact_phone = cont.f_vendor_no

        for prod in self.order_line.filtered(lambda r: r.product_id.detailed_type == 'product' or r.product_id.detailed_type == 'service'):
            planned = self.env['f.purchase.order.planning'].search([('f_po_line_id', '=', prod.id)])
            if not planned:
                plans = self.env['f.purchase.order.planning'].sudo().create({
                    'f_po_id': self.id,
                    'f_po_line_id': prod.id,
                    'f_planned_amount': prod.product_qty,
                    'f_vendor_contact_person': contact_name,
                    'f_vendor_num': contact_phone,
                })

        self._compute_validation_message()

        return {
            'type': 'ir.actions.act_window',
            'name': 'Purchase Order Planning',
            'view_mode': 'tree,form',
            'res_model': 'f.purchase.order.planning',
            'target': 'current',
            'domain': [('f_po_id', '=', self.id)],
            'context': {'default_f_po_id': self.id,

                        },
            }


class F_Purchase_Order_Line_Inherit(models.Model):
    _inherit = 'purchase.order.line'

    f_show_planning = fields.Boolean(related='order_id.f_show_planning', string="PO Planning")
    # f_prod_img = fields.Binary(related='product_id.image_1920', string="Product Image")
    #
    # f_package_volume = fields.Float(string="Package Volume")
    # f_package_qty = fields.Float(string="Contained QTY")
    # f_number_of_packages = fields.Float(string="Number of Packages")
    # f_total_volume = fields.Float(string="Total Volume")
    # #
    # f_prod_weight = fields.Float(related='product_id.weight', string="Product Weight")
    # f_total_weight = fields.Float(string="Total Weight")
    #
    # f_product_ref = fields.Char(related='product_id.default_code', store=True)

    f_total_shipped_qty = fields.Float(string="Total Shipped", store=True)
    f_total_canceled_qty = fields.Float(string="Total Canceled", store=True)
    f_total_remaining_qty = fields.Float(string="Total Remaining", store=True)

    f_po_classification = fields.Many2many('f.po.classification', string="Classifications",
                                           compute='_f_compute_classification_access_domain')

    @api.depends('order_id.f_po_classification')
    def _f_compute_classification_access_domain(self):
        param = self.env["ir.config_parameter"].sudo().get_param('falak_purchase_logistics.f_po_access_based_class')
        for record in self:
            if param:
                if record.order_id.f_po_classification:
                    classes = self.env['f.po.classification'].sudo().search(
                        [('id', '=', record.order_id.f_po_classification.id)])
                    record.f_po_classification = classes
                else:
                    classes = self.env['f.po.classification'].sudo().search([])
                    record.f_po_classification = classes
            else:
                classes = self.env['f.po.classification'].sudo().search([])
                record.f_po_classification = classes

    def _recompute_remaining_qty(self):
        for line in self:
            line.f_total_remaining_qty = round(
                line.product_qty
                - line.qty_received
                - line.f_total_shipped_qty
                - line.f_total_canceled_qty,
                2
            )

    # @api.onchange('product_qty', 'f_package_volume', 'f_package_qty')
    # def f_onchange_vol_qty_fields(self):
    #     number_of_packages = 0.0
    #     total_volume = 0.0
    #     for line in self:
    #         if line.f_package_volume and line.f_package_qty:
    #             number_of_packages = line.product_qty / line.f_package_qty
    #             line.f_number_of_packages = number_of_packages
    #
    #             total_volume = line.f_number_of_packages * line.f_package_volume
    #             line.f_total_volume = total_volume
    #         if line.f_package_qty == 0 or line.f_package_volume == 0:
    #             line.f_number_of_packages = 0
    #             line.f_total_volume = 0

    # @api.onchange('product_qty', 'f_prod_weight')
    # def f_onchange_weight(self):
    #     total_weight = 0.0
    #     for line in self:
    #         total_weight = line.f_prod_weight * line.product_qty
    #         line.f_total_weight = total_weight

    # def f_update_lines(self):
    #     total_volumes = 0.0
    #     total_weights = 0.0
    #     total_remaining = 0.0
    #     for rec in self:
    #         total_volumes += rec.f_total_volume
    #         total_weights += rec.f_total_weight
    #
    #         total_remaining = rec.product_qty - rec.qty_received - rec.f_total_canceled_qty - rec.f_total_shipped_qty
    #         rec.write({'f_total_remaining_qty': total_remaining})
    #         rec.order_id.write({'f_total_volumes': total_volumes})
    #         rec.order_id.write({'f_total_weights': total_weights})
    #
    # def f_create_lines(self):
    #     total_volumes = 0.0
    #     total_weights = 0.0
    #     for rec in self:
    #         total_volumes += rec.f_total_volume
    #         total_weights += rec.f_total_weight
    #
    #         total_remaining = rec.product_qty - rec.qty_received - rec.f_total_canceled_qty - rec.f_total_shipped_qty
    #         rec.write({'f_total_remaining_qty': total_remaining})
    #         rec.order_id.write({'f_total_volumes': total_volumes})
    #         rec.order_id.write({'f_total_weights': total_weights})
    #
    # def f_delete_lines(self):
    #     total_volumes = 0.0
    #     total_weights = 0.0
    #     total_remaining = 0.0
    #     for rec in self:
    #         total_volumes += rec.f_total_volume
    #         total_weights += rec.f_total_weight
    #
    #         rec.order_id.write({'f_total_volumes': total_volumes})
    #         rec.order_id.write({'f_total_weights': total_weights})

    @api.depends('product_qty', 'product_uom')
    def _compute_price_unit_and_date_planned_and_name(self):
        for rec in self:
            price = rec.price_unit
            sup = super(F_Purchase_Order_Line_Inherit, rec)._compute_price_unit_and_date_planned_and_name()
            if price > 0:
                rec.price_unit = price

    def f_purchase_order_lines_action(self):
        contact_name = ""
        contact_phone = ""

        for cont in self.partner_id.f_one_contact_person:
            if cont.f_primary == True:
                contact_name = cont.f_vendor_name
                contact_phone = cont.f_vendor_no

        planned_line = self.env['f.purchase.order.planning'].search(
            [('f_po_line_id', '=', self.id), (('f_po_id', '=', self.order_id.id))])
        if not planned_line and self.product_id.detailed_type == 'product':
            plans = self.env['f.purchase.order.planning'].sudo().create({
                'f_po_id': self.order_id.id,
                'f_po_line_id': self.id,
                'f_planned_amount': self.product_qty,
                'f_vendor_contact_person': contact_name,
                'f_vendor_num': contact_phone,
            })

        self.order_id._compute_validation_message()

        return {
            'type': 'ir.actions.act_window',
            'name': 'Purchase Order Lines Planning',
            'view_mode': 'tree,form',
            'res_model': 'f.purchase.order.planning',
            'target': 'current',
            'domain': [('f_po_line_id', '=', self.id)],
            'context': {'default_f_po_line_id': self.id,
                        },
        }
