# -*- coding: utf-8 -*-
{
    'name': "openacademy_portal",

    'summary': """
        A web portal module for openacademy""",

    'description': """
        Added new functionality for openacademy web, added a new portal to see user's sessions and more
    """,

    'author': "Josito",
    'website': "http://www.binhex.es",

    'category': 'Uncategorized',
    'version': '0.1',


    'depends': ['base', 'openacademy','portal'],

    'data': [
        'security/ir.model.access.csv',
        'views/portal_menu.xml',
        'views/confirm_messages.xml',
    ],

}
