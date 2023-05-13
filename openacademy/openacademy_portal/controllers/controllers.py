# -*- coding: utf-8 -*-
from odoo.http import content_disposition, Controller, request, route
from odoo import fields as odoo_fields, http, tools, _, SUPERUSER_ID
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager

    # RUTA DE CURSO
class UserPortal(CustomerPortal):

    def _prepare_home_portal_value(self, counters):
        values = super()._prepare_home_portal_value(counters)
        if 'sessions_count' in counters:
            values['sessions_count'] = request.env['openacademy.sessions'].search_count(['attendees', '=', request.env.user.partner_id.id]) \
                if request.env['openacademy.sessions'].check_access_rights('read', raise_exception=False) else 0

    # RUTA DEL PORTAL
    @http.route(['/my/sessions', '/my/sessions/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_sessions(self, page=0):
        uid = request.env.user.partner_id.id
        name = request.env.user.partner_id.name
        session = request.env['openacademy.sessions'].sudo().search([('attendees','=', int(uid))])
        sessions_count = request.env['openacademy.sessions'].sudo().search_count([('attendees','=', int(uid))])
        pager = request.website.pager(
                url='/my/sessions',
                total= sessions_count,
                page=page,
                step=5,
            )

        offset = pager['offset']
        session = session[offset: offset + 5]    
        return request.render('openacademy_portal.portal_my_sessions', {
            'sessions': session,
            'pager': pager,
            'total': sessions_count,
            # 'name': name,
            
        })


    # RUTA DE SESIONES DENTRO DE PORTAL
    @http.route(['/my/sessions/<session_namee>', '/my/sessions/<session_namee>/page/<int:page>'], auth='user', website=True)
    def session_detail(self, session_namee, page=0):
        session = request.env['openacademy.sessions'].sudo().search([('id','=', int(session_namee))])
        course_nam = request.env['openacademy.sessions'].sudo().search([('id','=', int(session_namee))]).course_name.name

        pager = request.website.pager(
                url='/my/sessions/%s' % session_namee,
                total=session.sudo().search_count([('id','=', int(session_namee))]),
                page=page,
                step=3,
            )

        offset = pager['offset']
        session = session[offset: offset + 3]    
        return request.render('openacademy_portal.my_sessions', {
            'course': course_nam,
            'sessions': session,
            'pager': pager,
        
        })

    # RUTA DE REGISTRO A SESIONES
    @http.route('/add_user_to_session/<int:session>', type='http', auth='user', website=True)
    def add_user_to_session_submit(self, session):
        user_id = request.env.user.partner_id.id
        session_w = request.env['openacademy.sessions'].sudo().browse(session)
        session_w.update({'attendees': [(4, user_id)]})
        message = "You have been registered to the session successfully!"
        return request.render('openacademy_portal.register_to_session_success', {'message': message})

    # RUTA DE CANCELAR REGISTRO A SESIONES
    @http.route('/delete_user_to_session/<int:session>', type='http', auth='user', website=True)
    def delete_user_to_session_submit(self, session):
        user_id = request.env.user.partner_id.id
        # Busca la sesión correspondiente
        session = request.env['openacademy.sessions'].sudo().search([('id', '=', session)])

        # Si la sesión existe
        if session:
            # Crea una lista de tuplas con el campo attendees actualizado
            updated_values = [(3, user_id)]
            # Actualiza el registro de la sesión
            session.write({'attendees': updated_values})

        message = "You have been deleted to the session successfully!"
        return request.render('openacademy_portal.delete_to_session_success', {'message': message})
