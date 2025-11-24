from odoo import models, fields, api
from datetime import timedelta
class SaleOrder(models.Model):
    _inherit = 'sale.order'

    state = fields.Selection(selection_add=[
            ('draft', 'Draft'),
            ('approved', 'Approved'),
    ],)

    def action_approved(self):
       
        self.write({'state': 'approved'})
        
        template = self.env.ref('sale_task.email_template_sale_order_approved')
        for order in self:
            template.send_mail(order.id, force_send=True)

    def cron_auto_approve_orders(self):
        limit_date = fields.Datetime.now() - timedelta(days=3)
        orders = self.search([
            ('state', '=', 'confirmed'),
            ('date_order', '<=', limit_date)
        ])
        
        for order in orders:
            order.state = 'approved'
       
    def action_confirm(self):
        res = super().action_confirm()

        template = self.env.ref('sale_task.email_template_sale_order_confirmed')
        
        for order in self:
            template.send_mail(order.id, force_send=True)

        return res
  

    



# # -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class sale_task(models.Model):
#     _inherit='sale.order'
    
    
#     state= fields.Selection([
#         ('draft', 'Draft'),
#         ('confirmed', 'Confirmed'), 
#         ('approved', 'Approved'),
#         ('cancelled', 'Cancelled')

#     ], string='state')
    
#     def change_to_confirmed(self):
#         pass 
    
#     def change_to_approved(self):
#         pass 
    
#     def change_to_cancelled(self):
#         pass 
    
    
# #     1. Add State Field (Draft → Confirmed → Approved → Cancelled)
# # inherit the sale.order model to include a new state flow with stages: draft, confirmed, approved, cancelled.
# # Task:
# #  Modify or extend the state field in the sale.order model to implement this new workflow add approved state

    
# #
# #     @api.depends('value')
# #     def _value_pc(self):
# #         for record in self:
# #             record.value2 = float(record.value) / 100

