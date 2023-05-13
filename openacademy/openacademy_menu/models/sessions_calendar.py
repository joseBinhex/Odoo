# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class getColors(models.Model):
    _inherit = "openacademy.sessions"

    get_color = fields.Integer(compute='_get_color', store=True)


    @api.depends('taken_seats')
    def _get_color(self):
        for record in self:
            if record.taken_seats < 100:
                record.get_color = 10 # verde
            else:
                record.get_color = 1 # rojo