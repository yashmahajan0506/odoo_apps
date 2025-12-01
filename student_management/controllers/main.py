# from odoo import http
# from odoo.http import request

# class StudentPortal(http.Controller):


#     @http.route(['/my/student'], type='http', auth='portal', website=True)
#     def portal_my_student(self, **kw):
#         partner = request.env.user.partner_id

#         students = request.env['student.student'].sudo().search([
#             ('parent_id', '=', partner.id)
#         ])

#         return request.render("student_management.portal_my_student_template", {
#             'students': students,
#         })


#     @http.route(['/my'], type='http', auth='portal', website=True)
#     def portal_my_home(self, **kw):
#         response = super(StudentPortal, self).portal_my_home(**kw)

#         partner = request.env.user.partner_id

#         student_count = request.env['student.student'].sudo().search_count([
#             ('parent_id', '=', partner.id)
#         ])

#         response.qcontext.update({
#             'student_count': student_count,
#         })

#         return response


# from odoo import http
# from odoo.http import request

# class StudentPortal(http.Controller):

#     @http.route('/my/student', type='http', auth="user", website=True)
#     def my_student_info(self, **kw):
#         students = request.env['student.student'].sudo().search([
#             ('user_id', '=', request.env.user.id)
#         ])

#         return request.render("student_management.student_info_simple", {
#             'students': students
#         })



from odoo import http
from odoo.http import request

class StudentPortal(http.Controller):

    @http.route('/my/student', type='http', auth="user", website=True)
    def my_student_info(self, **kw):
        user = request.env.user

        # for our admin 
        if user.has_group("base.group_system") or user.has_group("base.group_user"):
            students = request.env['student.student'].sudo().search([])

            page_title = "All Students (Admin View)"

        else:
            students = request.env['student.student'].sudo().search([
                ('user_id', '=', user.id)
            ])

            page_title = "My Student Information"

        return request.render("student_management.student_info_simple", {
            'students': students,
            'page_title': page_title,
        })
