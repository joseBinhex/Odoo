# -*- coding: utf-8 -*-
{
    'name': "openacademy_crm",

    'summary': """
        CRM Module for OpenAcademy""",

    'description': """
    This module is responsible for handling the Customer Relationship Management (CRM) functionality of OpenAcademy. 
    It includes all the necessary components and features to manage customer interactions, track leads and sales, and provide insights into the customer base. With this module, businesses can effectively manage their customer relationships, streamline their sales processes, and optimize their marketing efforts.
    """,

    'author': "Josito",
    'website': "http://www.binhex.es",

    'application': True,
    'category': 'OpenAcademy',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','crm','openacademy', 'website','website_form'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/custom_field.xml',
        'views/views.xml',
        'views/email_from.xml',
        'views/web_form_view.xml',
    ],

}
