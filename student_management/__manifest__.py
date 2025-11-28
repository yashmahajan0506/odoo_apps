# -*- coding: utf-8 -*-
{
    'name': "Student Management",

    'summary': "Manage student details efficiently",

    'description':  """A simple Student Management module""",

    'author': "Yash",                            
    'website': "https://wanbuffer.com/",
    
    'assets': {
          'web.assets_backend': [
                # 'student_management/static/lib/chart/chart.umd.js',
                "student_management/static/src/js/student_dashboard.js",
                "student_management/static/src/xml/student_dashboard_template.xml",
                "student_management/static/src/css/student_dashboard.css",
                "student_management/static/src/css/student_kanban.css",
                "student_management/static/src/css/student_style.css",
        ],
    #     'web.assets_frontend': [
    #         'student_management/static/src/js/my_script.js',
    #     ],
    #     'web.assets_qweb': [
    #     'student_management/static/src/xml/student_dashboard_templates.xml',
    #      ],
        },

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Education',
    'version': '1.0',   

    # any module necessary for this one to work correctly
    'depends': ['base','mail','sale_management'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/record_rules.xml',
        'security/ir.model.access.csv',
        'data/cron.xml',
        'data/mail_template.xml',   
        'data/student_birthday_email_template.xml',
         # 'data/student_mail_template.xml',
        #  'data/website_page.xml',
        'data/student_cron.xml',
        'data/addmission_confirmation_mail_template.xml',
        # 'views/assets.xml',9
        'views/student_views.xml',
         'views/student_dashboard_view.xml',
        'views/menu.xml', 
        'views/alumni_reason_view.xml',
        'views/student_application_form.xml',
        'views/student_submit_success.xml',
        'views/portal_inherit.xml',
        'views/portal_student_template.xml',
        # 'views/check_student_dashbord.xml',
        # 'views/student_dashboard_template.xml',
        # 'views/assests_backup.xml',
        # 'views/template.xml',
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

