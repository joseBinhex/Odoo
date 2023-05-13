from odoo import http
from odoo.http import request, Controller
import base64
from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.web.controllers.main import content_disposition

class OpenAcademyController(http.Controller):

    # RUTA DE CURSO

    @http.route(['/courses', '/courses/page/<page>'], auth='public', website=True)
    def list_courses(self, page=0, search='', order='', filt='', **post):
        courses = request.env['openacademy.course'].search([])

        if search:
            courses = courses.search([('title', 'ilike', search)])

        if order:
            order_field = order 
            courses = courses.sorted(order_field)

        post['order'] = order

        post['filt'] = filt

        pager = request.website.pager(
            url='/courses',
            total=courses.sudo().search_count([]),
            page=page,
            step=2,
            url_args=post,
        )
        
        uid = request.env.user.partner_id.id

        enrolled_sessions = request.env['openacademy.sessions'].search([('attendees', 'in', uid)])

        # Add filter for available sessions
        if filt:
            courses = courses.filtered(lambda c: not c.sessions or all(session not in enrolled_sessions for session in c.sessions))

        keep = QueryURL('/courses', search=search, order=post.get('order'))

        offset = pager['offset']
        courses = courses[offset: offset + 2]

        return request.render('openacademy_web.data_template', {
            'courses': courses,
            'pager': pager,
            'search': search,
            'order': order,
            'keep': keep,
            'filt': filt,
        })

        
    # RUTA CURSOS ESPECIFICO
    @http.route(['/course/data/<int:course_name>'], auth='public', website=True)
    def plus_course(self, course_name):
        course = request.env['openacademy.course'].sudo().search([('id','=', course_name)])
        return request.render('openacademy_web.plus_course', {
            'courses': course,
            'images': course.image,
        })

    # RUTA DE SESIONES POR CURSO
    @http.route(['/course/<int:course_namee>', '/course/<int:course_namee>/page/<int:page>'], auth='public', website=True)
    def course_sessions(self, course_namee, page=0):
        session = request.env['openacademy.sessions'].sudo().search([('course_name','=', course_namee)])
        course_nam = request.env['openacademy.sessions'].sudo().search([('course_name','=', course_namee)]).course_name.name
        course_id = request.env['openacademy.course'].sudo().browse(course_namee)
        uid = request.env.user.partner_id.id
        pager = request.website.pager(
                url='/course/%s' % course_namee,
                total=request.env['openacademy.sessions'].sudo().search_count([('course_name','=', course_namee)]),
                page=page,
                step=2,
            )

        offset = pager['offset']
        session = session[offset: offset + 2]    
        return request.render('openacademy_web.course_sessions', {
            'course': course_nam,
            'sessions': session,
            'pager': pager,
            'userid': uid,
            'course_id': course_id,
        })

    # RUTA DE TODOS LOS ARCHIVOS
    @http.route('/course/<int:course>/attachments', type='http', auth='public', website=True)
    def all_attachments(self, course):
        course = request.env['openacademy.course'].sudo().search([('id','=', course)])
        return request.render('openacademy_web.all_attachmentos', {'courses': course})
    