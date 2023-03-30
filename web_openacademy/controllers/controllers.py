from odoo import http
from odoo.http import request, Controller
import base64
from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.web.controllers.main import content_disposition

class OpenAcademyController(http.Controller):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'sessions_count' in counters:
            values['sessions_count'] = request.env['openacademy.sessions'].search_count([]) \
                if request.env['openacademy.sessions'].check_access_rights('read', raise_exception=False) else 0
        return values

    # RUTA DE CURSO

    @http.route(['/courses', '/courses/page/<page>'], auth='public', website=True)
    def list_courses(self, page=0, search='', order='', **post):
        courses = request.env['openacademy.course'].search([])

        if search:
            courses = courses.search([('title', 'ilike', search)])

        if order:
            order_field = order 
            courses = courses.sorted(order_field)

        pager = request.website.pager(
            url='/courses',
            total=courses.sudo().search_count([]),
            page=page,
            step=2,
        )
        uid = request.env.user.partner_id.id

        # Add filter for available sessions
        courses = courses.filtered(lambda c: not c.sessions or request.env['openacademy.sessions'].search([('id', 'not in', c.sessions.ids)]))

        keep = QueryURL('/courses', search=search, order=post.get('order'))

        offset = pager['offset']
        courses = courses[offset: offset + 2]

        return request.render('web_openacademy.data_template', {
            'courses': courses,
            'pager': pager,
            'search': search,
            'order': order,
            'keep': keep,
        })

        
    # RUTA CURSOS ESPECIFICO
    @http.route(['/course/data/<int:course_name>'], auth='public', website=True)
    def plus_course(self, course_name):
        course = request.env['openacademy.course'].sudo().search([('id','=', course_name)])
        return request.render('web_openacademy.plus_course', {
            'courses': course,
        })

    # RUTA DE SESIONES POR CURSO
    @http.route(['/course/<course_namee>', '/course/<course_namee>/page/<page>'], auth='public', website=True)
    def course_sessions(self, course_namee, page=0):
        session = request.env['openacademy.sessions'].sudo().search([('course_name','=', int(course_namee))])
        course_nam = request.env['openacademy.sessions'].sudo().search([('course_name','=', int(course_namee))]).course_name.name
        uid = request.env.user.partner_id.id
        pager = request.website.pager(
                url='/course/%s' % course_namee,
                total=session.sudo().search_count([('course_name','=', int(course_namee))]),
                page=page,
                step=1,
            )

        offset = pager['offset']
        session = session[offset: offset + 1]    
        return request.render('web_openacademy.course_sessions', {
            'course': course_nam,
            'sessions': session,
            'pager': pager,
            'userid': uid,
        })

    ## RUTA DEL PORTAL
    @http.route(['/my/sessions', '/my/sessions/page/<page>'], type='http', auth="user", website=True)
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
        return request.render('web_openacademy.portal_my_sessions', {
            'sessions': session,
            'pager': pager,
            'total': sessions_count,
            # 'name': name,
            
        })


    # RUTA DE SESIONES DENTRO DE PORTAL
    @http.route(['/my/sessions/<session_namee>', '/my/sessions/<session_namee>/page/<page>'], auth='user', website=True)
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
        return request.render('web_openacademy.my_sessions', {
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
        return request.render('web_openacademy.register_to_session_success', {'message': message})

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
        return request.render('web_openacademy.delete_to_session_success', {'message': message})

    # RUTA DE DESCARGA DE ARCHIVOS
    @http.route(['/web/content/<int:id>'], type='http', auth='public', website=True)
    def download_attachment(self, id):
        attachment = request.env['ir.attachment'].sudo().search([('id','=', id)])
        if attachment.exists():
            content_base64 = attachment.datas and attachment.datas.decode('base64') or ''
            content = base64.b64decode(content_base64)
            headers = [
                ('Content-Type', 'application/octet-stream'),
                ('Content-Disposition', content_disposition(attachment.name))
            ]
            response = request.make_response(content, headers=headers)
            return response
        else:
            return "Attachment not found"

    # RUTA DE TODOS LOS ARCHIVOS
    @http.route('/course/<int:course>/attachments', type='http', auth='public', website=True)
    def all_attachments(self, course):
        course = request.env['openacademy.course'].sudo().search([('id','=', course)])
        return request.render('web_openacademy.all_attachmentos', {'courses': course})