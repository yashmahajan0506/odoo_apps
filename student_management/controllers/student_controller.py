from odoo import http
from odoo.http import request
import re

class Studentapplication(http.Controller):

    @http.route('/student/application', auth='public', website=True)
    def student_application_form(self, **kwargs):
        return request.render('student_management.student_application_form', {})

    @http.route('/student/application/submit', auth='public', website=True, csrf=False, methods=['POST'])
    def submit_student_application(self, **post):

        email = post.get('email')

        email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,10}$"  

       
        if not re.match(email_regex, email):
            return request.render('student_management.student_application_form', {
                'error': "Invalid email format! Please enter a valid email.",
                'post': post 
            })
                 
        student = request.env['student.student'].sudo().create({
            'name': post.get('name'),
            'age': post.get('age'),
            'email': post.get('email'),
            'phone': post.get('phone'),
            'roll_no': post.get('roll_no'),
        })
        template = request.env.ref('student_management.student_creation_email_template')
        template.sudo().send_mail(student.id, force_send=True)

        return request.render('student_management.student_submit_success', {
            'student': student
        })

    @http.route('/test/hello', auth='public')
    def test_hello(self):
        return "Controller Working!"
