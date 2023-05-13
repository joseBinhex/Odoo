# -*- coding: utf-8 -*-
{
    'name': "openacademy",

    'summary': """
        This test module has been created for the purpose of learning to develop in Odoo 14 and exploring its basic functionalities.
    """,

    'description': """
        This test module has been created to provide a hands-on learning experience in Odoo 14 development. It includes basic features such as models, views, and menus, and serves as a starting point for exploring more advanced concepts.

        Through this module, you will gain experience in creating new fields and models, designing custom views, and implementing business logic using Python. You will also learn how to package and distribute your module, and how to integrate it with other Odoo modules.

        Whether you're new to Odoo development or looking to refresh your skills, this module is an excellent way to get started and become more proficient in building custom Odoo applications.
    """,

    'author': "Jose Alberto ",
    'website': "http://www.binhex.es",

    'category': 'OpenAcademy',
    'version': '0.1',

    'depends': ['base','board','portal'],
    'application' : True,

    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/courses_views.xml',
        'views/sessions_views.xml',
        'views/partner_views.xml',
        'views/reports.xml',
        'views/dashboard_views.xml',
        'views/dashboard_actions.xml',
    ],
    
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
