from odoo import http
from odoo.http import request

class SalesDashboardController(http.Controller):
    
    @http.route('/sales/dashboard/data', type='json', auth='user')
    def sales_dashboard_data(self):
        orders = request.env['sale.order'].search([])
        total_orders = len(orders)
        total_sales = sum(orders.mapped("amount_total"))

        return {
            "total_orders": total_orders,
            "total_sales": total_sales,
        }
