from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, _
from datetime import datetime, timedelta, date
from odoo.exceptions import UserError


class FShippingStage(models.Model):
    _name = 'f.shipping.stage'
    _description = 'Shipping Stages'
    _rec_name = 'f_stage_name'

    f_stage_name = fields.Char(string="Name")
    f_owner = fields.Selection(string="Owner",
                               selection=([('shipping', 'Shipping Stage'), ('planning', 'Planning Stage')]))
    f_stage_code = fields.Char(string="Code")


class F_Shipping_Details(models.Model):
    _name = 'f.shipping.details'
    _description = 'Shipping Details'
    _rec_name = 'f_shipment_num'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    f_shipment_num = fields.Char(string="Shipment Name", required=True)
    f_po_plan_id = fields.One2many('f.purchase.order.planning', inverse_name='f_shipping', string="PO Planning",
                                   tracking=True, domain="[('f_shipping','=',False)]")
    f_po_classifications = fields.Many2many('f.po.classification', string="Classifications", compute='_f_compute_po_classifications', store=True)
    f_shipping_time = fields.Char(string="Shipping Period")

    # Dates
    f_dep_date = fields.Date(string="Dep Date")

    f_real_shipping_date = fields.Date(string="ATD")
    f_delta_shipping_date = fields.Integer(string="Diff", store=True)
    f_estimated_port_arrival_date = fields.Date(string="ETA")
    f_real_port_arrival_date = fields.Date(string="ATA")
    f_delta_port_arrival_date = fields.Integer(string="Diff", compute='compute_port_arrival_date', store=True)
    f_estimated_company_arrival_date = fields.Date(string="ETAF")
    f_real_company_arrival_date = fields.Date(string="ATAF")
    f_delta_company_arrival_date = fields.Integer(string="Diff", compute='compute_company_arrival_date', store=True)

    f_shipping_company = fields.Many2one('res.partner', string='Shipping Company')

    f_containers = fields.One2many('f.container.details', 'f_con_shipping', string="Containers",
                                   tracking=True)
    f_shipping_line = fields.Many2one('f.shipping.line', string='Shipping Line')
    f_shipping_company_agent = fields.Many2one('res.partner', string="Shipping Agent(Forwarder)")
    f_booking_no = fields.Char(string="Job #")
    f_freight_cost = fields.Float(string="Freight Cost")
    f_free_days_of_demurrage = fields.Char(string="Free Days of Demurrage",
                                           help="Number of days allowed before returning the container ")
    f_ship_stage = fields.Char(string="Stage_old")

    f_shipp_stage = fields.Many2one('f.shipping.stage', string="Stage", domain="[('f_owner','=','shipping')]",
                                    tracking=True)

    f_bill_of_lading_type = fields.Selection([('original', 'Original'),
                                              ('telex', 'Telex Release'), ('Seaway bill', 'Seaway Bill')],
                                             string="B/L Type")

    f_bill_of_lad_status = fields.Selection([('invoice', 'Invoice'),
                                             ('final MBL ', 'Final MBL'), ('received', 'Received')],
                                            string="B/L Status")

    f_supplier_name = fields.Many2one('res.partner', string="Supplier Name")
    f_port_of_discharge = fields.Many2one('f.purchase.ports', string="Port Of Discharge",
                                          domain="[('f_port_type', 'in', ('discharge','both'))]")
    f_port_of_loading = fields.Many2one('f.purchase.ports', string="Port Of Loading",
                                        domain="[('f_port_type', 'in', ('loading','both'))]")
    f_consignee = fields.Char(string="Consignee")

    f_import_agent = fields.Many2one('res.partner', string="Import Agent",
                                     domain="[('category_id.name', '=', 'Internal Agent')]", tracking=True)

    # Clearance Details
    f_clearance_file_name = fields.Char(string="Clearance File Name")
    f_clearance_file_number = fields.Char(string="Custom File Number")
    f_clearance_time = fields.Date(string="Actual Clearance Time")

    f_clearance_representative = fields.Many2one('res.partner', string="Clearance Agent",
                                                 domain="[('category_id.name', '=', 'Internal Agent')]", tracking=True)

    f_teken = fields.Boolean(string="Teken")
    f_security_check = fields.Boolean(string="Security Check")
    f_bank_garantee = fields.Boolean(string="Bank Guarantee")
    f_driver = fields.Char(string="Driver")
    f_custom_broker = fields.Many2one('res.partner', string="Custom Broker",
                                      domain="[('category_id.name', '=', 'Custom Broker')]")

    f_suppliers_names = fields.Text(string='Suppliers Names')

    # f_total_volumes = fields.Float(string="PO Planning Volumes", compute='f_compute_totals')
    # f_total_weights = fields.Float(string="PO Planning Weights", compute='f_compute_totals')

    f_note = fields.Html(string='Note')

    f_bank_guarantee_amount = fields.Float(string="Bank Guarantee Amount")

    f_lc_number = fields.Char(string="LC Number")

    f_seq = fields.Char(string='Shipment Sequence', readonly=True)

    f_clearance_period = fields.Integer(string="Clearance Period", default=10)

    f_shipping_security_check = fields.Boolean(string="Security Check", compute='f_compute_shipping_security_check',
                                               store=True)

    f_document_count = fields.Integer('Document Count', compute='f_compute_document_count')

    def _f_default_classification_access(self):
        f_classification_access = (self.env["ir.config_parameter"].sudo().
                                   get_param('falak_purchase_logistics.f_po_access_based_class'))
        return f_classification_access

    f_classification_access = fields.Boolean(string='Classification Access', default=_f_default_classification_access,
                                             compute='_f_compute_classification_access')

    def _f_compute_classification_access(self):
        self.f_classification_access = (self.env["ir.config_parameter"].sudo().
                                        get_param('falak_purchase_logistics.f_po_access_based_class'))

    @api.depends('f_po_plan_id')
    def _f_compute_po_classifications(self):
        for order in self:
            classifications = order.f_po_plan_id.mapped('f_po_classification')
            order.f_po_classifications = [(6, 0, classifications.ids)]

    def f_compute_document_count(self):
        for order in self:
            order.f_document_count = self.env['documents.document'].search_count(
                [('res_id', '=', order.id), ('res_model', '=', self._name)]
            )

    def f_action_see_documents(self):
        self.ensure_one()
        return {
            'name': _('Documents'),
            'domain': [
                ('res_id', '=', self.id),
                ('res_model', '=', self._name)
            ],
            'res_model': 'documents.document',
            'type': 'ir.actions.act_window',
            'views': [(False, 'kanban')],
            'view_mode': 'kanban',
            'context': {
                "default_res_id": self.id,
                "default_res_model": self._name,
                "searchpanel_default_folder_id": self.env.ref(
                    'falak_purchase_logistics.f_shipping_workspace').id,
            },
        }

    @api.onchange('f_real_shipping_date', 'f_port_of_loading')
    def _onchange_update_eta(self):
        shipping_period = int(self.f_port_of_loading.f_shipping_period or 0)

        if not isinstance(self.f_real_shipping_date, date):
            return

        eta = self.f_real_shipping_date + timedelta(days=shipping_period)

        self.f_estimated_port_arrival_date = eta

    @api.constrains('f_real_shipping_date', 'f_real_port_arrival_date')
    def _check_real_dates(self):
        if self.f_real_shipping_date and self.f_real_port_arrival_date:
            if self.f_real_shipping_date > self.f_real_port_arrival_date:
                raise UserError("ATD (Actual time of departure) cannot be after ATA (Actual time of arrival).")

    @api.depends('f_containers.f_security_check')
    def f_compute_shipping_security_check(self):
        for shipping in self:
            shipping.f_shipping_security_check = any(container.f_security_check for container in shipping.f_containers)

    @api.onchange('f_real_port_arrival_date', 'f_clearance_period')
    def _onchange_f_real_port_arrival_date(self):
        clearance_period = int(self.f_clearance_period or 0)

        if not isinstance(self.f_real_port_arrival_date, date):
            return

        etaf = self.f_real_port_arrival_date + timedelta(clearance_period)
        self.f_estimated_company_arrival_date = etaf

    @api.onchange('f_estimated_port_arrival_date', 'f_clearance_period')
    def _onchange_f_estimated_port_arrival_date(self):
        clearance_period = int(self.f_clearance_period or 0)

        if not isinstance(self.f_estimated_port_arrival_date, date):
            return

        etaf = self.f_estimated_port_arrival_date + timedelta(clearance_period)
        self.f_estimated_company_arrival_date = etaf

    @api.onchange('f_po_plan_id')
    def _onchange_f_po_plan_id(self):
        for plan in self.f_po_plan_id:
            plan.f_stat = self.f_shipp_stage

    @api.onchange('f_real_company_arrival_date')
    def onchange_f_real_company_arrival_date(self):
        arrived_company_stage = self.env['f.shipping.stage'].sudo().search([('f_stage_code', '=', 'arrived_company')],
                                                                           limit=1).id
        for rec in self:
            if rec.f_real_company_arrival_date:
                rec.f_shipp_stage = arrived_company_stage

    @api.onchange('f_clearance_file_number')
    def onchange_f_clearance_file_number(self):
        clearance_stage = self.env['f.shipping.stage'].sudo().search([('f_stage_code', '=', 'clearance')], limit=1).id
        for rec in self:
            if rec.f_real_port_arrival_date:
                rec.f_shipp_stage = clearance_stage

    @api.onchange('f_real_port_arrival_date')
    def onchange_f_real_port_arrival_date(self):
        arrived_stage = self.env['f.shipping.stage'].sudo().search([('f_stage_code', '=', 'arrived')], limit=1).id
        for rec in self:
            rec.f_shipp_stage = arrived_stage

    @api.onchange('f_real_shipping_date')
    def onchange_f_real_shipping_date(self):
        shipped_stage = self.env['f.shipping.stage'].sudo().search([('f_stage_code', '=', 'shipped')], limit=1).id
        for rec in self:
            rec.f_shipp_stage = shipped_stage

    def f_set_quantities(self):
        for shipp in self:
            for plan in shipp.f_po_plan_id:
                if plan.f_shipped_amount == 0.0:
                    plan.write({'f_shipped_amount': plan.f_planned_amount})

    @api.onchange('f_import_agent')
    def onchange_f_import_agent(self):
        for rec in self:
            rec.f_clearance_representative = rec.f_import_agent

    # @api.depends('f_po_plan_id')
    # def f_compute_totals(self):
    #     total_volumes = 0.0
    #     total_weights = 0.0
    #     for rec in self:
    #         total_volumes = sum(rec.f_po_plan_id.mapped('f_total_volume'))
    #         total_weights = sum(rec.f_po_plan_id.mapped('f_total_weight'))
    #         rec.f_total_volumes = total_volumes
    #         rec.f_total_weights = total_weights

    def f_get_suppliers(self):
        for rec in self:
            suppliers_names = '\n'.join(map(str, rec.f_po_plan_id.mapped('f_vendor_name.name')))
            rec.f_suppliers_names = suppliers_names

    def dates_hist_audit(self, field_name, f_from_date, f_to_date, f_user, f_shipping_id):
        values = {
            'f_date_name': field_name,
            'f_from_date': f_from_date,
            'f_to_date': f_to_date,
            'f_user_id': f_user,
            'f_updated_at': datetime.today(),
            'f_shipping_id': f_shipping_id,
        }
        self.env['f.ship.dates.hist'].create(values)

    @api.model
    def create(self, vals):
        user_id = self.env['res.users'].sudo().browse(self.env.uid).id

        f_real_shipping_date = False
        f_estimated_port_arrival_date = False
        f_real_port_arrival_date = False
        f_estimated_company_arrival_date = False
        f_real_company_arrival_date = False

        f_delta_shipping_date = False
        f_delta_port_arrival_date = False
        f_delta_company_arrival_date = False

        atd_audit = False
        eta_audit = False
        ata_audit = False
        etaf_audit = False
        ataf_audit = False

        if 'f_real_shipping_date' in vals:
            f_real_shipping_date = vals['f_real_shipping_date']
            atd_audit = True
        if 'f_estimated_port_arrival_date' in vals:
            f_estimated_port_arrival_date = vals['f_estimated_port_arrival_date']
            eta_audit = True
        if 'f_real_port_arrival_date' in vals:
            f_real_port_arrival_date = vals['f_real_port_arrival_date']
            ata_audit = True
        if 'f_estimated_company_arrival_date' in vals:
            f_estimated_company_arrival_date = vals['f_estimated_company_arrival_date']
            etaf_audit = True
        if 'f_real_company_arrival_date' in vals:
            f_real_company_arrival_date = vals['f_real_company_arrival_date']
            ataf_audit = True

        f_delta_shipping_date, f_delta_port_arrival_date, f_delta_company_arrival_date = self.calc_dates_diff(
            f_real_shipping_date, f_estimated_port_arrival_date, f_real_port_arrival_date,
            f_estimated_company_arrival_date, f_real_company_arrival_date)

        vals['f_delta_shipping_date'] = f_delta_shipping_date
        vals['f_delta_port_arrival_date'] = f_delta_port_arrival_date
        vals['f_delta_company_arrival_date'] = f_delta_company_arrival_date
        vals['f_seq'] = self.env['ir.sequence'].next_by_code([('ship.seq')])
        res = super(F_Shipping_Details, self).create(vals)

        if atd_audit and f_real_shipping_date:
            self.dates_hist_audit('ATD', False, f_real_shipping_date, user_id, res.id)
        if eta_audit and f_estimated_port_arrival_date:
            self.dates_hist_audit('ETA', False, f_estimated_port_arrival_date, user_id, res.id)
        if ata_audit and f_real_port_arrival_date:
            self.dates_hist_audit('ATA', False, f_real_port_arrival_date, user_id, res.id)
        if etaf_audit and f_estimated_company_arrival_date:
            self.dates_hist_audit('ETAF', False, f_estimated_company_arrival_date, user_id, res.id)
        if ataf_audit and f_real_company_arrival_date:
            self.dates_hist_audit('ATAF', False, f_real_company_arrival_date, user_id, res.id)

        return res

    def write(self, vals):
        user_id = self.env['res.users'].sudo().browse(self.env.uid).id

        if 'f_real_shipping_date' in vals:
            f_real_shipping_date = vals['f_real_shipping_date']
            self.dates_hist_audit('ATD', self.f_real_shipping_date, f_real_shipping_date, user_id, self.id)
        else:
            f_real_shipping_date = self.f_real_shipping_date
        if 'f_estimated_port_arrival_date' in vals:
            f_estimated_port_arrival_date = vals['f_estimated_port_arrival_date']
            self.dates_hist_audit('ETA', self.f_estimated_port_arrival_date, f_estimated_port_arrival_date, user_id,
                                  self.id)
        else:
            f_estimated_port_arrival_date = self.f_estimated_port_arrival_date
        if 'f_real_port_arrival_date' in vals:
            f_real_port_arrival_date = vals['f_real_port_arrival_date']
            self.dates_hist_audit('ATA', self.f_real_port_arrival_date, f_real_port_arrival_date, user_id, self.id)
        else:
            f_real_port_arrival_date = self.f_real_port_arrival_date
        if 'f_estimated_company_arrival_date' in vals:
            f_estimated_company_arrival_date = vals['f_estimated_company_arrival_date']
            self.dates_hist_audit('ETAF', self.f_estimated_company_arrival_date, f_estimated_company_arrival_date,
                                  user_id, self.id)
        else:
            f_estimated_company_arrival_date = self.f_estimated_company_arrival_date
        if 'f_real_company_arrival_date' in vals:
            f_real_company_arrival_date = vals['f_real_company_arrival_date']
            self.dates_hist_audit('ATAF', self.f_real_company_arrival_date, f_real_company_arrival_date, user_id,
                                  self.id)
        else:
            f_real_company_arrival_date = self.f_real_company_arrival_date

        f_delta_shipping_date, f_delta_port_arrival_date, f_delta_company_arrival_date = self.calc_dates_diff(
            f_real_shipping_date, f_estimated_port_arrival_date,
            f_real_port_arrival_date, f_estimated_company_arrival_date, f_real_company_arrival_date)

        vals['f_delta_shipping_date'] = f_delta_shipping_date
        vals['f_delta_port_arrival_date'] = f_delta_port_arrival_date
        vals['f_delta_company_arrival_date'] = f_delta_company_arrival_date
        return super(F_Shipping_Details, self).write(vals)

    def calc_dates_diff(self, f_real_shipping_date, f_estimated_port_arrival_date,
                        f_real_port_arrival_date, f_estimated_company_arrival_date, f_real_company_arrival_date):
        fmt = '%Y-%m-%d'
        f_delta_shipping_date = False
        f_delta_port_arrival_date = False
        f_delta_company_arrival_date = False

        if f_estimated_port_arrival_date and f_real_port_arrival_date:
            d1 = datetime.strptime(str(f_estimated_port_arrival_date), fmt)
            d2 = datetime.strptime(str(f_real_port_arrival_date), fmt)

            f_delta_port_arrival_date = str((d2 - d1).days)

        if f_estimated_company_arrival_date and f_real_company_arrival_date:
            d1 = datetime.strptime(str(f_estimated_company_arrival_date), fmt)
            d2 = datetime.strptime(str(f_real_company_arrival_date), fmt)

            f_delta_company_arrival_date = str((d2 - d1).days)

        return f_delta_shipping_date, f_delta_port_arrival_date, f_delta_company_arrival_date

    def f_ship_dates_history_action_window(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Shipping Dates History',
            'view_mode': 'tree',
            'res_model': 'f.ship.dates.hist',
            'target': 'current',
            'domain': [('f_shipping_id', '=', self.id)],
            'context': {'create': False},
        }

    def f_onchange_ETAF(self):
        for line in self.f_po_plan_id:
            line.f_estimated_company_arrival_date = self.f_estimated_company_arrival_date

    def f_onchange_ETD(self):
        fmt = '%Y-%m-%d'
        for line in self.f_po_plan_id:
            if line.f_ready_to_shipping_date and line.f_estimated_shipping_date:
                d1 = datetime.strptime(str(line.f_ready_to_shipping_date), fmt)
                d2 = datetime.strptime(str(line.f_estimated_shipping_date), fmt)

                f_delta_port_arrival_date = str((d1 - d2).days)
                line.f_delta_shipping_date = f_delta_port_arrival_date

    def f_change_planning_state(self):
        for line in self.f_po_plan_id:
            line.f_stat = self.f_shipp_stage
