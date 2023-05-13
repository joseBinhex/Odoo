from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging
import time
from odoo.addons.web.controllers.main import clean_action
_logger = logging.getLogger(__name__)

class joinSes(models.TransientModel):
    _name = 'openacademy.joinses'
    _description = 'Wizard creation'

    # default fields for session
    def _default_session(self):
        active_id = self.env.context.get('active_id')
        if active_id:
            return self.env['openacademy.sessions'].browse((active_id))
        else:
            return False

    # default fields for partner
    def _default_partner(self):
        return [(6, 0, [self.env.user.partner_id.id])]

    sesion_name = fields.Many2many(comodel_name='openacademy.sessions', string=_("Session Name"), default=_default_session)
    partners_name = fields.Many2many(comodel_name='res.partner', string=_("Partner's Name"), default=_default_partner)
    is_attendee = fields.Boolean(string="Is Attendee", compute='_compute_is_attendee', store=True)
    
    # button sub
    def subscribe(self):
        for session in self.sesion_name:
            session.attendees |= self.partners_name
        action = self.env.ref('openacademy_menu.session_kanban_custom').read()[0]
        ir_model_data = self.env['ir.model.data']
        view_id = ir_model_data.get_object_reference('openacademy_menu', 'session_kanban_custom')[1]
        return {'type': 'ir.actions.act_window', 
                'res_model': 'openacademy.sessions', 
                'view_mode': 'kanban', 
                'view_type': 'kanban', 
                'views': [(view_id, 'kanban')], 
                'target': 'current',
                'context': {'create':False}
                }


    # button unsub  
    def unsubscribe(self):
        for session in self.sesion_name:
            session.attendees -= self.partners_name        
        return {
            'type': 'ir.actions.client',
            'tag': 'reload_context',
        }

    # calculated field for button sub/unsub
    @api.depends('sesion_name', 'partners_name')
    def _compute_is_attendee(self):
        for wizard in self:
            is_attendee = False
            for session in wizard.sesion_name:
                if self.env.user.partner_id.id in session.attendees.ids:
                    is_attendee = True
                    break
            wizard.is_attendee = is_attendee

        