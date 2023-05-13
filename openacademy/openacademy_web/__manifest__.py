# -*- coding: utf-8 -*-
{
    'name': "openacademy_web",

    'summary': """
        Web Module for Open Academy""",

    'description': """
    This module is responsible for handling the web frontend of OpenAcademy. 
    It includes all the necessary components and features to provide users with an intuitive and seamless experience when interacting with the web interface.
    """,

    'author': "Josito",
    'website': "http://www.binhex.es",

    'category': 'OpenAcademy',
    'version': '0.1',
    'application': True,

    # any module necessary for this one to work correctly
    'depends': ['base', 'openacademy', 'website','website_form'],

    'data': [
        'security/ir.model.access.csv',
        'views/templates.xml',
        'views/custom_navbar.xml',
    ],

}
