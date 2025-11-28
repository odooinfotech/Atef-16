from odoo import models, fields, api


class F_Shipping_Dates_History(models.Model):
    _name='f.ship.dates.hist'
    _order ='f_updated_at'
    _description = 'Shipping Dates History'
    
    
    f_date_name = fields.Char(string="Date Name")
    f_from_date = fields.Date(string="From Date")
    f_to_date = fields.Date(string="To Date")
    f_user_id = fields.Many2one('res.users', string="User")
    f_user = fields.Char(string="User")
    f_updated_at = fields.Date(string="Date")
    f_shipping_id = fields.Many2one('f.shipping.details', string="Shipping")
