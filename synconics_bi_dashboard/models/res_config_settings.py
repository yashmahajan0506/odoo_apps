from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    enable_ocn = fields.Boolean('Push Notifications', config_parameter='mail_mobile.enable_ocn')
    disable_redirect_firebase_dynamic_link = fields.Boolean(
        "Disable link redirection to mobile app",
        config_parameter='mail_mobile.disable_redirect_firebase_dynamic_link'
    )

    barcodelookup_api_key = fields.Char(
        string='API key',
        config_parameter='product_barcodelookup.api_key',
        help='Barcode Lookup API Key for create product from barcode.',
    )

    map_box_token = fields.Char(
        default='',
        store=True
    )

    setting_account_avatax = fields.Boolean(string='Use AvaTax')
    avalara_environment = fields.Selection(
        string="Avalara Environment",
        selection=[
            ('sandbox', 'Sandbox'),
            ('production', 'Production'),
        ],
        default='sandbox',
    )
    avalara_api_id = fields.Char(string='Avalara API ID')
    avalara_api_key = fields.Char(string='Avalara API KEY')
    avalara_partner_code = fields.Char(string='Avalara Company Code')
    avalara_commit = fields.Boolean(string="Commit in Avatax")
    avalara_address_validation = fields.Boolean(string="Avalara Address Validation")
    avalara_use_upc = fields.Boolean(string="Use UPC", default=True)
