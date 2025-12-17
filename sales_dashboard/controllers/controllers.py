# from odoo import http


# class SalesDashboard(http.Controller):
#     @http.route('/sales_dashboard/sales_dashboard', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sales_dashboard/sales_dashboard/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('sales_dashboard.listing', {
#             'root': '/sales_dashboard/sales_dashboard',
#             'objects': http.request.env['sales_dashboard.sales_dashboard'].search([]),
#         })

#     @http.route('/sales_dashboard/sales_dashboard/objects/<model("sales_dashboard.sales_dashboard"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sales_dashboard.object', {
#             'object': obj
#         })

