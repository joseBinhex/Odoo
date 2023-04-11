# -*- coding: utf-8 -*-
# from odoo import http


# class OpenacademyCrm(http.Controller):
#     @http.route('/openacademy_crm/openacademy_crm/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/openacademy_crm/openacademy_crm/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('openacademy_crm.listing', {
#             'root': '/openacademy_crm/openacademy_crm',
#             'objects': http.request.env['openacademy_crm.openacademy_crm'].search([]),
#         })

#     @http.route('/openacademy_crm/openacademy_crm/objects/<model("openacademy_crm.openacademy_crm"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('openacademy_crm.object', {
#             'object': obj
#         })
