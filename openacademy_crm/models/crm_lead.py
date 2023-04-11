from odoo import api, fields, models
import logging
from odoo.http import request
_logger = logging.getLogger(__name__)


class Lead(models.Model):
    _inherit = 'crm.lead'
    course_id = fields.Many2one('openacademy.course', string="Course")

    def send_confirmation_email(self):
        # Envía un correo electrónico de confirmación utilizando una plantilla de correo electrónico
        template_id = self.env.ref('openacademy_crm.email_template_confirmationC').id
        template = self.env['mail.template'].browse(template_id)
        template.send_mail(self.id, force_send=True)

    @api.model
    def create(self, vals):

        # Modificar el nombre para organizacion
        if 'name' in vals:
            course_name = vals['name'] + ' ('+ self.env['openacademy.course'].browse(course_id).name +')'
        else:
            course_name = self.env['openacademy.course'].browse(course_id).name
            
        vals.update({'name': course_name})
        lead = super(Lead, self).create(vals)
        # _logger.info('****************************************** %s', vals)
        if 'active' in vals and vals['active'] == True:
            lead.send_confirmation_email()
        return lead


