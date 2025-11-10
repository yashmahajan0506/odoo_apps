from odoo import models, fields, api
class SaleOrder(models.Model):
    _inherit = 'sale.order'

    delivery_date = fields.Date(string="Delivery Date")
    customer_ref = fields.Char(string="Customer Reference")
    payment_status = fields.Selection([
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('partial', 'Partial Paid'),
    ], string="Payment Status", default='pending')


    def _prepare_invoice(self):
        res = super(SaleOrder, self)._prepare_invoice()
        res.update({
            'delivery_date': self.delivery_date,
            'customer_ref': self.customer_ref,
            'payment_status': self.payment_status,
        })
        return res
