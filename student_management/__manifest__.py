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
    'depends': ['base','mail','sale_management','website'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/record_rules.xml',
        'security/ir.model.access.csv',
        'data/cron.xml',
        'data/mail_template.xml',   
        'data/student_birthday_email_template.xml',
        'data/student_mail_template.xml',
        'data/student_cron.xml',
        'data/addmission_confirmation_mail_template.xml',
        'views/student_views.xml',
        'views/menu.xml', 
        'views/server_action.xml',
        'views/alumni_reason_view.xml',
        'views/student_application_form.xml',
        'views/student_submit_success.xml',
        'reports/report_student_template.xml',
        'reports/report.xml',
        # 'wizards/student_wizard_views.xml',
        # 'wizards/student_message_wizard_views.xml',
        'wizards/alumni_wizard_view.xml',
        
           ],
    'installable':True,
    'application': True,
    'auto_install': False,

    'demo': [
        'demo/demo.xml',
    ],
}

