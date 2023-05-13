# -*- coding: utf-8 -*-
{
    'name': "br_reports",

    'summary': """
        Reports based of Business Requirements""",

    'description': """
        News reports based of Business Requirements, added some features to reports of business requirements
    """,

    'author': "Josito",
    'website': "http://www.binhex.es",

    'category': 'Uncategorized',
    'version': '0.1',


    'depends': ['base', 'business_requirement'],


    'data': [
        # 'security/ir.model.access.csv',
        "reports/action_report.xml",
        'reports/br_paperformat.xml',
        'reports/br_actual_report.xml', 
    ],

    'css': ['static/css/my.css'],

}
