from odoo import http
from odoo.http import request
from odoo.addons.base.models import ir_http as ir_http_module

# Backup the original dispatch method
_original_dispatch = ir_http_module.IrHttp._dispatch


def _patched_dispatch(self):
    try:
        # Check only if user is logged in
        if request.session.uid:
            user = request.env['res.users'].sudo().browse(request.session.uid)

            # Only enforce IP logic if the user has IP restrictions
            if user.allowed_ips:
                # Get the current request IP
                current_ip = request.httprequest.headers.get('X-Forwarded-For') or request.httprequest.remote_addr
                stored_ip = request.session.get('client_ip')

                allowed_ips = [rec.ip_address for rec in user.allowed_ips]

                # First time: store the IP
                if not stored_ip:
                    request.session['client_ip'] = current_ip

                # IP changed or not in allowed list → logout
                elif stored_ip != current_ip or current_ip not in allowed_ips:
                    request.session.logout()
                    return request.redirect('/web/login?error=ip_changed')

    except Exception as e:
        # If something fails, safely rollback
        if hasattr(request, 'env') and request.env.cr:
            request.env.cr.rollback()

    # Proceed with the normal dispatch
    return _original_dispatch(self)


# Monkey patch only once
ir_http_module.IrHttp._dispatch = _patched_dispatch

