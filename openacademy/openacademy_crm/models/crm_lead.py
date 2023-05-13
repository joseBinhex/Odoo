from odoo import api, fields, models, _
import logging
from odoo.http import request
_logger = logging.getLogger(__name__)


class Lead(models.Model):
    _inherit = 'crm.lead'
    course_id = fields.Many2one('openacademy.course', string=_("Course"), store=True)

    def send_confirmation_email(self):
        # Envía un correo electrónico de confirmación utilizando una plantilla de correo electrónico
        template_id = self.env.ref('openacademy_crm.email_template_confirmationC').id
        template = self.env['mail.template'].browse(template_id)
        template.send_mail(self.id, force_send=True)

    @api.model
    def create(self, vals):
        # _logger.info('****************************************** %s', vals)
        if 'name' in vals and 'course_id' in vals:
            course_name = vals['name'] + ' ('+ self.env['openacademy.course'].browse(vals['course_id']).name +')'
            vals.update({'name': course_name})

        lead = super(Lead, self).create(vals)
        
        if 'active' in vals and vals['active'] == True:
            lead.send_confirmation_email()
        return lead