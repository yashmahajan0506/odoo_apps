# -*- coding: utf-8 -*-
{
    'name': "sale_task",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'data/cron.xml',
        'data/mail_template_for_approved.xml',
        'data/server_action_mail.xml',
        'data/mail_template_for_confirmation.xml',
         'views/sale_order_menu.xml',
        
        
    ],
    
    'installable':True,
    'application': True,
    'auto_install': False,

 
    'demo': [
        'demo/demo.xml',
    ],
}

