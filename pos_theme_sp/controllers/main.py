# -*- coding: utf-8 -*-

import json
import logging
import werkzeug.utils
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)
from odoo.addons.point_of_sale.controllers.main import PosController


class PosController(PosController):
    @http.route('/pos/web', type='http', auth='user')
    def pos_web(self, debug=False, **k):
        pos_sessions = request.env['pos.session'].search([('state', '=', 'opened'), ('user_id', '=', request.session.uid)])
        if not pos_sessions:
            return werkzeug.utils.redirect('/web#action=point_of_sale.action_client_pos_menu')
        pos_sessions.login()
        context = {
            'session_info': json.dumps(request.env['ir.http'].session_info()),
            'theme_id': pos_sessions.config_id.theme_type if pos_sessions.config_id.allow_pos_theme else '',
        }
        return request.render('point_of_sale.index', qcontext=context)
