from odoo import models, fields, api
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    state = fields.Selection(selection_add=[
        ("waiting_approval", "Waiting for Approval"),
        ("approved", "Approved"),
    ])

    approval_required = fields.Boolean(
        compute="_compute_approval_required",
        store=True
    )

    @api.depends("amount_total", "order_line.discount")
    def _compute_approval_required(self):
        for order in self:
            discount_exceeded = any(
                line.discount > 10 for line in order.order_line
            )
            amount_exceeded = order.amount_total > 100000
            order.approval_required = discount_exceeded or amount_exceeded

    def action_confirm(self):
        orders_needing_approval = self.filtered(lambda o: o.approval_required and o.state in ('draft', 'sent'))
        orders_to_confirm = self - orders_needing_approval

        if orders_needing_approval:
            orders_needing_approval.write({'state': 'waiting_approval'})

        if orders_to_confirm:
            return super(SaleOrder, orders_to_confirm).action_confirm()
            
        return True

    def action_approve(self):
        self.ensure_one()
        if not self.env.user.has_group("sales_team.group_sale_manager"):
            raise UserError("Only Sales Managers can approve sales orders.")
        self.state = "approved"

    def action_confirm_after_approval(self):
        self.ensure_one()
        if self.state != "approved":
            raise UserError("Order must be approved first.")
        
        self.write({'state': 'sent'})
        return super().action_confirm()

    def action_rainbow_effect(self):
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'Rainbow Effect Triggered!',
                'type': 'rainbow_man',
            }
        }
        
    def get_all_active_id(self):
        active_ids=self.env.context.get("active_ids",[])
        
        print(active_ids)
        
        orders=self.env['sale.order'].browse(active_ids)
        for order in orders:
            print(order.name ,order.state)
    
class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    attachment_ids = fields.Many2many('ir.attachment', string="Attachments")

