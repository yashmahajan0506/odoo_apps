from odoo import models, fields

class AccountMove(models.Model):
    _inherit = 'account.move'

    delivery_date = fields.Date(string="Delivery Date")
    customer_ref = fields.Char(string="Customer Reference")
    payment_status = fields.Selection([
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('partial', 'Partial Paid'),
    ], string="Payment Status", default='pending')
