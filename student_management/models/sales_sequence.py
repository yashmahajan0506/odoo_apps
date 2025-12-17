from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'


    @api.model
    def create(self, vals):
        if 'name' not in vals or vals['name'] == 'New':
            seq = self.env['ir.sequence'].next_by_code('sale.order.custom') or '/'
            vals['name'] = seq
        return super(SaleOrder, self).create(vals)
