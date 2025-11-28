# -*- coding: utf-8 -*-

from odoo import models, fields, api


class FCustomerRoute(models.Model):
    _name = 'f.customer.routes'
    _description = 'Customer Routes'
    _rec_name="f_name"

    f_name = fields.Char(string="Name")
    f_note = fields.Text(string="Note")
    f_days = fields.Selection([('saturday','Saturday'),('sunday','Sunday'),('monday','Monday'),('tuesday','Tuesday'),('wednesday','Wednesday'),('thursday','Thursday'),('friday','Friday')],string="Day",required=True)
