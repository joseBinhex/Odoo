from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class sessions(models.Model):
    _name = 'openacademy.sessions'
    _description = 'Esto es una descripcion!'
    _inherit = ['portal.mixin', 'mail.thread.cc', 'mail.activity.mixin']
    _rec_name = "name"

    def _get_category(self):
        cat1 = self.env.ref('openacademy.openacademy_teacher1')
        cat2 = self.env.ref('openacademy.openacademy_teacher2')
        return "['|',('instructor','=','true'),('category_id.id','in',[{},{}])]".format(cat1.id, cat2.id)

    name = fields.Char(string=_("Name"), required=True)
    duration = fields.Float(string=_("Duration"), default=1)
    number_seats = fields.Integer(string=_("Attendees count"), compute='_get_attendees', store=True)
    max_seats = fields.Integer(string=_("Max Seats"), default=1)
    instructor = fields.Many2one('res.partner',string=_("Instructor"), domain= _get_category)
    course_name = fields.Many2one('openacademy.course', string=_("Course"))
    attendees = fields.Many2many('res.partner', string=_('Attendees'), required=True)
    attendees_count = fields.Integer(string=_("Attendees count"), compute='_get_attendees', store=True)
    taken_seats = fields.Integer(string=_("Taken Seats"), compute='_percentage_seats')
    date_start = fields.Date(string=_("Start Date"),required=True)
    finish_date = fields.Date(string=_('Finish Date'))
    localization = fields.Selection([('TF', 'Tenerife'), ('GC', 'Gran Canaria'), ('FTV', 'Fuerteventura')], default='TF', string=_('Localization'))

    

    @api.depends('attendees')
    def _get_attendees(self):
        for r in self:
            r.attendees_count= len(r.attendees)

    @api.constrains('instructor', 'attendees')
    def _check_instructor(self):
        for record in self:
            ############ SE PUEDE HACER CON LA VARIABLE ATTENDEES
            if record.instructor in record.attendees:
                raise ValidationError("%s is on the attendees list" % record.instructor)
        # all records passed the test, don't return anything


    @api.depends('attendees_count', 'max_seats')
    def _percentage_seats(self):
        try:
            for record in self:
        
                total = (record.attendees_count / record.max_seats) * 100
                record.taken_seats = int(total)
        except: 
            record.taken_seats = 1

    @api.onchange('duration', 'max_seats')
    def _onchange_negative(self):
        # set auto-changing field
        if self.max_seats < 0:
        # Can optionally return a warning and domains
            return {
                'warning': {
                    'title': "Introduce positive numbers!",
                    'message': "0 It's not an option",
                },
            }
        if self.max_seats < len(self.attendees):
            return {
                'warning': {
                    'title': "No more Attendees!",
                    'message': "Increase max seats",
                },
            }
        
    @api.onchange('number_seats', 'max_seats')
    def _onchange_plus(self):
        # set auto-changing field
        if self.number_seats > self.max_seats:

        # Can optionally return a warning and domains
            return {
                'warning': {
                    'title': "U can't put more seats than the maximum!",
                    'message': "That's not an option",
                }
            }