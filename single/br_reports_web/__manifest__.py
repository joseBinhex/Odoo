# -*- coding: utf-8 -*-
{
    'name': "br_reports_web",

    'summary': """
        New functional download button on Business Requirements Portal""",

    'description': """
        Added a new download button on Business Requirements Portal on each br 
    """,

    'author': "Josito",
    'website': "http://www.binhex.es",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base','br_reports','business_requirement', 'portal'],

    'data': [
        # 'security/ir.model.access.csv',
        'views/brd_portal_print.xml',
    ],

}
