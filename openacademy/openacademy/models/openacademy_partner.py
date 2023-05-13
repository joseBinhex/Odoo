
from odoo import models, fields, api, _

class partner(models.Model):
    _inherit = 'res.partner'
    _description = 'Esto es una descripcion!'

    instructor = fields.Boolean(string=_('Instructor'))
    session_partner = fields.Many2many(comodel_name='openacademy.sessions', string=_('Session Partner'))