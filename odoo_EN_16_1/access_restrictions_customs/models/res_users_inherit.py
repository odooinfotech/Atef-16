from odoo import models, fields, api
from odoo import http
from odoo.http import request
from pytz import timezone
from datetime import datetime, timedelta
import requests

import logging
_logger = logging.getLogger(__name__)

class ResUsersInherit(models.Model):
    _inherit = 'res.users'

    login_from_hour = fields.Float(string='From Hour')
    login_to_hour = fields.Float(string='To Hour')
    
    auto_logout_flag = fields.Boolean(string='Auto Logout',store=True)
    expiration_time = fields.Datetime(string='Expiration Time', help='Time when the user session will expire')

    def _perform_logout_actions(self):
        _logger.info("/////////////////////////////Checking and logging out expired users...")
        current_time = fields.Datetime.now()
        expired_users = self.search([('auto_logout_flag','=',True),('expiration_time','<=',current_time)])
        _logger.info("///////////////////////////////Expired Users: %s", expired_users.ids)
        
        for user in expired_users:
            logout_url = "{}/web/session/logout".format(self.env['ir.config_parameter'].sudo().get_param('web.base.url'))
            response = requests.get(logout_url)
            if response.status_code == 200:
                _logger.warning("User %s logged out due to exceeding login time", user.name)
            else:
                _logger.error("Failed to log out user %s. Status code: %s", user.name, response.status_code)