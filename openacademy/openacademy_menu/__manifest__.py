# -*- coding: utf-8 -*-
{
    'name': "openacademy_menu",

    'summary': """
        New functionality for openacademy addon, a new button for the menu""",

    'description': """
        Added new button menu with a User-Friendly interface for users to see courses or sessions and create both    """,

    'author': "Josito",
    'website': "http://www.binhex.es",

    'category': 'Uncategorized',
    'version': '0.1',
    'application':'True',
    'depends': ['base', 'openacademy','web'],

    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/menu_action.xml',
        'views/assets.xml',
        'views/course_views.xml',
        'views/session_views.xml',
        'views/oportunities_views.xml',

    ],
    'qweb': [
        'static/src/xml/menu_root.xml',
    ],

}
