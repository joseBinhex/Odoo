from odoo import models, fields, api
from odoo.exceptions import ValidationError

class sessions(models.Model):
    _name = 'openacademy.sessions'
    _description = 'Esto es una descripcion!'
    _inherit = ['portal.mixin', 'mail.thread.cc', 'mail.activity.mixin']
    _rec_name = "name"

    name = fields.Char(required=True)
    finish_date = fields.Date()
    duration = fields.Float(default=1)
    max_seats = fields.Integer(default=1)
    number_seats = fields.Integer(string="Attendees count", compute='_get_attendees', store=True)
    instructor = fields.Many2one('res.partner', domain="['|',('instructor','=','true'),('category_id','like','Teacher /')]")
    course_name = fields.Many2one('openacademy.course')
    attendees = fields.Many2many('res.partner', required=True)
    date_start = fields.Date(required=True)
    attendees_count = fields.Integer(string="Attendees count", compute='_get_attendees', store=True)
    taken_seats = fields.Integer(compute='_percentage_seats')
    localization = fields.Selection([('TF', 'Tenerife'), ('GC', 'Gran Canaria'), ('FTV', 'Fuerteventura')], default='TF')
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

