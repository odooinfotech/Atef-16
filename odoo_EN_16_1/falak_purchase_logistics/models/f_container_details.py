# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class F_Container_Details(models.Model):
    _name = 'f.container.details'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'f_container_name'
    _description = 'Container Details'
    _order = 'create_date DESC'

    # To represent the rec name with this formula:(container name/container number)
    def name_get(self):
        result = []
        for rec in self:
            if rec.f_container_name and rec.f_container_number:
                name = rec.f_container_name + '/' + rec.f_container_number
                print('name', name)
                result.append((rec.id, name))
        return result

    f_container_name = fields.Char(string="Container Name", required=True)
    f_container_size = fields.Many2one('f.container.size', string="Container Type(Size)")
    f_container_number = fields.Char(string="Container Number", required=True)
    f_total_weight = fields.Float(string="Total Weight KG")

    f_qty_in_con = fields.Float(string="Qty In Container")
    f_bl_number = fields.Char(string="B/L Number")
    f_con_shipping = fields.Many2one('f.shipping.details', string="Shipping", tracking=True)
    f_storage = fields.Char(string="Storage", help="External Storage Location")
    f_port_fees = fields.Float(string="Port Fees")
    f_storage_fees = fields.Float(string="Storage Fees")
    f_transport = fields.Float(string="Transport", help="Transport Fees")

    f_demurrage = fields.Char(string="Demurrage", compute='f_compute_demurrage', store=True,
                              help="Number of Days Exceeding Container Return")
    f_demurrage_amount = fields.Float(string="Demurrage Amount", help="Demurrage Amount")
    f_lc_details = fields.Many2one('f.lc.management', string="LC")

    f_security_check = fields.Boolean(string="Security Check")
    f_date_hour = fields.Datetime(string="Data & Hour (SC)")

    f_container_plans = fields.One2many('f.container.plans', 'f_container_details', string="Container Plans")

    f_shipping_lc_number = fields.Char(related="f_con_shipping.f_lc_number", string="LC Number")
    f_shipping_ATA_date = fields.Date(related="f_con_shipping.f_real_port_arrival_date", string="ATA")
    f_date_entered_company = fields.Datetime(string="Date Entered To Company")
    f_date_exit_company = fields.Datetime(string="Date Exist From Company")
    f_date_returned_to_port = fields.Date(string="Date Returned To Port")

    f_deliver_date = fields.Date(string="Deliver Date to WH", tracking=True)
    f_notes = fields.Char(string="Notes")

    @api.depends('f_date_returned_to_port', 'f_shipping_ATA_date')
    def f_compute_demurrage(self):
        for rec in self:
            if rec.f_date_returned_to_port and rec.f_shipping_ATA_date:
                delta = rec.f_date_returned_to_port - rec.f_shipping_ATA_date
                rec.f_demurrage = delta.days + 1
            else:
                rec.f_demurrage = 0

    def f_add_plan_in_container_plans(self):
        action = {
            'name': _('Shipping Plans'),
            'view_mode': 'tree',
            'res_model': 'f.purchase.order.planning',
            'view_id': self.env.ref(
                'falak_purchase_logistics.f_purchase_planning_list').id,
            'type': 'ir.actions.act_window',
            'target': 'new',
            'domain': [('f_shipping', '=', self.f_con_shipping.id)],
            'context': {
                'create': False,
                'edit': False,
                'delete': False,
                'container_id': self.id,
            },
        }
        return action
