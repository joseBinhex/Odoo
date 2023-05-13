from odoo import models, fields, api, _


class AttendSes(models.TransientModel):
    _name = 'openacademy.attendses'
    _description = 'Wizard creation'
    
    def _default_session(self):
        return self.env['openacademy.sessions'].browse(self._context.get('active_id'))

    sesion_name = fields.Many2many(comodel_name='openacademy.sessions', default=_default_session, string=_("Session Name"))
    partners_name = fields.Many2many(comodel_name='res.partner', string=_("Partner's Name"))

    def subscribe(self):
        for session in self.sesion_name:
            session.attendees |= self.partners_name
        return {}