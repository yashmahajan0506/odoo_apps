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
                line.discount > 15 for line in order.order_line
            )
            amount_exceeded = order.amount_total > 100000
            order.approval_required = discount_exceeded or amount_exceeded

    def action_confirm(self):
        for order in self:
            if order.approval_required and order.state == "draft":
                order.state = "waiting_approval"
                return True
        return super().action_confirm()

    def action_approve(self):
        self.ensure_one()
        if not self.env.user.has_group("sales_team.group_sale_manager"):
            raise UserError("Only Sales Managers can approve sales orders.")
        self.state = "approved"

    def action_confirm_after_approval(self):
        self.ensure_one()
        if self.state != "approved":
            raise UserError("Order must be approved first.")
        return super().action_confirm()


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    attachment_ids = fields.Many2many('ir.attachment', string="Attachments")

