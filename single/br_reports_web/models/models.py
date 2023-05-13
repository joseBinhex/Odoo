# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.http import request

class br_reports_web(models.Model):
    _inherit = ['business.requirement', 'portal.mixin']
    _name = 'business.requirement'

    def _get_report_base_filename(self):
        return self.name