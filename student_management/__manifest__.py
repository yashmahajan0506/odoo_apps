# -*- coding: utf-8 -*-
{
    'name': "Student Management",

    'summary': "Manage student details efficiently",

    'description':  """A simple Student Management module""",

    'author': "Yash",                            
    'website': "https://wanbuffer.com/",

    'assets': {
    'web.assets_backend': [
        'student_management/static/src/css/student_kanban.css',
                ],
                },

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Education',
    'version': '1.0',   

    # any module necessary for this one to work correctly
    'depends': ['base','mail'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/record_rules.xml',
        'security/ir.model.access.csv',
        'views/student_views.xml',
        'views/menu.xml',      

    ],
    'installable':True,
    'application': True,
    'auto_install': False,

    'demo': [
        'demo/demo.xml',
    ],
}

