from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager

class YourController(CustomerPortal):
    @http.route("/my/business_requirement/print/<model('business.requirement'):br_id>", type='http', auth='user', website=True)
    def print_report(self, br_id ,**kw):

        return self._show_report(model=br_id,report_type='pdf',
                                report_ref="br_reports.business_new_requirement_report",
                                download=True )
