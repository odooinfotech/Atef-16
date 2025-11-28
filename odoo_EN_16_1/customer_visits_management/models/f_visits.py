from odoo import models, fields, api, _
import calendar
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from datetime import date
from odoo.exceptions import UserError, ValidationError


class FVisits(models.Model):
    _name = 'f.visits'
    _description = 'Visits'
    _rec_name = "f_customer"

    f_customer = fields.Many2one('res.partner', string="Customer Name", required=True)
    f_date = fields.Date(string="Date", required=True, default=fields.Date.context_today)
    f_date_from = fields.Datetime(string="Time From", default=fields.Date.context_today)
    f_date_to = fields.Datetime(string="Time To", default=fields.Date.context_today)
    f_note = fields.Char(string="Notes")
    f_route = fields.Many2one("f.customer.routes", string="Route", required=True)

    def _set_default_sp(self):
        self.f_sales_person = self.env.user.id
        return self.env.user.id

    f_sales_person = fields.Many2one('res.users', string="Sales Person", default=_set_default_sp)
    sequence = fields.Integer(string='Sequence', default=0)
    f_payments_total = fields.Float(string="Total Payments")
    f_sales_total = fields.Float(string="Total Sales", store=True)
    f_invoice_total = fields.Float(string="Total Invoices")
    f_reason_cancel = fields.Char(string="Reason Of Cancel")
    state = fields.Selection([('draft', 'Draft'), ('done', 'Done'), ('cancel', 'Cancelled')], default='draft',
                             string="Status")
    f_sales_perc = fields.Float(string="%", store=True)

    f_partner_latitude = fields.Float(string='Partner Latitude', related='f_customer.partner_latitude')
    f_partner_longitude = fields.Float(string='Partner Longitude', related='f_customer.partner_longitude')

    f_checkin_latitude = fields.Float(string='Check In Latitude')
    f_checkin_longitude = fields.Float(string='Check In Longitude')

    f_deference = fields.Float(string='Deference')

    def get_total_sales(self):
        recs = self
        if not recs:
            recs = self.sudo().search([])
        for rec in recs:
            target = self.env['f.cust.target'].search([('f_target_type', '=', 'sales'),
                                                       ('f_customer', '=', rec.f_customer.id),
                                                       ('active', '=', True),
                                                       ('f_status', '=', 'inprogress')], limit=1)
            target.get_total_sales()
            print("Visits Target", target)
            print("Visits Target Sale", target.f_total_sales)
            rec.f_sales_total = target.f_total_sales
            rec.f_sales_perc = target.f_sales_perc

    def get_allowed_user(self):
        self.f_allowed_user = False
        for visit in self:
            print('f_allowed_user', visit.f_allowed_user, self.env.user.id, visit.f_sales_person.id)
            if (self.env.user.id == visit.f_sales_person.id or
                    self.user_has_groups('customer_visits_management.customer_visits_admin')):
                visit.f_allowed_user = True

    f_allowed_user = fields.Boolean(string="check", compute="get_allowed_user", default=True)

    def write(self, vals):
        cancel_reason = self.env['f.cancel.wizard'].search([('f_visit', '=', self._origin.id)], limit=1).f_reason_cancel
        if cancel_reason:
            cancel_reason = cancel_reason.replace("<p>", "")
            cancel_reason = cancel_reason.replace("</p>", "")
            print(vals, cancel_reason)
            vals['f_reason_cancel'] = cancel_reason
        print('vals', vals)
        res = super(FVisits, self).write(vals)
        return res

    @api.onchange('f_sales_person')
    def _f_onchange_sp(self):
        if (self.env.user.id != self.f_sales_person.id and
                not self.user_has_groups('customer_visits_management.customer_visits_admin')):
            raise UserError('You Are not allowed to change the Sales Person')

    @api.onchange('f_customer')
    def _f_onchange_customer(self):
        self.f_route = False
        route_id = self.env['res.partner'].search([('id', '=', self.f_customer.id)]).f_route.id
        self.f_route = route_id
        domain = [('id', '=', route_id)]
        return {'domain': {'f_route': domain}}

    @api.onchange('f_date')
    def _f_onchange_date(self):
        self.f_date_from = self.f_date
        self.f_date_to = self.f_date

    @api.onchange('f_date_from', 'f_date_to')
    def _f_onchange_from_to_date(self):
        print(self.f_date_from.date())
        if self.f_date_from.date() != self.f_date:
            raise ValidationError(_("From date must be the same date you entered."))
        elif self.f_date_to.date() != self.f_date:
            raise ValidationError(_("To date must be the same date you entered."))

    #     def createQuotation(self):
    #         return {
    #             'name':'Quotations',
    #             'view_mode': 'tree,form',
    #             'res_model': 'sale.order',
    #             'domain': [('f_visit', '=', self.id)],
    #             'type': 'ir.actions.act_window',
    #
    #                 }
    #
    #
    #
    #     def createInvoice(self):
    #         return {
    #             'name':'Invoice',
    #             'view_mode': 'tree,form',
    #             'res_model': 'account.move',
    #             'domain': [('f_visit', '=', self.id)],
    #             'type': 'ir.actions.act_window',
    #             }
    #
    #     def createPayment(self):
    #         return {
    #             'name':'Payment',
    #             'view_mode': 'tree,form',
    #             'res_model': 'f.multi.payments',
    #             'type': 'ir.actions.act_window',
    #             'domain': [('f_visit', '=', self.id)],
    #             }

    def done(self):
        self.state = 'done'

    def target(self):
        print('self.f_customer', self.f_customer)
        action = {
            'name': _('Target'),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'f.cust.target',
            'domain': [('active', '=', True), ('f_customer', '=', self.f_customer.id), ('f_status', '=', 'inprogress')],
        }
        return action

    def aging(self):
        action = {
            'name': _('Partner Aging Report'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'f.partner.aging.wizard',
            'target': 'new',
            #  'domain':['partner_id','=',self.f_customer.id],
            'context': {'default_partner_id': self.f_customer.id},
        }

        return action

    def create_visits(self):
        # date = self.search([]).f_date
        today = date.today()
        for i in range(0, 7):
            weekdays = today + timedelta(days=i)
            print(weekdays)
            weekdays_name = calendar.day_name[weekdays.weekday()].lower()
            routes = self.env['f.customer.routes'].search([('f_days', '=', weekdays_name)])
            for route in routes:
                customers = self.env['res.partner'].search([('f_route', '=', route.id)])
                for customer in customers:
                    today_visit = self.search([('f_customer', '=', customer.id), ('f_date', '=', weekdays)])
                    if not today_visit:
                        freq_date = weekdays
                        last_visit = self.search([('f_customer', '=', customer.id)], order='f_date desc', limit=1)
                        if last_visit:
                            if customer.f_frequency_unit == 'days':
                                freq_date = last_visit.f_date + timedelta(days=customer.f_frequency)
                            elif customer.f_frequency_unit == 'weeks':
                                freq_date = last_visit.f_date + timedelta(weeks=customer.f_frequency)
                            elif customer.f_frequency_unit == 'months':
                                freq_date = last_visit.f_date + relativedelta(months=customer.f_frequency)
                            elif customer.f_frequency_unit == 'years':
                                freq_date = last_visit.f_date + relativedelta(years=customer.f_frequency)
                        if freq_date <= weekdays:
                            visit_values = {
                                'f_customer': customer.id,
                                'f_date': weekdays,
                                'f_date_from': weekdays,
                                'f_date_to': weekdays,
                                'f_route': route.id,
                                'f_sales_person': customer.user_id.id,
                            }

                            self.env['f.visits'].sudo().create(visit_values)
