from odoo import models, api, fields

class SaleDashboard(models.Model):
    _name = "sale.dashboard"
    _description = "Sales Dashboard Helper"

    @api.model
    def get_sales_data(self):
        SaleOrder = self.env["sale.order"]

        total_orders = SaleOrder.search_count([])

        confirmed_orders = SaleOrder.search_count([
            ("state", "=", "sale")
        ])

        quotations = SaleOrder.search_count([
            ("state", "=", "draft")
        ])

        orders = SaleOrder.search([("state", "=", "sale")])
        total_amount = sum(orders.mapped("amount_total"))

        return {
            "total_orders": total_orders,
            "confirmed_orders": confirmed_orders,
            "quotations": quotations,
            "total_amount": total_amount,
        }

    @api.model
    def search_orders(self, query, filter_type="all"):
        domain = [("name", "ilike", query)]
        
        if filter_type == 'last_7_days':
             domain.append(('date_order', '>=', fields.Datetime.subtract(fields.Datetime.now(), days=7)))
        elif filter_type == 'last_30_days':
             domain.append(('date_order', '>=', fields.Datetime.subtract(fields.Datetime.now(), days=30)))

        orders = self.env["sale.order"].search(domain)
    
        total_amt = sum(orders.mapped("amount_total"))
        confirmed = orders.filtered(lambda r: r.state == "sale")
        quotes = orders.filtered(lambda r: r.state in ("draft", "sent"))
    
        return {
            "total_orders": len(orders),
            "confirmed_orders": len(confirmed),
            "quotations": len(quotes),
            "total_amount": total_amt,
        }


