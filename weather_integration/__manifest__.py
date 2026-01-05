{
    'name': "weather_integration",

    'summary': "Premium Weather Dashboard with OpenWeatherMap Integration",

    'description': """
        A state-of-the-art weather forecasting application for Odoo.
        Features:
        - Real-time weather data fetching.
        - Premium Kanban dashboard with vibrant visuals.
        - Support for multiple cities.
        - Configurable API settings.
    """,

    'author': "DeepMind Antigravity",
    'website': "https://www.deepmind.com",

    'category': 'Sales/Sales',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        # 'views/res_config_settings_views.xml',
        # 'views/templates.xml',
        'views/menu.xml',
        
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    
    'installable':True,
    'application': True,
    'auto_install': False,
}

