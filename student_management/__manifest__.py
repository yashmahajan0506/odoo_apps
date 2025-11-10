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
    'depends': ['base','mail','sale_management'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/record_rules.xml',
        'security/ir.model.access.csv',
        'data/mail_template.xml',   
        'data/cron.xml',
        'data/student_email_templates.xml',
        # 'data/student_birthday_cron.xml',
        'views/sales_order_inherit_views.xml',
        'views/student_views.xml',
        'views/menu.xml', 
        'views/custom_fileds_to_invoice.xml',  
        'views/server_action.xml',
        'views/sale_order_excel_button.xml',   
        # 'views/student_wizard_views.xml',
        'views/student_message_wizard_views.xml',
        'reports/report_student_template.xml',
        'reports/report_saleorder_inherit.xml',
        'reports/invoice_report_inherit.xml',
           ],
    'installable':True,
    'application': True,
    'auto_install': False,

    'demo': [
        'demo/demo.xml',
    ],
}

