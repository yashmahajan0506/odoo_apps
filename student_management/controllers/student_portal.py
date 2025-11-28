from odoo import http
from odoo.http import request

class StudentPortal(http.Controller):

    @http.route('/my/student', type='http', auth="user", website=True)
    def my_student_info(self):
        students = request.env['student.student'].search([
            ('user_id', '=', request.env.user.id)
        ])

        return request.render("website_myaccount_student.student_info_simple", {
            'students': students
        })