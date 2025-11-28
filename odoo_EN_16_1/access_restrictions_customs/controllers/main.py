from odoo.addons.web.controllers import home
from odoo.http import request
from odoo.exceptions import Warning
import odoo
from odoo import fields
from datetime import datetime, timedelta
from pytz import timezone, UTC
import odoo.modules.registry
from odoo.tools.translate import _
from odoo import http
from odoo.addons.web.controllers.utils import ensure_db, _get_login_redirect_url, is_user_internal
import logging
from odoo.addons.resource.models.resource import float_to_time

_logger = logging.getLogger(__name__)

SIGN_UP_REQUEST_PARAMS = {'db', 'login', 'debug', 'token', 'message', 'error', 'scope', 'mode',
                          'redirect', 'redirect_hostname', 'email', 'name', 'partner_id',
                          'password', 'confirm_password', 'city', 'country_id', 'lang', 'signup_email'}


class HomeCustom(home.Home):

    @http.route('/web/login', type='http', auth="none")
    def web_login(self, redirect=None, **kw):
        ensure_db()
        request.params['login_success'] = False

        if 'login' not in request.params:
            return request.render('web.login')

        if request.httprequest.method == 'GET' and redirect and request.session.uid:
            return request.redirect(redirect)

        if request.env.uid is None:
            if request.session.uid is None:
                request.env["ir.http"]._auth_method_public()
            else:
                request.update_env(user=request.session.uid)

        values = {k: v for k, v in request.params.items() if k in SIGN_UP_REQUEST_PARAMS}
        try:
            values['databases'] = http.db_list()
        except odoo.exceptions.AccessDenied:
            values['databases'] = None

        user_rec = request.env['res.users'].sudo().search(
            [('login', '=', request.params['login'])])

        login_from_hour = user_rec.login_from_hour
        login_to_hour = user_rec.login_to_hour

        tz = user_rec.tz
        user_timezone = timezone(tz)
        local_timezone = timezone('UTC')
        local_date = local_timezone.localize(fields.Datetime.now()).astimezone(timezone(tz))
        current_hour = local_date.hour

        today_date = datetime.now().date()
        expiration_time = user_timezone.localize(datetime.combine(today_date, float_to_time(login_to_hour))).astimezone(
            UTC).replace(tzinfo=None)
        user_rec.expiration_time = expiration_time

        if not login_from_hour == 0.0 and not login_to_hour == 0.0:
            if not (login_from_hour <= current_hour <= login_to_hour):
                _logger.warning("User not allowed to login at this time.")
                values['error'] = _("Not allowed to login at this time")
                return request.render('web.login', values)

        response = super(HomeCustom, self).web_login(redirect=redirect, **kw)
        return response

