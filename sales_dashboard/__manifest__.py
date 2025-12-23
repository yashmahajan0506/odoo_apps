{
    'name': "sales_dashboard",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
    Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",
    
    
    
'assets': {
            'web.assets_backend': [
                "sales_dashboard/static/src/js/sales_dashboard.js",
                "sales_dashboard/static/src/js/custom_sale_smart_filter.js",
                "sales_dashboard/static/src/js/counter_widget.js",
                "sales_dashboard/static/src/js/attachment_preview_widget.js",
                "sales_dashboard/static/src/xml/sales_dashboard_template.xml",
                "sales_dashboard/static/src/xml/counter_widget_template.xml",
                "sales_dashboard/static/src/xml/custom_sale_smart_filter.xml",
                "sales_dashboard/static/src/xml/attachment_preview.xml",
                "sales_dashboard/static/src/scss/sales_dashboard.scss",

        ],
        },

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale', 'web'],


    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/sale_order_view.xml',
        'views/sales_base_menu.xml',
        'views/sales_dashboard_template.xml',
        'views/snippet_templates.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable':True,
    'application': True,
    'auto_install': False,
}


