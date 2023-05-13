# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.addons.base.models.ir_attachment import IrAttachment
import logging

_logger = logging.getLogger(__name__)

class course(models.Model):

    _name = 'openacademy.course'
    _description = 'Esto es una descripcion!'
    _rec_name = "name"
    _sql_constraints = [('name_unique', 'unique(name)','Course name must be unique'), ('title_unique','CHECK(title IS DISTINCT FROM description)','TITLE SAME AS DESCRIPTION'), ]

    name = fields.Char(compute='_course_name',string=_("Name") ,store=True)
    title = fields.Char(string=_("Title"), required=True)
    description = fields.Char(string=_("Description"))
    responsible = fields.Many2one(string=_("Responsible"), comodel_name='res.users')
    name_responsible = fields.Char(related='responsible.name', string=_('Responsible name'))
    sessions = fields.One2many('openacademy.sessions', 'course_name', string=_('Sessions'))
    contenido = fields.Html("Content")
    image = fields.Many2many(comodel_name='openacademy.gallery', relation='course_gallery_rel', column1='course_id', column2='gallery_id', string=_('Gallery'))
    attachment_ids = fields.Many2many(comodel_name='ir.attachment', string=_('Attachments'))
    num_attachments = fields.Integer(compute='_get_num_attachments', string=_('Number of attachments'))

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

    @api.model
    def create(self, vals):
        cours = super(course, self).create(vals)
        for attachment in cours.attachment_ids:
            if not attachment.access_token:
                attachment.generate_access_token()
        return cours