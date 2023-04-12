# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class course(models.Model):

    _name = 'openacademy.course'
    _description = 'Esto es una descripcion!'
    _rec_name = "name"
    _sql_constraints = [('name_unique', 'unique(name)','Course name must be unique'), ('title_unique','CHECK(title IS DISTINCT FROM description)','TITLE SAME AS DESCRIPTION'), ]

    name = fields.Char(compute='_course_name', store=True)
    title = fields.Char(required=True)
    description = fields.Char()
    responsible = fields.Many2one(comodel_name='res.users')
    name_responsible = fields.Char(related='responsible.name', string='Responsible name')
    sessions = fields.One2many('openacademy.sessions', 'course_name', string='Sessions')
    contenido = fields.Html("Content")
    image = fields.Many2many(comodel_name='openacademy.gallery', relation='course_gallery_rel', column1='course_id', column2='gallery_id', string='Gallery')
    attachment_ids = fields.Many2many(comodel_name='ir.attachment', string='Attachments')

    num_attachments = fields.Integer(compute='_get_num_attachments', string='Number of attachments')

    @api.depends('attachment_ids')
    def _get_num_attachments(self):
        for record in self:
            record.num_attachments = len(record.attachment_ids)
            
    
    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        if default is None:
            default = {}
        if not default.get('name'):
            default['name'] = "Copy of " + "("+self.name+")"
        return super(course, self).copy(default)
    
    @api.depends('title', 'responsible')
    def _course_name(self):
        for record in self:
            record.name = f"{record.title} - {record.responsible.name}"

