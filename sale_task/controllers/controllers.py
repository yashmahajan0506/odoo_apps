# -*- coding: utf-8 -*-
# from odoo import http


# class SaleTask(http.Controller):
#     @http.route('/sale_task/sale_task', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sale_task/sale_task/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('sale_task.listing', {
#             'root': '/sale_task/sale_task',
#             'objects': http.request.env['sale_task.sale_task'].search([]),
#         })

#     @http.route('/sale_task/sale_task/objects/<model("sale_task.sale_task"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sale_task.object', {
#             'object': obj
#         })

